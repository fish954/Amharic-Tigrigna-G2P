# Amharic-Tigrigna-G2P

Grapheme-to-phoneme conversion and comparison between Amharic and Tigrigna using a custom dictionary-based approach.

## Project Goals

- Compare linguistic similarity between Amharic and Tigrigna.
- Use phoneme-based analysis to go beyond surface-level word matching.
- Visualize and interpret similarity through frequency overlap metrics.

## Features

- Custom G2P dictionary for phoneme transcription of Ge'ez script.
- Frequency analysis of both words and phonemes.
- Computes overlap scores:
  - Word Overlap (Exact matches)
  - Phoneme Overlap (Sound similarity)
- Normalized scoring from 0 to 1:
  - 1.0 = full overlap
  - 0.0 = no overlap

## Interpretation

- A high phoneme overlap indicates that the languages sound very similar despite vocabulary differences.
- A high word overlap means that the languages may share a lot of common words or the two texts use a lot of the same vocabulary.
