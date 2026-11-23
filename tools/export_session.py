#!/usr/bin/env python3
# INF601 - Advanced Programming in Python
# Samuel Hart
# Hermes Lab
"""Export Hermes sessions from state.db as a plain-text transcript.

Read-only. The database is opened with mode=ro so the export cannot change the
agent's state. Used to produce runs/*/session-log.md on the lab box.

Usage:
    python export_session.py SESSION_ID [SESSION_ID ...]

Each session prints its messages in order: role, time, tool name, tool
arguments, content. The CLI writes each continued turn as its own session, so a
task's transcript is the list of its session ids in time order; pass them all.
List them with:

    select id, started_at from sessions where source = 'cli' order by started_at;
"""

import argparse
import datetime
import json
import sqlite3
import sys

DB = "/opt/data/state.db"


def connect(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def print_session(conn, sid):
    row = conn.execute(
        "select started_at from sessions where id = ?", (sid,)
    ).fetchone()
    if row is None:
        print(f"SESSION {sid} not found", file=sys.stderr)
        return
    started = datetime.datetime.fromtimestamp(row[0]).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nSESSION {sid}  ({started})")
    for role, content, tcs, tname, ts in conn.execute(
        "select role, content, tool_calls, tool_name, timestamp "
        "from messages where session_id = ? order by id",
        (sid,),
    ):
        when = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        print(f"\n--- {role} {when} ---")
        if tname:
            print(f"[tool: {tname}]")
        if content:
            print(content.strip())
        if tcs:
            try:
                calls = json.loads(tcs)
            except ValueError:
                print(tcs)
                continue
            for call in calls:
                fn = call.get("function", {})
                print(f"[call {fn.get('name')}] {fn.get('arguments')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("session_ids", nargs="+")
    ap.add_argument("--db", default=DB)
    args = ap.parse_args()

    conn = connect(args.db)
    for sid in args.session_ids:
        print_session(conn, sid)


if __name__ == "__main__":
    main()
