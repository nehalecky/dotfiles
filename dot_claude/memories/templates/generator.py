#!/usr/bin/env python3
"""
Smart Project Template Generator for Claude Code Memory System

Automatically generates project-specific CLAUDE.md files with appropriate
imports based on project detection and user preferences.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ProjectType(Enum):
    """Detected project types with associated technology stacks."""
    PYTHON = "python"
    NODEJS = "nodejs"
    WEB_FRONTEND = "web-frontend"
    RUST = "rust"
    GO = "golang"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class ProjectInfo:
    """Information about a detected project."""
    name: str
    type: ProjectType
    description: str
    stack_components: List[str]
    package_files: List[str]
    has_tests: bool
    has_ci: bool
    git_repo: bool


class ProjectDetector:
    """Detects project type and characteristics from directory contents."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.files = list(project_path.rglob("*")) if project_path.exists() else []
        self.file_names = {f.name for f in self.files if f.is_file()}
    
    def detect(self) -> ProjectInfo:
        """Detect project type and characteristics."""
        project_name = self.project_path.name
        project_type = self._detect_project_type()
        description = self._generate_description(project_type)
        stack_components = self._detect_stack_components()
        package_files = self._find_package_files()
        has_tests = self._has_tests()
        has_ci = self._has_ci()
        git_repo = self._is_git_repo()
        
        return ProjectInfo(
            name=project_name,
            type=project_type,
            description=description,
            stack_components=stack_components,
            package_files=package_files,
            has_tests=has_tests,
            has_ci=has_ci,
            git_repo=git_repo
        )
    
    def _detect_project_type(self) -> ProjectType:
        """Detect primary project type based on key files."""
        type_indicators = {
            ProjectType.PYTHON: {
                'pyproject.toml', 'setup.py', 'requirements.txt', 
                'Pipfile', 'poetry.lock', 'uv.lock'
            },
            ProjectType.NODEJS: {
                'package.json', 'package-lock.json', 'yarn.lock', 
                'pnpm-lock.yaml', 'tsconfig.json'
            },
            ProjectType.WEB_FRONTEND: {
                'vite.config.js', 'vite.config.ts', 'webpack.config.js',
                'next.config.js', 'react-scripts', 'vue.config.js'
            },
            ProjectType.RUST: {
                'Cargo.toml', 'Cargo.lock'
            },
            ProjectType.GO: {
                'go.mod', 'go.sum'
            }
        }
        
        detected_types = []
        for project_type, indicators in type_indicators.items():
            if indicators & self.file_names:
                detected_types.append(project_type)
        
        if len(detected_types) == 0:
            return ProjectType.UNKNOWN
        elif len(detected_types) == 1:
            return detected_types[0]
        else:
            return ProjectType.MIXED
    
    def _detect_stack_components(self) -> List[str]:
        """Detect specific technology stack components."""
        components = []
        
        # Python ecosystem
        if 'pyproject.toml' in self.file_names:
            components.append('uv/pyproject.toml')
        if 'pytest.ini' in self.file_names or 'conftest.py' in self.file_names:
            components.append('pytest')
        if any('ruff' in f for f in self.file_names):
            components.append('ruff')
        
        # Node.js ecosystem
        if 'package.json' in self.file_names:
            try:
                package_json = self.project_path / 'package.json'
                if package_json.exists():
                    with open(package_json) as f:
                        data = json.load(f)
                        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                        
                        if 'typescript' in deps:
                            components.append('TypeScript')
                        if 'react' in deps:
                            components.append('React')
                        if 'vue' in deps:
                            components.append('Vue')
                        if 'next' in deps:
                            components.append('Next.js')
                        if 'vite' in deps:
                            components.append('Vite')
                        if 'webpack' in deps:
                            components.append('Webpack')
                        if 'jest' in deps or 'vitest' in deps:
                            components.append('Testing')
            except (json.JSONDecodeError, IOError):
                pass
        
        # Frontend specific
        if 'tailwind.config.js' in self.file_names:
            components.append('Tailwind CSS')
        if any('eslint' in f for f in self.file_names):
            components.append('ESLint')
        if any('prettier' in f for f in self.file_names):
            components.append('Prettier')
        
        return components
    
    def _find_package_files(self) -> List[str]:
        """Find package/dependency management files."""
        package_files = []
        package_indicators = {
            'pyproject.toml', 'setup.py', 'requirements.txt',
            'package.json', 'Cargo.toml', 'go.mod', 'Gemfile'
        }
        
        for file_name in package_indicators:
            if file_name in self.file_names:
                package_files.append(file_name)
        
        return package_files
    
    def _has_tests(self) -> bool:
        """Check if project has test files or directories."""
        test_indicators = {
            'test', 'tests', '__tests__', 'spec', 'specs',
            'pytest.ini', 'jest.config.js', 'vitest.config.ts'
        }
        
        # Check for test directories
        test_dirs = {f.name for f in self.files if f.is_dir()}
        if test_indicators & test_dirs:
            return True
        
        # Check for test files
        if test_indicators & self.file_names:
            return True
        
        # Check for files with test patterns
        test_patterns = ['test_', '_test', '.test.', '.spec.']
        for file_path in self.files:
            if file_path.is_file():
                for pattern in test_patterns:
                    if pattern in file_path.name:
                        return True
        
        return False
    
    def _has_ci(self) -> bool:
        """Check if project has CI/CD configuration."""
        ci_indicators = {
            '.github/workflows', '.gitlab-ci.yml', '.travis.yml',
            'azure-pipelines.yml', 'Jenkinsfile', '.circleci'
        }
        
        # Check for CI directories and files
        for indicator in ci_indicators:
            ci_path = self.project_path / indicator
            if ci_path.exists():
                return True
        
        return False
    
    def _is_git_repo(self) -> bool:
        """Check if project is a git repository."""
        git_dir = self.project_path / '.git'
        return git_dir.exists()
    
    def _generate_description(self, project_type: ProjectType) -> str:
        """Generate a descriptive summary based on project type."""
        descriptions = {
            ProjectType.PYTHON: "Python development project",
            ProjectType.NODEJS: "Node.js/TypeScript development project",
            ProjectType.WEB_FRONTEND: "Frontend web application",
            ProjectType.RUST: "Rust development project",
            ProjectType.GO: "Go development project",
            ProjectType.MIXED: "Multi-technology project",
            ProjectType.UNKNOWN: "Development project"
        }
        return descriptions.get(project_type, "Development project")


