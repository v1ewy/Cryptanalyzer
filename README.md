# Frequency Analysis Decoder for Russian Texts
# Description
This project is a laboratory work for the subject "Fundamentals of Information Security". It implements a console-based tool for decrypting monoalphabetic substitution ciphers (simple substitution ciphers) using frequency analysis of Russian letters. The tool assists a cryptanalyst in performing step‑by‑step decryption, providing statistical data, word grouping, manual substitution with undo/redo, and an automatic substitution mode based on pre‑defined Russian letter frequencies.

# Features
Frequency Analysis – displays all symbols of the ciphertext sorted by their occurrence frequency (most frequent first).

Word Grouping:

By word length – helps to identify short words (prepositions, conjunctions).

By number of unknown letters – shows words that are almost deciphered.

Current Decryption State – shows the partially decrypted text: already substituted letters are displayed in lowercase, unknown symbols remain uppercase.

Manual Substitution – allows the user to assign a Russian letter to any ciphertext symbol. Every change is saved in a history stack for easy undo.

Undo/Redo – revert any number of previous substitution steps.

Automatic Substitution – suggests initial replacements by matching the most frequent ciphertext symbols with the most frequent Russian letters (based on a built‑in frequency table). The algorithm ensures that no letter is used twice and warns if there are not enough free letters.

Save Results – export the current decrypted text to a file.

# Requirements
Python 3.6 or higher.

No external libraries are required (only standard modules: os, copy, collections).

# Installation
Clone this repository or download the source code.

Make sure you have Python 3 installed.

Prepare a ciphertext file (plain text file, UTF‑8 encoding) containing the encrypted message. The ciphertext should consist of uppercase Russian letters and spaces only (other characters may be ignored or cause unexpected behavior).

# License
This project is for educational purposes only and is not intended for production use. You are free to use and modify the code for your own studies.


