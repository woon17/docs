# Agentic Ticket Workflow

## 0. Tailor (paste this, then paste templates 1 + 2 right below it in the same message)

````markdown
# Task: Tailor the template prompts below to my existing AI coding agent setup

Below this message are 2 TEMPLATE prompts: "Improve my agent automation flow" and
"Evaluate my agent automation flow". They were written without knowing my setup, so some
parts are too specific and may conflict with it (paths, file names, phase names, script
template, ticket files, command names, metrics).
Your job: rewrite both templates so they fit my existing flow. Do NOT run them yet and
do NOT change my setup.

## Mode: READ-ONLY
- Built-in file tools only (read, list/glob, search). NO shell.
- Don't modify any existing file. Only write the 2 new prompt files in Step 4.

## Step 1: Learn my existing flow
Read all agent instruction/memory files, agent settings, custom commands, workflow
scripts/launchers, and 2–3 recent ticket folders. Summarize my flow in ≤ 20 lines:
folder layout, ticket files, session naming, phases/commands, script conventions,
what gets logged where.

## Step 2: Map template → my setup
For each template section, decide one of:
- KEEP: already fits as is
- ADAPT: same intent, but use my real names/paths/conventions
  (e.g. my ticket file names instead of TICKET.md/PLAN.md/LOG.md, my phase names,
  my script style instead of the template script)
- SUGGEST: I don't have this yet; keep it, but mark it "(optional suggestion)"
- DROP: conflicts with my flow or adds no value for my setup
Show a table: template section | decision | my equivalent | reason.

## Step 3: Ask before writing
List the unclear points (max 8 short questions), e.g. where two conventions in my setup
disagree, or a template idea could go either way. Wait for my answers.

## Step 4: Write the tailored prompts
After I answer, write 2 NEW files (pick a folder next to my existing setup, e.g.
<hub>/prompts/; tell me the path):
- improve.md: tailored version of template 1
- evaluate.md: tailored version of template 2 (metrics + "how to measure" use MY files
  and conventions; drop metrics that don't apply; keep scoring comparable across runs)

Rules for the rewrite:
- NON-NEGOTIABLE, copy as is: local changes only (no git writes/remote), no destructive
  commands, minimize shell approvals, preserve existing setup (no delete/rename/rewrite,
  additive changes, ask on conflict), read-only evaluation mode.
- Everything else: follow MY conventions over the template's.
- Use concrete paths/names from my setup, no placeholders like <hub> left unresolved.
- Keep each prompt self-contained (it must work when pasted into a fresh session).

## Step 5: Report
List what changed vs. the templates (KEEP/ADAPT/SUGGEST/DROP counts + key changes), and how
to run them later, e.g. `@<path>/evaluate.md run this`.
````

## 1. Improve (template)

````markdown
# Task: Improve my agent automation flow

You are improving my existing multi-ticket AI coding agent setup. Don't assume paths. Discover them.

IMPORTANT: my setup already works and other things depend on it. The Target Rules below
are SUGGESTIONS, not a spec. Improve incrementally. Do NOT redesign or rewrite.

## Preservation rules (highest priority)
- My existing setup wins. If a Target Rule conflicts with it, keep mine and flag the
  conflict. Never silently replace it.
- Keep all existing paths, folder names, file names, command names, script names,
  and file formats. Adapt the suggestions to them, not the other way round.
- Never delete, rename, or move existing files, folders, or commands.
- Prefer ADDING (new section, new optional command, new script) over EDITING.
  When an edit is needed, keep it minimal: change only the lines needed, never
  rewrite whole files.
- Don't touch anything outside the agent setup files (instruction files, settings, commands, ticket
  folders, workflow scripts). Never touch service source code.
- Skip a suggestion when its value is low or its risk of breaking something is unclear.

## Hard constraints (never violate)
- LOCAL CHANGES ONLY. Never run: git add, commit, push, pull, fetch, merge, rebase,
  reset, checkout, switch, stash, branch -d/-D, tag, worktree remove, or anything that
  touches a remote or rewrites git history.
- Allowed git (read-only): status, diff, log, show, branch --list, worktree list, rev-parse.
- No destructive commands: rm -rf, deleting files outside tickets/<KEY>/scripts|logs,
  DB writes, deploys, docker push.
- No commands are allowlisted. Every shell command costs me one manual approval.
  Your top goal: minimize shell approvals.

## Step 1: Discover (built-in tools only, NO shell)
Using your built-in file tools (read, list/glob, search), find and read:
- every agent instruction/memory file (root and nested), agent settings, custom commands
- the ticket folder structure (where tickets live, what files each has)
- the service/repo list and where each service lives, plus its build/test tool
  (pom.xml, build.gradle, package.json, Makefile...)
- any existing scripts, launcher, or notes about my workflow
Then report: a map of my current setup (paths, files, commands), max 30 lines.

## Step 2: Gap analysis
Compare my setup against the Target Rules below. Table with columns:
rule | status (already have / missing / conflicts) | suggestion | risk (low/med/high) | value
- "already have" rows: keep as is, no change.
- "conflicts" rows: explain what mine does vs. the suggestion, and ask me which to keep.
  Default = keep mine.
