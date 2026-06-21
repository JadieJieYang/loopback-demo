# LoopBack — Architecture

---

## What LoopBack is

**One-liner:** Every problem your organization solves should only ever need to be solved once.

LoopBack is a Slack-native system built around two pieces working together:

- **Mira** — the AI you `@` in Slack, just like a colleague. She understands intent, checks
  the Knowledge Vault, searches Slack history, and escalates to a human only when genuinely needed.
- **Knowledge Vault** — the growing, verified memory Mira builds from every conversation she
  and a human resolve together.

Mira does **not** sit between the requester and the resolver as a relay. They talk directly,
in the same thread, exactly as they always have. Mira works alongside that conversation —
checking for existing answers before a human needs to get involved, and documenting what
happens afterward.

---

## The problem

Every conversation in Slack disappears the moment the thread goes quiet. The person asking
just wants to be unblocked; the person answering spends time explaining something they may
have explained before. McKinsey data: knowledge workers spend ~20% of their workweek
re-finding information someone else already knew.

LoopBack's bet: knowledge doesn't need to be manually documented. It's produced constantly
in Slack — it just needs to be captured at the moment it's created, verified by the person
who created it, and made reusable.

---

## Core mechanism

```
User @ Mira with a question
  → Mira understands intent (semantic, not keyword matching)
  → Mira checks the Knowledge Vault FIRST (cheapest, fastest check)
      → Vault has a verified answer → Mira replies instantly, done
      → Vault has no answer → Mira searches Slack history
          → History has a candidate → Mira surfaces it, asks a
            clarifying question if needed to confirm it's the same problem
          → Still nothing → Mira escalates: posts the task card to the resolver
              → Resolver replies DIRECTLY to the requester, in the same thread
                Mira does not relay — she listens in the background
              → Once the exchange settles, Mira documents it, writes a Vault
                entry, and follows up: "did this actually resolve it?"
      → Answer verified → written to the Vault, ready for the next person
```

---

## System overview

```
                         Slack Workspace
                  (the only surface end users see)
┌──────────────────────────────────────────────────────────┐
│                                                            │
│   User/Requester ◄──────────────────────► Resolver/Owner  │
│         │           (direct, in-thread)          ▲        │
│         │                                        │         │
│         ▼                                        │         │
│   ┌─────────────┐                        ┌───────┴────┐   │
│   │  mira-app   │── escalates, listens ──►(Slack thread)  │
│   │   (Mira)    │                        └────────────┘   │
│   └──────┬──────┘                                         │
│          │                                                  │
└──────────┼──────────────────────────────────────────────────┘
           │  API contract (3 functions — see below)
           ▼
   ┌──────────────────┐
   │  vault-service   │
   │ (Knowledge Vault)│
   └──────────────────┘
           │
           ▼
   ┌──────────────────┐
   │    Supabase      │
   │  (PostgreSQL +   │
   │    pgvector)     │
   └──────────────────┘
```

Two independently built services, talking through a fixed 3-function API contract.
Neither needs to know the other's internals.

---

## Components

### `mira-app/` — the conversational layer

**Owns:** everything that happens inside Slack.

```
mira-app/
├── app.py                  # entry point — starts the Bolt app (Socket Mode)
├── config.py               # env var loading + validation
├── handlers/
│   └── mention_handler.py  # @Mira event listener; drives the full card lifecycle
├── services/
│   ├── intent.py           # Claude API — classifies question vs. noise
│   ├── task_card.py        # Block Kit card builder for all statuses
│   └── vault_client.py     # Python wrapper around vault-service's 3 API functions
└── dashboard/
    └── home_view.py        # App Home — Knowledge Vault Dashboard (Week 3)
```

**Responsibilities:** receive Slack events, classify intent, query the Vault, search Slack
history, render and update the task card, detect confirmation signals, render the Dashboard.

**Does NOT own:** embeddings, confidence scoring, the database schema, or any persistence.
Mira talks to the Vault only through the three contract functions below.

---

### `vault-service/` — the storage and verification layer

**Owns:** everything related to persisting and retrieving knowledge.

```
vault-service/
├── schema.sql               # CREATE TABLE for task_cards + vault_entries
├── embeddings.py            # OpenAI text-embedding-3-small wrapper
├── confidence.py            # confidence scoring + accumulation logic
└── api/
    ├── search_vault.py      # semantic search against vault_entries
    ├── upsert_vault_entry.py# writes/updates an entry, applies signal logic
    └── update_status.py     # status field update on task_cards
```

