# strata

> strata is a composable, cross-platform developer machine management framework — declarative layers from dotfiles to applications — that agentic tooling makes sustainable for anyone to maintain what previously required a team.

Pronounced **STRAY-tah**.

```
                S T R A T A
       ___________________________
      /                           \
     |  ~ ~ ~  personal  ~ ~ ~ ~ ~ |   <- your work builds here
     |-----------------------------|
     |  - - -  team     - - - - -  |
     |=============================|
     |  = = =  org      = = = = =  |
     |#############################|
     |  # # #  engine   # # # # #  |
      \___________________________/
```

`strata` is the engine. `strata.rc` is a configured instance. The relationship mirrors `bash` and `.bashrc`: one is the runtime, the other is your configuration of it.

## Quick start

On a clean machine:

```bash
chezmoi init --apply github.com/nehalecky/strata
```

That is the entire bootstrap. The engine clones, prompts for the values it needs, and applies the layers in order.

## The layer model

A machine is a stack of declarative layers. The engine resolves them in order; each layer overrides the one below.

| Layer | Repo | Purpose |
|-------|------|---------|
| Engine | `nehalecky/strata` | Runtime, schemas, layer resolution, bootstrap |
| Org | `descript/strata.rc` | Org-wide identity, packages, tooling, policies |
| Team | `descript-platform/strata.rc` | Team-specific tooling (platform ≠ data ≠ frontend) |
| Personal | `nehalecky/strata.rc` | Your packages, shell, git config, machine-specific overrides |

Layers are additive. A setup can use two (engine + personal) or four. Each layer only needs to express what it changes.

A LAYERS.md document covering precedence rules, override semantics, and merge strategy is coming soon.

## Your personal `strata.rc`

A configured instance of `strata` lives in a repo named `<username>/strata.rc`. At minimum it contains:

```
strata.rc/
├── Brewfile          # packages (or equivalent for your platform)
├── zshrc.local       # shell additions, aliases, env
└── gitconfig.local   # identity, signing, aliases
```

To create yours:

1. Fork `nehalecky/strata.rc` or start from scratch with the three files above
2. Push to `github.com/<your-username>/strata.rc`
3. Reference it from your `strata` init prompts; the engine will pull and apply it

Anything chezmoi can manage, a `strata.rc` can carry. Templating, profiles, secrets via 1Password, and machine-conditional logic all work because the engine is chezmoi underneath.

## What strata manages

- **Dotfiles** — shell, editor, terminal, prompt, git
- **Shell configuration** — zsh, environment, aliases, completions
- **Git** — identity, signing, hooks, per-host overrides
- **Applications** — Homebrew bundles today; cross-platform package managers over time
- **Claude Code** — agents, memories, hooks, commands, skills, MCP servers

macOS is the working surface today. The architecture is POSIX-first and platform-agnostic; Linux and Windows support follow the same layer model as the primitives stabilize.

## Philosophy

**Consistent ground for everything you build on a machine.** strata gives a developer one declarative environment that reproduces across machines and across people. The same engine, the same layer model, the same resolved state — whether you are setting up a new laptop, onboarding a teammate, or letting an automated process change a config file. That reproducibility is what makes work reliable, for humans and for the tools they delegate to. The scope reaches past dotfiles into applications, package managers, Claude Code configuration, and MCP servers, because the full developer environment is what determines whether anything on top of it actually works.

**POSIX primitives, not a new platform.** The engine composes chezmoi, shell, git, and package managers — tools that already exist on every developer machine. There is no daemon, no proprietary state store, no service to keep alive. If `strata` disappeared tomorrow, the underlying configuration would still apply.

**Not a platform-engineering tool.** The capabilities here historically required a dedicated team: declarative provisioning, multi-machine consistency, environment reproducibility, secrets management. strata makes those capabilities available to a single developer — and to non-engineers who want a managed machine without owning the management.

**Agentic tooling is the multiplier.** A framework like this is only sustainable for one person to maintain because agents can read, route, and write the right files. A change request gets routed:

- Framework change → `nehalecky/strata` (engine)
- Personal change → `<username>/strata.rc` (your layer)

Anyone can interact in natural language. The agent understands the layer model, opens the PR in the correct repo, and the engine applies the result on the next sync. strata is **not an agentic framework** — it is a framework whose architecture flows seamlessly with agentic tools.

---

**Status:** active development. The vision is settled; the surface is moving. Issues and discussion welcome at [nehalecky/strata](https://github.com/nehalecky/strata).
