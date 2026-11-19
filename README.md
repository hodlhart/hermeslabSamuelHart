# hermeslabSamuelHart

INF 601 Hermes Lab: a persistent Hermes agent on the course server, taught one
reusable skill, and directed through three multi-step automation tasks.

The agent runs in a container on the course server. Two ways in:

```
Telegram  a bot I created with @BotFather
SSH       ssh -p <port> hermes@<course-server>
```

## Contents

```
runs/     transcripts and outputs from the three automation tasks
skill/    the reusable skill, copied out of the agent's /opt/data/skills/
```

Any Python submitted here heads with:

```python
# INF601 - Advanced Programming in Python
# Samuel Hart
# Hermes Lab
```

## What I automated

Filled in as each task completes, in `runs/`.

1. TODO
2. TODO
3. TODO

## The skill I taught it

TODO, plus the run where the skill was invoked.

## How I directed the agent

The loop for each task: state the goal, read the tool calls it proposes, check
the result against what I asked for, correct it where it drifted.

TODO: the specific corrections, and what each one changed.

## Hermes compared to Claude Code

Both are harnesses around a model: the model proposes tool calls, the harness
runs them, results come back. TODO: what felt the same, what differed.

Points worth comparing, from using both this week:

- Persistent memory. The Hermes agent keeps memory and sessions across
  conversations in its container. Claude Code starts fresh per session unless
  something is written to disk in the repo.
- Channel. Telegram means the agent is reachable away from the machine. Claude
  Code is a terminal in the project.
- Environment ownership. The Hermes box is a server I do not administer. Claude
  Code runs on my own machine, on files I own.
- Skills. Same idea in both: a folder with a SKILL.md, loaded when relevant.
  TODO: compare what each harness does with it.

## Final project connection

The Week 13 outline sketched two agentic requirements, an MCP server and an
Agent Skill. TODO: confirm or revise that choice, using what this lab showed
about persistent memory, tools, permissions, and who controls the environment.

## AI Usage

This assignment is AI use by design. Being specific about the split:

- **What the agent did.** TODO
- **What I decided, specified, and verified.** TODO
- **What I corrected when it went wrong.** TODO

## Notes

- The Telegram bot token and the SSH credentials are not in this repo. They live
  in the agent's `.env` on the server.
- The instructor reviews the agent's live state on the server (memory, skills,
  logs) against this repo, so the evidence here is what the agent actually did.
