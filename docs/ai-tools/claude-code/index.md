# Claude Code Customization

Portable knowledge base for Claude Code skills and commands.
Copy the `.claude/` directory to any project to replicate the same behaviour.

## `.claude` Directory Structure

```
.claude/
├── commands/
│   ├── new-service.md
│   ├── refactor.md
├── java-architect/
│   ├── SKILL.md
│   └── references/
│       ├── aeron-agent.md
│       ├── data-access.md
│       ├── rest-api.md
│       ├── spring-boot-setup.md
└── settings.local.json
```

## How It Works

| Mechanism | Location | How to Invoke |
|-----------|----------|---------------|
| Slash commands | `.claude/commands/*.md` | `/command-name` in Claude Code |
| Skills | `.claude/<skill>/SKILL.md` | Auto-loaded based on triggers |
| Permissions | `.claude/settings.local.json` | Applied on every tool call |

!!! tip "Copy to a new device"
    Copy the entire `.claude/` directory into the project root.
    Claude Code picks it up automatically — no extra configuration needed.
