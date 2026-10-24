# Paper 1 reproducible mathematical checks

These scripts check the algebra in [the derivation notes](../../proofs/PAPER1_GEOMETRY.md). They use small linear causal models with deterministic single-variable interventions. They are not statistical coverage experiments or evidence of a new algorithm outperforming existing methods.

## Environment and execution

Python 3.11 or later is required by the pinned NumPy dependency. The reference runs were reproduced with Python 3.12.14 and NumPy 2.3.5.

From the repository root:

```bash
python3 -m venv experiments/paper1/.venv
source experiments/paper1/.venv/bin/activate
python -m pip install -r experiments/paper1/requirements.txt
python experiments/paper1/validate_paper1_geometry.py
python experiments/paper1/validate_paper1_noise.py
python experiments/paper1/validate_paper1_certificate.py
```

The scripts write `results.json`, `noise_results.json`, and `certificate_results.json` beside themselves. These generated copies are ignored by Git. Committed reference outputs are in [reference_results](reference_results/).

## What is checked

| Script | Check | Reference result |
|---|---|---|
| `validate_paper1_geometry.py` | Width and covariance calibration for unit-row candidate encoders; exact intervention geometry; partial-target, Gaussian-support, and small-sample counterexamples | 6,400 candidate matrices on two models with dimensions 3 and 4; no bound violations |
| `validate_paper1_noise.py` | Isotropic-noise debiasing; symmetric covariance perturbations; normalized smooth widths; constructed descent paths | 21 eigenvector checks, 258 loss checks, 18 smooth-width cases, and 96 descent steps passed |
| `validate_paper1_certificate.py` | Recovery-error interval under exactly known operator-error budgets | 312 candidate checks passed |

All three scripts exited successfully in a clean directory on 2026-10-24. The newly generated JSON files matched the committed reference data byte-for-byte in the tested environment. Floating-point roundoff may differ in other environments.

## Interpretation limits

- The 6,400 count refers to candidate encoder matrices, not 6,400 independent datasets or causal models.
- The noisy covariance matrices are perturbed with constructed, known operator-error bounds. This does not test the sampling concentration inequality or frequentist coverage.
- The certificate examples have positive certified spectral gaps. Abstention and vacuous intervals need their own experiments.
- The descent construction uses the true normals to verify a proof argument. It is not an implementable oracle-free training method or a convergence guarantee for an arbitrary optimizer.
- Exact permutation enumeration is intentional for dimensions 3 and 4. Do not use it for the planned dimensions 10 and 20; use a polynomial-time linear assignment solver there.
- Population clamping is distinct from a random perfect intervention with positive target variance. Unknown anisotropic measurement noise is outside the current exact debiasing guarantee.

The [experiment plan](../../docs/paper1_experiments_zh.md) specifies what remains to establish practical usefulness, statistical reliability, and limits. The covariance objective is a spectral form of constant fitting; an algebraically equivalent baseline cannot support a claim of a new, better algorithm.