**Responsibilities:** own the schema, generate embeddings, run cosine similarity search,
implement the three-signal confirmation logic, manage version history, expose exactly
three functions to `mira-app`.

**Does NOT own:** anything Slack-specific. This service has no idea what a thread, a
mention, or a Block Kit card is — it only knows questions, answers, owners, and confidence.

---

### Supabase (PostgreSQL + pgvector)

Hosted database. Both tables live here. `vault-service` is the only component that talks
to Supabase directly — `mira-app` never queries the database.

---

## API contract

The **only** coupling point between the two services. Changing any of these signatures
requires agreement from both team members — not a unilateral edit.

### `search_vault(query_text)`

```
Input:  query_text: str

Returns:
{
  match_found: boolean,
  entry_id:    uuid | null,
  answer:      string | null,
  owner_id:    string | null,
  confidence:  float,           // 0–1
  last_confirmed_at: string | null
}
```

Confidence thresholds: `> 0.85` = return instantly · `0.7–0.85` = ask a clarifying
question first · `< 0.7` = treat as no match.

### `upsert_vault_entry(task_card_id, answer, owner_id, signal)`

```
Input:
{
  task_card_id:       uuid,
  question_canonical: string,
  answer:             string,
  owner_id:           string,
  signal:             'signal_1' | 'signal_2' | 'signal_3'
}

Returns:
{
  entry_id:        uuid,
  status:          'verified' | 'unconfirmed' | 'outdated',
  confidence_score: float
}
```

### `update_status(task_card_id, new_status)`

```
Input:   { task_card_id: uuid, new_status: string }
Returns: { success: boolean, updated_at: string }
```

---

## Data flow — one full resolution cycle

```
1. User @ Mira with a question
        │
        ▼
2. intent.classify_intent() → QUESTION or NOISE
        │ (QUESTION)
        ▼
3. vault_client.search_vault(query)
        │
        ├── confidence > 0.85 ──► render Verified Answer card → DONE
        │
        ├── 0.7–0.85 ──────────► ask clarifying question, confirm same problem
        │
        └── < 0.7 (no match)
                │
                ▼
        4. Search Slack history (Real-Time Search API)
                │
                ├── candidate found ──► surface it, ask clarifying question
                │
                └── nothing found
                        │
                        ▼
                5. Post task card → status: human_working
                        │
                        ▼
                6. Resolver replies DIRECTLY to requester in-thread
                   (Mira listens, does not relay)
                        │
                        ▼
                7. Mira detects resolution → status: pending_confirm
                        │
                        ▼
                8. 30-min confirmation window opens (signal 1 / 2 / 3)
                        │
                        ▼
                9. vault_client.upsert_vault_entry(...)
                        │
                        ▼
                10. vault-service applies confidence logic, writes entry
                        │
                        ▼
                11. Task card updates to final status (verified / unconfirmed)
```

For the detailed logic behind steps 7–10 (signal definitions, confidence accumulation,
two-tier unconfirmed), see `docs/implementation/DESIGN.md`.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Bot framework | Slack Bolt for Python |
| LLM — intent, extraction, clarifying questions | Claude (`claude-sonnet-4-6`) |
| Embeddings — semantic search | OpenAI `text-embedding-3-small` |
| Database | Supabase (PostgreSQL + pgvector) |
| UI | Slack Block Kit — task cards + App Home Dashboard (no external frontend) |
| History search | Slack Real-Time Search API |
| Hosting | Railway |

---

## Deployment

```
mira-app/      → Railway (Socket Mode for dev, HTTP mode once deployed)
vault-service/ → Python package imported directly by mira-app in the same process
Supabase       → hosted, free tier
```

---

## Why this split

The `mira-app` / `vault-service` boundary isn't just a convenient way to divide work —
it mirrors a real product boundary:

- `mira-app` is about **conversation** — understanding what's being asked, talking to
  people, deciding when to step back and let humans talk directly.
- `vault-service` is about **trust** — deciding whether an answer is reliable enough
  to return instantly, and how that trust builds or decays over time.

Keeping these separate means either piece can be built, tested, and reasoned about without
needing to understand the other's internals.
