# LoopBack — Demo Script

**Total runtime:** under 3:00 · **Roles:** Jie = BA (requester) · Jinqiu = DE + Product Owner (resolver)
**Critical:** First 60 seconds carry the most weight with judges. Start strong.

---

## High-Level Overview

| Act | Duration | What it shows | Key moment |
|-----|----------|---------------|------------|
| **Act 1 — Cold start** | 0:00–1:00 | Mira investigates autonomously, confirms direction, loops in resolver | Direction check: "does this look right?" |
| **Act 2 — Vault hit** | 1:00–1:50 | Semantic search, instant answer, no resolver disturbed | 77% match on different wording |
| **Act 3 — Channel Insights** | 1:50–2:40 | Canvas dashboard + AI-generated Enhancement Opportunity | Claude notices a pattern, proposes a fix |
| **Closing** | 2:40–3:00 | Slogan | Logo out |

---

## Act 1 — Cold start (0:00–1:00)

**What this shows:** Complete resolution cycle — Mira investigates the codebase autonomously,
confirms direction with the requester, loops in the resolver with context already prepared.
Differentiator: Mira never relays. She investigates first, confirms direction, then steps back.

**Use case:** Approval rate anomaly — root cause is `product_type` NULL in the analytics schema.

**What gets called:**
1. `search_vault(query)` → no match
2. `investigator.py` Claude tool use loop:
   - `search_github("approval rate product_type")` → finds `da_approval_metrics.sql`
   - `read_file("schema/raw_applications.sql")` → sees nullable product_type
   - `read_known_issues()` → finds Issue #003 (40% drop root cause)
3. Direction check posted in thread
4. `resolution_handler` detects Jie's "yes" → `update_status(human_working)`
5. `resolution_handler` detects Jinqiu's reply → `update_status(pending_confirm)`
6. Jie gives ✅ → `upsert_vault_entry(signal_1)` → `verified`

**Script:**

1. Jie (BA): `@Mira we're seeing an unexpected drop in our approval rate this week — can you help me investigate?`
2. Card: Draft → **🔍 Searching** *(show the card updating in-thread)*
3. Card → **🔎 Direction Check** + Mira posts findings in thread:
   > *"Based on what I found: `product_type` is nullable in `raw_applications` — applications with NULL `product_type` are excluded from approval rate calculations. This matches known issue #003 in your analytics repo. Does this look like the right direction?"*
4. Jie replies: `yes`
5. Card → **🆕 First time this has been asked** with investigation findings visible
6. Jinqiu (DE) replies directly in thread *(Mira stays silent)*:
   > *"Confirmed — product_type was missing from ~18% of records after the March migration. The NOT NULL constraint has been added. Numbers should normalize in the next refresh."*
7. Jie reacts ✅
8. Card → **✅ Verified Answer** · source thread link visible

**Narration:**
> "Mira didn't just escalate — she investigated first. She read your actual SQL schema and data
> dictionary, surfaced the root cause, and confirmed the direction with the requester before
> looping anyone in. The resolver started from understanding, not from scratch.
> And notice: Mira never forwarded a single message. They talked directly."

---

## Act 2 — Vault hit (1:00–1:50)

**What this shows:** Semantic search, not keyword matching. Different wording, instant answer.
The resolver is never disturbed. Full provenance (confidence score, owner, source thread).

**Use case:** PTO question — relatable, universal, different from how it was originally answered.

**What gets called:**
1. `search_vault("how much vacation time do I get")` → match found, ~77% confidence
2. `update_status(pending_confirm)`
3. New BA clicks "This helped ✓" → `upsert_vault_entry(signal_1)` → confidence rises

**Script:**

1. Switch to second Slack account *(different channel or user)*
2. New BA: `@Mira how much vacation time do I get?`
3. Card: Draft → **⚡ Answered from Knowledge Vault** in ~3 seconds
4. Card shows: answer text · **77% confidence** · answered by @Jie · source thread link
5. New BA clicks **This helped ✓**
6. Card → **✅ Verified** · confidence ticks up

**Narration:**
> "Three months later. A different person. A different way of phrasing it.
> Mira recognized the intent — not the keywords — and returned a verified answer in seconds.
> The original resolver was never disturbed."

---

## Act 3 — Channel Insights Canvas (1:50–2:40)

**What this shows:** Mira's PM identity. Questions accumulate, Mira sees patterns,
surfaces them as actionable Enhancement Opportunities. AI-generated, not templated.

**Use case:** After several resolved task cards, Claude notices a recurring theme
and proposes a product improvement.

**What gets called:**
1. `@Mira insights` → `get_or_create_canvas(channel_id)`
2. Time period selector appears → Jinqiu clicks **This Month**
3. `list_task_cards(period)` → `cluster_by_embedding()` → Canvas sections rebuild
4. Enhancement Opportunity block: Claude reads task cards and generates insight
5. Jinqiu clicks **Approve**

**Script:**

1. Jinqiu (Product Owner): `@Mira insights`
2. Mira posts time period selector in channel
3. Jinqiu clicks **This Month**
4. Canvas updates — show three sections:
   - **✅ Knowledge** (verified answers, grouped by topic)
   - **💡 Answered, Pending** (unconfirmed answers)
   - **❓ Open Questions** (human_working / escalate)
5. Scroll to **Enhancement Opportunity** block — Claude-generated text:
   *(e.g. "I noticed 4 questions this month pointing to the same schema issue...")*
6. Jinqiu clicks **Approve**
7. Mira: *"Added to the product backlog."*

**Narration:**
> "After enough questions are resolved, Mira starts to see what they collectively reveal —
> not just individual answers, but product-level patterns. This Enhancement Opportunity
> wasn't written from a template. Claude read the actual task cards and decided what was
> worth surfacing."

---

## Closing (2:40–3:00)

Show the three task card states side by side (human_working → pending_confirm → verified).

> *"Every problem solved becomes organizational memory.*
> *Every pattern becomes a product fix."*

LoopBack logo out.

---

## Pre-recording checklist

**Setup:**
- [ ] App deployed to Railway — no terminal visible during recording
- [ ] Real Supabase connected (`VAULT_STUB=false`)
- [ ] `GITHUB_TOKEN` set, `loopback-analytics` repo public
- [ ] `message.channels` event subscribed in Slack API settings
- [ ] Two Slack accounts ready (Jie = BA, Jinqiu = DE / Product Owner)

**Seed data (do this before recording):**
- [ ] 1 verified PTO entry in Vault (for Act 2 hit)
- [ ] 3–5 task cards in the channel (for Act 3 Canvas + Enhancement Opportunity)
- [ ] Confirm Act 2 question returns ≥70% confidence match

**Demo run:**
- [ ] Do a full dry run — time each act, confirm all cards update correctly
- [ ] Act 1 from question to Verified under 60 seconds
- [ ] Act 2 Vault hit under 10 seconds
- [ ] Act 3 Canvas loads without errors
- [ ] Record 2–3 takes, keep cleanest one under 3:00
- [ ] Upload to YouTube/Vimeo, set to **Public** before submitting

**Submission:**
- [ ] Share sandbox URL with `slackhack@salesforce.com` AND `testing@devpost.com`
