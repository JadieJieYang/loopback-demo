# LoopBack — Demo Video Script

Total runtime: 2:50–3:00
Format: Single Slack window, full screen. No slides. Real working product only.
Roles: Jie = Business Analyst / requester · Jinqiu = Data Engineer / resolver
Voice: One narrator
Tone: Calm, human, understated. Let the product speak for itself.

# INTRO — 0:00–0:28

**[SCREEN]** LoopBack logo and tagline over a blurred Slack background.

Hold for two seconds, then cut to a live Slack channel.

**[SAY]**
> "Every day, someone asks a question
> their team may have already answered.
>
> The answer exists — in a resolved thread,
> from a colleague who took the time to explain it.
> But when the conversation ends,
> the context, the owner, and the proof that it worked
> disappear with it.
>
> LoopBack turns resolved conversations
> into verified organizational memory.
>
> Mira —
> an AI teammate who lives inside your workspace.
> She helps questions get answered,
> and captures every resolved conversation
> into a Knowledge Vault:
> a growing, verified memory built from real team exchanges.
>
> The next time anyone asks — Mira remembers."

**[SCREEN]** In the Slack message box, type and send:

```
/invite @Mira
```

**[SCREEN]** Slack confirms that Mira has joined the channel.

Hold for one quiet second.

---

# ACT 1 — LEARNING THE TEAM — 0:28–1:30

## A normal question

**[SCREEN]** Jie moves the cursor into the message box and begins typing.

```
Hi team, our approval rate has dropped quite a bit this week.
Has anyone seen this before or know what might be causing it?
```

**[SCREEN]** Jie sends the message.

Mira automatically look into the question,

Mira is checking:

- Knowledge Vault
- Slack history (via Real-Time Search API)
- Codebase (GitHub — Claude tool use)
- Data dictionary

## Mira begins learning

**[SCREEN]** The Task Card updates in place. Briefly show Claude's tool calls in progress — Claude autonomously deciding what to look at:

```
→ read_file("schema/raw_applications.sql")
→ read_file("schema/da_approval_metrics.sql")
→ search_slack_history("approval rate drop")
```

**[SAY]**
> "Mira is new here, too.
>
> She doesn't begin by knowing everything
> about the product or the way this team works.
>
> She begins by paying attention —
> running an agentic Claude tool-use loop:
> reading the actual SQL schema files from GitHub,
> searching your Slack history in real time via the Real-Time Search API,
> and deciding on her own what to look at next.
>
> This isn't keyword search.
> Claude is driving the investigation."

**[SCREEN]** Card transitions to Direction Check with two concise findings:

```
I found two things that may be related:

• product_type is missing from part of the incoming data
• the approval metric excludes records without that field
```

Show citations linking directly to the files Claude read:

```
raw_applications.sql  ↗
da_approval_metrics.sql  ↗
```

Then show:

```
Does this look like the right direction?
```

**[SAY]**
> "She read the actual files — and decided what mattered.
>
> But finding something relevant
> isn't the same as understanding what someone needs.
>
> So before looping anyone in,
> Mira checks with Jie first."

---

## The team helps Mira understand

**[SCREEN]** Jie replies in the same thread:

```
yes, that makes sense.
can someone from the data team confirm and fix it?
```

**[SCREEN]** The Task Card changes to human_working. A ❓ reaction appears on Jie's original message. The findings remain visible inside the card.

**[SAY]**
> "Jie confirms that Mira is looking
> in the right direction.
>
> It's a small moment, but it matters.
>
> Mira isn't only helping the team
> understand the problem.
>
> The team is also teaching Mira
> how their product and their work fit together."

---

## Jinqiu answers directly

**[SCREEN]** Switch to Jinqiu's Slack account. Jinqiu opens the thread.

Hold briefly so the viewer can see:

- Jie's original question
- Mira's findings
- The SQL filenames
- Jie's confirmation

**[SAY]**
> "So when Jinqiu steps in,
> no one has to begin from scratch."

**[SCREEN]** Jinqiu replies directly in the same thread:

```
confirmed — product_type was missing from a batch of records
after the March migration.

we added the NOT NULL constraint and completed the backfill.
the numbers should return to normal after tonight's refresh.
```

Pause for one second after the reply appears.

**[SAY]**
> "The answer still comes from Jinqiu.
>
> Mira helps them reach the conversation faster—
> and then she steps out of the way."

---

## The answer becomes knowledge

**[SCREEN]** The same Task Card changes to pending_confirm. Show:

```
Did this resolve your question?

[ Yes, resolved ]   [ Not yet ]
```

**[SAY]**
> "Because an answer isn't knowledge just because someone said it."

**[SCREEN]** Jie clicks `Yes, resolved`.

The card changes to verified. The ❓ reaction becomes ✅.

**[SCREEN — hold 3 seconds, let the viewer read every line]**

```
Verified Answer

Answered by @Jinqiu
Verified by @Jie
Confidence: 96%
View original thread
```

**[SAY]**
> "It becomes knowledge when the person who needed it
> confirms that it worked.
>
> The answer keeps its owner,
> its source,
> and the reason the team can trust it."

Pause.

**[SAY]**
> "This time, Mira was learning.
>
> Next time, she'll remember."

---

# ACT 2 — THE NEXT TIME — 1:30–2:00

**[SCREEN]** Cut to a new message in the same channel from a different requester. The requester types:

