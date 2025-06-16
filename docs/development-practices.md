# Global Development Practices

This document outlines the development standards, tools, and practices used across all my projects and repositories.

## Code Standards

### General Principles
- **Clarity over cleverness** - Write code that's easy to understand
- **Consistency** - Follow established patterns within each project
- **Documentation** - Comment non-obvious decisions and complex logic
- **Testing** - Write tests for all new features and bug fixes
- **Security first** - Never commit secrets, validate inputs, follow best practices

### Style Guidelines
- **Indentation**: 2 spaces for shell scripts, 4 spaces for Python
- **Naming**: Use descriptive names, avoid abbreviations
- **Comments**: Explain "why" not "what"
- **Line length**: Generally 80-100 characters max
- **File organization**: Group related functionality, clear directory structure

## Technology Stack

### Core Development Tools
- **Language-specific**: Python (uv), JavaScript/Node.js, Swift
- **Version Control**: Git with conventional commits
- **CI/CD**: GitHub Actions
- **Package Management**: Homebrew (system), uv (Python), npm (Node.js)

### Containerization
- **Primary**: [Apple Container](https://github.com/apple/container) - Native macOS containerization
  - Lightweight virtual machines on Apple silicon
  - OCI-compliant container images
  - Native integration with macOS development workflow
  - Sub-second startup times
- **Benefits over Docker Desktop**:
  - Native Apple silicon optimization
  - No Docker Desktop licensing concerns
  - Better resource utilization
  - Seamless macOS integration

### Infrastructure & Deployment
- **Cloud**: Prefer serverless and managed services
- **Databases**: PostgreSQL for relational, appropriate NoSQL when needed
- **Monitoring**: Built-in observability from day one
- **Secrets**: Environment variables, 1Password for development

## Testing Strategy

### Test Types
- **Unit Tests**: Cover individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Critical user workflows only
- **Performance Tests**: For latency-sensitive applications

### Testing Tools
- **Python**: pytest, coverage.py
- **JavaScript**: Jest, Vitest
- **Swift**: XCTest
- **General**: GitHub Actions for CI

### Coverage Requirements
- **Minimum**: 80% line coverage
- **Focus**: Critical business logic and edge cases
- **Documentation**: Test purpose and expected behavior

## Security Requirements

### Code Security
- **Input Validation**: Validate all external inputs
- **Authentication**: Use established libraries and patterns
- **Authorization**: Principle of least privilege
- **Cryptography**: Use vetted libraries, never roll your own

### Secrets Management
- **Development**: 1Password CLI integration
- **Production**: Environment variables and managed secret services
- **Git**: Never commit secrets, use pre-commit hooks to prevent
- **Rotation**: Regular secret rotation procedures

### Dependencies
- **Updates**: Regular dependency updates
- **Scanning**: Automated vulnerability scanning
- **Pinning**: Lock dependency versions in production
- **Minimal**: Only include necessary dependencies

## Git Workflow

### Commit Standards
- **Format**: [Conventional Commits](https://conventionalcommits.org/)
  - `feat:` - New features
  - `fix:` - Bug fixes
  - `docs:` - Documentation changes
  - `refactor:` - Code improvements without functional changes
  - `test:` - Test additions or modifications
- **Messages**: Descriptive, explain "why" not just "what"
- **Atomic**: One logical change per commit

### Branch Strategy
- **Main**: Always deployable
- **Feature**: Short-lived branches for new features
- **Hotfix**: Direct fixes to production issues
- **Naming**: `feature/description`, `fix/issue-description`

### Code Review
- **Required**: All code changes require review
- **Automated**: CI checks must pass
- **Manual**: Focus on logic, security, maintainability
- **Documentation**: Update relevant docs with changes

## Project Structure

### Common Patterns
- **README.md**: Project overview and setup for users
- **CLAUDE.md**: AI assistant context and development guidelines
- **.cursorrules**: Cursor editor AI rules (if using Cursor)
- **CONTRIBUTING.md**: Development setup and contribution guidelines

### Directory Organization
```
project/
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── scripts/          # Build and deployment scripts
├── .github/          # GitHub workflows and templates
└── config/           # Configuration files
```

### Documentation Requirements
- **API Documentation**: For all public interfaces
- **Architecture Decision Records**: For significant technical decisions
- **Setup Instructions**: Clear development environment setup
- **Deployment Guide**: How to deploy and configure

## Development Environment

### Required Tools
- **Terminal**: Modern shell with good history and completion
- **Editor**: VS Code, Cursor, or Emacs with appropriate extensions
- **CLI Tools**: gh, git, uv, node, Apple Container
- **Monitoring**: Basic observability tools during development

### Environment Setup
- **Dotfiles**: Standardized development environment
- **Secrets**: 1Password integration for development credentials
- **Dependencies**: Automated installation via package managers
- **Containers**: Apple Container for consistent development environments

## Performance Considerations

### General Guidelines
- **Premature optimization**: Avoid until proven necessary
- **Measurement**: Profile before optimizing
- **Caching**: Implement appropriate caching strategies
- **Scalability**: Design with growth in mind

### Specific Targets
- **API Response Times**: < 200ms for most operations
- **Build Times**: < 5 minutes for most projects
- **Test Suite**: < 30 seconds for unit tests
- **Container Startup**: < 5 seconds with Apple Container

## Maintenance

### Regular Tasks
- **Dependency Updates**: Monthly security updates, quarterly major updates
- **Performance Review**: Quarterly performance analysis
- **Security Audit**: Annual security review
- **Documentation**: Update with significant changes

### Monitoring
- **Error Rates**: Track and alert on error spikes
- **Performance**: Monitor key metrics continuously
- **Dependencies**: Automated vulnerability scanning
- **Usage**: Understand how features are actually used

## Project-Specific Overrides

Individual projects may override these practices when there are specific requirements:
- **Document deviations** in project's CLAUDE.md
- **Explain reasoning** for different approaches
- **Maintain consistency** within the project
- **Reference this document** for general practices

---

## Resources

- **[Apple Container Documentation](https://github.com/apple/container/tree/main/docs)**
- **[Python Development Guide](python-development.md)** - uv-based workflow
- **[Conventional Commits](https://conventionalcommits.org/)**
- **[Architecture Guide](architecture.md)** - System design patterns

---

*These practices evolve with experience and new tools. Last updated: June 2025*