"""Print the letter body and the key Reg 30 annexure fields from saved raw sources.

  python scripts/reg30_fields.py S045 S046 ...
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parent.parent / "sources" / "raw"
KEYS = [r"Cost of acquisition", r"Percentage of shareholding", r"turnover", r"Revenue from operations",
        r"Objects and (effects|impact)", r"time period for completion", r"consideration of"]

for sid in sys.argv[1:]:
    f = next(RAW.glob(f"{sid}_*.txt"))
    t = re.sub(r"\s+", " ", f.read_text(encoding="utf-8").split("-" * 70, 1)[-1])
    i = t.find("Dear Sir")
    print(f"##### {f.name}\nBODY: {t[i:i+900] if i >= 0 else t[:900]}")
    for k in KEYS:
        for m in list(re.finditer(k, t, re.I))[:2]:
            print(f"  [{k}] {t[m.start():m.start()+380]}")
    print()
