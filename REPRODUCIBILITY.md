# Reproduce the checks

Run from the repository root with Python 3.9 or newer.

    python3 -I scripts/verify_repository.py
    python3 -I verification/src/replay.py

The second command checks every pair and arc in the witness lattices, compares the printed and computed layer counts, and verifies three meet/join inequalities and their nine elementary squares. It also checks the published family's adaptation and an integer threshold for the empty-set-only modification. The expected text appears in [replay.txt](verification/logs/replay.txt). The replay runs without a solver and uses the Python standard library.

[Build the PDF](paper/BUILD.md) · [Regenerate and use the explorer](visualization/README.md)
