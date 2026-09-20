# Project Configuration Example

This example is illustrative. Copy relevant values into `config/project.md`; do not treat it as active project configuration.

## Project

| Field | Value |
|---|---|
| Project Name | Example Inventory Portal |
| Project Description | Internal web application for warehouse inventory and audit history |
| Target Stage | implementation |
| Workflow Mode | STANDARD |
| Execution Mode | GATED_AUTO |

## Technology

| Field | Value |
|---|---|
| Language | TypeScript |
| Language Version | 5.x |
| Framework | auto |
| Frontend | React |
| Backend | Node.js |
| Database | PostgreSQL |
| UI Framework | auto |
| API Style | REST with OpenAPI |
| Build System | auto |
| Package Manager | pnpm |
| Testing Framework | Vitest and Playwright |
| Target Platform | Linux containers and modern evergreen browsers |
| Deployment Target | Existing Kubernetes cluster |

## Constraints and Preferences

| Field | Value |
|---|---|
| Must Use Technologies | Company SSO; PostgreSQL |
| Forbidden Technologies | Public unauthenticated endpoints |
| Technical Preferences | Prefer established libraries and explicit API contracts |
| Performance Requirements | Inventory lookup p95 below 300 ms at expected load |
| Security Requirements | Least privilege; audit log for inventory changes; no secrets in repository |
| Compatibility Requirements | Latest two versions of Chrome, Edge, and Firefox |
| Other Constraints | Follow all files under `input/standards/`; reuse the existing database schema when valid |

## Configuration Notes

- Product requirements are expected under `input/requirements/`.
- Existing schema and API material are expected under `input/data/` and `input/api/`.
- Authentication choice is explicit; other unresolved high-impact architecture decisions require clarification.
