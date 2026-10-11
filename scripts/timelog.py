"""Task timer for data/time_log.csv (task, part, start, end, claude_run_time_min, my_elapsed_time, notes).

claude_run_time_min = minutes logged by this script; my_elapsed_time is filled in by hand.

  python scripts/timelog.py start "Tab A research" --part "Tables"
  python scripts/timelog.py end   "Tab A research" [--notes "..."]
  python scripts/timelog.py add   "Prompt 0 setup" --part Setup --start 2026-10-10T11:41 --end 2026-10-10T11:52 --notes "..."

`start` writes a row with an empty end; `end` fills the most recent open row for that task.
"""
import argparse
import csv
import datetime as dt
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "data" / "time_log.csv"
FIELDS = ["task", "part", "start", "end", "claude_run_time_min", "my_elapsed_time", "notes"]
FMT = "%Y-%m-%dT%H:%M"


def now():
    return dt.datetime.now().strftime(FMT)


def load():
    if not LOG.exists() or LOG.stat().st_size == 0:
        return []
    with LOG.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in rows)


def minutes(start, end):
    return str(round((dt.datetime.strptime(end, FMT) - dt.datetime.strptime(start, FMT)).total_seconds() / 60))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["start", "end", "add"])
    ap.add_argument("task")
    ap.add_argument("--part", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--start")
    ap.add_argument("--end")
    a = ap.parse_args()
    rows = load()

    if a.action == "start":
        rows.append(dict(task=a.task, part=a.part, start=now(), notes=a.notes))
    elif a.action == "add":
        rows.append(dict(task=a.task, part=a.part, start=a.start, end=a.end,
                         claude_run_time_min=minutes(a.start, a.end), notes=a.notes))
    else:
        open_rows = [r for r in rows if r["task"] == a.task and not r.get("end")]
        if not open_rows:
            raise SystemExit(f"No open row for task '{a.task}'")
        r = open_rows[-1]
        r["end"] = now()
        r["claude_run_time_min"] = minutes(r["start"], r["end"])
        if a.notes:
            r["notes"] = (r["notes"] + " " + a.notes).strip()
    save(rows)
    print(rows[-1] if a.action != "end" else r)


if __name__ == "__main__":
    main()
