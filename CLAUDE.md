# strata — Engine Repository

`nehalecky/strata` is the **strata engine** — the composable, cross-platform developer machine management framework. This is the public repo other users fork (or `chezmoi init`) to bootstrap their machines.

The engine defines *how* configuration is applied. A `strata.rc` defines *what* gets applied. The relationship mirrors `bash` and `.bashrc`: one is the runtime, the other is the configuration.

- See `README.md` for the vision and quick start.
- See `LAYERS.md` for the layer model fundamentals (what a `strata.rc` is, composition, precedence, agent routing).

This file serves agents and developers working in this repo. Read it before any non-trivial change.

---

## Three-Repo Model — Where Changes Belong

Before editing anything, decide which repo owns the change. Most accidental work happens in the wrong repo.

| Change type | Target repo |
|-------------|-------------|
| Engine / framework behavior, schemas, layer resolution, bootstrap | **this repo** (`nehalecky/strata`) |
| Org-wide layer config (identity, packages, policies) | `<org>/strata.rc` |
| Team layer config (team-specific tooling) | `<org>/<team>.strata.rc` |
| Personal config (your packages, shell, git, machine overrides) | `<username>/strata.rc` |

**Key rule:** if a change affects ALL users of strata, it belongs in this repo. If it's specific to one person, team, or org, it belongs in their `strata.rc`.

When in doubt, ask: "would another strata user need this?" If no, it's not engine work.

---

## Critical Workflow Enforcement

**YOU MUST follow this decision tree before ANY file operation in this repo.**

### File location check (mandatory)

This repo IS the chezmoi source directory (`~/.local/share/chezmoi`). The rule depends on what the file's purpose is:

| File type | Location | Workflow |
|-----------|----------|----------|
| Dotfile that deploys to HOME (`dot_*`, `.chezmoi*`) | Source = here, Runtime = HOME | **HOME → Source**: edit in HOME → test → `chezmoi add` → commit |
| Repo file (`README.md`, `LAYERS.md`, `CLAUDE.md`, `tests/`, `.chezmoiscripts/`, `dot_claude/`) | Source only | Edit directly in source |

**Course correction:** if you're about to edit `~/dot_zshrc` directly in the source, STOP. That deploys to HOME — edit `~/.zshrc` first, then `chezmoi add`. The `dot_claude/` directory is a special case: it's the source for `~/.claude/` runtime, but it's edited directly in source (not via HOME→Source) because chezmoi treats it as repo content.

### Git operations

**Golden rule:** always use `chezmoi git -- <command>` in this directory. Never raw `git` in HOME.

```bash
chezmoi git -- status
chezmoi git -- checkout -b feat/description
chezmoi git -- commit -m "feat: ..."
chezmoi git -- push
```

Use `chezmoi add <path>` (not `git add`) when staging dotfile changes from HOME.

### PR workflow (mandatory)

Never push directly to master. All changes go through PRs.

1. `chezmoi git -- checkout -b feat/description` (or `fix/`, `docs/`, `chore/`)
2. Commit and push the branch
3. `gh pr create` — CI validates the change
4. Ask user for review before merging
5. Close related GitHub issues with commit references

---

## Repo Structure

| Path | Purpose |
|------|---------|
| `README.md` | Vision, quick start, philosophy |
| `LAYERS.md` | Layer model fundamentals — what a `strata.rc` is, composition, precedence, routing |
| `SETUP.md` | Detailed onboarding for new machines |
| `CLAUDE.md` | This file — agent and developer orientation |
| `.chezmoi.toml.tmpl` | Init-time prompts: identity, terminal, `strata_layers` URLs |
| `.chezmoiexternal.yaml.tmpl` | Composition mechanism — pulls strata layers from `strata_layers` into numbered layer dirs |
| `.chezmoiignore` | Files excluded from runtime apply (local data, machine-specific overrides) |
| `dot_*` | Chezmoi-managed files deployed to HOME (e.g., `dot_zshrc` → `~/.zshrc`) |
| `dot_claude/` | Claude Code config source (agents, hooks, memories, commands) → `~/.claude/` |
| `dot_docs/` | Documentation deployed to `~/.docs/` |
| `.chezmoiscripts/` | Lifecycle scripts: `run_once_*`, `run_onchange_*` (Python preferred) |
| `tests/` | Pytest suite — run with `uv run pytest tests/ -v` |

