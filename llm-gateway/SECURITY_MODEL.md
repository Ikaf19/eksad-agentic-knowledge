# LLM Gateway Security Model

## Git boundary

Allowed in Git:

- Alias names and policy.
- Example config with environment variable placeholders.
- Render-only scripts.
- Validators.
- Runtime adapter documentation.

Forbidden in Git:

- Provider API keys.
- LiteLLM master keys/proxy keys.
- Live `config.yaml` with real provider bindings.
- Prompt/response logs containing confidential data.
- Billing exports with identities.
- Credentialed endpoint URLs.

## Runtime boundary

Runtime operators own:

- Provider key storage.
- LiteLLM/gateway deployment.
- Key rotation.
- Network allowlists.
- Audit log retention.
- Data residency controls.

Role agents own:

- Requesting appropriate capability aliases.
- Respecting role permissions and approval gates.
- Avoiding direct provider/model hardcoding.

## Default deny

New providers, high-cost aliases, multimodal aliases, and raw logging are disabled until explicitly approved for the environment.