class CLAUDETemplateGenerator:
    """Generates CLAUDE.md files with appropriate imports and configuration."""
    
    def __init__(self, project_info: ProjectInfo, global_claude_path: Path):
        self.project_info = project_info
        self.global_claude_path = global_claude_path
    
    def generate(self) -> str:
        """Generate complete CLAUDE.md content."""
        sections = [
            self._generate_header(),
            self._generate_project_context(),
            self._generate_session_startup(),
            self._generate_import_chain(),
            self._generate_architecture_decisions(),
            self._generate_workflow_integration(),
            self._generate_project_specific_sections(),
            self._generate_session_checklist()
        ]
        
        return "\n\n".join(sections)
    
    def _generate_header(self) -> str:
        """Generate project header with name and context."""
        return f"""# Claude Development Instructions - {self.project_info.name}

## Project Context

**Repository:** `{self.project_info.name}` - {self.project_info.description}  
**Stack:** {', '.join(self.project_info.stack_components) if self.project_info.stack_components else 'To be determined'}  
**Origin:** {self._infer_origin()}  
**Current Phase:** {self._infer_current_phase()}"""
    
    def _generate_project_context(self) -> str:
        """Generate project-specific context information."""
        return """## Critical Session Startup

**ALWAYS start development sessions with:**

1. **Global Context Review:** Read global CLAUDE.md for established workflows
2. **Task Check:** `task list` - Check current Jira tasks and priorities  
3. **Project Status:** `git status` and `git log --oneline -5`
4. **Environment Validation:** {environment_checks}""".format(
            environment_checks=self._generate_environment_checks()
        )
    
    def _generate_session_startup(self) -> str:
        """Generate session startup procedures."""
        if self.project_info.type == ProjectType.PYTHON:
            return """
### Python Environment Validation
```bash
# Verify UV and Python environment
uv --version                  # Check UV installation
uv sync                       # Ensure dependencies current
uv run python --version       # Verify Python version
```"""
        elif self.project_info.type == ProjectType.NODEJS:
            return """
### Node.js Environment Validation
```bash
# Verify Node.js and package manager
node --version               # Check Node.js version
npm --version                # Or pnpm --version
npm install                  # Ensure dependencies current
```"""
        elif self.project_info.type == ProjectType.WEB_FRONTEND:
            return """
### Frontend Environment Validation
```bash
# Verify development environment
node --version               # Check Node.js version
npm run dev                  # Start development server
npm run test                 # Verify tests pass
```"""
        else:
            return """
### Environment Validation
```bash
# Project-specific environment checks
# Add validation commands as needed
```"""
    
    def _generate_import_chain(self) -> str:
        """Generate appropriate import chain based on project type."""
        imports = ["## Global Memory System Import Chain"]
        
        # Always include core workflows
        imports.append("### Core Development Workflows")
        imports.append(f"@{self._relative_path_to_global()}.claude/memories/workflows/core-workflows.md")
        
        # Add stack-specific imports
        stack_imports = self._get_stack_imports()
        if stack_imports:
            imports.append("\n### Technology Stack")
            imports.extend(stack_imports)
        
        # Add tool imports
        imports.append("\n### Essential Tools")
        imports.append(f"@{self._relative_path_to_global()}.claude/memories/tools/git-practices.md")
        imports.append(f"@{self._relative_path_to_global()}.claude/memories/tools/essential-tools.md")
        
        # Add MCP imports if relevant
        if self.project_info.git_repo:
            imports.append("\n### MCP Integrations")
            imports.append(f"@{self._relative_path_to_global()}.claude/memories/mcp/github-integration.md")
        
        return "\n".join(imports)
    
    def _get_stack_imports(self) -> List[str]:
        """Get appropriate stack imports based on project type."""
        base_path = f"@{self._relative_path_to_global()}.claude/memories/stacks"
        
        stack_map = {
            ProjectType.PYTHON: [f"{base_path}/python.md"],
            ProjectType.NODEJS: [f"{base_path}/nodejs.md"],
            ProjectType.WEB_FRONTEND: [
                f"{base_path}/nodejs.md",
                f"{base_path}/web-frontend.md"
            ],
            ProjectType.MIXED: [
                f"{base_path}/python.md",
                f"{base_path}/nodejs.md"
            ]
        }
        
        return stack_map.get(self.project_info.type, [])
    
    def _generate_architecture_decisions(self) -> str:
        """Generate architecture decisions section."""
        status_items = []
        
        if self.project_info.package_files:
            status_items.append(f"✅ **Package Management:** {', '.join(self.project_info.package_files)}")
        
        if self.project_info.has_tests:
            status_items.append("✅ **Testing Framework:** Configured and available")
        else:
            status_items.append("❌ **Testing Framework:** Not yet configured")
        
        if self.project_info.has_ci:
            status_items.append("✅ **CI/CD:** Configured and active")
        else:
            status_items.append("❌ **CI/CD:** Not yet configured")
        
        return f"""## Architecture Decisions

### Current Implementation Status
{chr(10).join(f"- {item}" for item in status_items)}

### Technology Decisions (DO NOT CHANGE without good reason)

**Core Stack:**
{self._generate_stack_decisions()}

**Architecture Pattern:**
```
{self._generate_architecture_pattern()}
```"""
    
    def _generate_stack_decisions(self) -> str:
        """Generate stack-specific technology decisions."""
        if self.project_info.type == ProjectType.PYTHON:
            return """- **Python 3.12+** - Modern Python with performance improvements
- **UV Package Manager** - Fast, modern Python dependency management
- **Pytest** - Testing framework with excellent plugin ecosystem
- **Ruff** - Ultra-fast linting and formatting"""
        
        elif self.project_info.type == ProjectType.NODEJS:
            return """- **Node.js LTS** - Stable runtime environment
- **TypeScript** - Type safety and modern language features
- **pnpm/npm** - Package management with efficient disk usage
- **ESLint + Prettier** - Code quality and formatting"""
        
        elif self.project_info.type == ProjectType.WEB_FRONTEND:
            return """- **React/Vue** - Component-based frontend framework
- **TypeScript** - Type safety for large applications
- **Vite** - Fast build tool and development server
- **Vitest/Jest** - Fast unit testing framework"""
        
        else:
            return """- **Technology Stack** - To be determined based on requirements
- **Package Manager** - Standard tooling for chosen technology
- **Testing Framework** - Comprehensive test coverage approach
- **Code Quality** - Linting and formatting standards"""
    
    def _generate_architecture_pattern(self) -> str:
        """Generate architecture pattern based on project type."""
        patterns = {
            ProjectType.PYTHON: """src/
├── {package_name}/
│   ├── __init__.py
│   ├── main.py
│   └── core/
├── tests/
└── pyproject.toml""",
            ProjectType.NODEJS: """src/
├── index.ts
├── types/
├── utils/
└── components/
tests/
├── unit/
└── integration/
package.json""",
            ProjectType.WEB_FRONTEND: """src/
├── components/
├── hooks/
├── utils/
├── assets/
└── App.tsx
public/
tests/
package.json"""
        }
        
        pattern = patterns.get(self.project_info.type, """src/
├── main files
├── modules/
└── utilities/
tests/
config files""")
        
        return pattern.format(package_name=self.project_info.name.replace('-', '_'))
    
    def _generate_workflow_integration(self) -> str:
        """Generate workflow integration section."""
        return """## Development Workflow

### Global Workflow Integration
**This project follows global patterns with project-specific adaptations:**

1. **Discovery-First Development** - For complex features or system exploration
2. **Test-Driven Workflow** - For well-defined feature requirements  
3. **Visual Feedback Loop** - For UI/UX components (if applicable)

### Project-Specific Workflow
```bash
# Project setup
{setup_commands}

# Development cycle  
{dev_commands}

# Testing
{test_commands}

# Build/Deploy
{build_commands}
```""".format(
            setup_commands=self._generate_setup_commands(),
            dev_commands=self._generate_dev_commands(),
            test_commands=self._generate_test_commands(),
            build_commands=self._generate_build_commands()
        )
    
    def _generate_project_specific_sections(self) -> str:
        """Generate project-specific sections."""
        sections = []
        
        # Code standards
        sections.append(self._generate_code_standards())
        
        # Key implementation patterns
        sections.append(self._generate_implementation_patterns())
        
        # Dependencies and tools
        sections.append(self._generate_dependencies_section())
        
        # Performance considerations
        sections.append(self._generate_performance_section())
        
        return "\n\n".join(sections)
    
    def _generate_code_standards(self) -> str:
        """Generate code standards section."""
        return """## Code Standards

**Follow global standards plus project-specific conventions:**
- **Consistent formatting** - Use project linting and formatting tools
- **Type safety** - Comprehensive type annotations where applicable
- **Test coverage** - Aim for high test coverage on critical paths
- **Documentation** - Clear inline documentation for complex logic"""
    
    def _generate_implementation_patterns(self) -> str:
        """Generate key implementation patterns."""
        if self.project_info.type == ProjectType.PYTHON:
            return """## Key Implementation Patterns

### Error Handling
```python
from typing import Union, Optional
from enum import Enum

class ErrorCode(Enum):
    INVALID_INPUT = "invalid_input"
    NETWORK_ERROR = "network_error"

def process_data(data: str) -> Union[str, ErrorCode]:
    if not data:
        return ErrorCode.INVALID_INPUT
    try:
        return process_result
    except NetworkError:
        return ErrorCode.NETWORK_ERROR
```"""
        
        elif self.project_info.type == ProjectType.NODEJS:
            return """## Key Implementation Patterns

### Error Handling
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export function handleAsyncError<T>(
  fn: (...args: any[]) => Promise<T>
) {
  return (...args: any[]): Promise<T> => {
    return Promise.resolve(fn(...args)).catch((error) => {
      logger.error('Async error:', error);
      throw error;
    });
  };
}
```"""
        
        else:
            return """## Key Implementation Patterns

### Error Handling
```
// Add project-specific error handling patterns
// as they are established during development
```"""
    
    def _generate_dependencies_section(self) -> str:
        """Generate dependencies and tools section."""
        deps_content = "## Dependencies and Tools\n\n### Core Dependencies\n"
        
        if self.project_info.package_files:
            deps_content += f"```\n# Managed via: {', '.join(self.project_info.package_files)}\n"
            
            if self.project_info.type == ProjectType.PYTHON:
                deps_content += "# Add with: uv add package-name\n"
            elif self.project_info.type == ProjectType.NODEJS:
                deps_content += "# Add with: npm install package-name\n"
            
            deps_content += "```\n"
        
        deps_content += "\n### Development Tools\n"
        deps_content += "- **Code Quality** - Linting and formatting tools\n"
        deps_content += "- **Testing** - Framework and utilities\n"
        if self.project_info.has_ci:
            deps_content += "- **CI/CD** - Automated testing and deployment\n"
        
        return deps_content
    
    def _generate_performance_section(self) -> str:
        """Generate performance considerations."""
        return """## Performance Considerations

### Development Targets
- **Startup Time** - Fast development environment setup
- **Build Time** - Efficient compilation and bundling
- **Test Execution** - Quick feedback during development
- **Memory Usage** - Reasonable resource consumption

### Optimization Strategies
- **Caching** - Leverage build and dependency caches
- **Incremental Builds** - Only rebuild what changed
- **Parallel Processing** - Use available CPU cores effectively"""
    
    def _generate_session_checklist(self) -> str:
        """Generate session checklist."""
        return """## Session Checklist

**Before starting development:**
- [ ] Read global CLAUDE.md for workflow reminders
- [ ] Check Jira project tasks and priorities
- [ ] Review recent commits and project status
- [ ] Verify development environment is ready
- [ ] Review this project's architectural decisions

**During development:**
- [ ] Update Jira task status as you work  
- [ ] Follow established architecture patterns
- [ ] Write tests for new functionality
- [ ] Run linting/formatting before commits
- [ ] Document architectural decisions

**Before ending session:**
- [ ] Update Jira with progress and discoveries
- [ ] Commit work with conventional commit messages
- [ ] Update this CLAUDE.md if architecture changes
- [ ] Note any blockers or next session priorities

*This file serves as your development context and architectural memory for the {project_name} project. Keep it updated as the project evolves and always reference the global CLAUDE.md for foundational workflows.*""".format(
            project_name=self.project_info.name
        )
    
    def _generate_setup_commands(self) -> str:
        """Generate setup commands based on project type."""
        if self.project_info.type == ProjectType.PYTHON:
            return "uv sync                      # Install dependencies"
        elif self.project_info.type == ProjectType.NODEJS:
            return "npm install                 # Install dependencies"
        else:
            return "# Add setup commands as determined"
    
    def _generate_dev_commands(self) -> str:
        """Generate development commands."""
        if self.project_info.type == ProjectType.PYTHON:
            return """uv run ruff format .          # Format code
uv run ruff check . --fix     # Lint and fix
uv run mypy src/              # Type check"""
        elif self.project_info.type == ProjectType.NODEJS:
            return """npm run dev                   # Start development
npm run lint:fix              # Lint and fix
npm run type-check            # Type validation"""
        else:
            return "# Add development commands as determined"
    
    def _generate_test_commands(self) -> str:
        """Generate test commands."""
        if self.project_info.type == ProjectType.PYTHON:
            return "uv run pytest                # Run tests"
        elif self.project_info.type == ProjectType.NODEJS:
            return "npm test                     # Run tests"
        else:
            return "# Add test commands as determined"
    
    def _generate_build_commands(self) -> str:
        """Generate build commands."""
        if self.project_info.type == ProjectType.PYTHON:
            return "uv run python -m build       # Build package"
        elif self.project_info.type == ProjectType.NODEJS:
            return "npm run build                # Build for production"
        else:
            return "# Add build commands as determined"
    
    def _infer_origin(self) -> str:
        """Infer project origin."""
        if self.project_info.git_repo:
            return "Git repository project"
        else:
            return "New development project"
    
    def _infer_current_phase(self) -> str:
        """Infer current development phase."""
        if not self.project_info.package_files:
            return "Discovery"
        elif not self.project_info.has_tests:
            return "Development"
        elif not self.project_info.has_ci:
            return "Testing"
        else:
            return "Maintenance"
    
    def _relative_path_to_global(self) -> str:
        """Calculate relative path to global CLAUDE.md directory."""
        # For now, assume we're always relative to home directory
        # This could be made more sophisticated based on actual paths
        return ""
    
    def _generate_environment_checks(self) -> str:
        """Generate environment validation checks."""
        if self.project_info.type == ProjectType.PYTHON:
            return "UV environment and Python dependencies"
        elif self.project_info.type == ProjectType.NODEJS:
            return "Node.js version and package dependencies"
        elif self.project_info.type == ProjectType.WEB_FRONTEND:
            return "Frontend build tools and development server"
        else:
            return "Project-specific environment requirements"


def main():
    """Main entry point for the template generator."""
    if len(sys.argv) < 2:
        print("Usage: python generator.py <project_path> [output_path]")
        sys.exit(1)
    
    project_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else project_path / "CLAUDE.md"
    
    if not project_path.exists():
        print(f"Error: Project path {project_path} does not exist")
        sys.exit(1)
    
    # Detect project characteristics
    detector = ProjectDetector(project_path)
    project_info = detector.detect()
    
    print(f"Detected project: {project_info.name}")
    print(f"Type: {project_info.type.value}")
    print(f"Stack: {', '.join(project_info.stack_components)}")
    print(f"Tests: {'Yes' if project_info.has_tests else 'No'}")
    print(f"CI/CD: {'Yes' if project_info.has_ci else 'No'}")
    
    # Generate CLAUDE.md content
    global_claude_path = Path.home() / "CLAUDE.md"
    generator = CLAUDETemplateGenerator(project_info, global_claude_path)
    content = generator.generate()
    
    # Write to output file
    output_path.write_text(content, encoding='utf-8')
    print(f"Generated CLAUDE.md at: {output_path}")


if __name__ == "__main__":
    main()