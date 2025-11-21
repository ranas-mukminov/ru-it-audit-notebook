# Contributing

Thank you for improving `ru-it-audit-notebook`! This project follows a strict test-first workflow and focuses on safe defaults for audit data.

## Ground rules
- Write unit tests before implementing functionality for core modules (`checklist_loader`, `scoring`, `context_builder`, `markdown_renderer`, AI summary/workplan generators, CLI commands).
- Keep formulations generalized; do not paste legal texts from 152-ФЗ, 187-ФЗ, 54-ФЗ or ГОСТ.
- Avoid sending customer data to external services by default.

## Required workflow
1. Add or update tests to describe the expected behavior.
2. Implement the code to satisfy those tests.
3. Run the full developer suite before opening a PR:
   ```bash
   ./scripts/dev_run_all_tests.sh
   ```
   PRs/commits are not accepted without a green result.

## Coding standards
- Python: prefer type hints, small pure functions, and informative error messages for YAML loading/validation.
- Notebooks: keep dependencies minimal and avoid destructive actions; prefer reading prepared CSV/JSON/YAML inputs.
- Security: default to `NoopAIProvider` and require explicit opt-in for external LLM usage.

## Reporting issues
When filing an issue, share a minimal reproducible example and relevant CLI commands. Avoid publishing sensitive configuration data.
