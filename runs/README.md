# runs/

One directory per automation task, numbered in the order they were done. Each
holds the evidence for that task:

```
runs/01-<slug>/
  transcript.md     what I asked, the tool calls, the result
  <output files>    anything the task produced
```

## How transcripts get here

Saved during the task, not rebuilt afterwards. The assignment says it plainly:
save them as you go, do not reconstruct them at the end. The instructor compares
this repo against the agent's own logs, so a reconstructed transcript is worse
than a short honest one.

Two ways to capture, both fine:

- Copy the exchange out of Telegram (long-press a message, or use the desktop
  app's chat export) into `transcript.md`.
- Use the agent's own `capture-run` skill, which writes the directory and the
  transcript from the live session.

## Tasks

TODO as each one is done.
