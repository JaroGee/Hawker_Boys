#!/usr/bin/env bash
set -euo pipefail

echo "=== Intel macOS Node setup ==="
echo "arch: $(uname -m)"

# 1) Backup and sanitize ~/.zshrc to remove curly-quote PATH lines and node@18 hacks
ZRC="$HOME/.zshrc"
if [ -f "$ZRC" ]; then
  cp "$ZRC" "${ZRC}.before-node-fix.bak"
  # Remove lines containing node@18 or smart quotes
  awk 'index($0,"node@18")==0 && index($0,"“")==0 && index($0,"”")==0 {print}' "$ZRC" > "${ZRC}.tmp"
  mv "${ZRC}.tmp" "$ZRC"
fi

# 2) Install nvm if missing
if [ ! -d "$HOME/.nvm" ]; then
  echo "Installing nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi

# 3) Ensure zsh loads nvm on every shell
if ! grep -q 'NVM_DIR' "$ZRC" 2>/dev/null; then
  cat >> "$ZRC" <<'ZSHRC'
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
ZSHRC
fi

# 4) Load nvm now
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# 5) Install Node 20 LTS and set default
nvm install 20
nvm alias default 20
nvm use 20

node -v
npm -v

# 6) Remove Homebrew node@18 if present to avoid PATH confusion
if brew list --versions node@18 >/dev/null 2>&1; then
  brew uninstall node@18 || true
fi

# 7) Harden npm for flaky networks
npm config set fetch-timeout 600000
npm config set fetch-retry-maxtimeout 120000

# 8) Add .nvmrc in repo root
cd "$(git rev-parse --show-toplevel)"
echo "20" > .nvmrc

# 9) Reinstall frontend deps
TARGET="."
if [ -f frontend/package.json ]; then
  TARGET="frontend"
fi
if [ -f "$TARGET/package.json" ]; then
  echo "Installing npm deps in $TARGET ..."
  cd "$TARGET"
  rm -rf node_modules package-lock.json pnpm-lock.yaml yarn.lock 2>/dev/null || true
  corepack enable || true
  npm install
  echo "Deps installed."
else
  echo "No package.json found in repo root or ./frontend. Skipping npm install."
fi

echo "=== Done. Open a new shell or run: source ~/.zshrc ==="
