# LoopBack — Demo Video Script

Total runtime: 2:50–3:00
Format: Single Slack window, full screen. No slides. Real working product only.
Roles: Jie = Business Analyst / requester · Jinqiu = Data Engineer / resolver
Voice: One narrator
Tone: Calm, human, understated. Let the product speak for itself.

---

## Pre-recording checklist

- Bot running, terminal hidden
- Slack full screen
- Notifications silenced
- Knowledge Vault empty at the beginning of Act 1
- Act 1 completed once before recording Act 2, so the Vault can return a verified result
- Canvas deleted before recording, so Mira creates a fresh one
- Jie and Jinqiu accounts ready in separate browser windows or devices
- Channel #loopback-test-env cleared or scrolled past previous test messages
- Screen recording started
- Microphone tested

---

# INTRO — 0:00–0:28

**[SCREEN]** LoopBack logo and tagline over a blurred Slack background.

Hold for two seconds, then cut to a live Slack channel.

**[SAY]**
> "Every day, someone asks a question
> their team may have already answered.
>
> The person asking just wants to keep moving.
>
> And the person who knows the answer
> has probably had to explain it before.
>
> When the conversation ends,
> all of that effort usually disappears with it—
>
> who understood the problem,
> what finally worked,
> and whether the answer could be trusted."

**[SCREEN]** In the Slack message box, type and send:

```
/invite @Mira
```

**[SCREEN]** Slack confirms that Mira has joined the channel.

Hold for one quiet second.

**[SCREEN]** Jie moves the cursor into the message box and begins typing.

**[SAY]**
> "LoopBack helps a team remember
> what it has already learned—
>
> directly from the conversations
> where the work actually happened."

---

# ACT 1 — LEARNING THE TEAM — 0:28–1:30

## A normal question

**[SCREEN]** Jie finishes typing:

```
Hi team, our approval rate has dropped quite a bit this week.
Has anyone seen this before or know what might be causing it?
```

**[SAY]**
> "It begins like any other question."

**[SCREEN]** Jie sends the message.

Mira automatically creates a Task Card in the thread.

The card begins in the draft state and quietly transitions into ai_searching.

Show:

```
Searching what the team already knows…
```

The card indicates that Mira is checking:

- Knowledge Vault
- Slack history
- Codebase
- Data dictionary

**[SAY]**
> "Jie doesn't know whether anyone has seen this before.
>
> She only knows that something looks wrong
> and she needs help understanding why."

---

## Mira begins learning

**[SCREEN]** Mira continues searching. The Task Card updates in place.

**[SAY]**
> "Mira is new here, too.
>
> She doesn't begin by knowing everything
> about the product or the way this team works.
>
> She begins by paying attention—
>
> looking through the places where the team works
> and gathering the context around the question."

**[SCREEN]** Show a Direction Check with two concise findings:

```
I found two things that may be related:

• product_type is missing from part of the incoming data
• the approval metric excludes records without that field
```

Show citations to:

```
raw_applications.sql
da_approval_metrics.sql
```

Then show:

```
Does this look like the right direction?
```

**[SAY]**
> "But finding something relevant
> isn't the same as understanding what someone needs.
>
> So before bringing in another person,
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
> Mira never becomes the messenger
> between two people.
>
> She helps them reach the conversation faster—
> and then she steps out of the way."

---

## The answer becomes knowledge

**[SCREEN]** The same Task Card changes to pending_confirm. Show:

```
Did this resolve your question?

[ Yes, resolved ]   [ Not yet ]
```

**[SAY]**
> "Because an answer isn't knowledge
> just because someone said it."

**[SCREEN]** Jie clicks `Yes, resolved`.

The card changes to verified. The ❓ reaction becomes ✅. Show:

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

Pause briefly.

**[SAY]**
> "And each time the team works through a problem,
> Mira learns a little more—
>
> about the product,
> about the way the team works,
> and about what will help the next person."

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
>
> They don't know Jie asked it.
>
> And they don't know Jinqiu already solved it."

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
> "Different words.
>
> Same problem.
>
> This time, Mira remembers.
>
> The answer returns in seconds—
>
> and the person who solved it the first time
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
> Five questions can be a signal."

**[SCREEN]** Send the command. Mira displays a period selector. Jinqiu clicks `This Month`.

Mira confirms:

```
Canvas updated — This Month
```

Open the Slack Canvas.

---

## What the team has learned

**[SCREEN]** Show the first sections of the Canvas:

```
Impact
Knowledge Vault
Verified Answers
Open Questions
```

Hold long enough for the viewer to understand the page.

**[SAY]**
> "Over time, Mira can see more than individual answers.
>
> She can see what the team keeps running into—
>
> what has been resolved,
> what is still uncertain,
> and what people keep needing help with."

