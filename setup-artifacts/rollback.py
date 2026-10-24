#!/usr/bin/env python3
"""Restore backed-up files; move newly created files aside without deleting them."""
from pathlib import Path
import datetime, json, shutil, sys
backup = Path(sys.argv[1]).expanduser().resolve()
suffix = '.before-rollback-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
for item in reversed(json.loads((backup/'manifest.json').read_text())):
    dest = Path(item['path'])
    if dest.exists():
        shutil.move(str(dest), str(dest)+suffix)
    if item['backup']:
        shutil.copy2(item['backup'], dest)
    print('Restored prior state:', dest)
print('Installed packages/extensions are retained. Start a fresh shell; reload Ghostty and Herdr.')
