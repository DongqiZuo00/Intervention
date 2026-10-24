#!/usr/bin/env python3
"""Small, independent checks of noise, smooth width, and descent statements.

Requires NumPy and validate_paper1_geometry.py in this directory.
Run: python3 validate_paper1_noise.py
Writes noise_results.json next to the script; does not modify the earlier script.

All W rows have unit Euclidean norm. C denotes the squared covariance loss,
min_pi mean_j w_j.T Q_pi(j) w_j, rather than its square root.
"""

from pathlib import Path
import json

import numpy as np

from validate_paper1_geometry import (
    build_model, objectives, permutation_min, unit_rows, jsonable,
)


SEED = 20261024


def covariance_loss(model, w, matrices):
    costs = np.stack([np.einsum('ja,ab,jb->j', w, q, w) for q in matrices], axis=1)
    return permutation_min(model, costs)[0]


def signed_distance(x, y):
    return float(min(np.linalg.norm(x - y), np.linalg.norm(x + y)))


def candidate_matrices(model, rng):
    d = model['d']
    candidates = [unit_rows(rng.normal(size=(d, d))) for _ in range(40)]
    candidates.extend([
        model['normals'].copy(),
        unit_rows(model['normals'] + .01 * rng.normal(size=(d, d))),
        np.eye(d),
    ])
    return candidates


def isotropic_noise_check(model, candidates):
    d = model['d']
    variances = 1.0 + .2 * np.arange(d)
    sigma = np.stack([x['Sigma'] for x in model['interventions']])
    q = sigma + variances[:, None, None] * np.eye(d)[None, :, :]
    eigenvalues, eigenvectors = np.linalg.eigh(q)
    floor = float(np.mean(eigenvalues[:, 0]))
    errors = []
    for w in candidates:
        clean = objectives(model, w)['E_sigma_sq']
        errors.append(abs(covariance_loss(model, w, q) - floor - clean))
    distances = [signed_distance(eigenvectors[i, :, 0], model['normals'][i]) for i in range(d)]
    assert max(errors) < 1e-12
    assert max(distances) < 1e-12
    report = {
        'observed_coordinate_noise_variances': variances,
        'smallest_eigenvalues_Q': eigenvalues[:, 0],
        'mean_smallest_eigenvalue': floor,
        'max_loss_debias_identity_error': float(max(errors)),
        'max_minimum_eigenvector_signed_distance': float(max(distances)),
        'candidate_count': len(candidates),
        'identity': 'C_Q(W) - mean_i lambda_min(Q_i) = C_Sigma(W)',
        'qualification': 'Isotropic noise is in observed Y coordinates; target-dependent variances cancel because every full permutation uses every target exactly once.',
    }
    return q, report


def symmetric_perturbation_checks(model, q, candidates, rng):
    d = model['d']
    all_batches = []
    for relative_error in [.05, .1, .2]:
        disturbances, epsilons, vector_checks = [], [], []
        for i, x in enumerate(model['interventions']):
            alpha = float(x['singular_values'][-1] ** 2 / 3)
            epsilon = relative_error * alpha
            raw = rng.normal(size=(d, d))
            raw = (raw + raw.T) / 2
            disturbance = raw * (epsilon / np.max(np.abs(np.linalg.eigvalsh(raw))))
            qhat = q[i] + disturbance
            eigenvalues, eigenvectors = np.linalg.eigh(qhat)
            assert eigenvalues[0] > 0
            distance = signed_distance(eigenvectors[:, 0], model['normals'][i])
            bound = np.sqrt(2) * epsilon / (alpha - epsilon)
            assert distance <= bound + 1e-12
            disturbances.append(disturbance)
            epsilons.append(float(np.linalg.norm(disturbance, ord=2)))
            vector_checks.append({
                'target': i, 'alpha': alpha, 'epsilon': epsilon,
                'actual_operator_norm': epsilons[-1],
                'signed_normal_distance': distance, 'distance_upper_bound': float(bound),
                'distance_over_bound': float(distance / bound),
                'smallest_eigenvalue_Qhat': float(eigenvalues[0]),
            })
        qhat = q + np.stack(disturbances)
        mean_epsilon = float(np.mean(epsilons))
        floor = float(np.linalg.eigvalsh(q)[:, 0].mean())
        floor_hat = float(np.linalg.eigvalsh(qhat)[:, 0].mean())
        errors, debiased_errors = [], []
        for w in candidates:
            raw_loss, noisy_loss = covariance_loss(model, w, q), covariance_loss(model, w, qhat)
            errors.append(abs(noisy_loss - raw_loss))
            debiased_errors.append(abs((noisy_loss - floor_hat) - (raw_loss - floor)))
        assert max(errors) <= mean_epsilon + 1e-12
        assert max(debiased_errors) <= 2 * mean_epsilon + 1e-12
        all_batches.append({
            'epsilon_over_alpha': relative_error,
            'mean_operator_norm_epsilon': mean_epsilon,
            'eigenvector_checks': vector_checks,
            'max_uniform_loss_error': float(max(errors)),
            'max_uniform_loss_error_over_mean_epsilon': float(max(errors) / mean_epsilon),
            'max_reestimated_floor_loss_error': float(max(debiased_errors)),
            'max_reestimated_floor_error_over_2mean_epsilon': float(max(debiased_errors) / (2 * mean_epsilon)),
            'mean_floor_error': float(abs(floor_hat - floor)),
            'perturbations_E': disturbances,
        })
    return {
        'batches': all_batches,
        'all_eigenvector_bounds_pass': True,
        'all_uniform_loss_bounds_pass': True,
        'all_reestimated_floor_2epsilon_bounds_pass': True,
        'qualification': 'The 1*mean(epsilon) bound is for C_Qhat-C_Q, or equal known-floor subtraction. Re-estimating both minimum-eigenvalue floors gives the general 2*mean(epsilon) bound by Weyl.',
    }


