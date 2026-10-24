# Development environment setup — 2026-10-24

Configuration and command-line validation completed on macOS 26.6.2, Apple Silicon. Visual acceptance checks remain below.

## Components

| Component | Result |
| --- | --- |
| Ghostty 1.3.1 | Already installed; configured |
| Herdr 0.9.5 | Already installed and running; reloaded without restart |
| Codex CLI 0.164.0 | Already installed; approval settings untouched |
| VS Code 1.136.1 arm64 | Already installed; `code` works |
| Starship 1.27.0 | Installed through Homebrew |
| JetBrains Mono Nerd Font 3.5.1 | Installed through Homebrew; detected family: `JetBrainsMono Nerd Font Mono` |
| Oh My Zsh | Installed from official installer; commit `2100c63` |
| zsh-autosuggestions | Installed in OMZ custom plugins; commit `85919cd` |
| zsh-syntax-highlighting | Installed in OMZ custom plugins; commit `e6683f2` |
| Git 2.39.5, Node 26.4.0 | Existing commands still resolve |
| Claude Code / Cursor | Not detected; not installed |

VS Code extensions installed: `openai.chatgpt@26.1021.22027`, `ms-python.python@2026.10.0`, `ms-python.vscode-pylance@2026.4.1`, `ms-toolsai.jupyter@2025.9.1`, `charliermarsh.ruff@2026.90.0`, `catppuccin.catppuccin-vsc@3.19.0`. The marketplace also installed their dependencies: Codex Audio, Python Debugger, Python Environments, Jupyter Keymap/Renderers/Cell Tags/Slideshow. No previous extensions were present. GitLens and Remote SSH remain optional and were not installed.

## Files and backups

Backup root: `/Users/wanglingyun/dev-setup-backups/20261024-142012` (private directory). `manifest.json` records exact source and backup paths. `changes.diff` records the configuration additions. Files absent before setup are recorded with a null backup.

| File relative to home | Change | Previous state / backup relative to backup root |
| --- | --- | --- |
| `.zshrc` | OMZ, empty OMZ theme, git/autosuggestions/highlighting plugins, then Starship | New file |
| `.config/starship.toml` | Official Catppuccin Powerline/Mocha preset; directory shortened to 2 components, branch truncated to 24 characters, username shown only when needed | New file |
| `Library/Application Support/com.mitchellh.ghostty/config.ghostty` | Detected Nerd Font family, 14 pt, Catppuccin Mocha, steady bar cursor, 8×6 padding, transparent titlebar | Same relative path under backup root; originally empty |
| `.config/herdr/config.toml` | Preserved `onboarding = false`; added Catppuccin theme and auto shell/follow CWD | `.config/herdr/config.toml` |
| `Library/Application Support/Code/User/settings.json` | Mocha theme, detected font for editor/terminal, 14 pt | New file |

The font family was corrected after detection; timestamped pre-repair copies are in `before-font-repair/` under the same backup root. Existing file permissions were preserved. `.zprofile` and its Homebrew initialization were left intact. No duplicate Ghostty config location was found. No keybindings, global formatting rules, source files in other repositories, Git identity, SSH configuration, credentials, login shell, or agent approval policies were changed.

New directories include `~/.oh-my-zsh` and its plugins, Starship configuration, the installed fonts and extensions, plus normal tool caches. Installation helpers and downloaded official instructions are retained in `setup-artifacts/`. Helpers refuse unexpected pre-existing configuration rather than overwriting it.

## Verification

- Fresh interactive login Zsh starts successfully outside the restricted sandbox; `zsh -n ~/.zshrc` passes.
- Plugin list is exactly git, zsh-autosuggestions, zsh-syntax-highlighting, in that order. Both external plugin functions are loaded. OMZ and Starship each have one initialization line; one `prompt_starship_precmd` hook is registered.
- Homebrew, Git, Node, Codex, Herdr, Starship and VS Code remain available on PATH.
- Starship renders its prompt without configuration errors.
- Ghostty `+validate-config` passes; `+show-config` confirms the font, theme, size, cursor and padding. `+list-fonts` confirms the exact installed font family.
- Herdr reload returned `diagnostics: []`, status applied. Server remains running, endpoint and protocol compatible. Existing Codex integration is current v10 and required no modifications.
- VS Code lists all requested extensions. Installed theme metadata confirms `Catppuccin Mocha`. `code --version` passes in a login shell. `code --new-window /private/tmp/dev-setup-ide-check` returned successfully.
- No coding agents were launched and no project worktrees were created. Existing Herdr sessions were not restarted.

## Remaining visual checks

Computer access to Ghostty was blocked by the computer-use tool; VS Code UI inspection timed out. Therefore actual glyph rendering, keyboard handling, extension activation, notebook diagnostics, Git diff UI, and window-close/session persistence are not claimed as verified.

1. In Ghostty reload configuration with Command+Shift+comma, or use its menu. A new window picks up the titlebar setting. Open a fresh shell for the new prompt.
2. From a shell outside Herdr, run `herdr` to attach. If already inside Herdr, open a new pane instead. Use the mouse/right-click menus first; Ctrl+B then `v` splits right, `-` splits down, `c` adds a tab, `?` shows help, `q` detaches. Check fonts, pane switching and the new prompt. Existing panes keep their old shell until you open a fresh shell.
3. In VS Code, reload the window if required and check Mocha/font appearance. Open Codex manually and sign in yourself if requested. Check Python/notebook tooling in a suitable project environment; no interpreter or project dependencies were changed.
4. Check a Git diff in an existing repository when convenient. No real repository was opened or mutated for this test.

## Rollback

From this workspace:

```sh
python3 setup-artifacts/rollback.py /Users/wanglingyun/dev-setup-backups/20261024-142012
```

The rollback restores backed-up files with their original metadata. Newly created configuration files, and current versions of restored files, are moved aside with a timestamp instead of deleted. Reload Ghostty, run `herdr server reload-config`, reload VS Code and open a fresh shell afterwards. This command needs home-directory write access if executed by a sandboxed agent.

Packages, fonts, OMZ and extensions are intentionally retained during config rollback. For a complete uninstall, first restore configuration, then explicitly uninstall the six listed extensions and their listed dependencies through VS Code (all were absent before setup), and run `brew uninstall starship` and `brew uninstall --cask font-jetbrains-mono-nerd-font`. Move `~/.oh-my-zsh` to a timestamped archive if no longer wanted. Do not uninstall pre-existing Ghostty, Herdr, Codex, VS Code, Git or Node. No Homebrew cleanup is necessary.

## Official references used

- [Ghostty configuration](https://ghostty.org/docs/config)
- [Herdr configuration](https://herdr.dev/docs/configuration/) and [integrations](https://herdr.dev/docs/integrations/)
- [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)
- [Starship Catppuccin Powerline](https://starship.rs/presets/catppuccin-powerline)
- [Codex IDE documentation](https://learn.chatgpt.com/docs/ide) and [official marketplace extension](https://marketplace.visualstudio.com/items?itemName=OpenAI.chatgpt)
- Official marketplace listings for [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [Pylance](https://marketplace.visualstudio.com/items/?itemName=ms-python.vscode-pylance), [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter), [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff), and [Catppuccin](https://marketplace.visualstudio.com/items?itemName=Catppuccin.catppuccin-vsc)
