# Status Line — Configuration & Customization Guide

**Last Updated:** 2026-04-04  
**Purpose:** Manage, modify, and restore the custom status line for the terminal  
**Backup:** `G:\My Drive\AITools\claude-code-backup\statusline\`

---

## Table of Contents

1. [Overview](#overview)
2. [File Locations](#file-locations)
3. [Architecture](#architecture)
4. [JSON Input Fields](#json-input-fields)
5. [Display Layout](#display-layout)
6. [Themes](#themes)
7. [Adding a Process Animation](#adding-a-process-animation)
8. [Adding a Model](#adding-a-model)
9. [Escalation Patterns](#escalation-patterns)
10. [Design Constraints](#design-constraints)
11. [Restore from Backup](#restore-from-backup)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The status line is a two-line bash script that renders live context in the terminal footer. It shows context window usage, token counts, rate limits, model, git branch state, active process animations, and more.

It runs as a `"type": "command"` status line — the terminal pipes a JSON blob to stdin on every tick, and the script prints two lines of ANSI-colored output.

### Dependencies

| Dependency | Why |
|-----------|-----|
| `python3` | JSON parsing (jq not available on this Windows system) |
| `git` | Branch, ahead/behind, dirty file count |
| `ps` | Process detection for animations |
| `awk` | Token abbreviation (1000 → 1.0k) |
| `sed` | Short CWD extraction |

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| Settings | `~/.claude/settings.json` | Contains `statusLine` config entry |
| Active script | `~/.claude/statusline-command.sh` | The running status line script |
| Backup (Google Drive) | `G:\My Drive\AITools\claude-code-backup\statusline\` | Full backup with README |

### Settings entry

The `statusLine` key in `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

---

## Architecture

```
Terminal tick
  │
  ├── pipes JSON blob to stdin
  │
  └── statusline-command.sh
        │
        ├── 1. python3 parses ALL JSON fields in one call → shell vars
        ├── 2. git commands for branch / ahead-behind / dirty count
        ├── 3. ps for process detection → animated emoji
        ├── 4. Assemble line1[] and line2[] arrays
        └── 5. Print two lines with ANSI colors
```

### Performance notes

- **Single python3 call** parses every JSON field at once (not one per field)
- **Single ps call** feeds all process detection checks
- Git uses `--no-optional-locks` to avoid blocking other git operations
- No subshells in the hot path after initial parsing

---

## JSON Input Fields

The terminal provides this JSON blob on stdin each tick. The script extracts:

| Shell Variable | JSON Path | Example |
|---------------|-----------|---------|
| `model` | `model.display_name` | `"Opus 4.6"` |
| `model_id` | `model.id` | `"claude-opus-4-6"` |
| `agent_name` | `agent.name` | `"HUEY"` |
| `cwd` | `workspace.current_dir` | `"C:\\projects\\bphc-gam2010"` |
| `worktree_branch` | `worktree.branch` | `"agent-abc123"` |
| `used_pct` | `context_window.used_percentage` | `42.5` |
| `total_input` | `context_window.total_input_tokens` | `150000` |
| `total_output` | `context_window.total_output_tokens` | `25000` |
| `cache_read` | `context_window.current_usage.cache_read_input_tokens` | `80000` |
| `cache_write` | `context_window.current_usage.cache_creation_input_tokens` | `5000` |
| `five_hr` | `rate_limits.five_hour.used_percentage` | `15.2` |
| `seven_day` | `rate_limits.seven_day.used_percentage` | `8.0` |
| `output_style` | `output_style.name` | `"concise"` |
| `session_name` | `session_name` | `"team build"` |
| `vim_mode` | `vim.mode` | `"NORMAL"` |

---

## Display Layout

### Line 1

```
[vim] | context% | tokens | rate limits | model | agent | branch sync dirty | folder | session
```

| Segment | Condition | Example |
|---------|-----------|---------|
| Vim mode | Only when vim enabled | `⌨️ [N]` or `✏️ [I]` |
| Context % | Always (shows remaining) | `🫧 72%` |
| Tokens | When > 0 | `🔋 45.2k` |
| Rate limits | When present | `💧 5h: 12%` |
| Model | Always | `👾 O4.6` |
| Agent | When subagent active | `🧠 HUEY` |
| Branch | When in git repo | `🌿 dev/DME/feature/anthony 🐾 ⬆ 3 📝 5` |
| Folder | Always | `📁 bphc-gam2010` |
| Session | When named | `💬 "team build"` |

