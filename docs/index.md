# Technical Documentation Hub

Welcome to comprehensive technical documentation covering Java development, database operations, system design, and high-performance messaging systems.

## What You'll Find Here

### Core Technologies
- **[Java Development](/docs/java/)** - Memory management, concurrency patterns, and threading best practices
- **[KDB+ Database](/docs/kdb/)** - Time-series database operations, setup guides, and integration examples  
- **[System Design](/docs/system_design/frAndNfre/)** - Architecture patterns, IPC mechanisms, and design principles
- **[Aeron Messaging](/docs/aeron/)** - High-performance messaging protocols and low-latency communication

### Development & Tools
- **[Spring Boot](/spring-boot/)** - Application frameworks and multi-module Maven projects
- **[Linux Operations](/linux/)** - Command reference and system administration
- **[Setup Guides](/setup/)** - Environment configuration for Python, SSH, and development tools
- **[Productivity Tools](/ai-tools/)** - AI assistance and development workflow optimization

## Getting Started

!!! tip "New to the Documentation?"
    Start with the [setup guides](/setup/) to configure your development environment, then explore topics by category above.

### Quick Navigation
- **Beginners**: Start with [Java basics](/java/) and [setup guides](/setup/)
- **Database work**: Jump to [KDB+ documentation](/kdb/) 
- **System architecture**: Explore [system design](/system_design/) concepts
- **Performance optimization**: Check out [Aeron messaging](/aeron/) guides

## Development Commands

For contributors and maintainers:

```bash
# Start local development server
python write_timestamp.py && mkdocs serve

# Build documentation site  
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy --force
``` 
