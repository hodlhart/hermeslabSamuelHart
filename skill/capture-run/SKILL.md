---
name: capture-run
description: Capture the outcome of an automation task into a run folder
---

## Capture Run

### Description
After completing an automation task, this skill captures the evidence into a run folder with transcript.md, any files produced, and a two-line summary at the top. Rules:

- Never overwrite an existing run folder
- Never write a transcript from memory or guesswork
- Confirm the paths it wrote at the end

### Usage

1. Create a timestamped directory runs/<NN>-<slug>/
2. Write transcript.md with what you were asked, the tool calls, and the outcome
3. Copy any files the task produced into runs/<NN>-<slug>/
4. Print the paths it created
