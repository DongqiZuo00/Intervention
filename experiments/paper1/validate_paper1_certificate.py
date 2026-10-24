#!/usr/bin/env python3
"""Check the deterministic confidence interval in Eq. (26) of the notes.

Requires NumPy and the two companion validation scripts in this directory.
The operator error budgets are constructed exactly, not estimated from data.
This validates the algebra of the interval, not a probabilistic coverage claim.
"""
from pathlib import Path
import json
import numpy as np
from validate_paper1_geometry import build_model, objectives, unit_rows
from validate_paper1_noise import covariance_loss


def main():
    rng = np.random.default_rng(20261025)
    records = []
    for dimension in (3, 4):
        model = build_model(dimension, rng)
        identity = np.eye(dimension)
        covariances = np.stack([item['Sigma'] for item in model['interventions']])
        signal_eigenvalues = np.linalg.eigvalsh(covariances)
        population = covariances + (1 + .3 * np.arange(dimension))[:, None, None] * identity
        for fraction in (.01, .05, .1):
            errors, sample = [], []
            for target in range(dimension):
                raw = rng.normal(size=(dimension, dimension))
                raw = (raw + raw.T) / 2
                error = fraction * signal_eigenvalues[target, 1]
                perturbation = raw / np.linalg.norm(raw, 2) * error
                errors.append(np.linalg.norm(perturbation, 2))
                sample.append(population[target] + perturbation)
            errors, sample = np.array(errors), np.array(sample)
            eig = np.linalg.eigvalsh(sample)
            alpha_lower = np.min(eig[:, 1] - eig[:, 0] - 2 * errors)
            beta_upper = np.max(eig[:, -1] - eig[:, 0] + 2 * errors)
            assert alpha_lower > 0
            baseline = eig[:, 0].mean()
            candidates = [model['normals'], np.eye(dimension)]
            candidates += [unit_rows(rng.normal(size=(dimension, dimension))) for _ in range(50)]
            max_violation = 0.
            for candidate in candidates:
                gap_hat = covariance_loss(model, candidate, sample) - baseline
                actual = objectives(model, candidate)['Delta']
                lower = np.sqrt(max(0., gap_hat - 2 * errors.mean()) / beta_upper)
                upper = min(np.sqrt(2.), np.sqrt(2 * (gap_hat + 2 * errors.mean()) / alpha_lower))
                violation = max(0., lower - actual, actual - upper)
                assert violation < 1e-12
                max_violation = max(max_violation, violation)
            records.append({
                'dimension': dimension, 'epsilon_fraction_of_gap': fraction,
                'candidate_count': len(candidates),
                'alpha_lower': float(alpha_lower), 'beta_upper': float(beta_upper),
                'max_violation': float(max_violation),
            })
    result = {
        'seed': 20261025,
        'total_candidate_checks': sum(item['candidate_count'] for item in records),
        'all_passed': True,
        'interpretation': 'Deterministic interval check under exact operator error budgets; not a simulation of statistical coverage.',
        'cases': records,
    }
    output = Path(__file__).with_name('certificate_results.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
