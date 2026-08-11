# Macroscopic Quantum Tunneling Between Acoustic Black and White Holes in the Michel Flow

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21881838.svg)](https://doi.org/10.5281/zenodo.21881838)

This repository contains the preprint, LaTeX source, bibliography, and figures for:

> [Alexander V. Semyannikov](https://orcid.org/0009-0007-0926-8272),
> “Macroscopic Quantum Tunneling Between Acoustic Black and White Holes in the Michel Flow” (2026).

## Abstract

This work formulates and estimates macroscopic quantum tunneling between the acoustic black-hole and acoustic white-hole states of the relativistic Michel flow. The accretion branch ($\upsilon < 0$) and the wind branch ($\upsilon > 0$) are degenerate stationary points of a single energy functional, separated by an inertial–kinematic barrier due to the necessity of stopping and reversing the macroscopic flow. Within a one-parameter collective-coordinate reduction, an instanton trajectory in Euclidean time is constructed that connects the two branches through the saddle point of the phase space; the instanton action is finite and takes the closed form $\mathcal{S}_{\mathrm{inst}} = \frac{4}{3} \sqrt{2\,I\,\Delta E}$ in terms of the effective moment of inertia of the flow and the barrier height. Numerical estimates for $a_{\infty} \in \left\{ 0.05, 0.1 \right\}$ show that the action is controlled by the macroscopic scales of the acoustic horizon and grows in the cold limit. The transition probability is exponentially suppressed and acquires physical meaning only for systems with a quantum microstructure ($\hbar_{\mathrm{eff}} > 0$); the detailed balance between the forward and reverse transitions is broken owing to the classical blue-shift instability of the acoustic white hole, and Coleman bubble nucleation is inapplicable owing to the branch degeneracy. The construction is consistent with the invariant quantities established in the companion studies.

## Repository contents

- `EN_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.tex` — English LaTeX source (primary)
- `RU_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.tex` — Russian LaTeX source
- `EN_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.pdf` / `RU_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.pdf` — compiled preprints (after build)
- `article.bib` — bibliography database
- `figs/` — figures (`fig_double_well_potential.pdf`, `fig_inertia_localization.pdf`, `fig_instanton_scaling.pdf`, `fig_phase_topology.pdf`)
- `CITATION.cff` — machine-readable citation metadata
- `.zenodo.json` — Zenodo deposit metadata

## Building the article

A TeX distribution with `latexmk`, BibTeX, and the `elsarticle` document class is required. Build from the repository root:

```sh
latexmk -pdf EN_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.tex
latexmk -pdf RU_macroscopic_quantum_tunneling_between_acoustic_black_and_white_holes_in_the_michel_flow.tex
```

To remove generated auxiliary files:

```sh
latexmk -c
```

## Citation

Please use the metadata in `CITATION.cff` when citing this work. The DOI for all versions is [10.5281/zenodo.21881838](https://doi.org/10.5281/zenodo.21881838).

## License

The article, its source, and the accompanying figures are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See `LICENSE` for details.
