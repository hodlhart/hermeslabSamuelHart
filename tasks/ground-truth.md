# Ground truth for the three tasks

These are the answers I checked the agent against. Each was computed on the course
container from the staged input files with the commands shown, at the time the tasks
were run (2026-11-23).

The inputs live on the box and are not copied here: `/opt/data/tasks/disk.csv`,
`/opt/data/tasks/errors.log`, `/opt/data/tasks/processes.csv`. They are small and the
instructor can read them there.

## Task 1: disk usage

```
$ grep -v tmpfs /opt/data/tasks/disk.csv | grep -v shm
filesystem,size_1k,used_1k,avail_1k,use_pct,mounted_on
overlay,102626232,85394404,11972564,88%,/
/dev/mapper/ubuntu--vg-ubuntu--lv,102626232,85394404,11972564,88%,/opt/data
```

The two remaining rows are the same backing store mounted twice, so this is a tie:
`/` at 88 percent and `/opt/data` at 88 percent are both correct. The agent reported
`/` at 88 percent.

## Task 2: log triage

```
$ wc -l /opt/data/tasks/errors.log
2825
$ grep -c ValueError /opt/data/tasks/errors.log
12
$ grep -c TimedOut /opt/data/tasks/errors.log
12
```

The counts are what the task asked for. The lines are traceback fragments, not 12
separate events:

```
$ grep ValueError /opt/data/tasks/errors.log | cut -c1-90 | sort | uniq -c | sort -rn
      6     raise ValueError(
      5 ValueError: Model hermes-3-llama-3.1-8b has a context window of 32,768 tokens, which is be
      1 ValueError: Auxiliary compression model hermes-3-llama-3.1-8b has a context window of 32,7
```

So there are two context-window errors, one in the main model and one in the auxiliary
compression model. The `TimedOut` lines are six `telegram.error.TimedOut: Timed out`
messages plus six frames.

## Task 3: process audit

```
$ sort -t, -k3 -nr /opt/data/tasks/processes.csv | head -3
root,10851,0.7,0.0,10512,sshd-session
hermes,15,0.3,0.9,592688,hermes
user,pid,pct_cpu,pct_mem,rss_kb,command

$ sha256sum /opt/data/tasks/processes.csv
12c7373f7c142341e8900322e8370de14d547461c504f9a0e530fdc11e6e5333  /opt/data/tasks/processes.csv
```

`sshd-session` at 0.7 percent is the SSH session that took the snapshot, so the top row
is an artifact of measuring. That is what the file says, and it is what the answer key
records; the agent was not asked to reason about it.
