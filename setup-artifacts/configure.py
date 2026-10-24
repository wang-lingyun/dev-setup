#!/usr/bin/env python3
"""Apply the inspected, minimal configuration, recording reversible file changes."""
from pathlib import Path
import datetime, difflib, json, os, shutil, subprocess

home = Path.home()
root = Path(__file__).resolve().parent
backup = home / 'dev-setup-backups' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup.mkdir(parents=True, mode=0o700)
changes = []
diffs = []

def write(rel, content):
    dest = home / rel
    old = dest.read_text() if dest.exists() else ''
    if dest.exists() and old == content:
        return
    saved = backup / rel if dest.exists() else None
    if saved:
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, saved)
    changes.append({'path': str(dest), 'backup': str(saved) if saved else None})
    # Persist the manifest before changing the file, including on partial failure.
    (backup / 'manifest.json').write_text(json.dumps(changes, indent=2)+'\n')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)
    if not saved:
        dest.chmod(0o644)
    diffs.extend(difflib.unified_diff(old.splitlines(True), content.splitlines(True), fromfile=rel+' (before)', tofile=rel+' (after)'))

zshrc = home / '.zshrc'
block = '''# BEGIN dev-setup managed shell
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source "$ZSH/oh-my-zsh.sh"
eval "$(starship init zsh)"
# END dev-setup managed shell
'''
if zshrc.exists() and zshrc.read_text() != block:
    raise SystemExit('Unexpected .zshrc appeared after inventory; refusing to replace it.')
write('.zshrc', block)

preset = subprocess.check_output(['starship','preset','catppuccin-powerline'], text=True)
# Keep the official preset, shorten directory/branch display for narrower panes.
preset = preset.replace('truncation_length = 3', 'truncation_length = 2')
preset = preset.replace('[git_branch]\n', '[git_branch]\ntruncation_length = 24\n')
preset = preset.replace('show_always = true', 'show_always = false')
assert "palette = 'catppuccin_mocha'" in preset or 'palette = "catppuccin_mocha"' in preset
write('.config/starship.toml', preset)

ghostrel = 'Library/Application Support/com.mitchellh.ghostty/config.ghostty'
ghost = (home / ghostrel).read_text()
settings = '''# BEGIN dev-setup appearance
font-family = JetBrainsMono Nerd Font Mono
font-size = 14
theme = Catppuccin Mocha
cursor-style = bar
cursor-style-blink = false
window-padding-x = 8
window-padding-y = 6
macos-titlebar-style = transparent
# END dev-setup appearance
'''
if '# BEGIN dev-setup appearance' not in ghost:
    write(ghostrel, ghost + settings)

herdrel = '.config/herdr/config.toml'
herd = (home / herdrel).read_text()
if '[theme]' not in herd and '[terminal]' not in herd:
    write(herdrel, herd.rstrip()+'''\n\n[theme]
name = "catppuccin"

[terminal]
shell_mode = "auto"
new_cwd = "follow"
''')

vscode = 'Library/Application Support/Code/User/settings.json'
if (home / vscode).exists():
    raise SystemExit('VS Code settings appeared since inventory; inspect before merging JSONC.')
write(vscode, json.dumps({
    'workbench.colorTheme': 'Catppuccin Mocha',
    'editor.fontFamily': "'JetBrainsMono Nerd Font Mono', Menlo, Monaco, monospace",
    'editor.fontSize': 14,
    'terminal.integrated.fontFamily': 'JetBrainsMono Nerd Font Mono',
    'terminal.integrated.fontSize': 14,
}, indent=2)+'\n')

(backup / 'changes.diff').write_text(''.join(diffs))
(root / 'backup-location.txt').write_text(str(backup)+'\n')
print('Backups and manifest:', backup)
for change in changes:
    print('Configured:', change['path'])
