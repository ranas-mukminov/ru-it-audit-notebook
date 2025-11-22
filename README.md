# 📋 ru-it-audit-notebook

[![CI Status](https://github.com/ranas-mukminov/ru-it-audit-notebook/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/ru-it-audit-notebook/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Overview

`ru-it-audit-notebook` is an open-source, interactive IT audit report generator tailored for Russian business contexts. It combines Jupyter notebooks with YAML-based checklists to produce professional HTML and PDF reports covering critical compliance areas: personal data protection (152-ФЗ), backup resilience, critical information infrastructure (КИИ), and business applications like 1C.

The tool transforms technical inventory data and questionnaire answers into executive summaries for management and detailed technical appendices for engineers. Designed for DevOps/DevSecOps teams, internal auditors, and IT integrators, it streamlines recurring audit workflows without replacing formal legal assessments.

## Key Features

- **Compliance-focused checklists**: Pre-built YAML templates for 152-ФЗ (personal data), backup resilience, КИИ basics, and 1C application landscapes
- **Jupyter-based workflow**: Interactive notebooks that parse inventory CSVs, score controls, and generate Markdown sections
- **Dual-output reports**: Executive summary for leadership and technical detail for IT staff, rendered to HTML/PDF via `nbconvert`
- **Scoring and risk assessment**: Configurable weight-based scoring with `ok`/`warning`/`critical` thresholds per control
- **AI-ready stubs**: Optional hooks for AI-generated summaries and work plan recommendations (default to no-op provider for data safety)
- **Russian context**: All checklists, terminology, and examples adapted for Russian regulatory landscape and tooling (1C, etc.)
- **Automation-friendly**: CLI commands for batch processing inventories and building reports in CI/CD pipelines

## Architecture / Components

The project consists of three main layers:

1. **Core Python library** (`it_audit_report/`):
   - `checklist_loader.py`: Loads and validates YAML checklists.
   - `scoring.py`: Computes weighted scores and categorizes findings.
   - `inventory/`: Parses CSV inventories of servers, services, and applications.
   - `report/`: Jinja2-based Markdown rendering for executive and technical sections.
   - `ai/`: Optional AI integration stubs (default NoopAIProvider).

2. **YAML checklists** (`checklists/`):
   - `pdn_152fz.yaml`, `backup_resilience.yaml`, `kii_basic.yaml`, `app_1c.yaml`, `inventory.yaml`.
   - Each defines controls (ID, title, description, scoring weights, artifact references).

3. **Jupyter notebooks** (`notebooks/`):
   - `00_inventory_servers.ipynb` – Loads server inventory.
   - `01_pdn_152fz_checklist.ipynb` – Personal data controls.
   - `02_backup_resilience_checklist.ipynb` – Backup and DR assessment.
   - `03_kii_basic_checklist.ipynb` – КИИ basics.
   - `04_applications_1c_business.ipynb` – 1C landscape.
   - `99_report_assembler.ipynb` – Combines all outputs into final Markdown.

**Data flow**:  
Inventory CSV + Answers (YAML/JSON) → Notebooks (scoring + context) → Jinja2 templates → Markdown → `nbconvert` → HTML/PDF report

## Requirements

### Operating System
- **Recommended**: Ubuntu 22.04+ / Debian 11+, Rocky Linux 8+, or any recent Linux distribution with Python 3.10+
- **Windows/macOS**: Supported via Python virtual environments

### Software Dependencies
- **Python**: 3.10 or later
- **pip**: Latest version recommended
- **Packages**: Installed automatically via `pip install -e .`
  - `typer`, `pyyaml`, `jinja2`, `pandas`, `papermill`, `nbformat`, `nbconvert`

### Optional for Development
- **Development tools**: `pytest`, `mypy`, `ruff`, `bandit`, `pip-audit` (installed with `[dev]` extra)
- **Document conversion**: `pandoc` and LaTeX (e.g., `texlive-xetex`) for PDF output

### System Resources
- **CPU/RAM**: Minimal; notebooks process small datasets (hundreds of controls/servers)
- **Disk**: ~50 MB for code and dependencies, plus space for output artifacts

### Access Rights
- **User**: No root/sudo required for installation and normal usage
- **Network**: Internet access for `pip` package installation; no runtime network calls by default

## Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/ranas-mukminov/ru-it-audit-notebook.git
cd ru-it-audit-notebook

# 2. Install the package in editable mode
pip install -e .[dev]

# 3. Run example notebooks with sample data
ru-it-audit run-notebooks \
  --inventory examples/inventory/sample_inventory.csv \
  --answers-dir examples/inputs \
  --out-dir .artifacts/notebooks

# 4. Build HTML and PDF reports
ru-it-audit build-report \
  --artifacts-dir .artifacts/notebooks \
  --out-html .artifacts/report.html \
  --out-pdf .artifacts/report.pdf

# 5. Open the report
xdg-open .artifacts/report.html  # or open .artifacts/report.pdf
```

Default credentials/URLs: Not applicable (static report generator).

## Detailed Installation

### Install on Ubuntu / Debian

```bash
# Update package index and install Python 3.10+
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Clone the repository
git clone https://github.com/ranas-mukminov/ru-it-audit-notebook.git
cd ru-it-audit-notebook

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install the package with development dependencies
pip install --upgrade pip
pip install -e .[dev]

# Optional: Install LaTeX for PDF generation
sudo apt install -y pandoc texlive-xetex texlive-fonts-recommended texlive-lang-cyrillic
```

### Install on RHEL / Rocky / AlmaLinux

```bash
# Install Python 3.10+ (RHEL 8+ includes python39 or python3.11 module)
sudo dnf install -y python3.11 python3.11-pip

# Clone and navigate
git clone https://github.com/ranas-mukminov/ru-it-audit-notebook.git
cd ru-it-audit-notebook

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install
pip install --upgrade pip
pip install -e .[dev]

# Optional: LaTeX toolchain
sudo dnf install -y pandoc texlive-xetex
```

### Install with Docker (Optional)

If you prefer containerized execution:

```bash
# Build Docker image
docker build -t ru-it-audit-notebook:latest .

# Run notebooks in container (mount local data)
docker run --rm \
  -v $(pwd)/examples:/data \
  -v $(pwd)/.artifacts:/output \
  ru-it-audit-notebook:latest \
  ru-it-audit run-notebooks \
    --inventory /data/inventory/sample_inventory.csv \
    --answers-dir /data/inputs \
    --out-dir /output/notebooks
```

> **Note**: Dockerfile is not included in the current repository; you would need to create a simple Python-based image installing `ru-it-audit-notebook`.

## Configuration

### Inventory CSV Format

The `--inventory` file should be a CSV with columns matching your infrastructure:

```csv
hostname,ip,os,role,location,owner
app-db-01,10.0.1.10,Ubuntu 22.04,database,DC-Moscow,IT-Team
web-frontend,10.0.2.5,Debian 11,web,DC-SPB,DevOps
1c-server,192.168.1.20,Windows Server 2019,1C,Office,Accounting
```

Adjust column names as needed; notebooks read via `pandas.read_csv()`.

### Answers Directory Structure

Answer files can be YAML or JSON, named per checklist:

```
examples/inputs/
  pdn_152fz_answers.yaml
  backup_resilience_answers.yaml
  kii_basic_answers.yaml
  app_1c_answers.yaml
```

**Example answer file** (`pdn_152fz_answers.yaml`):

```yaml
# Answer values must match 'answer_type' and 'scoring' keys in checklist
PDN-001: true              # boolean: operator assigned
PDN-002: "complete"        # choice: registry state
PDN-003: "full"            # choice: legal basis coverage
PDN-004: 3                 # scale: documented controls level
PDN-005: true              # boolean: localization compliance
PDN-006: 2                 # scale: logging and access control
```

### Scoring Profiles

Edit `checklists/scoring_profiles.yaml` to adjust global weights and thresholds:

```yaml
profiles:
  strict:
    weight_multiplier: 1.2
    critical_threshold_pct: 10  # Any control >10% critical → overall fail
  relaxed:
    weight_multiplier: 0.8
    critical_threshold_pct: 25
```

Apply a profile via CLI (feature pending) or edit default in `it_audit_report/config.py`.

### Environment Variables

Set these to customize behavior:

```bash
export AUDIT_NOTEBOOK_AI_PROVIDER="openai"  # or "noop" (default)
export AUDIT_NOTEBOOK_AI_MODEL="gpt-4"
export AUDIT_NOTEBOOK_AI_API_KEY="sk-..."
```

AI features are opt-in; default `NoopAIProvider` ensures no external calls.

## Usage & Common Tasks

### Run All Notebooks

```bash
ru-it-audit run-notebooks \
  --inventory examples/inventory/sample_inventory.csv \
  --answers-dir examples/inputs \
  --out-dir .artifacts/notebooks
```

This executes all notebooks in `notebooks/` via `papermill`, injecting parameters and saving outputs.

### Build Final Report

```bash
ru-it-audit build-report \
  --artifacts-dir .artifacts/notebooks \
  --out-html .artifacts/report.html \
  --out-pdf .artifacts/report.pdf
```

Converts notebook outputs to Markdown, then to HTML/PDF via `nbconvert`.

### Access Web UI

Not applicable (this is a static generator). Open generated HTML in browser:

```bash
xdg-open .artifacts/report.html
# or
firefox .artifacts/report.html
```

### Add a New Checklist

1. Create `checklists/my_checklist.yaml` following the schema in existing files.
2. Add a corresponding notebook `notebooks/05_my_checklist.ipynb`.
3. Load and score in the notebook:

```python
from it_audit_report.checklist_loader import load_checklist
from it_audit_report.scoring import score_checklist

checklist = load_checklist("checklists/my_checklist.yaml")
results = score_checklist(checklist, answers)
print(results)
```

4. Update `99_report_assembler.ipynb` to include the new section.

### Validate Checklist YAML

```bash
yamllint checklists/*.yaml
```

Or use the CLI validator (if implemented):

```bash
ru-it-audit validate-checklist checklists/pdn_152fz.yaml
```

## Update / Upgrade

### Update from Git

```bash
cd ru-it-audit-notebook
git pull origin main
pip install -e .[dev]  # reinstall in case dependencies changed
```

### Upgrade Python Dependencies

```bash
pip install --upgrade -e .[dev]
```

### Breaking Changes

- **v0.1 → v0.2 (future)**: Checklist schema may add required fields; review migration guide in `CHANGELOG.md`.

## Logs, Monitoring, Troubleshooting

### Logs Location

- **CLI logs**: Printed to stdout/stderr; redirect with `ru-it-audit run-notebooks 2>&1 | tee audit.log`
- **Notebook execution**: Papermill outputs cell logs to `.artifacts/notebooks/*.ipynb` (executed notebooks)

### Common Issues

#### Notebooks fail to run

**Symptom**: `FileNotFoundError: inventory file not found`

**Fix**:
```bash
# Check inventory path matches CLI argument
ls -lh examples/inventory/sample_inventory.csv
# Ensure it's passed correctly
ru-it-audit run-notebooks --inventory examples/inventory/sample_inventory.csv ...
```

#### PDF generation fails

**Symptom**: `nbconvert` error or missing fonts in PDF

**Fix**:
```bash
# Install LaTeX backend
sudo apt install -y pandoc texlive-xetex texlive-fonts-recommended texlive-lang-cyrillic
# If Cyrillic fonts are missing:
sudo apt install -y fonts-liberation fonts-dejavu
```

#### No data in report / empty scores

**Symptom**: Report shows "No controls evaluated"

**Fix**:
- Verify answer file names match checklist IDs.
- Check `answers_dir` contains `*_answers.yaml` files.
- Inspect notebook outputs in `.artifacts/notebooks/` for errors.

#### Import errors

**Symptom**: `ModuleNotFoundError: No module named 'it_audit_report'`

**Fix**:
```bash
# Ensure package is installed in editable mode
pip install -e .
# Or activate the virtual environment if you created one
source venv/bin/activate
```

### Enable Debug Mode

Set environment variable for verbose CLI output:

```bash
export AUDIT_NOTEBOOK_DEBUG=1
ru-it-audit run-notebooks ...
```

## Security Notes

### Minimal Security Checklist

- **Protect sensitive data**: Do not commit real inventory CSVs or answer files with production hostnames/IPs to public repos.
- **AI provider safety**: Default `NoopAIProvider` makes no external API calls. Enable AI features only if you trust the provider and have reviewed data sharing policies.
- **Report confidentiality**: Generated HTML/PDF reports may contain sensitive infrastructure details. Store and transmit securely (encrypt, restrict access).
- **Dependency hygiene**: Run `pip-audit` and `bandit` regularly to detect known vulnerabilities in dependencies (see `scripts/security_scan.sh`).

### Recommendations

- Use private Git repositories for audit data.
- Encrypt report artifacts at rest (e.g., LUKS volumes, VeraCrypt).
- Limit access to `.artifacts/` and `examples/` directories (set `chmod 700` if needed).
- Review AI-generated content manually before including in official deliverables.

> **Legal Disclaimer**: This tool does not provide legal advice or certification. Always consult legal and compliance experts for 152-ФЗ, КИИ, and other regulations.

## Project Structure

```
ru-it-audit-notebook/
├── checklists/               # YAML definitions for compliance controls
│   ├── pdn_152fz.yaml       # Personal data (152-ФЗ)
│   ├── backup_resilience.yaml
│   ├── kii_basic.yaml       # Critical information infrastructure
│   └── app_1c.yaml          # 1C application landscape
├── it_audit_report/          # Core Python library
│   ├── checklist_loader.py
│   ├── scoring.py
│   ├── models.py
│   ├── inventory/           # CSV parsing
│   ├── report/              # Markdown generation
│   ├── ai/                  # AI integration stubs
│   └── cli/                 # Typer CLI commands
├── notebooks/                # Jupyter notebooks for execution
│   ├── 00_inventory_servers.ipynb
│   ├── 01_pdn_152fz_checklist.ipynb
│   └── 99_report_assembler.ipynb
├── examples/                 # Sample data for testing
│   ├── inventory/
│   ├── inputs/
│   └── outputs/
├── templates/                # Jinja2 templates for reports
├── tests/                    # pytest unit and integration tests
├── scripts/                  # CI/CD and dev helper scripts
│   ├── lint.sh
│   ├── security_scan.sh
│   └── dev_run_all_tests.sh
├── .github/workflows/        # GitHub Actions CI
├── pyproject.toml            # Project metadata and dependencies
├── CONTRIBUTING.md
├── LEGAL.md
└── LICENSE                   # Apache-2.0
```

## Roadmap / Plans

- **v0.2**: Add CLI command `validate-checklist` for schema validation.
- **v0.3**: Support for additional checklists (FSTEC GosSOPKA profile, ISO 27001 mapping).
- **v0.4**: Web UI for interactive questionnaire filling (Flask/FastAPI-based).
- **v0.5**: Integration with asset management tools (API connectors for popular CMDB/ITSM systems).

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Contributing

We welcome contributions! To maintain quality and safety:

### How to Open Issues

- Use GitHub Issues: [https://github.com/ranas-mukminov/ru-it-audit-notebook/issues](https://github.com/ranas-mukminov/ru-it-audit-notebook/issues)
- Provide minimal reproducible example (inventory CSV, answer YAML, CLI command).
- Avoid sharing sensitive production data; anonymize hostnames and IPs.

### How to Propose a Pull Request

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-checklist`.
3. Write tests first (TDD approach required for core logic).
4. Implement changes.
5. Run the full test suite: `./scripts/dev_run_all_tests.sh`.
6. Ensure linting passes: `./scripts/lint.sh`.
7. Commit with clear messages: `git commit -m "Add КИИ extended checklist"`.
8. Push and open a PR against `main`.

### Code Style Basics

- **Python**: PEP 8, type hints everywhere, use `ruff` for formatting and linting.
- **YAML**: Use `yamllint` to validate checklist files.
- **Notebooks**: Keep cells minimal and reproducible; avoid destructive actions.
- **Security**: Default to `NoopAIProvider`; require explicit opt-in for external services.
- **Documentation**: Update both `README.md` and `README.ru.md` for user-facing changes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed workflow rules.

## License

This project is licensed under the **Apache License 2.0**.  
See [LICENSE](LICENSE) for full text.

You may use this software commercially, modify, and distribute it, provided you retain the original license notices.

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

For production-grade deployment, customized checklists, integration with your CMDB/ITSM, and professional audit services, commercial support is available:

- **IT infrastructure audit**: Servers, 1C landscapes, cloud (Yandex.Cloud, VK Cloud, etc.)
- **Compliance assessment**: 152-ФЗ, КИИ, FSTEC standards
- **Regular reporting**: Automated workflows, CI/CD integration, executive dashboards
- **Training**: Workshops for internal audit teams and DevSecOps engineers

Visit [https://run-as-daemon.ru](https://run-as-daemon.ru) (Russian) or contact via GitHub profile for inquiries.

---

**Acknowledgments**: Thank you to the open-source community for Jupyter, Pandas, and Python tooling that made this project possible.
