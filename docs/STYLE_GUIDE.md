# Style guide for a game translation

The Lithuanian decisions made in this project, written so another language can reuse the
reasoning. Every rule below comes from a line that read badly at first.

## Register

| context | choice |
|---|---|
| dialogue, subtitles, radio chatter | informal **tu**, rough, often hostile |
| menu labels | short, uppercase where the English is uppercase |
| settings descriptions | 3rd person present (*Reguliuoja…*, *Nustato…*, *Rodo…*) |
| notes, letters, journals | the writer's own voice, literary, past tense |

Mixing *tu* and *jūs* is the fastest way to make a translation feel machine-made. In this game
characters almost always address each other with *tu*; a stranger in a hostile scene uses
*jūs* only when the English is deliberately cold.

## Swearing is graded, not literal

English profanity has levels; the translation must have the same levels with real curses, not
body-part calques. Borrowed profanity (*nahui*, *blet*) is authentic in modern Lithuanian
speech and is used the way English uses *fuck* — inside the sentence, as an intensifier.

| level | English | Lithuanian |
|---|---|---|
| 1 — annoyance | damn, hell, goddamn | po velnių, po galais, prakeiktas |
| 2 — standard | shit, bullshit | šūdas, blet, velnias |
| 3 — strong | fuck (intensifier), son of a bitch, bastard | nahui, kalės vaikas, kalė |
| 4 — heaviest | motherfucker, cunt | pizdec, kurva |

Rules learned from reviewing 1 179 swearing lines:

- A single *Fuck.* is not always *Blet.* — rotate through the level's words, or the character
  sounds like a stuck record.
- *Fuck those Fireflies* is not “fuck them” but “to hell with them”: **Dėjau ant tų
  Jonvabalių** — a shrug, not a curse aimed at someone.
- *Look at this shit* is usually not “look at this shit”: use “look at this”, “look what he
  did”, “matei tą numerį?” depending on what the character means.
- Interjections stay short. A two-word line translated into five words loses its punch.

## Gender

Lithuanian marks gender in participles and adjectives, and English does not, so every
“you are…” line is a trap:

- `You're capable.` → *Tu esi pajėgus* (wrong to a woman) / **pajėgi**
- `I'm sorry for getting caught.` → *buvau pastebėtas* / **pastebėta**

Two independent checks:

1. **The voice file name** (`text2\sid-lookup`) gives the speaker and the scene, so the
   addressee can be inferred — see [HOW_IT_WORKS.md](HOW_IT_WORKS.md).
2. **A Slavic translation** (Polish, Russian) marks gender in the past tense and in
   adjectives. Comparing the same id across slots settles most remaining cases.

A masculine noun does not change: *skeneris sugedęs*, *tu keistas vaikas*, *tu esi
Jonvabalis* stay as they are even when said to a woman.

## Names

Write the names down once and never improvise:

- decline them like Lithuanian words (Džoelas → Džoelo, Džoelui, Džoelą, Džoelai)
- keep one spelling for the whole script, in dialogue and in the speaker labels the game
  shows above subtitles (Henris, not Henri)
- watch out for names that are also ordinary words in your language

## Consistency tools

- the same sentence appears many times under different ids — translate it once, fill the rest
- a search for the English text finds every occurrence
- keep a glossary file in the repository; it is what makes a translation feel like one voice
