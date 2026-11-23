# runs/

One folder per automation task, in the order they were done:

```
runs/NN-<slug>/
  transcript.md     what I asked, the commands, the outcome
  <output files>    what the task produced
  session-log.md    the same turns, exported from the agent's state.db
  correction.md     only where a later check found the summary wrong
```

`00-first-attempt/` is the single-prompt attempt that failed. It is kept because the
failure is the iteration evidence.

## How these were made

- `transcript.md` was written by the agent itself, following the `capture-run` skill in a
  normal turn on the box.
- `session-log.md` is a read-only export of the agent's own session records from
  `/opt/data/state.db`: prompt, tool arguments, raw tool results, replies. Nothing in it
  is retyped.
- `disk_finding.md`, `log_triage.md`, and `process_audit.md` are the files the tasks
  produced, copied out of the run folders on the box.

The assignment asks for transcripts saved during the work, not rebuilt afterwards. The
session logs are the strongest form of that, because they come from the agent's state
rather than from anyone's memory.

## Task list

1. `01-disk-usage`: highest used filesystem in `tasks/disk.csv`.
2. `02-log-triage`: line count and error counts in `tasks/errors.log`.
3. `03-process-audit`: highest CPU process in `tasks/processes.csv`, with file
   verification.
