---
name: natural-writing
description: Draft, rewrite, polish, proofread, or humanize reader-facing Simplified Chinese and English while preserving facts, evidence strength, format, and authorial voice. Use when the user asks to 写作、改写、重写、润色、校对、去 AI 味、改自然点、匹配语气, or to draft, rewrite, polish, proofread, humanize, or match a voice in Chinese or English. Let a more specific skill lead for specialized deliverables such as weekly reports; do not use for translation-only, code/config/data-only, or AI-authorship detection tasks.
---

# Natural Writing｜自然写作

## Overview

Create or edit natural reader-facing prose in Simplified Chinese, English, or a mixed-language document. Treat stereotyped “AI writing” patterns as editing signals, never proof of authorship. Natural writing means accurate, purposeful, audience-appropriate writing, not forced casualness or deliberate imperfection.

When a more specific skill governs the deliverable, let it define the content workflow and use this skill only as the writing-quality layer.

## Priority Order

Resolve conflicts in this order:

1. Facts, quotations, citations, evidence strength, logic, privacy, and safety.
2. The user's latest instructions, intended use, protected text, and required format.
3. The source's meaning, position, uncertainty, and confirmed authorial voice.
4. Clear structure and idiomatic expression in the target language.
5. Rhythm, concision, headings, and visual polish.

No stylistic improvement can compensate for a factual or constraint error.

## Workflow

1. **Set the editing contract.** Identify the operation, language, audience, genre, channel, length, output mode, and protected material. Infer ordinary details when low risk; ask only when different answers would materially change the result.
2. **Choose the allowed scope.** Use the narrowest scope that fulfills the request:
   - `draft`: create prose only from supplied facts and clearly authorized invention.
   - `rewrite/humanize`: sentence, paragraph, and document structure may change while claims stay fixed.
   - `polish`: improve wording, flow, and local ordering; preserve stance, emphasis, and overall proportions.
   - `proofread`: correct spelling, grammar, punctuation, and unambiguous errors only.
3. **Protect the source.** For editing, make a mental ledger of names, numbers, dates, claims, qualifications, exclusions, quotations, citations, links, terminology, and explicit placeholders. Keep each citation attached to the claim it actually supports. Do not expose or repeat apparent credentials; ask for a redacted copy when prose work cannot proceed safely.
4. **Set voice and register.** Use the user's confirmed sample when provided. Otherwise derive register from the task and source. A sample may influence wording, syntax, punctuation, rhythm, and structure, but never supply facts. Do not search personal files or infer a person's voice from account ownership without explicit direction.
5. **Build the information path.** Decide what each paragraph must do and order facts, reasoning, examples, limits, and actions by their real relationship. Do not default to a fixed introduction, three-part body, conclusion, or uniformly sized sections.
6. **Write or rebuild.** Prefer concrete subjects, direct verbs, stable terminology, and sentences that sound natural when read aloud. Rewrite around a paragraph's main point instead of swapping isolated “AI words.” Preserve useful quirks, technical language, uncertainty, and genuine tension.
7. **Apply language guidance.** Read [references/zh-writing.md](references/zh-writing.md) for Simplified Chinese and [references/en-writing.md](references/en-writing.md) for English. For mixed text, load both and preserve code, names, commands, and established terms.
8. **Review the whole artifact.** Reconcile the result against the source ledger and task contract. Then use [references/voice-and-evaluation.md](references/voice-and-evaluation.md) for voice-sensitive work, ambiguous humanization, or a formal quality review.
9. **Return the requested artifact.** Keep process notes outside the prose. Do not add a title, summary, change log, disclaimer, call to action, or uplifting ending unless the task calls for one.

## Decision Rules

- A watched phrase or punctuation mark is not a ban. Edit it only when it creates empty emphasis, false logic, repetition, register mismatch, or mechanical rhythm. Look for clusters and function, not isolated tokens.
- Preserve authentic quotations, legal text, standard definitions, code, formulas, product names, citations, and explicitly protected wording. Edit surrounding prose unless the user authorizes changes to them.
- Never invent a fact, source, experience, feeling, consensus, or first-person claim to create “personality.” Fiction and clearly authorized creative invention are exceptions.
- Do not strengthen uncertainty, correlation, exclusion, comparison, or causality. If the source's own claim exceeds its evidence, preserve the author's claim when possible and flag the risk outside the final prose; pause if a safe faithful rewrite is impossible.
- Do not equate natural with informal. Technical, academic, legal, brand, support, and social writing each have different valid rhythms and conventions.
- If the user asks to remove content, remove the content and its residual references. Do not replace it with “X was removed,” “X is not supported,” or another echo unless the document is specifically a policy, deprecation notice, or history.
- Translation alone belongs to a translation workflow. When translation and rewriting are both requested, apply this skill to the target-language draft after meaning has been translated.
- This skill improves prose and cannot certify human authorship or guarantee passage of an AI detector. Do not assist with deceptive claims about authorship or policy evasion.

## Output Modes

- **Direct text:** return the finished prose. Add a brief edit note only when requested or when unresolved risk matters.
- **File edit:** change only the authorized prose. Preserve frontmatter, code blocks, data, link targets, and unrelated sections unless the user says otherwise.
- **Embedded use:** return only the finished text to the calling workflow.
- **Review request:** provide prioritized findings and suggested rewrites; do not silently rewrite the source unless asked.

## Verification

Before delivery, confirm:

- Every retained or new claim is supported by the task material or authorized creative scope.
- Names, numbers, dates, quotations, citations, rankings, qualifiers, and exclusions still match the source.
- The result follows the requested language, audience, genre, length, format, and editing scope.
- No protected span, terminology, link target, code, or placeholder changed accidentally.
- Each paragraph advances information; headings and lists help navigation, comparison, or execution.
- No empty framing, vague authority, forced symmetry, repeated conclusion, chatbot residue, or generic uplift remains without a real function.
- Sentence and paragraph rhythm varies naturally without fabricated personality.
- The prose ends at the last useful fact, judgment, or action unless a formal conclusion is required.
