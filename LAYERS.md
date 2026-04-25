# LAYERS

The foundational concepts of strata: what a `strata.rc` is, what composition means, and how layers resolve.

## What is a `strata.rc`

A `strata.rc` is a configured instance of strata. The relationship to the strata engine mirrors `bash` and `.bashrc`: the engine defines *how* configuration is applied; a `strata.rc` is *what* gets applied.

Any entity — a person, a team, an org — can have a `strata.rc`. It lives in a git repo. The engine pulls it and applies it.

A minimum viable `strata.rc` contains four files:

| File | Purpose |
|------|---------|
| `Brewfile` | Packages (Homebrew today, cross-platform over time) |
| `zshrc.local` | Shell additions, aliases, env vars; sourced by the engine's `dot_zshrc` |
| `gitconfig.local` | Git overrides; included by the engine's git config |
| `CLAUDE.md` | Agent orientation: what this layer is, what repo owns what changes |

Anything chezmoi can manage is also supported: templates, profiles, secrets via 1Password, machine-conditional logic. The engine is chezmoi underneath, so a `strata.rc` inherits the full chezmoi surface.

## Naming convention

| Scope | Repo pattern | Example |
|-------|-------------|---------|
| Personal | `<username>/strata.rc` | `username/strata.rc` |
| Org | `<org>/strata.rc` | `acme/strata.rc` |
| Team | `<org>/<team>.strata.rc` | `acme/platform.strata.rc` |

The `.strata.rc` suffix on team repos distinguishes team layers from the org's single `strata.rc`. Teams live under the same GitHub org — no separate org needed.

## What is composition

Composition is what happens when the engine applies multiple `strata.rc` layers in order. Each layer is additive — it extends the one below. Nothing is replaced unless a file explicitly overrides a value set by an earlier layer.

The user configures layers as a comma-separated list of SSH git URLs, lowest priority first:

```
git@github.com:acme/strata.rc.git,git@github.com:acme/platform.strata.rc.git,git@github.com:username/strata.rc.git
```

The engine generates numbered layer directories (`.strata_layer_0/`, `.strata_layer_1/`, ...) and applies them in index order. A user with one layer and a user with three use the same mechanism — composition is just the list length.

## Precedence rules

Higher index = higher priority. Personal always overrides team; team always overrides org.

| File | Merge strategy |
|------|---------------|
| `Brewfile` | Stacked additively — `brew bundle` runs once per layer, packages accumulate |
| `zshrc.local` | Sourced in layer order; last one wins for shell variable assignments, aliases accumulate |
| `gitconfig.local` | Included via git's `[include]` directive in layer order; last include wins for same-key settings |

No layer can remove what an earlier layer installed. **Composition is additive-only.**

## Agent routing

When an agent makes a change, it must commit to the correct repo:

| Change type | Target repo |
|-------------|------------|
| Framework, engine behavior | `nehalecky/strata` (engine) |
| Org-wide defaults | `<org>/strata.rc` |
| Team tooling | `<org>/<team>.strata.rc` |
| Personal config | `<username>/strata.rc` |

**Rule of thumb:** if only you would want it, it belongs in your `strata.rc`. If your whole team needs it, it belongs in the team layer. If the org should standardize on it, it belongs in the org layer.

`CLAUDE.md` in each repo documents this routing explicitly for agents.

## Creating a `strata.rc`

Three steps:

1. Create a git repo named `strata.rc` (personal) or `<team>.strata.rc` (team) on GitHub
2. Add the minimum files: `Brewfile`, `zshrc.local`, `gitconfig.local`, `CLAUDE.md`
3. Add the SSH URL to the `strata_layers` prompt when running `chezmoi init`

The engine pulls all registered layers automatically on `chezmoi update`.