---

## Key Concepts (defer to `LAYERS.md` for detail)

- **`strata_layers`** — comma-separated SSH git URLs configured at init time. The engine pulls each layer and applies them in order; higher index = higher priority (personal overrides team overrides org).
- **`.local` convention** — the engine ships sourcing hooks (e.g., `dot_zshrc`, `dot_gitconfig`) that source layer-provided `zshrc.local`, `gitconfig.local`, and stack `Brewfile`s. Layers fill content; the engine wires it up.
- **`chezmoi update`** — pulls latest engine + all registered layers, then applies. This is the standard sync command after the initial `chezmoi init`.
- **Composition is additive-only** — no layer can remove what an earlier layer installed. Last layer wins for same-key shell/git settings; brew packages accumulate.

---

## Development Standards

### Code

- **Python over bash for all scripts.** Python's context managers, `pathlib`, and `subprocess` eliminate bash quoting/trap/scope footguns. When editing any shell script, migrate the whole file to Python and update callers (Dockerfiles, CI configs).
- Use `uv run` for Python execution (not raw `python3` or `pip`). Project deps via `uv add`.
- 4-space indentation for Python; 2-space for shell (legacy only).
- Comment non-obvious configuration choices.
- Never commit secrets — use 1Password references in templates.

### Pre-PR checklist (run before every PR)

```bash
uv run pytest tests/ -v       # full test suite must pass
chezmoi apply --dry-run       # validate templating + script logic
```

CI runs broader validation across profiles and terminals. Local checks catch the obvious failures first.

### Commits

- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Imperative mood, subject under 50 chars, explain "why" in body
- SSH commit signing via 1Password is automatic — no extra flags needed
- Reference issues: `Fixes #123` or `Refs #456`

### Workflow principles

- **Proactive agent delegation.** Before non-trivial tasks, check `~/.claude/agents/` for specialists. Delegate when an agent matches the domain (e.g., `dotfiles-manager` for chezmoi work, `repo` for git/PR ops).
- **Verify success.** After source-side edits, confirm `chezmoi apply --dry-run` is clean. After HOME→Source, confirm the source diff matches what you edited.
- **Ask before creating** new tools/scripts — prefer enhancing existing ones.
- **Strict spec compliance.** When implementing per docs, implement exactly as specified — no extra files, no "helpful" assumptions.
- **Always ask for explicit review** before posting GitHub issues, PRs, or external comms.

---

## Environment

- **Platform:** macOS (working surface today). Architecture is POSIX-first; Linux/Windows track the same layer model as primitives stabilize.
- **Shell:** Zsh
- **Package managers:** Homebrew (system), `uv` (Python)
- **Core CLI tools:** `rg`, `fd`, `eza`, `bat`, `delta` — Claude Code prefers these over their traditional counterparts
- **Git:** SSH commit signing enforced via 1Password agent

---

## Memory and Skills (Auto-Loaded)

@.claude/memories/workflows/core-workflows.md
@.claude/memories/tools/essential-tools.md
@.claude/memories/tools/git-standards.md

Stack-specific modules under `~/.claude/memories/stacks/` (Python, Node.js, frontend) load on demand. Superpowers skills handle tactical execution (TDD, brainstorming, plan writing/execution); memories handle strategic patterns and environment specifics.

---

*This file is the entry point for any agent or developer working in the strata engine. Keep it current — when the engine's contract with layers changes, update this file and `LAYERS.md` together.*
