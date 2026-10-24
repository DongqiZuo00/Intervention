# Intervention

**Minimal Active Interventions for Causal Representation Learning** — a three-paper research program:

1. **Identifiability** as a measurable, convex-geometric quantity;
2. **Where to intervene** — adaptive intervention placement importing structural controllability from control theory (flagship, in progress);
3. **Minimal interventions** — convex relaxations, budgets, and sample complexity.

## Start here

- 📄 [`WHITEPAPER.md`](WHITEPAPER.md) — the complete program whitepaper
- 📐 [`proofs/THEOREM1.md`](proofs/THEOREM1.md) — self-contained proofs (Proposition 0: batch = vertex cover; Theorem 1: adaptive–batch separation with $\lfloor n/2\rfloor$ vs $\Theta(\log n)$ on paths)
- 🧪 [`experiments/`](experiments/) — running code and data validating Theorem 1(b) (28× separation at n=256)
- 📚 [`docs/`](docs/) — literature sweep (~80 works), research plan, formalization notes (中文)

## Paper 1 mathematical development

- [Derivations and proofs](proofs/PAPER1_GEOMETRY.md) (中文): width and covariance calibration, finite-sample certificates, and counterexamples.
- [Reproducible checks](experiments/paper1/README.md): three NumPy scripts with reference outputs.
- [Experiment plan](docs/paper1_experiments_zh.md) (中文): statistical coverage, conditioning, negative controls, and comparisons with existing objectives.

**Scope:** the current guarantees concern linear encoders and complete deterministic single-variable clamping, with nondegenerate variation and explicit noise assumptions. They do not establish general nonlinear CRL or scientific novelty. Existing runs are algebraic sanity checks on small models; statistical coverage and real-data validation remain planned.

## Key experimental result

![Theorem 1(b) separation on path graphs](assets/fig_path_separation.png)

