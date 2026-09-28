# Harness Building Blocks

The 8 parts most production harnesses are built from. Each one fixes a limit of the raw model.

```mermaid
flowchart TB
    M(("🧠 Model"))
    SP["1. System prompt"] --> M
    M <--> T["2. Tools"]
    T --> SB["3. Sandbox"]
    SB <--> FS["4. Filesystem"]
    MEM["5. Memory +<br/>context mgmt"] --> M
    M --> FB["6. Feedback /<br/>verification"]
    FB --> M
    GR["7. Guardrails"] -.blocks.-> T
    OB["8. Observability"] -.watches.-> M & T
```

| # | Block | Fixes this model limit | Claude Code example |
|---|---|---|---|
| 1 | [System prompt](#1-system-prompt) | No standing role or rules | system prompt + `CLAUDE.md` |
| 2 | [Tools](#2-tools-and-tool-execution) | Can't touch the outside world | Read, Edit, Bash, MCP servers |
| 3 | [Sandbox](#3-sandbox) | Running agent code is risky | sandbox mode, worktrees |
| 4 | [Filesystem](#4-filesystem-and-durable-storage) | Chat disappears | repo files, `PLAN.md` hand-offs |
| 5 | [Memory + context](#5-memory-and-context-management) | Forgets anything outside the window | auto-compact, memory files |
| 6 | [Feedback loops](#6-feedback-loops-and-self-verification) | Declares success too early | hooks, test runs |
| 7 | [Guardrails](#7-guardrails-and-human-in-the-loop) | Takes irreversible actions | permission prompts, allow/deny rules |
| 8 | [Observability](#8-observability-and-logging) | Can't debug or audit | transcripts, OpenTelemetry |

---

## 1. System prompt

Standing instructions sent on **every** run: who the agent is, its goal, and its rules. They shape behavior before any user input arrives.

!!! example
    ```text
    You are a Java code reviewer for a low-latency trading system.
    - Never suggest allocations on the hot path.
    - Flag any use of synchronized in Agrona agents.
    - Answer with file:line references.
    ```

!!! warning "Common problem"
    A vague or conflicting system prompt is one of the top causes of **inconsistent** agent behavior.

---

## 2. Tools and tool execution

Functions the model can call. The **model picks** the tool; the **harness runs** it.

```mermaid
sequenceDiagram
    participant M as 🧠 Model
    participant H as 🦾 Harness
    participant DB as 🗄️ Database
    M->>H: tool_call: query_db("SELECT count(*) FROM orders WHERE status='FAILED'")
    H->>DB: run SQL
    DB-->>H: 42
    H-->>M: tool_result: 42
    M->>M: "42 failed orders"
```

!!! example "Tool definition the model sees"
    ```json
    {
      "name": "query_db",
      "description": "Run a read-only SQL query on the orders DB",
      "input_schema": {
        "type": "object",
        "properties": { "sql": { "type": "string" } },
        "required": ["sql"]
      }
    }
    ```

!!! tip "Trend: fewer narrow tools, more code execution"
    Instead of 50 tools (`get_order`, `get_trade`, `get_client`, …), give the agent **one** general tool: *write and run code*. The model builds the workflow on the fly.

    | Narrow tools | General tool |
    |---|---|
    | `get_order(id)`, `cancel_order(id)`, `list_orders(date)` … | `run_python(code)` |
    | Fixed set of actions | Model writes whatever it needs |
    | Many tool descriptions eat context | One description |

---

## 3. Sandbox

An isolated workspace where agent code runs **without affecting the real system**.

```mermaid
flowchart LR
    M["🧠 Model"] -->|"rm -rf build/"| H["🦾 Harness"]
    H --> SB
    subgraph SB["📦 Sandbox (container / VM)"]
        C[Agent code runs here]
    end
    SB -.❌ no access.-> Prod[("Prod DB,<br/>home dir, network")]
```

Why it matters:

- **Safe to experiment**: a bad command only breaks the sandbox.
- **Resettable**: throw it away and start clean.
- **Parallel**: run 10 agents in 10 sandboxes at once.

!!! example
    Claude Code sandbox mode limits Bash to the project dir and blocks network access. A git **worktree** gives each agent its own copy of the repo.

---

## 4. Filesystem and durable storage

A place to read and write files that **outlive the chat**: code, notes, plans, and intermediate results.

```mermaid
flowchart LR
    S1["Session 1<br/>🔍 Research"] -->|writes| R[RESEARCH.md]
    R -->|reads| S2["Session 2<br/>📝 Plan"]
    S2 -->|writes| P[PLAN.md]
    P -->|reads| S3["Session 3<br/>🛠️ Implement"]
    Human([👤 Human]) -.reviews/edits.-> P
```

!!! example
    Long task over 3 days: the agent keeps `PLAN.md` with checkboxes. Each new session reads it and continues from the first unticked item. A human or another agent can also edit the same file.

---

## 5. Memory and context management

The model only knows what's in its **context window**. The harness decides what goes in and what gets dropped.

**Within a task: context compaction**

```mermaid
flowchart LR
    subgraph Before["Context: 95% full ⚠️"]
        direction TB
        a[System prompt]
        b[Turn 1-40: old tool output]
        c[Turn 41-50: recent]
    end
    subgraph After["Context: 30% full ✅"]
        direction TB
        a2[System prompt]
        b2["Summary of turns 1-40"]
        c2[Turn 41-50: recent]
    end
    Before -->|compact| After
```

**Across sessions: stored memory**

| Kind | Example |
|---|---|
| User preference | "User prefers concise answers" |
| Project fact | "Deploy with `mkdocs gh-deploy --force`" |
| Work history | "Ticket ABC-123: done steps 1-3, blocked on step 4" |

!!! example
    Claude Code auto-compacts when the window fills up. `CLAUDE.md` and memory files are loaded at session start, so the agent knows the project without being told again.

---

## 6. Feedback loops and self-verification

A good harness doesn't just let the model act. It **checks the work**.

```mermaid
flowchart LR
    A[🧠 Make change] --> B[🦾 Run tests / lint / build]
    B -->|❌ fail| C[Feed errors back]
    C --> A
    B -->|✅ pass| D[🧠 Self-review diff]
    D -->|issue found| A
    D -->|looks good| E([Done])
```

!!! example "Claude Code hook: always run tests after an edit"
    ```json
    {
      "hooks": {
        "PostToolUse": [{
          "matcher": "Edit|Write",
          "hooks": [{ "type": "command", "command": "mvn -q test" }]
        }]
      }
    }
    ```
    If tests fail, the output goes back to the model, which has to fix it before claiming it's done.

---

## 7. Guardrails and human-in-the-loop

Rules that **block** unsafe or unapproved actions. A human-in-the-loop guardrail pauses until a person approves.

```mermaid
flowchart TD
    M["🧠 Model wants:<br/>DELETE FROM orders"] --> G{🛡️ Guardrail}
    G -->|safe: read-only| Run[Run it]
    G -->|risky: delete / send / buy| Ask{👤 Human approves?}
    Ask -->|yes| Run
    Ask -->|no| Back[Tell model: denied]
    G -->|forbidden| Block[❌ Block always]
```

| Action | Rule |
|---|---|
| `git status`, read file | allow |
| `git push`, send email, delete file | ask human |
| `rm -rf /`, drop prod table | deny |

!!! example "Claude Code permissions"
    ```json
    {
      "permissions": {
        "allow": ["Bash(git status)", "Bash(mvn test:*)"],
        "ask":   ["Bash(git push:*)"],
        "deny":  ["Bash(rm -rf:*)"]
      }
    }
    ```

---

## 8. Observability and logging

See **what** the agent did, **why**, and **where** it went wrong.

```mermaid
flowchart LR
    Run["Agent runs<br/>(thousands)"] --> L["📜 Logs / traces"]
    L --> Dbg["🐞 Debug:<br/>why did it fail?"]
    L --> Aud["📋 Audit:<br/>who approved what?"]
    L --> Ev["📊 Evals:<br/>success rate over time"]
```

!!! example "One trace"
    ```text
    [10:01:02] model  → tool_call Read(OrderService.java)
    [10:01:03] tool   ← 240 lines
    [10:01:07] model  → tool_call Edit(line 42)
    [10:01:07] guard  ✓ allowed (Edit in project dir)
    [10:01:09] hook   mvn test → FAILED (NullPointerException)
    [10:01:15] model  → tool_call Edit(line 40)
    [10:01:18] hook   mvn test → PASSED
    [10:01:19] model  → final answer
    ```

- **Developers:** debug bad decisions.
- **Enterprises:** audit trail (required in regulated industries).
- **At scale:** feeds evals that measure success over thousands of runs, not one demo.

---

Next: [Failure Modes & Future](failure-modes.md)