def logsumexp(values):
    maximum = float(np.max(values))
    return maximum + float(np.log(np.exp(values - maximum).sum()))


def smooth_width(values, tau, normalized):
    # Centering first makes the cancellation of affine offsets explicit.
    p = values - values.mean()
    total = tau * (logsumexp(p / tau) + logsumexp(-p / tau))
    return float(total - 2 * tau * np.log(len(p))) if normalized else float(total)


def smooth_width_checks(model, rng):
    x = model['interventions'][0]
    sample_count = 13
    sample_y = x['center'] + rng.uniform(-1, 1, size=(sample_count, model['d'] - 1)) @ x['A'].T
    n = model['normals'][0]
    tangent = np.linalg.svd(x['A'], full_matrices=False)[0][:, 0]
    projections = {
        'exact_constant': np.full(sample_count, 7.3),
        'true_normal_projection': sample_y @ n,
        'nonconstant_tangent_projection': sample_y @ tangent,
    }
    rows = []
    for tau in [.05, .2, 1.0]:
        for name, p in projections.items():
            normalized = smooth_width(p, tau, True)
            unnormalized = smooth_width(p, tau, False)
            expected_bias = float(2 * tau * np.log(sample_count))
            true_width = float(np.ptp(p))
            assert abs((unnormalized - normalized) - expected_bias) < 1e-12
            if name != 'nonconstant_tangent_projection':
                assert abs(normalized) < 1e-12
                assert abs(unnormalized - expected_bias) < 1e-12
            else:
                assert normalized > 0
                assert normalized <= true_width + 1e-12
                assert normalized >= max(0, true_width - expected_bias) - 1e-12
            rows.append({
                'case': name, 'tau': tau, 'N': sample_count,
                'projection_range': true_width,
                'normalized_logmeanexp_width': normalized,
                'ordinary_logsumexp_width': unnormalized,
                'ordinary_positive_offset': expected_bias,
            })
    return {
        'checks': rows,
        'formula': 'tau*log(mean(exp(p/tau))) + tau*log(mean(exp(-p/tau)))',
        'equality_reason': 'Cauchy-Schwarz gives mean(exp(p/tau))*mean(exp(-p/tau))>=1, with equality iff all p_k coincide, for finite tau>0.',
        'ordinary_lse_offset': '2*tau*log(N)',
        'qualification': 'This is empirical width: a zero identifies constancy only on the finite observed samples, not the whole population support.',
    }


def contract_toward_assigned_normals(model, w, assignment, angle_factor):
    target = model['normals'][list(assignment)].copy()
    cosine = np.sum(w * target, axis=1)
    target[cosine < 0] *= -1
    cosine = np.clip(np.abs(cosine), 0, 1)
    theta = np.arccos(cosine)
    result = np.empty_like(w)
    ratios = np.zeros(model['d'])
    for j in range(model['d']):
        sine = np.sin(theta[j])
        if sine < 1e-12:
            result[j] = target[j]
            ratios[j] = 0
        else:
            tangent = (w[j] - cosine[j] * target[j]) / sine
            result[j] = np.cos(angle_factor * theta[j]) * target[j] + np.sin(angle_factor * theta[j]) * tangent
            ratios[j] = np.sin(angle_factor * theta[j]) / sine
    return unit_rows(result), ratios


