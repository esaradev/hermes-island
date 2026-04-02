# Hermes Island

macOS Dynamic Island notch app for Hermes agents. Monitor sessions, fabric memory, and multi-agent workflows from the menu bar.

Forked from [claude-island](https://github.com/farouqaldori/claude-island) and adapted for the Hermes agent framework.

## What it does

A floating notch overlay at the top of your screen that expands when your Hermes agent is working:

- **Collapsed** -- agent name, green dot when active
- **Expanded** -- current action, tool being used, session status
- **Full view** -- session transcript, tool results, quick actions

## How it works

```
Hermes Agent
  └── hermes_island plugin (installed by the app)
        └── sends events over Unix socket (/tmp/hermes-island.sock)
              └── HermesIsland.app listens and renders notch UI
```

The app installs a Hermes plugin at `~/.hermes/plugins/hermes_island/` on first launch. The plugin hooks into `on_session_start`, `pre_tool_call`, `post_tool_call`, `post_llm_call`, and `on_session_end` to send real-time events to the notch.

When the Icarus memory plugin is also loaded, the notch also shows fabric write/recall events.

## Install

1. Build from source:
```bash
git clone https://github.com/esaradev/hermes-island.git
cd hermes-island
xcodebuild -scheme HermesIsland -configuration Release build
```

2. Or download from releases (when available).

3. Launch the app. It auto-installs the Hermes plugin.

4. Start Hermes in a terminal:
```bash
hermes chat
```

The notch should expand when the session starts and show tool activity.

## Requirements

- macOS 15.0+
- [Hermes](https://github.com/NousResearch/hermes-agent) v0.5.0+
- Xcode 16+ (for building from source)

## License

MIT (see LICENSE.md)
