# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Browser games built with vanilla HTML5 Canvas and JavaScript. Each game is a single self-contained `.html` file — no build tools, no dependencies, no server needed. All files run directly from `file://` in Chrome.

## Running

Open any `.html` file in Chrome (double-click or `start chrome <file>`). No build step.

## Architecture

- **tictactoe.html** — 2-player Tic-Tac-Toe with score tracking. Pure DOM-based (no canvas).
- **shooter.html** — Top-down retro shooter using HTML5 Canvas 2D API. Organized into 10 labeled sections within a single `<script>` block:
  1. Constants & config (canvas size, colors, enemy type definitions, level table)
  2. Input handler (keyboard state + mouse position/click tracking)
  3. Utility functions (math helpers, shuffle, edge spawning)
  4. Sprite drawing functions (all visuals drawn procedurally with `fillRect`/`arc` — no image assets)
  5. Entity classes: `Particle`, `Bullet`, `Enemy`, `Player`
  6. `WaveManager` class (level progression, spawn queue, difficulty scaling)
  7. Screen renderers (menu, HUD, level complete, game over)
  8. Collision detection (circle-circle) and screen shake
  9. Game state machine (`MENU → PLAYING → LEVEL_COMPLETE → GAME_OVER`) and main loop
  10. Bootstrap (`requestAnimationFrame` game loop)

## Key Conventions

- All sprites are drawn with canvas 2D calls — never reference external image files.
- Every draw function that changes ctx state must use `ctx.save()`/`ctx.restore()`.
- Always reset `ctx.shadowBlur = 0` after glow draws to avoid performance issues.
- Delta time is capped at 50ms to prevent teleporting when a tab is backgrounded.
- Entity arrays are cleaned up via `.filter()` at the end of `update()`, never during iteration.

## Git Workflow

Repository: https://github.com/kegoro/claude-code-games (remote `origin`, branch `master`).

**After completing every task or meaningful code change, you must:**
1. Stage the relevant files (`git add <files>` — never `git add .` blindly).
2. Write a clean commit message: imperative mood, short subject line, brief body if needed.
3. Push immediately: `git push origin master`.

This is non-negotiable — every session's work must be preserved on GitHub so progress is never lost and any change can be reverted. Do not batch up multiple features into one commit; commit at each logical checkpoint.
