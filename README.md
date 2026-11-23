# hermeslabSamuelHart

INF 601 Hermes Lab: a persistent Hermes agent on the course server, taught one reusable
skill, and directed through three multi-step automation tasks.

The agent runs in a container on the course server. Two ways in:

```
Telegram  a bot I created with @BotFather, allow-listed to my account
SSH       ssh -p <port> hermes@<course-server>
```

The bot token and the server address are not in this repository. The instructor has both.

## Contents

```
runs/     one folder per task: the agent's transcript, the output, and the session log
skill/    the reusable skill, copied out of the agent's /opt/data/skills/
tasks/    the answer key I checked each task against
tools/    the read-only exporter used to pull the session logs out of state.db
```

Any Python submitted here heads with:

```python
# INF601 - Advanced Programming in Python
# Samuel Hart
# Hermes Lab
```

## What I automated

Three tasks, each run on the container with the agent's terminal tool. The inputs were
staged first, so every answer had a fixed and checkable source.

### 1. Disk usage (`runs/01-disk-usage/`)

Input: `tasks/disk.csv` on the box, a `df -k` style table. The job was to name the
mounted filesystem with the highest used percentage.

The agent ran `grep -v tmpfs` and `grep -v shm` on the CSV, wrote
`Fullest filesystem: / at 88%` to a report file, and read it back. Output in
`disk_finding.md`.

Correction: its first answer was `/mnt/data at 92 percent`, values that appear nowhere in
the file, and part of the reply came back in Thai. A correction that banned answering
from memory and named the exact `grep` command produced the right rows.

### 2. Log triage (`runs/02-log-triage/`)

Input: `tasks/errors.log`, 2825 lines of the box's own error log. The job was the line
count plus counts of `ValueError` and `TimedOut` lines.

The agent ran `wc -l` (2825), then `grep -c` for each pattern (12 and 12), then read the
last matching lines. Output in `log_triage.md`.

Correction: the summary I dictated said the 12 `ValueError` lines repeat one message.
Counting distinct messages showed two context-window errors, one in the main model and
one in the auxiliary compression model. The counts the task asked for were right; the
interpretation was wrong, and `runs/02-log-triage/correction.md` records the fix and the
counts.

### 3. Process audit (`runs/03-process-audit/`)

Input: `tasks/processes.csv`, a `ps -eo` snapshot. The job was the process with the
highest CPU, plus file verification.

The agent sorted the file by `pct_cpu` and read `sshd-session` (pid 10851) at 0.7 percent,
then the `hermes` process at 0.3. It ran `sha256sum` on the input and recorded
`12c7373f...` with the result. Output in `process_audit.md`.

Corrections: two wrong answers came first. It proposed a fabricated `/proc/stat` loop
instead of reading the table, then claimed the table had never been provided and asked me
to fill in placeholders. Handing it the exact `sort` command and requiring raw output
fixed both.

Each run folder holds the transcript the agent wrote while following `capture-run`, the
output file it produced, and `session-log.md`. The session log is exported from the
agent's own `state.db` for the turns that produced the run: prompt, tool arguments, raw
tool result, reply.

## The skill I taught it

`capture-run` (in `skill/`) packages how a finished task becomes evidence:

- create `runs/<NN>-<slug>/`
- write `transcript.md` with what was asked, the commands, and the outcome
- copy any output the task produced into the folder
- print the paths it created

The rules in the skill are: never overwrite an existing folder, never write a transcript
from memory, and always confirm the paths.

It was built on 2026-11-19 over Telegram, in three passes. The first file was rejected by
`skill_manage` because the front matter had no closing `---`. The second used `layout:`
and `summary:` instead of the required `name:` and `description:`. The third was accepted,
and only after I told the agent to call `skill_manage` and report its raw result, because
before that it described the finished file in its reply without writing anything. The
copy here is byte-identical to `/opt/data/skills/capture-run/SKILL.md` (sha256
`7968107e...`).

It was used three times, once per task. Each folder in `runs/` was created by the agent
following the skill in a normal turn.

## How I directed it

The loop for every task: state the goal, make it run one command, read the raw output,
check it against `tasks/ground-truth.md`, and correct the specific thing that was wrong.

The first attempt was the exception, and it is kept in `runs/00-first-attempt/`. I gave
the agent one prompt with seven numbered steps. It read the CSV, then edited it, renaming
the column header it was only supposed to read. Its shell pipeline collapsed on quoting
(`sys/: No such file or directory`, `unexpected EOF while looking for matching quote`),
it produced two empty files, and then it reported success and listed a transcript path
that did not exist. Nothing in that final message was true.

What worked after that:

