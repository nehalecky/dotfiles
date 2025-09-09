# Claude Code Agent Guide

This guide provides comprehensive documentation for all 14 specialized Claude Code agents in this dotfiles configuration.

## Architecture Overview

Claude Code agents are specialized AI assistants that handle specific categories of tasks. Each agent has access to tailored tools and operates within defined contexts to provide optimal performance for their domain.

```
Agent Categories (14 Total)
├── Development (3)      # Code, infrastructure, workflows
├── Consulting (2)       # Professional documents, reports
├── Research (3)         # Data gathering, analysis
├── Platform (3)         # Service integrations
└── Utility (3)          # Meta tasks, summaries
```

## Development Agents

### repository-manager
**Purpose**: Complete Git and GitHub repository management
**Tools**: Git operations, GitHub API, SSH signing, branch management
**Use Cases**:
- Initialize new repositories with proper conventions
- Create and manage pull requests with conventional commits
- Handle branch workflows and merging strategies
- Manage SSH commit signing and repository settings

**Trigger**: Git operations, repository setup, GitHub integration tasks

### system-environment-manager
**Purpose**: macOS system management and development environment setup
**Tools**: Homebrew, uv (Python), system configuration, package management
**Use Cases**:
- Install and configure development tools
- Set up Python environments with uv
- Manage macOS system preferences
- Handle development environment bootstrapping

**Trigger**: "install", "setup", "configure", environment management

### workflow-designer
**Purpose**: Create and document systematic processes and workflows
**Tools**: Documentation tools, Markdown rendering (glow), process design
**Use Cases**:
- Design development methodologies
- Create workflow documentation
- Build systematic approaches to complex tasks
- Generate terminal-friendly process presentations

**Trigger**: Workflow creation, process documentation, methodology design

## Consulting Agents

### professional-document-architect
**Purpose**: Create high-quality professional consulting documents
**Tools**: Document formatting, citation standards, academic writing tools
**Use Cases**:
- Generate executive summaries and reports
- Create formal consulting deliverables
- Ensure proper document structure and formatting
- Apply academic citation standards

**Trigger**: "professional report", "consulting document", formal writing

### comprehensive-report-generator
**Purpose**: Integrated analysis and reporting with built-in validation
**Tools**: Web research, fact-checking, market analysis, reference validation
**Use Cases**:
- Generate comprehensive business reports
- Validate market data and statistics
- Perform competitive analysis
- Create credible consulting deliverables with verified sources

**Trigger**: Complex reports requiring multi-source validation and analysis

## Research Agents

### client-research-coordinator
**Purpose**: Multi-platform client research and analysis
**Tools**: Atlassian, GitHub, Google Workspace, Hugging Face APIs
**Use Cases**:
- Comprehensive client background research
- Multi-source analysis across platforms
- Prepare consulting deliverables
- Coordinate complex research projects

**Trigger**: "client", "research", "analysis", comprehensive studies

### confluence-research-agent
**Purpose**: Atlassian Confluence content research and analysis
**Tools**: Confluence API, CQL queries, content retrieval, comment analysis
**Use Cases**:
- Research company documentation
- Analyze product visions and strategies
- Extract insights from Confluence spaces
- Review and analyze collaborative content

**Trigger**: "confluence", "research", documentation analysis

### llm-ai-agents-and-eng-research
**Purpose**: Stay current with AI/ML developments and engineering trends
**Tools**: Web search, content scraping, technical analysis
**Use Cases**:
- Research latest AI/ML innovations
- Find actionable insights in AI engineering
- Discover new tools and techniques
- Analyze technical trends and developments

**Trigger**: AI research, staying current with technology trends

## Platform Agents

### github-operations-agent
**Purpose**: Comprehensive GitHub platform management
**Tools**: GitHub API, repository management, issue tracking, code search
**Use Cases**:
- Manage repositories and organizations
- Handle issues and pull requests
- Search code across repositories
- Coordinate GitHub-based workflows

**Trigger**: "github", "repository", "issue", "pull request"

### google-workspace-agent
**Purpose**: Google Workspace productivity and integration
**Tools**: Gmail, Drive, Docs, Calendar, Sheets APIs
**Use Cases**:
- Manage email communications
- Handle document creation and collaboration
- Coordinate calendar and scheduling
- Process spreadsheet data