- Also estimate the approval count for a typical ticket today vs. after the changes.
- Exception to "mine wins": any existing rule/command that runs git commit/push or other
  forbidden commands. Flag it and propose disabling it (not deleting it).
Keep it short.

## Step 3: Propose small changes
A numbered list, ordered by value/risk (highest value, lowest risk first). Each item has:
- file + exact diff (only changed lines, with a few lines of context)
- why it helps (approvals saved)
- what could break, and how to undo it
Areas where changes are likely (only where there's a real gap):
- Instruction file: ADD a new section (e.g. "## Approval-minimizing rules") using MY paths and
  names. Don't reorganize the existing sections.
- Custom commands: add missing ticket commands only. If a similar command exists,
  suggest a small tweak to it instead of a new one. Never overwrite one.
- scripts: add new reusable scripts only if nothing similar exists.
DO NOT write files yet. Wait for my answers to the conflict questions and my "apply".

## Step 4: Apply
- "apply 1,3" = apply only those items; "apply" = all items.
- Before editing an existing file, save a backup copy next to it (<file>.bak) with your file-write tool.
- Use targeted edits for existing files (no full-file rewrites). Use full-file writes only
  for new files. No shell.
- Afterwards, list what changed and how to roll back (restore from .bak).

---

# Target Rules (SUGGESTIONS: adapt to my setup, my existing conventions win)

## R1. Built-in tools over shell (no approval needed)
- read: built-in read tool. Never cat/head/tail/sed -n/less.
- find: built-in list/glob tool. Never find/ls -R.
- search: built-in search tool. Never grep/rg/ag.
- edit: built-in edit/write tools. Never sed -i, awk, echo >, tee, heredoc.
- Read logs from earlier runs with the built-in read tool. Never re-run a command to see its output.
- Shell ONLY for: build, test, lint, format, running local apps, read-only git.

## R2. One script per phase, run once
Never run shell commands one at a time. Per phase:
1. List every command the phase needs.
2. Write ONE script (built-in write tool) to <ticket-dir>/scripts/<NN>-<phase>.sh (NN increasing, never overwrite).
3. Run once: bash <ticket-dir>/scripts/<NN>-<phase>.sh
4. On failure: fix the code, then write a NEW script covering only failed + remaining steps.

Phases (max one script each):
- inspect: read-only git status/diff/log across touched services, dependency trees,
  tool versions (only what built-in tools can't do)
- build-test: compile + unit tests for all touched services
- verify: lint, format check, integration tests
- diff-report: git diff --stat + git diff per service → written to <ticket-dir>/CHANGES.md
  for my review (replaces commit; I commit manually)

## R3. Script template (required)
```bash
#!/usr/bin/env bash
set -uo pipefail
export CI=true GIT_PAGER=cat PAGER=cat
TICKET_DIR="<ticket-dir>"
LOG="$TICKET_DIR/logs/$(basename "$0" .sh).log"
mkdir -p "$(dirname "$LOG")"; : > "$LOG"
FAIL=()
step() {  # step <name> <dir> <cmd...>
  local name=$1 dir=$2; shift 2
  echo "=== $name ($dir): $* ===" >> "$LOG"
  if (cd "$dir" && "$@") >> "$LOG" 2>&1; then echo "OK   $name"
  else echo "FAIL $name"; FAIL+=("$name"); fi
}
# --- steps ---
# step "svc-a test" /path/to/svc-a ./gradlew test -q
# --- summary ---
echo "---- ${#FAIL[@]} failed: ${FAIL[*]:-none} | log: $LOG"
[ ${#FAIL[@]} -gt 0 ] && grep -nE "ERROR|FAIL|Exception|error:|No such file|not found" "$LOG" | head -40
exit ${#FAIL[@]}
```
- No set -e: independent steps keep going, so one run shows ALL failures.
- Full output goes to the log. Stdout shows only OK/FAIL plus the top 40 error lines.
- Non-interactive flags always (-q, -y, --no-pager, -B for maven, --no-daemon if needed).
- Idempotent; safe to re-run.
- Scripts must obey the Hard Constraints. No git write commands, ever.

## R4. Cadence
- Finish all edits for a logical change first (edits cost no approval), then ONE build-test.
- Don't run tests after every small edit.
- Target per ticket: ≤ 3–4 approvals (inspect?, build-test, fix-retest, diff-report).
- Before any shell call, ask yourself: "Can a built-in tool do this?" and "Can I merge
  this into the next planned script?"

## R5. Ticket state (so any new session can resume)
<ticket-dir> keeps:
- TICKET.md: Jira key, description, acceptance criteria, touched services
- PLAN.md: checkbox steps
- LOG.md: after each script: script name, OK/FAIL count, findings, next step
- CHANGES.md: latest diff-report for my manual review/commit
On resume: read those 4 files first, summarize in ≤ 10 lines, continue from "next step".

## R6. Session identity
- Jira key = ticket folder name = saved session name.
- At the end of each phase, update LOG.md and remind me to save the session as <KEY> (if my agent supports saved sessions).
````

## 2. Evaluate (template, re-run after every change)

````markdown
# Task: Evaluate my agent automation flow

Audit my current multi-ticket AI coding agent setup against the expected rules and score it.
This prompt is reusable: I run it after every change to the flow, so results must be
comparable across runs.

## Mode: READ-ONLY
- Built-in file tools only (read, list/glob, search). NO shell.
- Don't change any existing file. The ONLY file you may write is the new evaluation report.
- Propose fixes, but don't apply them.

## Source of truth (expected rules)
1. The rules in my agent instruction files (root + nested) and custom commands.
2. If a metric below isn't covered there, use the default expectation stated in the metric.
If the instruction files contradict themselves or the Hard Constraints, report that as a finding.

Hard Constraints (always apply, override everything):
- Local changes only. No git add/commit/push/pull/fetch/merge/rebase/reset/checkout/
  switch/stash/tag, or anything touching a remote or history. Read-only git is OK.
- No destructive commands (rm -rf, DB writes, deploys, docker push).
- No commands are allowlisted, so every shell call costs one manual approval.

## Step 1: Collect evidence (no shell)
Read:
- all agent instruction/memory files, agent settings, custom commands
- workflow scripts and launcher (wherever they live in my setup)
- ticket folders: TICKET.md, PLAN.md, LOG.md, CHANGES.md, scripts/, logs/
  (sample the 5 most recently modified tickets, or all if fewer)
- previous evaluation reports (see Step 4 for location)
Use real ticket history as evidence where possible, not just the rules text.
Cite evidence as file:line or file name for every score.

## Step 2: Score each metric (0–5)
0 = missing/violated, 3 = partly meets, 5 = fully meets with evidence in real tickets.

| # | Metric | Default expectation | How to measure |
|---|--------|--------------------|----------------|
| M1 | Safety: git | No git write command anywhere (rules, commands, scripts, logs) | search all scripts/commands/logs for forbidden git verbs |
| M2 | Safety: destructive | No rm -rf, DB writes, deploys; deletes only inside ticket scripts/logs | search scripts + commands |
| M3 | Approval count | ≤ 4 shell approvals per ticket | count scripts run per ticket (scripts/ + LOG.md entries); report avg / max |
| M4 | Built-in tool usage | No shell for read/find/search/edit | search scripts/LOG for cat, head, tail, find, grep, sed -i, echo > used for those jobs |
| M5 | Batching | One script per phase; retries only cover failed + remaining steps | per ticket: scripts per phase, repeated identical steps |
| M6 | Script quality | Follows template: set -uo pipefail, step(), log file, summary, non-interactive, idempotent | check each recent script against the template |
| M7 | Context efficiency | Full output goes to logs; stdout = OK/FAIL + top errors; logs read via built-in read tool | script structure + any evidence of huge outputs in LOG.md |
| M8 | Resumability | TICKET/PLAN/LOG present and current; LOG has "next step" after each phase | check each sampled ticket for all files + last entry |
| M9 | Session identity | Jira key = folder = saved session name, used consistently | folder names vs. keys in TICKET.md, commands |
| M10 | Parallel isolation | Tickets don't share mutable state; same service in 2 tickets can't clash | worktree/folder layout, shared files written by multiple tickets |
| M11 | Review handoff | CHANGES.md (diff-report) produced before handoff; I commit manually | presence + freshness vs. last LOG entry |
| M12 | Rule consistency | Instruction files, commands, and scripts agree; no duplicates, stale paths, or dead commands | cross-check referenced paths/commands exist |
| M13 | Simplicity | Minimal files/commands to learn; no unused rules | count rules/commands; flag unused ones (never referenced in tickets) |

If a metric can't be measured (e.g. no tickets yet), mark it N/A with the reason. Don't guess.

## Step 3: Simulate one ticket (dry run, no execution)
Walk through a typical ticket touching 2 services, using ONLY my current rules/commands:
start → inspect → edit → build-test → one failure + fix → retest → diff-report → resume in a new session.
List each shell approval it would need, plus any step where the rules are unclear or
would make the agent use shell unnecessarily. Result: expected approvals per ticket.

## Step 4: Write the report
Write ONE new file: <hub>/eval/EVAL-<NN>.md (NN = next number after existing reports;
create the eval/ folder if missing). Never overwrite old reports.
Structure:
1. Summary: total score (sum / max applicable), 3-line verdict
2. Score table: metric | score | previous score | Δ | evidence
3. Regressions: any metric that dropped vs. the previous report, and the likely cause
   (which changed file)
4. Violations: every Hard Constraint breach found (these are top priority, whatever the score)
5. Dry-run result: approvals per ticket + unclear steps
6. Top 5 fixes: ordered by value/risk; each with file, minimal diff, metric improved.
   Must follow the preservation rules: keep existing paths/names, prefer additive changes,
   no deletes/renames.
7. Changed since last eval: files changed since the previous report (compare the content/rules
   the previous report cites)

Then print the Summary + score table in chat. Don't apply any fix until I say "apply N".
````
