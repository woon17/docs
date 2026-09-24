# Agentic Workflows Catalog

Published workflows to explore, borrowing one idea at a time to improve [my own ticket workflow](agentic-ticket-workflow.md).

- **Harness** = the agent runtime (loop, tools, permissions). It's fixed, so it's not covered here.
- **Workflow** = the process and rules on top of the harness. That's what this page covers.

---

## How to use this page

1. Pick **one** workflow and read its docs.
2. Pick **one** idea from its "Borrow" list.
3. Adapt it with the prompt at the bottom of this page. It only makes small, additive changes.
4. Re-run the Evaluate prompt from my ticket workflow page and compare scores.
5. Tick it off below, then repeat.

---

## Overview

| Workflow | Type | Core flow | Best idea to borrow |
|---|---|---|---|
| [Research → Plan → Implement](#research-plan-implement) | methodology | research → plan → implement, compacting context between phases | fresh session per phase, files as hand-off |
| [Spec Kit](#spec-kit) | toolkit + templates | constitution → specify → plan → tasks → implement | spec vs. tasks split, "constitution" rules file |
| [Kiro](#kiro) | IDE + spec flow | requirements → design → tasks | acceptance criteria written as testable statements |
| [Conductor](#conductor) | agent extension | context → spec & plan → implement | persistent context files (product, tech stack, workflow) |
| [Superpowers](#superpowers) | skills library | brainstorm → plan → execute in batches → review → finish | "verify before claiming done", test-first |
| [BMAD Method](#bmad-method) | multi-role framework | analyst → PM → architect → dev → QA | role-specific prompts per phase |
| [Taskmaster](#taskmaster) | task manager | PRD → tasks → subtasks → status | dependency-ordered sub-tasks |
| [Building Effective Agents](#building-effective-agents) | pattern catalog | chaining, routing, parallel, orchestrator-workers, evaluator-optimizer | evaluator-optimizer loop |
| [12-Factor Agents](#12-factor-agents) | principles | 12 factors for reliable agents | own your prompts, own your context window |
| [AGENTS.md](#agentsmd) | file standard | one instruction file for all agents | tool-neutral rules file |

---

## Research → Plan → Implement

HumanLayer's "Advanced Context Engineering" / Frequent Intentional Compaction.

- **Idea**: the context window is the bottleneck. Split work into phases, each ending in a file, and start each phase in a fresh session reading only that file. Keep context usage around 40–60%.
- **Flow**: `research.md` (how the code works now) → `plan.md` (exact changes, reviewed by the human) → implement phase by phase.
- **Borrow**:
    - [ ] add a research phase + `RESEARCH.md` before `PLAN.md`
    - [ ] human reviews the research/plan, not every line of code
    - [ ] new session per phase, reading only the hand-off files
- **Links**: [repo](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents) · [blog](https://www.humanlayer.dev/blog/advanced-context-engineering)

## Spec Kit

GitHub's spec-driven development toolkit. It works with many agents.

- **Idea**: the spec is the source of truth, and code is generated from it.
- **Flow**: `constitution` (non-negotiable project rules, once) → `specify` (what/why) → `plan` (tech how) → `tasks` (small, testable) → `implement`.
- **Borrow**:
    - [ ] split the plan into spec (what/why) and tasks (checkboxes)
    - [ ] a "constitution" section of hard rules that every command references
    - [ ] approval gate after the spec, before any edit
- **Links**: [repo](https://github.com/github/spec-kit) · [docs](https://github.github.com/spec-kit/) · [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)

## Kiro

AWS's agentic IDE, built around specs.

- **Idea**: every feature has `requirements.md` → `design.md` → `tasks.md`.
- **Borrow**:
    - [ ] requirements written as testable "WHEN … THEN …" acceptance criteria
    - [ ] a design section (data flow, interfaces) before tasks
- **Links**: [kiro.dev](https://kiro.dev)

## Conductor

"Context-driven development" extension. It now supports several agents.

- **Idea**: move context out of chat into persistent markdown files in the repo (product goals, tech stack, style guides, workflow preferences). Each piece of work gets its own spec + plan.
- **Borrow**:
    - [ ] project-level context files (product, tech stack, conventions) separate from per-ticket files
    - [ ] per-ticket spec + plan with a review step before implementing
- **Links**: [repo](https://github.com/gemini-cli-extensions/conductor)

## Superpowers

A skills library and development methodology.

- **Idea**: turn good engineering habits into default agent behaviour.
- **Flow**: brainstorming → worktree → writing plans → executing plans (in batches) → TDD → code review → finishing the branch.
- **Borrow**:
    - [ ] "verify before declaring success": test evidence in the log before ticking a task
    - [ ] execute the plan in batches, with a review stop between batches
    - [ ] brainstorm step: the agent asks clarifying questions before planning
- **Links**: [repo](https://github.com/obra/superpowers)

## BMAD Method

Agile framework with specialised agent roles.

- **Idea**: a different persona and prompt per role (analyst, PM, architect, dev, QA), passing documents between them. Planning depth scales with task size.
- **Borrow**:
    - [ ] a "QA reviewer" prompt that checks the diff against acceptance criteria
    - [ ] light path for small bugs, full path for features (scale-adaptive)
- **Links**: [repo](https://github.com/bmad-code-org/BMAD-METHOD)

## Taskmaster

Task-management layer for AI coding.

- **Idea**: parse a PRD into tasks with dependencies, expand complex ones into subtasks, and track status.
- **Borrow**:
    - [ ] break multi-service tickets into dependency-ordered sub-tasks in `PLAN.md`
    - [ ] a complexity check: expand a task into subtasks only if it's complex
- **Watch out**: some commands call LLM APIs with **their own API keys**. Borrow the idea, not the tool, unless it's approved.
- **Links**: [repo](https://github.com/eyaltoledano/claude-task-master)

## Building Effective Agents

Anthropic's pattern catalog. It covers patterns, not a full workflow.

- **Patterns**: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- **Borrow**:
    - [ ] evaluator-optimizer: run Evaluate → fix → Evaluate as a loop with clear metrics
    - [ ] routing: small bug vs. feature vs. refactor → different phase sets
    - [ ] "start simple": add complexity only when a metric shows the need
- **Links**: [article](https://www.anthropic.com/engineering/building-effective-agents) · [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)

## 12-Factor Agents

Principles for reliable LLM software, modelled on the 12-Factor App.

- **Borrow**:
    - [ ] own your prompts: keep prompts versioned as files (already done here)
    - [ ] own your context window: decide what goes into context and keep it small
    - [ ] small, focused agents: one phase = one narrow job
- **Links**: [repo](https://github.com/humanlayer/12-factor-agents)

## AGENTS.md

Open format, a "README for agents", read by most coding agents.

- **Borrow**:
    - [ ] keep tool-neutral rules in one `AGENTS.md`, with thin tool-specific instruction files pointing to it
- **Links**: [agents.md](https://agents.md) · [repo](https://github.com/agentsmd/agents.md)

---

## Suggested order

Start with low-risk, high-value ideas:

1. [ ] Verify before done (Superpowers)
2. [ ] Research phase + fresh session per phase (Research → Plan → Implement)
3. [ ] Spec vs. tasks split + approval gate (Spec Kit / Kiro)
4. [ ] Testable acceptance criteria (Kiro)
5. [ ] Routing: light path for small bugs (Building Effective Agents / BMAD)
6. [ ] Evaluator-optimizer loop with the Evaluate prompt
7. [ ] Project-level context files (Conductor)
8. [ ] AGENTS.md as the single rules source

---

## Prompt: borrow one idea

````markdown
# Task: Borrow ONE idea into my existing agent workflow

Idea to borrow: <paste the idea, e.g. "verify before declaring success: test evidence in
the log before ticking a task">
Source: <workflow name>

## Rules
- My existing setup wins. Keep all paths, names, commands, and file formats.
- Additive and minimal: no delete/rename/move, no full-file rewrites, never touch service code.
- Local changes only: no git writes, no destructive commands.
- Built-in file tools only for this task (read, list/glob, search, edit). NO shell.
- Don't install any tool or extension. Adapt the idea into my own files.

## Steps
1. Read my agent instruction files, custom commands, workflow scripts, and 2 recent ticket
   folders. Summarize in ≤ 10 lines where this idea would fit.
2. Check: do I already have this (fully/partly)? If fully, stop and tell me.
3. Propose the smallest change: file + exact diff, why it helps, what could break, how to undo.
   If it conflicts with my flow, explain the conflict and ask me. Default = keep mine.
4. Wait for "apply". Before editing an existing file, save <file>.bak. Then apply and list the changes.
5. Tell me which Evaluate metric this should improve, so I can re-run Evaluate and compare.
````
