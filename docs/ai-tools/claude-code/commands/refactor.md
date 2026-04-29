# Command: /refactor

**Source file:** `.claude/commands/refactor.md`

## Command Prompt

```
Ultrathink before making any changes. You are doing a thorough code quality refactor of this service. Follow this exact process in order.

---

## Step 1 — Explore

Read every source file under `src/main/java`. Map the full structure: what each class does, what it owns, and how classes relate to each other.

---

## Step 2 — Audit (find every issue before touching anything)

For each file, check every category below. Be exhaustive — surface all issues, not just the obvious ones.

**Dead code**
- Commented-out code blocks that should be deleted
- Unused fields, local variables, method parameters
- Unused imports
- Fields declared but whose only condition/use is commented out

**Naming**
- Typos in identifiers (e.g. `lastFLush`)
- Inconsistent conventions across the codebase (e.g. one `roleName()` returns kebab-case, another returns PascalCase)
- Non-descriptive names that obscure intent

**Access modifiers & mutability**
- Missing `private` on fields
- Instance fields that never change → `private static final` constant
- Magic string/number literals inline → named constant at class level

**Error handling**
- `System.exit()` outside of `main()` → throw an exception instead
- Wrong log level (`log.error` for a recoverable/expected condition → `log.warn`)
- Broad `catch (Exception e)` that silently swallows without re-throwing where the caller needs to know
- Checked exceptions re-thrown as checked when `RuntimeException` is more appropriate

**Code structure**
- Duplicated logic across methods → extract shared helper
- Validation or guard check happening after the value is already used
- Collections or arrays allocated inside a method on every call → `static final`
- A method doing more than one thing that can be cleanly split

**Resource management**
- Class has a `close()` method but does not implement `Closeable` / `AutoCloseable`
- Resources opened but not in try-with-resources when they could be
- `close()` missing a final flush before releasing the resource

**Framework & API idioms**
- Using lower-level patterns when the framework provides an idiomatic API (e.g. `new Thread(runner)` vs `AgentRunner.startOnThread()`)
- `doWork()` returning `0` unconditionally when it always performs work (should return a positive count)
- `Thread.sleep()` inside `doWork()` of an Agent that already has an idle strategy

**Comments & logs**
- Comments that explain WHAT the code does (the code already says that) — remove them
- Developer notes / runbook snippets committed into source (e.g. docker run commands) — remove
- Emojis in log messages
- Fully-qualified class names where an import would be cleaner

---

## Step 3 — Report findings before any edits

Output a structured list grouped by file:

```
### FileName.java
- [Category] description of issue → proposed fix
- [Category] description of issue → proposed fix
```

State the total count of issues found.

---

## Step 4 — Refactor

Apply every fix. Make all independent file edits in parallel. Do not add features, new abstractions, tests, or error handling for scenarios that cannot happen — only fix what the audit found.

---

## Step 5 — Verify

Run `mvn compile` and confirm clean output. If it fails, diagnose and fix before reporting done.
```