```
hey, why are approved application numbers so low this month?
it feels like something might be wrong with the data
```

**[SAY]**
> "Three days later, someone else sees the same problem.
>
> They use different words.
> They don't know Jie asked it.
> They don't know Jinqiu already solved it."

**[SCREEN]** Send the message. Within two or three seconds, Mira displays:

```
Answered from Knowledge Vault
```

Show Jinqiu's original answer and:

```
Answered by @Jinqiu
Verified by @Jie
Confidence: 96%
View original thread
```

**[NO NARRATION FOR 4–5 SECONDS]**

Do not move the cursor. Do not scroll. Let the viewer experience the speed.

**[SAY]**
> "Different words. Same problem.
>
> Mira matched the intent using semantic vector search —
> not keywords, but meaning.
>
> The answer returns in seconds.
>
> The person who solved it the first time
> never has to solve it again."

---

# ACT 3 — WHEN QUESTIONS BECOME A SIGNAL — 2:00–2:40

**[SCREEN]** Switch back to Jinqiu's account. Jinqiu types:

```
@Mira insights
```

**[SAY]**
> "One question can be an interruption.
>
> Five questions can be a signal.
>
> Mira surfaces that signal in a Slack Canvas —
> a live, structured document that lives inside the workspace,
> updated automatically as questions get resolved."

**[SCREEN]** Send the command. Mira displays a period selector. Jinqiu clicks `This Month`.

Mira confirms:

```
✅ Canvas updated — This Month (July 2026)
```

Open the Slack Canvas.

---

## What the team has learned

**[SCREEN]** Show the Canvas — hold 4 seconds, scroll slowly through all sections:

```
📊 Impact

5 questions received this month.

→ 3 resolved — answers ready to reuse, no resolver needed next time
→ 1 unconfirmed — suggested at 68% confidence, flagged for follow-up
→ 1 open — resolver is being looped in

Mira can now auto-serve 3 topics instantly.
Every verified answer means one less interruption next time around.

─────────────────────────────────────────────────

🧠 Knowledge Vault

March migration caused NULL product_type drop in approval metrics
✅ 95% confidence · answered by @Jinqiu · View original thread ↗

  - Hey, why are approved application numbers so low... ↗
  - Hey, why are approved application numbers so low... ↗

─────────────────────────────────────────────────

❓ Open — no answer yet

Hi team, our approval rate has dropped quite a bit this week...
🔍 Investigated → ✓ Direction confirmed → ⏳ Awaiting resolver
View thread ↗
```

**[SAY]**
> "The Canvas shows the full picture in one place —
> what's been resolved, what's confirmed,
> what's still waiting.
>
> The Knowledge Vault groups similar questions
> under a single verified answer.
> Semantic similarity, not keywords —
> Mira recognizes they're asking the same thing
> even when the words are different."

**[SCREEN]** Scroll to `Enhancement Opportunities`.

---

## From repeated questions to a product insight

**[SCREEN]** Show the Enhancement Opportunities section — hold 4 seconds:

```
🌱 Enhancement Opportunities
AI-generated from resolved questions · This Month (July 2026)

1. 📖 Approval rate drops lack self-serve explanation  ·  5 related questions
   - All 5 questions this month are variations of the same concern...
   - No question was resolved without human involvement...
   - Suggested: Publish a runbook explaining common causes of
     approval rate fluctuations so users can self-diagnose first.
```

**[SAY]**
> "Claude read every resolved task card from this period —
> not to summarize what people said,
> but to identify what the pattern means.
>
> No predefined categories. No templates.
> A genuine AI-generated product insight,
> surfaced directly in Slack where the team already works.
>
> What looked like five separate support questions
> becomes one thing the product team can fix.
>
> Support work becomes product learning."

---

# CLOSING — 2:40–3:00

**[SCREEN]** Reveal the complete LoopBack cycle. Keep the diagram simple:

```
A question
    ↓
Shared context
    ↓
A direct human answer
    ↓
Verification
    ↓
Knowledge the team can reuse
    ↓
Patterns the product team can act on
    ↺
```

Let each stage illuminate slowly.

**[SAY]**
> "Teams spend nearly a full day every week
> chasing information a colleague already has.
>
> Most tools try to fix that
> by asking someone to stop working and start documenting.
>
> Nobody does."

**[SCREEN]** Show the three-tier flow side by side: Direction Check card → Verified Answer card → Canvas.

**[SAY]**
> "LoopBack is a three-tier AI agent built entirely inside Slack.
>
> Tier one: semantic vector search against the Knowledge Vault —
> verified answers returned in seconds.
>
> Tier two: an agentic Claude tool-use loop —
> reading your actual schema files via GitHub MCP,
> searching your workspace history via the Real-Time Search API,
> and reasoning about what it found before looping anyone in.
>
> Tier three: a human answers directly.
> Mira captures the conversation. The Vault grows.
>
> This only works because it lives inside Slack.
> The knowledge, the conversations, the Canvas —
> none of it leaves the place where the work happens."

**[SCREEN]** Transition to the LoopBack logo.

**[SAY]**
> "Every problem solved becomes organizational memory.
>
> Every recurring pattern becomes a product improvement."

Brief pause.

**[SAY]**
> "LoopBack."

**[SCREEN]** Final tagline:

```
Your team should never solve the same problem twice.
```

Fade to black.

---