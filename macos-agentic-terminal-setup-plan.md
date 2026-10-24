# macOS Agentic Terminal Setup — Codex CLI Implementation Plan

> Status: v0.2 — execution-oriented outline (总纲), not a blind installation script.
> Goal: set up **Ghostty + Herdr + Zsh + Oh My Zsh + Starship + Catppuccin Mocha + Visual Studio Code**, with a comfortable development experience for **Codex CLI and Claude Code**. VS Code is the primary IDE; Cursor is an optional alternative, not part of the automatic install.
> Target: macOS (detect Apple Silicon vs Intel at runtime). Use Homebrew where appropriate.

## Instructions to Codex CLI

You are the implementation agent. **Inspect the current machine before making changes**, then carry out the phases below end-to-end where safe. The machine may already have Ghostty, Herdr, a custom `.zshrc`, a prompt framework, and coding-agent configuration. Do not assume it is a clean install.

**Non-negotiable safety rules:**

1. Preserve working tools, PATH settings, aliases, environment managers, existing git configuration, and secrets. Never print credentials or API keys in reports.
2. Back up each file **before** editing it, with a timestamp, and maintain a change log and rollback instructions. Preserve file permissions.
3. Make changes idempotently: never append duplicate init lines or reinstall already-correct components.
4. Do not run destructive Homebrew cleanup, remove packages, overwrite unrelated dotfiles, modify SSH configuration, or change global Git identity.
5. Do not install FirstMate, tmux, Nix, or switch terminals. These are outside the scope of this phase. Do not install Cursor or replace a pre-existing IDE without explicit approval.
6. Do not enable dangerous/auto-approve flags for Codex or Claude Code. Preserve current approval/security settings.
7. Prefer official project documentation to blog snippets. Verify the flags, config keys, font names, and theme names against installed tool versions before writing them.
8. If a step requires administrator privileges, an interactive login, or would cause irreversible impact, explain the specific action and pause only for that action. Continue other safe tasks.
9. When modifying Codex/Claude integration hooks, inspect and merge their existing configuration rather than replacing it.
10. For VS Code, merge existing User/Workspace settings and keybindings; do not rewrite extension lists or enable settings sync without asking. Do not automatically change source files or repositories during IDE setup.

## Desired architecture

```text
Ghostty (macOS terminal + Catppuccin Mocha + Nerd Font)
  └── Herdr (workspaces / tabs / panes / agent status)
       └── Zsh + Oh My Zsh (plugin management)
            ├── git plugin
            ├── zsh-autosuggestions
            ├── zsh-syntax-highlighting (loaded last among OMZ plugins)
            └── Starship (prompt only; Catppuccin Powerline)
                 ├── Codex CLI
                 ├── Claude Code (if available)
                 └── shell / git / tests

VS Code (primary IDE; separate app/window)
  ├── Codex extension; optional Claude Code extension
  ├── Python / Pylance / Jupyter / Ruff
  ├── Git diffs and reviews (GitLens optional)
  └── Opens the same repositories / isolated agent worktrees

Cursor (alternative only; leave untouched if already installed)
```

## Phase 0 — Inventory (read-only)

- Detect macOS version, architecture, active shell, Homebrew prefix, PATH, installed executables, font availability.
- Determine whether Ghostty, Herdr, Oh My Zsh, Starship, VS Code, Cursor, Codex, and Claude Code are already installed and check relevant versions.
- Inspect (without revealing secrets) existing config paths and initialization order:
  - `~/.zshrc`, `~/.zprofile`, `~/.zshenv` (if present)
  - `~/.config/ghostty/config.ghostty` or legacy `config`
  - `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` or legacy `config`
  - `~/.config/starship.toml`
  - `~/.config/herdr/config.toml`
  - VS Code User settings, keybindings, installed extensions, and existing `code` CLI availability (read only)
  - coding-agent settings only to the extent needed for Herdr integrations
- Report existing conflicts, especially another Zsh theme/prompt framework, duplicate shell plugins, or multiple Ghostty config locations.

**Checkpoint:** Write a short inventory and propose minimal changes without disrupting existing functionality.

## Phase 1 — Backups and preflight

- Create a timestamped backup location under the user's home directory.
- Back up only files about to be changed; record exact source/destination paths.
- Run baseline shell syntax check and check that existing essential developer commands resolve.
- Use rollback-friendly, small file edits rather than replacing entire existing configs.

## Phase 2 — Core packages and font

Install or verify (skip already-correct installs):

