"""
Hermes Island Bridge Plugin
============================

Sends agent session events to the Hermes Island macOS notch app
over a Unix domain socket at /tmp/hermes-island.sock.

Events:
  on_session_start  -> {event: "session_start", agent, platform, session_id}
  pre_tool_call     -> {event: "running_tool", tool, session_id}
  post_tool_call    -> {event: "tool_complete", tool, result_preview, session_id}
  post_llm_call     -> {event: "processing", agent, session_id}
  on_session_end    -> {event: "session_end", agent, session_id}

Also detects Icarus fabric events when the Icarus plugin is loaded:
  fabric_write      -> {event: "fabric_write", agent, type, summary}
  fabric_recall     -> {event: "fabric_recall", count}
"""

import json
import logging
import os
import socket

logger = logging.getLogger(__name__)

SOCKET_PATH = "/tmp/hermes-island.sock"
AGENT_NAME = os.environ.get("HERMES_AGENT_NAME", "agent")


def _send(payload: dict):
    """Send a JSON event to the Hermes Island app. Fails silently."""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        sock.connect(SOCKET_PATH)
        data = json.dumps(payload).encode("utf-8")
        sock.sendall(data + b"\n")
        sock.close()
    except (ConnectionRefusedError, FileNotFoundError, OSError):
        pass  # app not running, silently ignore
    except Exception as exc:
        logger.debug("hermes-island: send failed: %s", exc)


def _on_session_start(session_id="", platform="", **kwargs):
    _send({
        "event": "SessionStart",
        "session_id": session_id,
        "status": "waiting_for_input",
        "agent": AGENT_NAME,
        "platform": platform or "cli",
    })


def _on_pre_tool_call(tool_name="", args=None, task_id="", **kwargs):
    _send({
        "event": "PreToolUse",
        "session_id": task_id,
        "status": "running_tool",
        "tool": tool_name,
        "agent": AGENT_NAME,
    })
    # detect Icarus fabric tools
    if tool_name == "fabric_recall":
        _send({
            "event": "Notification",
            "session_id": task_id,
            "notification_type": "fabric_recall",
            "message": "searching memory...",
            "agent": AGENT_NAME,
        })


def _on_post_tool_call(tool_name="", args=None, result="", task_id="", **kwargs):
    result_str = str(result)[:100] if result else ""
    _send({
        "event": "PostToolUse",
        "session_id": task_id,
        "status": "processing",
        "tool": tool_name,
        "agent": AGENT_NAME,
        "message": result_str,
    })
    # detect Icarus fabric writes
    if tool_name == "fabric_write" and result:
        try:
            r = json.loads(result) if isinstance(result, str) else result
            if r.get("status") == "written":
                _send({
                    "event": "Notification",
                    "session_id": task_id,
                    "notification_type": "fabric_write",
                    "message": f"wrote: {os.path.basename(r.get('path', ''))}",
                    "agent": AGENT_NAME,
                })
        except (json.JSONDecodeError, TypeError):
            pass


def _on_post_llm_call(session_id="", user_message="", assistant_response="", platform="", **kwargs):
    summary = (assistant_response or "")[:80].replace("\n", " ")
    _send({
        "event": "PostToolUse",
        "session_id": session_id,
        "status": "processing",
        "agent": AGENT_NAME,
        "message": summary,
    })


def _on_session_end(session_id="", platform="", completed=False, **kwargs):
    _send({
        "event": "SessionEnd",
        "session_id": session_id,
        "status": "ended",
        "agent": AGENT_NAME,
    })


def register(ctx):
    ctx.register_hook("on_session_start", _on_session_start)
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("post_llm_call", _on_post_llm_call)
    ctx.register_hook("on_session_end", _on_session_end)
    logger.info("hermes-island bridge plugin registered")
