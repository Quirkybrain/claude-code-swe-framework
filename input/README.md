# Project Asset Pool

`input/` contains everything the project already has. It is not only a requirements folder and it is not a required workflow sequence.

You may place files directly under `input/` or use the recommended directories:

```text
input/
├── project/
├── requirements/
├── references/
├── competitors/
├── design/
├── uml/
├── architecture/
├── api/
├── data/
├── existing/
├── tests/
├── standards/
└── other/
```

## Directory Guide

| Directory | Typical content |
|---|---|
| `project/` | Product description, goals, background, stakeholder notes |
| `requirements/` | Requirements, use cases, acceptance criteria, backlog exports |
| `references/` | Reference products, research, external documentation |
| `competitors/` | Competitor notes and comparative material |
| `design/` | UI designs, prototypes, flows, visual specifications |
| `uml/` | UML, class, sequence, activity, and state diagrams |
| `architecture/` | Architecture diagrams, ADRs, deployment topology |
| `api/` | API specifications, examples, contracts, schemas |
| `data/` | Data models, schemas, migrations, sample data descriptions |
| `existing/` | Existing code, modules, scripts, or legacy project material |
| `tests/` | Test cases, test plans, reports, failure logs |
| `standards/` | Coding, API, testing, security, documentation, and team standards; see [standards/README.md](standards/README.md) |
| `other/` | Anything that does not clearly fit elsewhere |

## Recognition Principle

Directory names, filenames, and extensions are hints only. They are not authoritative Artifact types. Project Intake must inspect accessible content before classifying an asset. For example, an image may be a UI prototype, architecture diagram, workflow, or deployment diagram.

If content cannot be read or confidently interpreted, record the limitation and classify the result as `UNVERIFIED`; do not invent its meaning.

## Standards

[`input/standards/`](standards/README.md) may contain:

- Coding Standard
- API Standard
- Testing Standard
- Security Standard
- Documentation Standard
- Team Engineering Standard

These are examples, not required filenames. Existing standards may keep their current names and formats.

The analysis/architecture responsibility reads these sources once, resolves conflicts, and produces shared Project Constraints with source references. Other Agents consume the normalized constraints rather than independently reinterpreting every standards document.

## Handling Guidance

- Keep original assets intact unless the user explicitly requests changes.
- Record conflicts between assets instead of silently selecting one.
- Do not commit credentials, secrets, private keys, production data, or regulated personal data.
- Reference large existing repositories in Project Configuration when copying them into `input/` would be wasteful.
- Existing assets are candidates for validation and reuse, not automatically trusted truth.
