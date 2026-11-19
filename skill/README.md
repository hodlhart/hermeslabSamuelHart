# skill/

The reusable skill I taught the agent, copied out of its container.

Source on the server: `/opt/data/skills/<name>/SKILL.md`
Copied here as: `skill/<name>/SKILL.md`

The assignment requires the skill to have been used at least once, so a
`runs/` entry shows the invocation. The copy here should be byte-identical to
what is on the server; the server copy is the live one and this is the snapshot.

## Copied out

`capture-run`, 2026-11-19, copied with:

```
scp -i ~/.ssh/id_ed25519_hermeslab -P <port> \
  hermes@<course-server>:/opt/data/skills/capture-run/SKILL.md skill/capture-run/SKILL.md
```

Verified byte-identical to the server copy (sha256 `7968107e...`).

## How it was built

Three attempts. The first two are worth keeping because they show the loop:

1. The agent wrote front matter using `layout` and `summary`, and invented a
   `hermes skill call` command. Neither exists: Hermes requires `name` and
   `description`, and there is no such subcommand.
2. Corrected, it described a finished file in its reply without calling any
   tool. The file did not exist. The shared model on the lab server is a chat
   model rather than a tool-call-tuned one, and it narrated the action instead
   of taking it.
3. Told to call `skill_manage` and report its raw result, it did, and the file
   landed.