- Ghostty, via Homebrew cask if missing.
- Herdr, via official Homebrew formula if missing.
- Starship, via Homebrew.
- **JetBrains Mono Nerd Font** via Homebrew cask, verifying the family name that Ghostty actually recognizes.
- Prerequisites: `git`, `curl` and Homebrew, without destructive system changes.

Preference: use installed macOS Zsh unless there is a compelling compatibility reason not to. Do not change the account's login shell unnecessarily.

## Phase 3 — Oh My Zsh and plugins

- Install Oh My Zsh using its official installation mechanism if missing; inspect installer and account for its `.zshrc` backup/replace behavior.
- Merge existing shell setup back into the generated config rather than losing PATH, aliases, language managers or other integrations.
- Disable Oh My Zsh's built-in prompt theme: `ZSH_THEME=""`.
- Enable the Oh My Zsh `git` plugin.
- Install `zsh-autosuggestions` and `zsh-syntax-highlighting` using **Oh My Zsh custom plugins**. Do **not** simultaneously source Homebrew copies.
- Ensure `zsh-syntax-highlighting` is the last loaded Oh My Zsh plugin.
- Source Oh My Zsh once and initialize Starship once, after Oh My Zsh.
- Avoid unnecessary plugins and startup overhead.

## Phase 4 — Starship prompt

- Configure the official `catppuccin-powerline` preset, with `catppuccin_mocha` palette.
- Ensure `eval "$(starship init zsh)"` occurs exactly once in `.zshrc`.
- Back up existing Starship config before applying the preset.
- Optimize for readability in narrow Herdr panes; keep a clear Git branch/status and current directory, and avoid excessive prompt modules where feasible.
- Do not show credentials, token counts or private environment values in the prompt.

## Phase 5 — Ghostty settings

Configure the **effective** Ghostty config location based on actual precedence; do not leave conflicting settings in XDG and macOS-specific files.

Desired appearance and behavior:

- Font: JetBrains Mono Nerd Font, around 14 pt.
- Theme: `Catppuccin Mocha` (verify exact installed spelling).
- Cursor: steady bar.
- Clean title bar; modest padding for usable pane space.
- Preserve standard macOS keyboard behavior unless a remapping is demonstrably needed.
- Avoid competing native pane/tab shortcuts; let **Herdr** manage workspaces, tabs and panes.

Validate the configuration with the installed Ghostty version and test reload/startup.

## Phase 6 — Herdr settings and coding-agent integrations

- Use `~/.config/herdr/config.toml` only as needed; merge rather than overwrite.
- Theme: `catppuccin`.
- Preserve or set `terminal.shell_mode = "auto"` and `terminal.new_cwd = "follow"` when compatible.
- Keep Herdr's default `Ctrl+B` prefix unless there is a real conflict.
- Enable notifications only after confirming supported settings; avoid unnecessary notification spam.
- Install Codex and Claude Code integrations **only if those applications are already present** and only after backing up any agent settings files the integration may modify.
- Do not launch multiple agents or create Git worktrees in a real project without an explicit task.
- Do not introduce tmux as another multiplexing layer.

## Phase 7 — Verification and repair

Perform available automated checks and document manual checks:

- Fresh interactive login Zsh starts without errors; Oh My Zsh, all three selected plugins, and Starship are loaded only once.
- Existing PATH, Homebrew commands, Git, coding-agent CLIs and environment managers still work.
- Ghostty uses the intended font and Catppuccin colors, with no glyph rendering issues.
- Herdr launches inside Ghostty; create/switch panes, tabs and workspaces; default keyboard prefix is functional.
- Herdr panes launch the expected Zsh and display the Starship prompt.
- If installed, Codex/Claude can launch from Herdr and their integration reports no setup errors.
- No existing configuration, credentials, projects, Git branches or running agent sessions were unnecessarily changed.

**Required completion report:**

1. Installed vs already-present components and their versions.
2. Files edited, with backup paths and concise diffs.
3. Successful verification results and any skipped/unverifiable GUI tests.
4. Remaining manual steps, if any.
5. Exact rollback commands or procedures.

## Phase 8 — Primary IDE: Visual Studio Code (Cursor optional)

**Decision:** VS Code is the default GUI IDE, while Ghostty + Herdr remain the primary agent execution environment. The IDE is for navigating code, reviewing Git diffs, interactive debugging, notebooks, and selectively editing files. **Do not install Cursor by default.** If Cursor is already installed, leave it intact and report its presence; do not migrate settings between the two IDEs automatically.

### Installation and extension audit

