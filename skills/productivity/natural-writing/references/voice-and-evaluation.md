# Voice matching and evaluation

Read this reference when the user asks for a personal or brand voice, supplies examples, requests a formal quality review, or when “humanize” could damage authentic wording.

## Evidence boundaries

Keep four evidence classes separate:

| Evidence | May influence | Must not supply |
|---|---|---|
| Current task material | Facts, examples, claims, conclusions | A personal voice unless confirmed as a voice sample |
| Confirmed user samples | Diction, syntax, rhythm, punctuation, structure | New facts or experiences |
| Brand guide or approved brand copy | Register, terminology, naming, established devices | Unstated product claims, prices, promises, or customer reactions |
| Third-party references | Broad techniques explicitly requested by the user | Distinctive wording, personal identity, facts, or a claim of exact imitation |

Do not automatically search a vault, knowledge base, account history, or nearby personal files. Use only samples the user provides or explicitly identifies for this task. A model draft, unreviewed transcript, document published under someone's account, or silence after delivery is not automatically a confirmed personal sample.

## Extract a working voice profile

From confirmed samples, note only traits that appear consistently and matter to the requested genre:

- degree of formality and relationship to the reader;
- typical sentence and paragraph length, including deliberate variation;
- preferred subjects, verbs, transitions, and level of explicitness;
- punctuation, headings, lists, parentheticals, fragments, and contractions;
- stance: directness, caution, humor, warmth, skepticism, or mixed feelings;
- how the writer opens, develops evidence, handles uncertainty, and stops;
- phrases or structures the user has explicitly asked to preserve or avoid.

Do not average unrelated writers into one voice. If samples conflict, favor the same language, genre, audience, channel, and recency as the current task. State that the match is approximate when evidence is sparse or mismatched.

## Apply voice without caricature

1. Plan the content from task facts before applying style.
2. Match relationships and habits, not catchphrases. A good match should not repeatedly advertise its own resemblance.
3. Preserve unusual concrete details, genuine asides, self-correction, unresolved tension, and intentional rhythm when they belong to the source.
4. Keep neutral genres neutral. Technical, reference, legal, and factual prose should not gain opinions, first person, jokes, or emotional detail merely to feel human.
5. After styling, run the full factual and constraint review again. Voice never overrides accuracy, privacy, citation, deletion, or format requirements.

## Avoid false positives in humanization

Do not rewrite solely because prose is polished, formal, dry, grammatical, consistently formatted, or contains one watched expression. Human writing can use all of these. Stronger evidence is a cluster of empty framing, vague attribution, repeated templates, unsupported uplift, uniform rhythm, and chatbot residue.

If a passage already has a coherent personal voice, make only the changes the user authorized. “Humanize” is permission to edit, not permission to replace the author.

## Evaluation order

Evaluate in this order. The first two are hard gates:

1. **Factual fidelity:** no unsupported, strengthened, weakened, omitted, or misattributed claim.
2. **Constraint fidelity:** language, audience, scope, length, format, privacy, protected spans, and citations are correct.
3. **Information design:** paragraphs advance a clear path; headings, lists, and examples have a function.
4. **Naturalness:** syntax, word choice, transitions, and rhythm fit the language and genre without formulaic residue.
5. **Voice fit:** the draft resembles confirmed traits without copying distinctive wording or becoming a caricature.
6. **Editing burden:** a user should need fewer substantive corrections than before.

Do not collapse these into one cosmetic score. A fluent draft with a factual error fails.

## Comparative testing

For a substantial reusable voice profile, compare a neutral baseline and the voice-matched candidate using the same fact packet and constraints. Keep at least one confirmed sample out of profile construction. Ask the user which draft needs fewer substantive edits and record preferences only after explicit confirmation. Repeated confirmed feedback is stronger than an isolated edit; silence is not acceptance.

## Source synthesis

This skill was synthesized on 2026-09-03 from the following MIT-licensed projects, using their workflows and editing principles rather than copying them wholesale:

- Voiceforge, commit `9eb975e`: universal writing layer, evidence separation, optional voice matching, and evaluation.
- oil-tone, commit `b9b250a`: factual boundaries, plain reader-facing prose, deletion semantics, and Chinese read-aloud checks.
- Humanizer-zh, commit `91f3d39`: Chinese adaptation of common AI-writing-pattern review.
- qu-ai-wei, commit `39da1cf`: authorization scope, fact ledger, structural rewriting, protected text, false-positive control, and platform/register boundaries.
- humanizer, commit `e2e92e7`: English pattern catalog, writer-voice protection, rewrite modes, and whole-draft review.

The source projects trace many pattern observations to Wikipedia's “Signs of AI writing” and related editing practice. Those patterns remain contextual clues, not authorship tests.