**[SCREEN]** Scroll slowly to `Enhancement Opportunities`.

---

## From repeated questions to a product insight

**[SCREEN]** Show an AI-written proposal such as:

```
Approval-rate reporting repeatedly fails
when product_type is missing or inconsistent.

Recommended enhancement:

Validate product_type during ingestion
and alert the data team before affected records
enter downstream reporting.
```

Do not scroll while the viewer is reading.

**[SAY]**
> "As Mira learns how the team works,
> she also begins to notice where the work keeps breaking down.
>
> She reads the resolved conversations together—
>
> not simply to summarize what people said,
> but to understand what the pattern means."

**[SCREEN]** A Slack notification appears:

```
Enhancement Opportunity identified

[ Approve ]   [ Defer ]   [ Reject ]
```

Jinqiu clicks `Approve`. Mira responds:

```
Added to the product backlog.
```

**[SAY]**
> "What looked like five separate support questions
> becomes one thing the product team can fix."

Pause briefly.

**[SAY]**
> "Support work becomes product learning."

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
> "Most knowledge tools begin
> after the work is finished.
>
> They ask someone to stop,
> write down what happened,
> and keep it updated."

**[SCREEN]** Show the verified answer and the approved product insight side by side.

**[SAY]**
> "LoopBack learns inside the work itself.
>
> From the questions people ask.
>
> From the context they uncover.
>
> From the answers that actually help."

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

# Delivery notes

## Let the screen show the features

Do not narrate every system state. The viewer can see Mira searching, the card changing, and the confidence score appearing. The narration should explain what Mira is learning and why those moments matter to the people involved.

## Present the cold start as a beginning

Do not describe the empty Vault as a limitation or technical state. The first question is Mira's first day with the team. She does not begin as an all-knowing system. She learns by:

- paying attention to real questions
- searching the places where the team works
- checking her understanding
- observing how the issue is resolved
- remembering what the requester confirms

The emotional payoff arrives in Act 2:

> "This time, Mira remembers."

## Keep the opening quiet

Do not rush the first 20 seconds. The logo, blurred Slack background, and `/invite @Mira` should feel like the arrival of a new teammate, not the launch of a software tool. Avoid dramatic music or an exaggerated voice-over.

## Protect the Vault pause

After the Act 2 answer appears, remain silent for four to five seconds. This is the central product moment. The viewer should have time to see:

- the original answer
- the answer owner
- who verified it
- the confidence score
- the link to the original thread

Speed and provenance are the demonstration.

## Emphasize direct communication

Keep both Jie and Jinqiu visible in the thread when saying:

> "Mira never becomes the messenger between two people."

This is one of LoopBack's strongest differentiators. Mira can search, clarify, organize, learn, and remember — but a real answer still comes directly from the person who owns it.

## Avoid surveillance language

Mira should feel attentive, not intrusive.

Prefer:
- "Mira begins by paying attention."
- "She learns from the way the team works."
- "She remembers what the team confirms."

Avoid:
- "Mira listens to everything."
- "Mira monitors every conversation."
- "Mira watches the team."

## Do not over-explain the architecture

Technical details such as Claude, MCP, Slack Real-Time Search, SQL parsing, and the seven-state machine can remain visible in the interface or appear in the Devpost submission. The demo narration should stay focused on:

- helping the requester keep moving
- helping a new AI teammate understand the product
- reducing repeated effort for the resolver
- preserving trust and provenance
- learning from each resolved conversation
- turning repeated problems into product learning

## Keep the Task Card changes subtle

The same Task Card should mutate in place through the visible stages:

```
draft
→ ai_searching
→ human_working
→ pending_confirm
→ verified
```

Do not stop the story to explain the full state machine. The additional paths — unconfirmed and escalate — do not need to be demonstrated in this video.

## Read naturally

Do not emphasize product terms such as Knowledge Vault, confidence score, intent matching, enhancement proposal, or task state. Read as though you are describing how a new teammate gradually becomes useful — not pitching a technical architecture.

## Three important quiet moments

Leave silence in these places:

- One second after Mira joins the channel
- One second after Jinqiu's answer appears
- Four to five seconds after the Vault answer appears

The silence gives the product room to feel real.

## Final emotional arc

The video should move through these ideas:

```
A new teammate joins
        ↓
Someone needs help
        ↓
Mira learns the product through real work
        ↓
A person provides the answer
        ↓
The requester confirms that it worked
        ↓
Mira remembers for the next person
        ↓
Repeated questions reveal what the product should fix
```

The audience should leave remembering:

> "Mira is new here, too."

> "Mira helps people reach the conversation faster —
> and then she steps out of the way."

> "This time, Mira was learning.
> Next time, she'll remember."

> "One question can be an interruption.
> Five questions can be a signal."
