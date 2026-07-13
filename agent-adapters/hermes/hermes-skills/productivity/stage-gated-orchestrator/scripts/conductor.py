#!/usr/bin/env python3
"""EKSAD stage-gated conductor: local state, HITL gates, and live tracker."""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
PIPELINE_TEMPLATE = SKILL_ROOT / "templates" / "eksad-pipeline.json"
UI_TEMPLATE = SKILL_ROOT / "templates" / "conductor.html"
VALID_STATUSES = {
    "pending", "locked", "in_progress", "validating", "awaiting_review",
    "approved", "revision_required", "blocked", "skipped", "aborted",
}
DECISIONS = {"APPROVE", "REVISE", "ABORT", "SKIP"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def workspace_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def paths(workspace: Path) -> dict[str, Path]:
    root = workspace / ".conductor"
    return {
        "root": root,
        "config": root / "config.json",
        "state": root / "state.json",
        "events": root / "events.jsonl",
        "ui": root / "index.html",
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def require_initialized(workspace: Path) -> dict[str, Path]:
    p = paths(workspace)
    missing = [str(p[k]) for k in ("config", "state", "events", "ui") if not p[k].exists()]
    if missing:
        raise SystemExit("Conductor not initialized; missing: " + ", ".join(missing))
    return p


def project_token(name: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").upper()
    return token or "PROJECT"


def load_events(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not path.exists():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            entries.append({"ts_iso": now_iso(), "role": "system", "stage": None,
                            "message": "Malformed event omitted"})
    return entries


def append_event(p: dict[str, Path], *, role: str, stage: str | None,
                 message: str, event_type: str = "progress", **extra: Any) -> dict[str, Any]:
    entry = {
        "ts_iso": now_iso(),
        "type": event_type,
        "role": role,
        "stage": stage,
        "message": message,
        **extra,
    }
    with p["events"].open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def get_stage(state: dict[str, Any], stage_id: str) -> dict[str, Any]:
    wanted = stage_id.upper()
    for stage in state["stages"]:
        if stage["id"].upper() == wanted:
            return stage
    raise SystemExit(f"Unknown stage: {stage_id}")


def dependencies_unlocked(state: dict[str, Any], stage: dict[str, Any]) -> bool:
    for dep_id in stage.get("depends_on", []):
        dep = get_stage(state, dep_id)
        if dep["status"] not in {"approved", "skipped"}:
            return False
    return True


def refresh_artifacts(workspace: Path, state: dict[str, Any]) -> None:
    for stage in state["stages"]:
        artifact = workspace / stage["artifact"]
        stage["artifact_exists"] = artifact.is_file()
        stage["artifact_size"] = artifact.stat().st_size if artifact.is_file() else 0
        stage["artifact_mtime"] = (
            datetime.fromtimestamp(artifact.stat().st_mtime, timezone.utc)
            .replace(microsecond=0).isoformat().replace("+00:00", "Z")
            if artifact.is_file() else None
        )


def cmd_init(args: argparse.Namespace) -> None:
    workspace = workspace_path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    p = paths(workspace)
    if p["root"].exists() and not args.force:
        raise SystemExit(f"{p['root']} already exists; use --force to replace conductor state")
    if p["root"].exists():
        shutil.rmtree(p["root"])
    p["root"].mkdir(parents=True)

    pipeline = read_json(PIPELINE_TEMPLATE)
    token = project_token(args.project)
    gates_enabled = not args.no_gates
    config = {
        "project": args.project,
        "project_token": token,
        "workspace": str(workspace),
        "pipeline": pipeline["pipeline"],
        "gates_enabled": gates_enabled,
        "created_at": now_iso(),
    }
    stages: list[dict[str, Any]] = []
    start_seen = args.start_stage is None
    for raw in pipeline["stages"]:
        stage = copy.deepcopy(raw)
        if args.start_stage and stage["id"].upper() == args.start_stage.upper():
            start_seen = True
            stage["depends_on"] = []
        if not start_seen:
            continue
        stage["artifact"] = stage["artifact"].replace("{PROJECT}", token)
        stage.update({
            "status": "pending" if not stage["depends_on"] else "locked",
            "last_message": "",
            "gate_decision": None,
            "gate_note": None,
            "revisions": 0,
            "artifact_exists": False,
            "artifact_size": 0,
            "artifact_mtime": None,
        })
        stages.append(stage)
    if not stages:
        raise SystemExit(f"Start stage not found: {args.start_stage}")

    state = {**config, "updated_at": now_iso(), "aborted": False, "stages": stages}
    atomic_write_json(p["config"], config)
    atomic_write_json(p["state"], state)
    p["events"].touch()
    shutil.copy2(UI_TEMPLATE, p["ui"])
    append_event(p, role="orchestrator", stage=None,
                 message=f"Conductor initialized for {args.project}; gates={'enabled' if gates_enabled else 'disabled'}",
                 event_type="init")
    print(json.dumps({"ok": True, "workspace": str(workspace), "tracker": str(p["ui"]),
                      "gates_enabled": gates_enabled, "stages": [s["id"] for s in stages]}, indent=2))


def cmd_event(args: argparse.Namespace) -> None:
    workspace = workspace_path(args.workspace)
    p = require_initialized(workspace)
    state = read_json(p["state"])
    stage = get_stage(state, args.stage)
    if args.status:
        if args.status not in VALID_STATUSES:
            raise SystemExit(f"Invalid status: {args.status}")
        if args.status in {"in_progress", "validating"} and not dependencies_unlocked(state, stage):
            raise SystemExit(f"Stage {stage['id']} is locked by unresolved dependencies")
        if state.get("aborted"):
            raise SystemExit("Pipeline is aborted")
        stage["status"] = args.status
    stage["last_message"] = args.message
    state["updated_at"] = now_iso()
    refresh_artifacts(workspace, state)
    atomic_write_json(p["state"], state)
    append_event(p, role=args.role, stage=stage["id"], message=args.message,
                 status=stage["status"])
    print(json.dumps({"ok": True, "stage": stage["id"], "status": stage["status"]}))


def cmd_complete(args: argparse.Namespace) -> None:
    workspace = workspace_path(args.workspace)
    p = require_initialized(workspace)
    state = read_json(p["state"])
    stage = get_stage(state, args.stage)
    if not dependencies_unlocked(state, stage):
        raise SystemExit(f"Stage {stage['id']} is locked by unresolved dependencies")
    artifact_rel = args.artifact or stage["artifact"]
    artifact = (workspace / artifact_rel).resolve()
    try:
        artifact.relative_to(workspace)
    except ValueError as exc:
        raise SystemExit("Artifact must be inside workspace") from exc
    if not artifact.is_file():
        raise SystemExit(f"Artifact not found: {artifact}")
    if artifact.stat().st_size < args.min_bytes:
        raise SystemExit(f"Artifact too small: {artifact.stat().st_size} < {args.min_bytes} bytes")
    stage["artifact"] = str(artifact.relative_to(workspace))
    stage["status"] = "awaiting_review" if state["gates_enabled"] else "approved"
    stage["last_message"] = args.summary
    if not state["gates_enabled"]:
        stage["gate_decision"] = "AUTO_APPROVE"
    refresh_artifacts(workspace, state)
    state["updated_at"] = now_iso()
    atomic_write_json(p["state"], state)
    append_event(p, role="orchestrator", stage=stage["id"], message=args.summary,
                 event_type="complete", status=stage["status"], artifact=stage["artifact"])
    print(json.dumps({"ok": True, "stage": stage["id"], "status": stage["status"],
                      "artifact": stage["artifact"], "size": stage["artifact_size"]}, indent=2))


def cmd_gate(args: argparse.Namespace) -> None:
    workspace = workspace_path(args.workspace)
    p = require_initialized(workspace)
    state = read_json(p["state"])
    stage = get_stage(state, args.stage)
    decision = args.decision.upper()
    if decision not in DECISIONS:
        raise SystemExit(f"Invalid decision: {decision}")
    if stage["status"] != "awaiting_review":
        raise SystemExit(f"Stage {stage['id']} is {stage['status']}, not awaiting_review")
    if decision in {"REVISE", "ABORT", "SKIP"} and not args.note.strip():
        raise SystemExit(f"{decision} requires --note")

    mapping = {
        "APPROVE": "approved",
        "REVISE": "revision_required",
        "ABORT": "aborted",
        "SKIP": "skipped",
    }
    stage["status"] = mapping[decision]
    stage["gate_decision"] = decision
    stage["gate_note"] = args.note
    stage["last_message"] = f"Gate {decision}: {args.note or 'no note'}"
    if decision == "REVISE":
        stage["revisions"] = int(stage.get("revisions", 0)) + 1
    if decision == "ABORT":
        state["aborted"] = True
    if decision in {"APPROVE", "SKIP"}:
        for candidate in state["stages"]:
            if stage["id"] in candidate.get("depends_on", []) and dependencies_unlocked(state, candidate):
                if candidate["status"] == "locked":
                    candidate["status"] = "pending"
                    candidate["last_message"] = f"Unlocked by {stage['id']} {decision}"
    state["updated_at"] = now_iso()
    atomic_write_json(p["state"], state)
    append_event(p, role="human", stage=stage["id"],
                 message=f"Gate {decision}: {args.note or 'approved'}",
                 event_type="gate", decision=decision)
    print(json.dumps({"ok": True, "stage": stage["id"], "decision": decision,
                      "status": stage["status"]}, indent=2))


def public_state(workspace: Path) -> dict[str, Any]:
    p = require_initialized(workspace)
    state = read_json(p["state"])
    refresh_artifacts(workspace, state)
    state["events"] = load_events(p["events"])[-300:]
    return state


def cmd_status(args: argparse.Namespace) -> None:
    print(json.dumps(public_state(workspace_path(args.workspace)), indent=2, ensure_ascii=False))


def cmd_serve(args: argparse.Namespace) -> None:
    workspace = workspace_path(args.workspace)
    p = require_initialized(workspace)

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, fmt: str, *values: Any) -> None:
            if args.verbose:
                super().log_message(fmt, *values)

        def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:
            route = self.path.split("?", 1)[0]
            if route == "/api/state":
                return self.send_json(public_state(workspace))
            if route == "/healthz":
                return self.send_json({"ok": True, "project": read_json(p["config"])["project"]})
            if route in {"/", "/conductor", "/conductor/", "/index.html"}:
                self.path = "/index.html"
            return super().do_GET()

    if args.host == "0.0.0.0":
        print("WARNING: tracker has no authentication or TLS; expose only on a trusted network", file=sys.stderr)
    os.chdir(p["root"])
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Conductor serving http://{args.host}:{args.port}/conductor", flush=True)
    server.serve_forever()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize conductor state in a workspace")
    init.add_argument("--workspace", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--start-stage", choices=["UR", "BRD", "FSD", "TSD"])
    init.add_argument("--no-gates", action="store_true")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    event = sub.add_parser("event", help="append progress and optionally update stage status")
    event.add_argument("--workspace", required=True)
    event.add_argument("--stage", required=True)
    event.add_argument("--role", required=True)
    event.add_argument("--message", required=True)
    event.add_argument("--status", choices=sorted(VALID_STATUSES))
    event.set_defaults(func=cmd_event)

    complete = sub.add_parser("complete", help="verify artifact existence and open/resolve gate")
    complete.add_argument("--workspace", required=True)
    complete.add_argument("--stage", required=True)
    complete.add_argument("--artifact")
    complete.add_argument("--summary", required=True)
    complete.add_argument("--min-bytes", type=int, default=1000)
    complete.set_defaults(func=cmd_complete)

    gate = sub.add_parser("gate", help="record a human gate decision")
    gate.add_argument("--workspace", required=True)
    gate.add_argument("--stage", required=True)
    gate.add_argument("--decision", choices=sorted(DECISIONS), required=True)
    gate.add_argument("--note", default="")
    gate.set_defaults(func=cmd_gate)

    status = sub.add_parser("status", help="print current state and recent events")
    status.add_argument("--workspace", required=True)
    status.set_defaults(func=cmd_status)

    serve = sub.add_parser("serve", help="serve live tracker UI and API")
    serve.add_argument("--workspace", required=True)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--verbose", action="store_true")
    serve.set_defaults(func=cmd_serve)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
