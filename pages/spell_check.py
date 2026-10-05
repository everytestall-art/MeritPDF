import runpy
from pathlib import Path


project_dir = Path(__file__).resolve().parent.parent
runpy.run_path(str(project_dir / "App_Spell.py"))