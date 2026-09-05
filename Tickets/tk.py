#!/usr/bin/env python3
"""Tiny local ticket tracker for the sign library. Tickets are markdown files in this folder.

  python3 Tickets/tk.py list [--status open] [--priority P0] [--area net] [--project econ] [--all]
  python3 Tickets/tk.py show SGN-004
  python3 Tickets/tk.py new "Title of the ticket" [--priority P1] [--area sources] [--project usa]
  python3 Tickets/tk.py set SGN-004 status in-progress     (also: priority, area, project)
  python3 Tickets/tk.py index                                (rewrites INDEX.md)

No dependencies. Edit ticket files by hand whenever you like; the frontmatter is the source of truth.
"""
import os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATUSES = ["open", "in-progress", "blocked", "done", "wontfix"]
PRIORITIES = ["P0", "P1", "P2", "P3"]
PROJECTS = {
    "australia": "Australia — national and state packs",
    "usa": "USA — federal and state packs",
    "nz": "New Zealand — TCD Manual pack",
    "uk": "United Kingdom — TSRGD packs",
    "pipeline": "Extractor and QA tooling",
    "repo": "Repo, docs and layout",
    "none": "Unassigned",
}
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def ticket_files():
    return sorted(f for f in os.listdir(HERE) if re.match(r"SGN-\d{3}-.*\.md$", f))


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = FM_RE.match(text)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    fm["_path"] = path
    fm["_body"] = text[m.end():]
    return fm


def load_all():
    out = []
    for f in ticket_files():
        t = parse(os.path.join(HERE, f))
        if t:
            out.append(t)
    return out


def find(tid):
    tid = tid.upper()
    if re.fullmatch(r"\d+", tid):
        tid = f"SGN-{int(tid):03d}"
    for t in load_all():
        if t.get("id") == tid:
            return t
    sys.exit(f"no ticket {tid}")


def write(t):
    keys = ["id", "title", "status", "priority", "area", "project", "created", "updated", "source"]
    fm = "\n".join(f"{k}: {t[k]}" for k in keys if k in t)
    open(t["_path"], "w", encoding="utf-8").write(f"---\n{fm}\n---\n{t['_body']}")


def cmd_list(args):
    want = {"status": None, "priority": None, "area": None, "project": None}
    show_all = "--all" in args
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--") and a[2:] in want and i + 1 < len(args):
            want[a[2:]] = args[i + 1]
            i += 2
        else:
            i += 1
    rows = []
    for t in load_all():
        if not show_all and want["status"] is None and t["status"] in ("done", "wontfix"):
            continue
        if any(v and t.get(k) != v for k, v in want.items()):
            continue
        rows.append(t)
    rows.sort(key=lambda t: (PRIORITIES.index(t["priority"]) if t["priority"] in PRIORITIES else 9, t["id"]))
    for t in rows:
        print(f"{t['id']}  {t['priority']}  {t['status']:<11} {t['area']:<9} {t['project']:<9} {t['title']}")
    print(f"\n{len(rows)} ticket(s)")


def cmd_show(args):
    t = find(args[0])
    print(open(t["_path"], encoding="utf-8").read())


def cmd_new(args):
    if not args or args[0].startswith("--"):
        sys.exit('usage: tk.py new "Title" [--priority P1] [--area sources] [--project usa]')
    title = args[0]
    opts = {"priority": "P2", "area": "sources", "project": "none"}
    i = 1
    while i + 1 < len(args):
        if args[i].startswith("--") and args[i][2:] in opts:
            opts[args[i][2:]] = args[i + 1]
        i += 2
    n = max([int(f[4:7]) for f in ticket_files()] + [0]) + 1
    tid = f"SGN-{n:03d}"
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48].rstrip("-")
    today = datetime.date.today().isoformat()
    body = f"""---
id: {tid}
title: {title}
status: open
priority: {opts['priority']}
area: {opts['area']}
project: {opts['project']}
created: {today}
updated: {today}
source: manual
---

## Summary

(what is wrong and why it matters)

## Evidence

- (sources, URLs, files — verified)

## Fix

(the concrete change)

## Verify

(how we know it is done)

## Log

- {today} — filed.
"""
    path = os.path.join(HERE, f"{tid}-{slug}.md")
    open(path, "w", encoding="utf-8").write(body)
    print(path)
    cmd_index([])


def cmd_set(args):
    if len(args) < 3:
        sys.exit("usage: tk.py set SGN-004 <status|priority|area|project> <value>")
    t = find(args[0])
    field, value = args[1], args[2]
    if field == "status" and value not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    if field == "priority" and value not in PRIORITIES:
        sys.exit(f"priority must be one of {PRIORITIES}")
    if field not in ("status", "priority", "area", "project"):
        sys.exit("field must be status, priority, area or project")
    t[field] = value
    t["updated"] = datetime.date.today().isoformat()
    t["_body"] = t["_body"].rstrip("\n") + f"\n- {t['updated']} — {field} → {value}.\n"
    write(t)
    print(f"{t['id']} {field} = {value}")
    cmd_index([])


def cmd_index(args):
    ts = load_all()
    ts.sort(key=lambda t: (PRIORITIES.index(t["priority"]) if t["priority"] in PRIORITIES else 9, t["id"]))
    open_ts = [t for t in ts if t["status"] not in ("done", "wontfix")]
    counts = {p: sum(1 for t in open_ts if t["priority"] == p) for p in PRIORITIES}
    lines = ["# Sign library tickets", "",
             f"Generated by `python3 Tickets/tk.py index` — edit the ticket files, not this table.",
             "",
             f"Open: {len(open_ts)} ({', '.join(f'{p} {n}' for p, n in counts.items() if n)}) · Closed: {len(ts) - len(open_ts)}",
             ""]
    for key, name in PROJECTS.items():
        group = [t for t in ts if t.get("project") == key]
        if not group:
            continue
        lines += [f"## {name} (`{key}`)", "", "| ID | Pri | Status | Area | Title |", "|---|---|---|---|---|"]
        for t in group:
            fn = os.path.basename(t["_path"])
            lines.append(f"| [{t['id']}]({fn}) | {t['priority']} | {t['status']} | {t['area']} | {t['title']} |")
        lines.append("")
    open(os.path.join(HERE, "INDEX.md"), "w", encoding="utf-8").write("\n".join(lines))
    if args is not None:
        print(f"INDEX.md: {len(ts)} tickets, {len(open_ts)} open")


if __name__ == "__main__":
    cmds = {"list": cmd_list, "show": cmd_show, "new": cmd_new, "set": cmd_set, "index": cmd_index}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]](sys.argv[2:])