def active_permutation_descent_checks(model, rng):
    d = model['d']
    paths = []
    for path_id in range(6):
        w = unit_rows(rng.normal(size=(d, d)))
        steps = []
        for step in range(8):
            before = objectives(model, w)
            assignment = before['permutation_width']
            next_w, ratios = contract_toward_assigned_normals(model, w, assignment, .6)
            widths_before = np.array([2 * np.abs(model['interventions'][assignment[j]]['A'].T @ w[j]).sum() for j in range(d)])
            widths_fixed_after = np.array([2 * np.abs(model['interventions'][assignment[j]]['A'].T @ next_w[j]).sum() for j in range(d)])
            fixed_upper = float(np.sqrt(np.mean(widths_fixed_after ** 2)))
            after = objectives(model, next_w)
            scaling_error = float(np.max(np.abs(widths_fixed_after - ratios * widths_before)))
            assert scaling_error < 1e-11
            assert fixed_upper < before['E']
            assert after['E'] <= fixed_upper + 1e-12
            assert after['E'] < before['E']
            steps.append({
                'step': step, 'active_permutation': assignment,
                'E_before': before['E'], 'E_after': after['E'],
                'fixed_active_assignment_upper_bound': fixed_upper,
                'pairwise_width_scaling_error': scaling_error,
                'minimum_candidate_row_norm': float(np.linalg.norm(next_w, axis=1).min()),
            })
            w = next_w
        paths.append({'path_id': path_id, 'steps': steps})
    return {
        'paths': paths, 'path_count': len(paths), 'steps_per_path': 8,
        'angle_shrink_factor_each_step': .6,
        'strict_descent_steps': 48,
        'max_pairwise_width_scaling_error': float(max(s['pairwise_width_scaling_error'] for p in paths for s in p['steps'])),
        'qualification': 'At each current W choose an active minimizing assignment, then contract each signed angle to its assigned normal. This verifies a descent direction on the product of unit spheres. It is not a claim that a fixed-initial-assignment upper bound makes the entire reoptimized loss path monotone.',
    }


def main():
    rng = np.random.default_rng(SEED)
    report = {'seed': SEED, 'numpy_version': np.__version__, 'models': {}}
    for d in [3, 4]:
        model = build_model(d, rng)
        candidates = candidate_matrices(model, rng)
        q, isotropic = isotropic_noise_check(model, candidates)
        perturbation = symmetric_perturbation_checks(model, q, candidates, rng)
        smooth = smooth_width_checks(model, rng)
        descent = active_permutation_descent_checks(model, rng)
        report['models'][str(d)] = {
            'B': model['B'], 'M': model['M'], 'true_unit_normals': model['normals'],
            'isotropic_noise': isotropic, 'symmetric_perturbations': perturbation,
            'smooth_empirical_width': smooth, 'active_assignment_descent': descent,
        }
        compact = {
            'd': d,
            'max_isotropic_debias_identity_error': isotropic['max_loss_debias_identity_error'],
            'max_isotropic_eigenvector_signed_distance': isotropic['max_minimum_eigenvector_signed_distance'],
            'perturbation_vector_tests': sum(len(b['eigenvector_checks']) for b in perturbation['batches']),
            'max_perturbed_signed_distance': max(c['signed_normal_distance'] for b in perturbation['batches'] for c in b['eigenvector_checks']),
            'max_eigenvector_distance_over_bound': max(c['distance_over_bound'] for b in perturbation['batches'] for c in b['eigenvector_checks']),
            'max_uniform_loss_error_over_mean_epsilon': max(b['max_uniform_loss_error_over_mean_epsilon'] for b in perturbation['batches']),
            'max_reestimated_floor_error_over_2mean_epsilon': max(b['max_reestimated_floor_error_over_2mean_epsilon'] for b in perturbation['batches']),
            'smooth_width_test_count': len(smooth['checks']),
            'strict_descent_steps': descent['strict_descent_steps'],
            'max_descent_scaling_error': descent['max_pairwise_width_scaling_error'],
        }
        print(json.dumps(jsonable(compact)))
    report['scope'] = 'Small deterministic numerical checks support the algebra; they do not substitute for a universal proof.'
    destination = Path(__file__).with_name('noise_results.json')
    destination.write_text(json.dumps(jsonable(report), ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    print('Saved ' + str(destination.resolve()))


if __name__ == '__main__':
    main()
