# Java Agent Skills (Claude + Gemini)

Popular Java / Spring Boot skills that work in **both** Claude Code and Gemini CLI, and how to install them once for both.

---

## Why one skill works in both

Both tools follow the [Agent Skills open standard](https://agentskills.io/specification): a skill is a folder with a `SKILL.md` (YAML frontmatter + markdown instructions), plus optional reference files.

```
spring-data-jpa/
├── SKILL.md          # name + description (frontmatter) + instructions
└── references/       # optional, loaded only when needed
```

```yaml
---
name: spring-data-jpa
description: Use when generating or refactoring JPA entities, repositories, queries...
---
# instructions for the agent ...
```

`description` is what the agent reads to decide **when** to load the skill. Only `name` + `description` sit in context until the skill is triggered.

Tool-specific frontmatter (e.g. `allowed-tools` for Claude Code) is ignored by the other tool, so the same folder is safe to share.

---

## Where each tool looks

| | Claude Code | Gemini CLI |
|---|---|---|
| User (all projects) | `~/.claude/skills/<name>/SKILL.md` | `~/.gemini/skills/` or `~/.agents/skills/` |
| Project | `.claude/skills/<name>/SKILL.md` | `.gemini/skills/` or `.agents/skills/` |
| List skills | `/skills`, or ask "what skills do you have?" | `/skills list`, `gemini skills list --all` |
| Install from git | copy folder, or `/plugin marketplace add` for plugin repos | `gemini skills install <url> --consent` |
| Link a local dir | symlink | `/skills link <path> --scope user` |
| Activation | auto, when description matches | auto, after a consent prompt |

---

## Popular Java skill repos

Stars as of 2026-09.

| Repo | ★ | Java skills | Good for |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 178k | none Java-specific | reference for how to write skills |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | 39k | `java-springboot`, `java-junit`, `java-docs`, `spring-boot-testing`, `javax-to-jakarta-migration`, `java-refactoring-extract-method`, `java-add-graalvm-native-image-support`, `create-spring-boot-java-project` | short, general best-practice skills |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | 11.6k | `java-architect`, `spring-boot-engineer`, `kotlin-specialist` | broad "senior engineer" persona skills |
| [spring-ai-community/spring-ai-agent-utils](https://github.com/spring-ai-community/spring-ai-agent-utils) | 0.6k | — (library) | running skills **inside** your own Spring AI app |
| [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) | 0.3k | ~50 in `plugins/developer-kit-java/`: `spring-boot-test-patterns`, `unit-test-*` (service, controller, wiremock...), `spring-data-jpa`, `spring-boot-resilience4j`, `spring-boot-saga-pattern`, `aws-sdk-java-v2-*`, `langchain4j-*` | deep testing + AWS + LangChain4j |
| [jdubois/dr-jskill](https://github.com/jdubois/dr-jskill) | 0.3k | `dr-jskill` (single skill) | generating a new Spring Boot 4 / Java 25 project |
| [rrezartprebreza/spring-boot-skills](https://github.com/rrezartprebreza/spring-boot-skills) | 0.3k | 33 skills × `spring-boot-3/` and `spring-boot-4/`: `spring-data-jpa`, `transactional-patterns`, `webflux-reactive-patterns`, `testing-pyramid`, `resilience-retry`, `spring-security-jwt`, `multi-module-maven`, `hexagonal-architecture`, `spring-modulith`... | focused, version-specific Spring Boot skills |
| [a-pavithraa/springboot-skills-marketplace](https://github.com/a-pavithraa/springboot-skills-marketplace) | <0.1k | `code-reviewer`, `creating-springboot-projects`, `spring-data-jpa`, `springboot-migration` | small, review + migration |

### Suggested starter set

| Need | Skill |
|---|---|
| General Spring Boot | `rrezartprebreza/.../spring-boot-3/*` (pick the ones you use) or `awesome-copilot/java-springboot` |
| JPA without N+1 | `rrezartprebreza/.../spring-data-jpa` |
| `@Transactional` pitfalls | `rrezartprebreza/.../transactional-patterns` |
| WebFlux | `rrezartprebreza/.../webflux-reactive-patterns` |
| Tests | `developer-kit/.../spring-boot-test-patterns` + `unit-test-service-layer` |
| New project | `jdubois/dr-jskill` |

!!! tip "Fewer, focused skills"
    Every installed skill puts its `description` in context and competes for triggering. Pick 5–10 you actually need rather than installing a whole repo.

---

## Install once, use in both

Keep one copy of each skill and symlink it into both tools.

```bash
# 1. clone sources once
mkdir -p ~/skills-src && cd ~/skills-src
git clone --depth 1 https://github.com/rrezartprebreza/spring-boot-skills
git clone --depth 1 https://github.com/giuseppe-trisciuoglio/developer-kit

# 2. pick skills into one shared folder
mkdir -p ~/.agents/skills
for s in spring-data-jpa transactional-patterns webflux-reactive-patterns testing-pyramid; do
  ln -s ~/skills-src/spring-boot-skills/skills/spring-boot-3/$s ~/.agents/skills/$s
done
ln -s ~/skills-src/developer-kit/plugins/developer-kit-java/skills/spring-boot-test-patterns \
      ~/.agents/skills/spring-boot-test-patterns

# 3. Gemini CLI reads ~/.agents/skills directly — nothing to do

# 4. Claude Code: link each skill into ~/.claude/skills
mkdir -p ~/.claude/skills
for s in ~/.agents/skills/*; do ln -s "$s" ~/.claude/skills/; done
```

Update later: `git -C ~/skills-src/spring-boot-skills pull`. Both tools see the change.

Verify:

```bash
gemini skills list --all      # Gemini
# Claude Code: /skills, or ask "what skills do you have?"
```

**Per project** instead of per user: same idea with `.agents/skills/` and `.claude/skills/` in the repo root, committed to git, so teammates on either tool get the same skills.

---

## Writing your own portable skill

- Only rely on `name` + `description` in frontmatter; everything else is optional.
- Write the `description` as *when to use*, with keywords: "Use when writing JPA entities, repositories, `@Query`, pagination...".
- Keep `SKILL.md` short; move long examples into `references/*.md` and link them.
- Don't mention tool names (`Read`, `Bash`, `/command`) in the instructions: they differ between Claude and Gemini.
- Test the trigger in both tools with a prompt that *should* and one that *shouldn't* load it.

!!! note "This site's `java-architect` skill"
    [Java Architect Skill](claude-code/java-architect/index.md) uses the same frontmatter layout as `Jeffallan/claude-skills/java-architect`, customised for Agrona/Aeron services. To make it portable, place it at `.agents/skills/java-architect/SKILL.md` and symlink into `.claude/skills/`.

---

## Sources

- [Agent Skills spec](https://agentskills.io/specification)
- [Gemini CLI: Agent Skills](https://geminicli.com/docs/cli/skills/)
- [JetBrains: AI-assisted Java development with Agent Skills](https://blog.jetbrains.com/idea/2026/03/ai-assisted-java-application-development-with-agent-skills/)
- [Spring AI: Agent Skills](https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills/)
