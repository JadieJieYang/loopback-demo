"""
Builds the Block Kit representation of a task card.
Card anatomy mirrors Diagram 3 — every state shows the same fields
so reviewers always know what's happening and who acts next:

  Task #[ID]
  [Question]
  ──────────
  Owner: [who's responsible]   [X min ago]
  [Next action note]
  Status: [label]
"""

import json
import time
from typing import Any, Optional

STATUS_LABELS = {
    "draft": "Draft",
    "ai_searching": "Searching",
    "human_working": "Waiting on a teammate",
    "pending_confirm": "Waiting on you to confirm",
    "verified": "Verified ✓",
    "unconfirmed": "Suggested, not yet verified",
    "escalate": "Escalated",
}

# Who is responsible at each state (mirrors Diagram 3 Status × Owner Mapping)
_OWNERS = {
    "draft": "—",
    "ai_searching": "Mira AI",
    "human_working": "Resolver",
    "pending_confirm": None,   # filled dynamically from asker_id
    "verified": "—",
    "unconfirmed": "—",
    "escalate": "Resolver",
}

# What happens next at each state (mirrors Diagram 3 action notes)
_NEXT_ACTIONS = {
    "draft": "Task created from a new question",
    "ai_searching": "No human intervention needed yet",
    "human_working": "Teammate is replying in the thread — Mira is listening",
    "pending_confirm": "Confirm whether this answer resolved your issue",
    "verified": "Verified answer — ready for reuse in the Knowledge Vault",
    "unconfirmed": "Suggested answer — waiting for the next person to confirm",
    "escalate": "New answer in progress — previous answer preserved in history",
}

_ANSWER_PREVIEW_LIMIT = 280


def build_task_card(
    question_text: str,
    status: str = "draft",
    results: Optional[list[dict[str, Any]]] = None,
    thread_ts: Optional[str] = None,
    asker_id: Optional[str] = None,
) -> list[dict]:
    status_label = STATUS_LABELS.get(status, status)
    task_id = _task_id(thread_ts)
    time_ago = _relative_time(thread_ts)

    owner = _OWNERS.get(status, "—")
    if status == "pending_confirm":
        owner = f"<@{asker_id}>" if asker_id else "Requester"

    next_action = _NEXT_ACTIONS.get(status, "")

    blocks: list[dict] = [
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"*{task_id}*"}],
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{question_text}*"},
        },
        {"type": "divider"},
    ]

    # Answer content for states that surface a result
    if status == "pending_confirm" and results:
        blocks.extend(_pending_confirm_blocks(results[0], thread_ts, asker_id))
        blocks.append({"type": "divider"})
    elif status == "verified" and results:
        blocks.extend(_verified_blocks(results[0]))
        blocks.append({"type": "divider"})
    elif status == "unconfirmed" and results:
        blocks.extend(_unconfirmed_blocks(results[0]))
        blocks.append({"type": "divider"})

    # Metadata row: owner (left) + time (right)
    blocks.append({
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": f"*Owner*\n{owner}"},
            {"type": "mrkdwn", "text": f"*{time_ago}*"},
        ],
    })

    # Next action note
    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": next_action}],
    })

    # Status footer
    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": f"Status: *{status_label}*"}],
    })

    return blocks


# ── helpers ──────────────────────────────────────────────────────────────────

def _task_id(thread_ts: Optional[str]) -> str:
    if not thread_ts:
        return "#----"
    return f"#{thread_ts.split('.')[0][-4:]}"


def _relative_time(thread_ts: Optional[str]) -> str:
    if not thread_ts:
        return "just now"
    try:
        elapsed = time.time() - float(thread_ts)
        if elapsed < 60:
            return "just now"
        if elapsed < 3600:
            return f"{int(elapsed / 60)} min ago"
        if elapsed < 86400:
            return f"{int(elapsed / 3600)} hr ago"
        return f"{int(elapsed / 86400)} days ago"
    except (ValueError, TypeError):
        return "just now"


def _truncate(answer: str) -> str:
    if len(answer) > _ANSWER_PREVIEW_LIMIT:
        return answer[:_ANSWER_PREVIEW_LIMIT].rstrip() + "…"
    return answer


def _button_value(result: dict[str, Any], answer: str,
                  thread_ts: Optional[str], asker_id: Optional[str]) -> str:
    return json.dumps({
        "entry_id": result.get("entry_id", ""),
        "answer": answer,
        "thread_ts": thread_ts or "",
        "asker_id": asker_id or "",
    })


def _pending_confirm_blocks(result: dict[str, Any],
                             thread_ts: Optional[str],
                             asker_id: Optional[str]) -> list[dict]:
    answer = _truncate(result.get("answer", ""))
    confidence = result.get("confidence", 0)
    meta = f"{int(confidence * 100)}% confidence"
    if result.get("verified"):
        meta += " · :white_check_mark: previously verified"

    value = _button_value(result, answer, thread_ts, asker_id)

    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Suggested answer:*\n{answer}"},
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": meta}],
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Confirm ✓"},
                    "style": "primary",
                    "action_id": "vault_confirm",
                    "value": value,
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Not Helpful"},
                    "action_id": "vault_not_helpful",
                    "value": value,
                },
            ],
        },
    ]


def _verified_blocks(result: dict[str, Any]) -> list[dict]:
    answer = _truncate(result.get("answer", ""))
    owner = result.get("owner_id", "")
    meta = f"{int(result.get('confidence', 0) * 100)}% confidence"
    if owner:
        meta += f" · answered by <@{owner}>"
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":white_check_mark: *Verified answer:*\n{answer}"},
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": meta}],
        },
    ]


def _unconfirmed_blocks(result: dict[str, Any]) -> list[dict]:
    answer = _truncate(result.get("answer", ""))
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Suggested answer:*\n{answer}"},
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": ":grey_question: Suggested, not yet verified — be the first to confirm it."}],
        },
    ]