**Trigger**: "gmail", "google drive", "google docs", "calendar"

### atlas-exec-assistant
**Purpose**: Executive assistant for consultancy operations
**Tools**: Google Workspace, Atlassian, task coordination, communications
**Use Cases**:
- Calendar orchestration and scheduling
- Communications management
- Task coordination across platforms
- Daily productivity rituals

**Trigger**: Executive assistance, calendar management, task coordination

## Utility Agents

### meta-agent
**Purpose**: Generate new Claude Code agent configurations
**Tools**: Agent configuration, prompt engineering, workflow design
**Use Cases**:
- Create new specialized agents
- Design agent prompt templates
- Configure agent tool access
- Extend the agent ecosystem

**Trigger**: "create new agent", agent development needs

### hello-world-agent
**Purpose**: Simple greeting and onboarding interactions
**Tools**: Web search, basic interactions
**Use Cases**:
- Welcome new users
- Provide friendly introductions
- Handle basic greeting scenarios
- Demonstrate agent capabilities

**Trigger**: "hi claude", "hello", greeting interactions

### work-completion-summary
**Purpose**: Provide audio summaries and next step suggestions
**Tools**: Text-to-speech (ElevenLabs), audio playback, task analysis
**Use Cases**:
- Generate concise work summaries
- Provide audio feedback on completed tasks
- Suggest logical next steps
- Create TTS summaries for productivity

**Trigger**: "tts", "audio summary", work completion scenarios

## Agent Selection Strategy

Claude Code automatically selects agents based on:

1. **Keyword Matching**: Specific terms trigger relevant agents
2. **Context Analysis**: Task complexity determines agent specialization needs  
3. **Tool Requirements**: Available tools match agent capabilities
4. **Proactive Triggers**: Agents activate based on workflow patterns

## Best Practices

### When to Use Agents
- **Complex Tasks**: Multi-step operations requiring specialized tools
- **Domain Expertise**: Tasks requiring specific platform knowledge
- **Workflow Automation**: Repetitive processes that benefit from agent optimization

### Agent Interaction Patterns
- **Single Agent**: Most tasks handled by one specialized agent
- **Agent Chains**: Complex workflows may involve multiple agents sequentially
- **Parallel Agents**: Independent tasks can run multiple agents concurrently

### Customization Options
- **Tool Access**: Modify agent tool permissions in configuration files
- **Trigger Keywords**: Customize activation patterns for specific workflows
- **Context Memory**: Agents inherit project-specific context from memory modules

## Integration with Development Workflows

### Discovery-First Development
- **workflow-designer**: Creates exploration and planning frameworks
- **client-research-coordinator**: Gathers comprehensive background information
- **github-operations-agent**: Analyzes existing codebases and repositories

### Test-Driven Development  
- **repository-manager**: Manages test commits and implementation cycles
- **system-environment-manager**: Sets up testing frameworks and tools
- **professional-document-architect**: Documents testing strategies

### Visual Feedback Loop
- **workflow-designer**: Creates visual validation processes
- **work-completion-summary**: Provides feedback on visual iterations
- **github-operations-agent**: Manages visual regression testing workflows

## Troubleshooting

### Agent Not Triggering
1. Check keyword patterns in agent configuration
2. Verify tool availability and permissions
3. Review context requirements for agent activation

### Performance Issues
1. Monitor concurrent agent usage
2. Check tool response times and API limits
3. Review agent memory usage and context size

### Configuration Updates
1. Modify agent files in `~/.claude/agents/`
2. Test changes with simple trigger scenarios
3. Use `chezmoi apply` to deploy configuration updates

## Future Extensions

The agent ecosystem supports:
- **Custom Agents**: Create domain-specific agents using meta-agent
- **Tool Integration**: Add new MCP servers for expanded capabilities
- **Workflow Templates**: Build reusable agent interaction patterns
- **Context Modules**: Develop specialized memory systems for agent use

---

*For detailed agent configurations, see individual files in `~/.claude/agents/`. For workflow integration, reference `~/.claude/memories/workflows/`.*