# Three inequalities, one obstruction

[Download the offline explorer ZIP](https://raw.githubusercontent.com/DannyExperiments/acyclic-submodular-threshold-obstruction/v1.0.0/visualization/acyclic-submodular-threshold-obstruction-explorer.zip). Extract it and open index.html. The controls step through the exact three inequalities and inspect all dependency arcs from each of the 64 masks.

Each diamond shows two incomparable inputs, their union at the top and their intersection at the bottom. The shown links are inclusion comparisons. The three diamonds together are an exact contradiction when the nine displayed family members have values below a strict threshold. The explorer separately lists dependency arcs, each of which moves from an earlier layer to a later layer.

The renderer produces the looping GIF. Run it with Python 3 and Pillow already installed.

    python3 visualization/render.py

Arial is the local default. Set Q335_FONT and Q335_BOLD_FONT to paths to suitable fonts if using another system.