- one command per turn, written out exactly, with no placeholders to fill in
- an explicit ban on answering from memory (`92 percent appears nowhere in the file`)
- a required read-back: `cat`, `wc -c`, `ls -l`, `sha256sum`
- every number checked against the answer key before it was accepted

That is the harness lesson of the lab. The model's tool calls were fine; its habit of
summarizing work it had not done was the failure, and only the raw output made the
difference visible.

## Iteration

Four things changed between attempts, each visible in the logs:

1. Step size. A seven-step prompt failed; single-command turns worked. The model does not
   hold a long procedure across one turn.
2. Trust. Asking for a value from a table it had already printed produced an invented one.
   Asking it to run a command that prints the value did not.
3. Verification. Every later turn specified the read-back up front, so a false success
   claim had somewhere to fail.
4. The answer key itself. The distinct-message count for the log task showed that my own
   dictated summary was wrong. Checking the agent is also checking the checker.

## Hermes compared to Claude Code

Both are harnesses around a model. The model proposes tool calls, the harness executes
them and returns the results, and the person in the loop decides whether the result is
real. In both tools, that last part is the job.

Where they differed in this course:

Hermes on the course server:

- Persistent. Memory, sessions, and skills live in `/opt/data/` and survive across
  conversations and days. The skill built on 2026-11-19 was still there on 2026-11-23 and
  loaded in a fresh session.
- Reachable away from the desk. Telegram works from a phone; SSH works from any terminal.
- Somebody else controls the environment. The container is administered by the course
  staff. There is no `sudo` and no web-search key, and inference comes from a shared
  endpoint. When the endpoint's context window was smaller than Hermes requires, that was
  a fact about the server, not something I could fix.
- The model is served under the id `hermes-3-llama-3.1-8b`, and this endpoint has been
  re-served with different weights under that same id before. Whatever the weights are, it
  behaves like a chat model rather than a tool-call-tuned one: it narrated writes it never
  made and invented values. The harness made that visible, but only because the raw tool
  output was there to compare against.

Claude Code on my machine:

- Fresh per session. State survives only if it is written into the project, which in
  practice meant `requirements.txt` and `CLAUDE.md`.
- I own everything: the files, the model endpoint (local Ollama with
  `deepseek-v4.1-flash:cloud`), and the permissions.
- No chat surface. It is a terminal in the project directory, not something I can message
  from a phone.
- The model follows a multi-step instruction far more reliably, so the loop is shorter and
  the corrections are about design rather than about whether a file exists.

What felt the same: the loop, the shape of a tool call, and the need to read the result
instead of the summary.

## Final project connection

The Week 13 outline proposed two agentic requirements: an MCP server and an Agent Skill.
The lab confirms both, and changes what I expect from each.

- The MCP server is `fathom`, built this week in `Week 15/fathom`. It exposes the Weirvern
  console as ten tools, nine read and one write. The write tool, `propose_block`, files a
  proposal and does not block.
- The Agent Skill is `threat-hunt`, at `.claude/skills/threat-hunt/SKILL.md` in that repo.
  It encodes the method for turning a detector score into a conclusion: find what fired,
  identify the host, pivot on its traffic, compare against history, and state what the
  evidence does not support.

The lab is why I am keeping both. A skill is how a procedure survives a session and gets
followed again; the three runs here are one skill applied three times without
re-explaining it. An MCP server is how a model reaches a system through named, described
tools instead of a shell. The lab also showed the failure that matters for `fathom`: a
weak model will fill a missing value rather than say it is missing. That is why `fathom`'s
tools say when the shape is not understood instead of returning blanks, and why its only
write tool proposes rather than acts.

## AI Usage

- What the agent did. On the course server it ran every command in `runs/`, read the
  inputs, wrote the three output files, and created each run folder by following
  `capture-run`. The session logs are its own record.
- What I decided and specified. I chose the three tasks, staged the three input files,
  wrote every prompt, and checked each result against `tasks/ground-truth.md` before
  accepting it.
- What I corrected. The failed first attempt is in `runs/00-first-attempt/`. The invented
  disk figure, the made-up `/proc/stat` command, and the claim that the table had not been
  provided are in the task session logs with the corrections that followed. My own wrong
  summary of the log task is corrected in `runs/02-log-triage/correction.md`.
- What a local assistant did. I used a Hermes instance on my own machine to help phrase the
  single-command prompts, to export the session logs from the agent's `state.db`, and to
  diff each answer against the staged data. I reviewed every exchange before committing
  it. The work recorded in `runs/` is the lab agent's, not the local assistant's.

## Notes

- No token, password, server address, or port is in this repository. The bot token lives
  in the agent's `.env` on the server.
- The instructor reviews the live agent (skills, memory, logs) against this repo, so the
  evidence here is what the agent actually did, including the parts where it was wrong.
