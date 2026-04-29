# Skill: java-architect

**Source file:** `.claude/java-architect/SKILL.md`

---
name: java-architect
description: Use when building, configuring, or debugging Java services in this codebase. Services are Spring Boot + Agrona Agent based (no REST, no DB by default). Invoke to create new services, add agents, wire AgentRunner, configure settings, or add REST/data-access layers when explicitly needed.
license: MIT
metadata:
  author: https://github.com/woon17
  version: "1.2.0"
  domain: language
  triggers: Spring Boot, Java, Agrona, Aeron, Agent, AgentRunner, microservices, Java Enterprise
  role: architect
  scope: implementation
  output-format: code
  related-skills: fullstack-guardian, api-designer, devops-engineer, database-optimizer
---

# Java Architect

Java specialist for this multi-module Maven project. Services are Spring Boot 3.x + Agrona agent-based, running on Java 17. The default service shape has no REST layer and no database — those are added only when explicitly required.

## Core Workflow

1. **Module setup** - Create module directory, pom.xml (inheriting from parent mmm), register in root pom.xml
2. **Template files** - Add main app class, Setting, TestService, ThreadFactoryUtils following `references/spring-boot-setup.md`
3. **Agent implementation** - Build agents implementing `org.agrona.concurrent.Agent`; follow `references/aeron-agent.md`
4. **Wire runner** - Wire `AgentRunner` + `ShutdownSignalBarrier` + `SigInt` in main app `run()` method
5. **Config** - Externalize all values under `settings:` in `application.yml`, bind via `Setting.java`
6. **Optional layers** - Add REST or data-access only when requested; load relevant reference first

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Service core | `references/spring-boot-setup.md` | New service, pom, main app, Setting, ThreadFactoryUtils |
| Agrona agents | `references/aeron-agent.md` | Adding agents, AgentRunner, CompositeAgent, shutdown |
| REST / HTTP | `references/rest-api.md` | Building HTTP endpoints, controllers, OpenAPI |
| Data access | `references/data-access.md` | JPA, Hibernate, Flyway, datasource config |
| Security | `references/spring-security.md` | OAuth2, JWT, method security |
| Testing | `references/testing-patterns.md` | JUnit 5, TestContainers, Mockito |

## Constraints

### MUST DO
- Inherit from parent pom (`example` / `mmm`); use `version 1.0.0` on each module
- Use Java 17
- Use `<domain>.explore` package convention (e.g. `market.explore`, `demo.explore`)
- Externalize all config under `settings:` — never hardcode values
- Use `@ConfigurationProperties("settings")` + `@Data` for the `Setting` class
- Use proper exception handling

### MUST NOT DO
- Add REST controllers, JPA, Flyway, or actuator unless explicitly requested
- Use Java 21-only language features (records with compact constructors, sealed classes)
- Add `spring-boot-maven-plugin` or test dependencies to the module pom unless asked
- Use blocking code inside `Agent.doWork()`
- Hardcode sleep/timing values — make them configurable via `Setting`

## Output Templates

When creating a new service, provide only the layers that apply:
1. `pom.xml` — inheriting from parent, with correct deps
2. Main application class — `CommandLineRunner` + `AgentRunner` wiring
3. `Setting.java` — `@ConfigurationProperties` placeholder
4. `TestService.java` — placeholder service
5. `ThreadFactoryUtils.java` — thread factory utility
6. Agent class(es) — one per logical concern
7. `application.yml` — `spring.application.name` + `settings:` block
8. Test class — commented out (matching project convention)

## Knowledge Reference

Spring Boot, Java 17, Agrona, Aeron, `org.agrona.concurrent.Agent`, `AgentRunner`, `CompositeAgent`, `SleepingIdleStrategy`, `ShutdownSignalBarrier`, `SigInt`, `SystemEpochClock`, Lombok, SLF4J, Logback, Maven multi-module
