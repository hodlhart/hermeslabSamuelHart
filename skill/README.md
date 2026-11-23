# skill/

The reusable skill I taught the agent, copied out of its container.

Source on the server: `/opt/data/skills/<name>/SKILL.md`
Copied here as: `skill/<name>/SKILL.md`

The assignment requires the skill to have been used at least once, so each folder in
`runs/` shows an invocation. The copy here is byte-identical to what is on the server.

## Copied out

`capture-run`, built 2026-11-19, copied with:

```
scp -i <key> -P <port> hermes@<course-server>:/opt/data/skills/capture-run/SKILL.md \
  skill/capture-run/SKILL.md
```

Verified byte-identical to the server copy (sha256 `7968107e...`).

## How it was built

Three passes, all on 2026-11-19 over Telegram:

1. The first file was rejected by `skill_manage`: the front matter had no closing `---`
   line.
2. Corrected, the agent described the finished file in its reply without calling any
   tool. The file did not exist. The shared model on the lab server is a chat model rather
   than a tool-call-tuned one, and it narrated the action instead of taking it.
3. Told to call `skill_manage` and report its raw result, it did, and the file landed.

The rule in the skill ("never write a transcript from memory") came out of that second
failure.
