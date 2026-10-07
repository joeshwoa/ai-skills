"""premium-design-kit — shared design engine for premium-presentations, premium-documents,
premium-spreadsheets and course-studio. Import with:  sys.path.insert(0, <kit>/lib); import pdk"""
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
SKILLS = KIT.parent
__version__ = "1.0.0"