### Line 2

```
active process animation | output style
```

Only appears when a detected process is running or output style is non-default.

---

## Themes

Two themes exist. The active theme is in `statusline-command.sh`.

### Robot/Alien Theme (current)

| Model | Emoji | Metaphor |
|-------|-------|----------|
| Opus | 👾 | Space invader boss — big & powerful |
| Sonnet | 🤖 | Robot — smart & fast |
| Haiku | 🛸 | UFO — small & quick |
| Unknown | 🦾 | Robot arm |

Context escalation: 🫧 bubbles → 🦑 squid → ⚙️ gears → 🚨 alarm
Tokens escalation: ✨ sparkle → 🔋 battery → 🛰️ satellite → 👽 alien → 🔩 bolt → 🔌 plug → 🏭 factory

### Animal Theme (backup file)

| Model | Emoji | Metaphor |
|-------|-------|----------|
| Opus | 🦁 | Lion — big & powerful |
| Sonnet | 🐬 | Dolphin — smart & fast |
| Haiku | 🐇 | Rabbit — small & quick |
| Unknown | 🤖 | Robot |

Context escalation: 🐋 whale → 🐈 cat → 🦔 hedgehog → 🐡 pufferfish
Tokens escalation: 🌱 seedling → 🐭 mouse → 🐇 rabbit → 🦊 fox → 🐺 wolf → 🦁 lion → 🐘 elephant

### Switching themes

Copy the desired backup over the active script:

```bash
cp ~/.claude/statusline-command.backup-*.sh ~/.claude/statusline-command.sh
```

Or swap:

```bash
# Save current as backup
cp ~/.claude/statusline-command.sh ~/.claude/statusline-command.backup-$(date +%Y%m%d-%H%M%S).sh
# Restore old theme
cp ~/.claude/statusline-command.backup-20260403-111009.sh ~/.claude/statusline-command.sh
```

---

## Adding a Process Animation

Process animations detect running commands via `ps` output and show an animated emoji sequence cycling every second (4 frames).

### Template

Add a new `elif` block in the process detection section (after the existing blocks, before the `fi`):

```bash
elif detect_proc "my-command\|my-other-command"; then
  # 🎯 Description — metaphor
  case $frame in
    0) active_anim="$(printf '\033[0;36m🎯 · · · Working...\033[0m')" ;;
    1) active_anim="$(printf '\033[0;36m· 🎯 · · Working...\033[0m')" ;;
    2) active_anim="$(printf '\033[0;36m· · 🎯 · Working...\033[0m')" ;;
    3) active_anim="$(printf '\033[0;36m· · · 🎯 Working...\033[0m')" ;;
  esac
```

### Rules

- `detect_proc` uses `grep -qi` — patterns are case-insensitive
- Use `\|` for OR within one pattern string (grep basic regex)
- Order matters — more specific patterns must come before general ones (e.g., `sf.*deploy.*destructive` before `sf project deploy`)
- ANSI color codes: `\033[0;36m` = cyan, `\033[0;33m` = yellow, `\033[0;35m` = magenta, `\033[1;35m` = bold magenta, `\033[0;90m` = dim gray
- Always end with `\033[0m` to reset color
- Use protanopia-safe colors only (cyan/yellow/magenta — never red/green alone)

### Existing animations

| Process | Pattern | Emoji | Metaphor |
|---------|---------|-------|----------|
| Destructive deploy | `sf.*deploy.*destructive` | 🐉 | Dragon fire |
| SF deploy | `sf project deploy` | 🚀 | Rocket launch |
| SF retrieve | `sf project retrieve` | 🎣 | Fishing |
| Apex tests | `sf apex run test` | 🐹 | Hamster wheel |
| Playwright E2E | `playwright` | 🦉 | Owl patrol |
| Jest tests | `jest\|npm test` | 🐁 | Mouse in maze |
| ESLint | `eslint` | 🐱 | Cat grooming |
| Prettier | `prettier` | 🐱 | Cat grooming (sparkle) |
| Git push | `git push` | 🕊️ | Carrier pigeon outbound |
| Git pull/fetch | `git pull\|git fetch` | 🕊️ | Carrier pigeon inbound |
| npm install | `npm install\|yarn\|pnpm` | 🐜 | Ant carrying packages |
| Build (webpack/vite) | `webpack\|vite\|npm run build` | 🦫 | Beaver at work |
| Python script | `python3\|python ` | 🐍 | Snake |
| Sleep (test) | `sleep` | 🐸 | Frog (remove after testing) |

