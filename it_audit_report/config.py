from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHECKLIST_DIR = BASE_DIR / "checklists"
TEMPLATE_DIR = BASE_DIR / "templates" / "report"
DEFAULT_PROFILE = "smb_default"

NOTEBOOKS = [
    "00_inventory_servers.ipynb",
    "01_pdn_152fz_checklist.ipynb",
    "02_backup_resilience_checklist.ipynb",
    "03_kii_basic_checklist.ipynb",
    "04_applications_1c_business.ipynb",
    "99_report_assembler.ipynb",
]
