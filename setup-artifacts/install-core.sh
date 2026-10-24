#!/bin/bash
set -euo pipefail
export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1
brew list --versions starship >/dev/null 2>&1 || brew install starship
brew list --cask font-jetbrains-mono-nerd-font >/dev/null 2>&1 || brew install --cask font-jetbrains-mono-nerd-font
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  # KEEP_ZSHRC only preserves an existing file; ZSH points to the normal install path.
  # Stage an empty config separately so the official installer cannot create a theme config.
  mkdir -p /private/tmp/dev-setup-omz-zdot
  touch /private/tmp/dev-setup-omz-zdot/.zshrc
  ZDOTDIR=/private/tmp/dev-setup-omz-zdot ZSH="$HOME/.oh-my-zsh" KEEP_ZSHRC=yes CHSH=no RUNZSH=no sh setup-artifacts/omz-install.sh --unattended --keep-zshrc
fi
for plugin in zsh-autosuggestions zsh-syntax-highlighting; do
  target="$HOME/.oh-my-zsh/custom/plugins/$plugin"
  [ -d "$target" ] || git clone --depth=1 "https://github.com/zsh-users/$plugin.git" "$target"
done
starship --version
ghostty +list-fonts | rg 'JetBrainsMono Nerd Font' | head -8
ghostty +list-themes | rg -i catppuccin