---

## Adding a Model

When a new model is released, update two sections:

### 1. Model emoji (robot/alien theme)

```bash
case "$model_lower" in
  *opus*)   model_emoji="👾" ;;
  *sonnet*) model_emoji="🤖" ;;
  *haiku*)  model_emoji="🛸" ;;
  *NEW*)    model_emoji="🎯" ;;   # add here
  *)        model_emoji="🦾" ;;
esac
```

### 2. Model short name

```bash
case "$model_id_lower" in
  *claude-sonnet-4-6*) model_short="S4.6" ;;
  *claude-opus-4-6*)   model_short="O4.6" ;;
  *claude-NEW-X-Y*)    model_short="N.X.Y" ;;   # add here
  *)                   model_short="$model" ;;
esac
```

Short name convention: first letter of model family + version (e.g., `S4.6`, `O4.6`, `H4.5`).

---

## Escalation Patterns

Escalation means the emoji/color changes as a value approaches a threshold, so you can read severity at a glance without relying on color alone.

### Pattern template

```bash
if [ "$value" -ge HIGH_THRESHOLD ]; then
  # Bold magenta + alarming emoji — critical
elif [ "$value" -ge MID_THRESHOLD ]; then
  # Yellow + cautious emoji — warning
else
  # Cyan or dim gray + calm emoji — normal
fi
```

### Current thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Context used | < 40% | 40-59% | 60-79% / 80%+ |
| Rate limit 5h | < 50% | 50-79% | 80%+ |
| Dirty files | < 10 | 10-19 | 20+ |
| Commits ahead | < 5 | 5-9 | 10+ |
| Commits behind | < 5 | 5-9 | 10+ |

---

## Design Constraints

These are non-negotiable:

- **Protanopia-safe palette:** Cyan (`\033[0;36m`), yellow (`\033[0;33m`), magenta (`\033[0;35m`), dim gray (`\033[0;90m`). Never use red/green as the sole status indicator.
- **Emoji + text:** Every status level uses both an emoji AND color — never color alone.
- **Two lines max:** Line 1 is always shown. Line 2 is conditional (only when a process is running or output style is set).
- **Performance:** One python3 call, one ps call. No repeated subshells. Git uses `--no-optional-locks`.
- **No jq dependency:** This Windows system doesn't have jq. Use python3 for JSON.

---

## Restore from Backup

### From Google Drive

```bash
# Copy script
cp "G:/My Drive/AITools/claude-code-backup/statusline/statusline-command.sh" ~/.claude/statusline-command.sh
chmod +x ~/.claude/statusline-command.sh

# Merge statusLine key into settings (read the backup settings.json and add the statusLine entry)
# The key entry to add to ~/.claude/settings.json:
# "statusLine": { "type": "command", "command": "bash ~/.claude/statusline-command.sh" }
```

### From scratch (if backup lost)

1. Create `~/.claude/statusline-command.sh` with the script content
2. Add `statusLine` key to `~/.claude/settings.json`
3. Restart the session

### Verify

```bash
# Syntax check
bash -n ~/.claude/statusline-command.sh

# Smoke test with dummy JSON
echo '{"model":{"display_name":"Sonnet 4.6","id":"claude-sonnet-4-6"},"context_window":{"used_percentage":35}}' | bash ~/.claude/statusline-command.sh
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No status line at all | Missing `statusLine` key in settings.json | Add the JSON key and restart |
| Blank status line | python3 not on PATH | Check `which python3` — install or alias |
| Git info missing | Not in a git repo, or cwd not parsed | Check the `cwd` field in JSON input |
| Animation not showing | Process pattern doesn't match | Test: `ps -eo args \| grep -i "your-pattern"` |
| Garbled colors | Terminal doesn't support ANSI | Use a modern terminal (Windows Terminal, iTerm2) |
| Slow rendering | Too many git calls | Already optimized — check if python3 is slow to start |

---

## Backup Schedule

After making changes to the status line, back up to Google Drive:

```bash
cp ~/.claude/statusline-command.sh "G:/My Drive/AITools/claude-code-backup/statusline/statusline-command.sh"
```

Keep the backup README current if the architecture changes.