- Detect whether VS Code is installed and where. If absent, install the official stable VS Code build (prefer Homebrew cask `visual-studio-code`, after verifying its availability); do not replace Insiders or another build.
- Verify that the `code` launcher works from a fresh interactive Zsh. If missing, use the documented VS Code “Install 'code' command in PATH” action or an official/safe method; do not overwrite a conflicting executable or silently alter unrelated PATH entries.
- Inspect existing VS Code extensions before installing anything. Install only missing extensions and verify their current publisher/extension IDs from official marketplace listings:
  - **OpenAI Codex** extension (use the official verified publisher; do not guess the identifier).
  - **Python** (Microsoft), **Pylance** (Microsoft), **Jupyter** (Microsoft), **Ruff** (official Astral Software extension).
  - **Catppuccin for VSCode** theme, and set Mocha if not overriding an existing deliberate preference.
  - **GitLens** and **Remote - SSH** are optional; report them as suggestions unless needed or already installed. Remote SSH connection configuration and GPU servers remain outside scope.
  - **Claude Code** extension is optional and should be installed only if the CLI is present and the user wants IDE integration; no extra authentication or billing changes.
- Keep agent execution primarily in Herdr. An IDE extension should not auto-start agents or duplicate ongoing sessions merely because the editor opens.

### Editing and review experience

- Use JetBrains Mono Nerd Font for the editor and integrated terminal when installed. Set a readable editor font size and preserve existing accessibility preferences.
- Keep a single Catppuccin Mocha visual scheme across Ghostty, Starship, Herdr, and VS Code, unless existing VS Code settings are intentionally different.
- Retain built-in Git diff/review capabilities and make it easy to open a specific worktree in its own VS Code window (`code <path>`), without automatically creating, switching, or pruning Git branches/worktrees.
- Enable sensible language-specific format-on-save **only where a formatter is configured and existing workspace/team settings permit it**. Do not impose new global lint/format rules on repositories. For Python prefer Ruff where already adopted, but do not change project-level formatter dependencies.
- Preserve debugger, Python interpreter selection, notebooks, remote profiles, existing extensions, settings sync state, shortcuts and workspace settings.
- Do not copy the entire Cursor configuration into VS Code or vice versa. They are different editors with partially overlapping settings.

### IDE acceptance criteria

1. `code --version` works, and VS Code launches via `code .` from a test directory.
2. Codex extension is available for manual use; no login is performed without user interaction.
3. Python/Pylance/Jupyter/Ruff are installed or preexisting; diagnostic and notebook tooling loads without extension errors.
4. Editor uses the intended font and theme without missing glyphs, where GUI verification is possible.
5. Git diff opens normally and separate worktree folders can be opened without mutating the worktrees.
6. Herdr/Codex CLI sessions keep running independently of VS Code closing; no new conflicting shortcuts, agents, or shell init lines are introduced.
7. Report anything requiring GUI interaction (permissions, sign-in, VS Code `code` command install, manual theme selection) rather than claiming it passed automatically.

## Explicitly deferred (Phase 2, separate request)

- FirstMate or other multi-agent orchestration tools.
- Automatic creation of per-agent Git worktrees and opinionated workflows.
- Nix / nix-darwin / Home Manager migrations.
- Global Codex/Claude permission or approval policy changes.
- Remote SSH connection setup and GPU server development environments.
- Cursor installation, settings migration, or Cursor-specific subscriptions.

## Authoritative references

- Ghostty config: https://ghostty.org/docs/config
- Oh My Zsh: https://github.com/ohmyzsh/ohmyzsh
- Autosuggestions: https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
- Syntax highlighting: https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md
- Starship prompt: https://starship.rs/guide/
- Starship Catppuccin Powerline: https://starship.rs/presets/catppuccin-powerline
- Herdr installation: https://herdr.dev/docs/install/
- Herdr configuration: https://herdr.dev/docs/configuration/
- Herdr integrations: https://herdr.dev/docs/integrations/
- VS Code documentation: https://code.visualstudio.com/docs
- VS Code Python: https://code.visualstudio.com/docs/python/python-tutorial
- VS Code extension marketplace: https://marketplace.visualstudio.com/vscode

## Definition of done

A new Ghostty session can open Herdr, create a pane with a fast and attractive Zsh + Oh My Zsh + Starship prompt, and launch Codex CLI without broken commands, duplicate prompts, conflicting themes, lost settings, or changes to unrelated projects. VS Code launches via `code .`, supports source review/debugging with the intended visual theme and verified development extensions, and works alongside Herdr without taking over agent sessions. Everything changed has a clear backup and recovery path.
