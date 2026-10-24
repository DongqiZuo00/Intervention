#!/usr/bin/env python3
"""Small reproducible validations for linear intervention-support geometry.

Requires Python >= 3.10 and NumPy. No training or repository modification.
Run: python3 validate_paper1_geometry.py
Writes results.json beside this script. All candidate normals are unit vectors.

SCM convention: B[a,b] is the coefficient on edge a -> b,
L = I-B.T, L Z = epsilon, epsilon ~ Uniform([-1,1]^d), Y=MZ.
For do(Z_i=c), the remaining structural equations are re-solved:
Z[-i] = inv(L[-i,-i]) * (epsilon[-i]-L[-i,i]*c).
Thus K_i = center_i + A_i[-1,1]^(d-1), n_i = normalize(M^(-T)e_i).

For d unit candidate rows W, all assignments are exhaustively enumerated:
E(W)^2 = min_pi mean_j width(K_pi(j), W_j)^2,
Delta(W)^2 = min_pi mean_j min_s ||W_j-s*n_pi(j)||_2^2.
Covariance objective uses the exact population Sigma_i=A_i A_i.T/3.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


SEED = 20261023
N_RANDOM = 2000
N_NEAR_PER_SCALE = 200
NEAR_SCALES = [1e-7, 1e-5, 1e-3, 1e-2, 1e-1, 5e-1]


def unit_rows(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def build_model(d, rng):
    # A fixed nontrivial DAG; labels are permuted independently of causal order.
    b = np.zeros((d, d))
    b[0, 1], b[0, 2], b[1, 2] = 0.8, -0.5, 0.6
    if d == 4:
        b[0, 3], b[1, 3], b[2, 3] = 0.35, -0.45, 0.7
    order = rng.permutation(d)
    b = b[np.ix_(order, order)]
    lmat = np.eye(d) - b.T
    q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    v, _ = np.linalg.qr(rng.normal(size=(d, d)))
    m = q @ np.diag(np.linspace(0.8, 1.9, d)) @ v.T
    normals = unit_rows(np.linalg.inv(m))
    interventions = []
    for i in range(d):
        keep = np.array([j for j in range(d) if j != i])
        inverse_reduced = np.linalg.inv(lmat[np.ix_(keep, keep)])
        generators_z = np.zeros((d, d - 1))
        generators_z[keep, :] = inverse_reduced
        c = float(0.3 + 0.2 * i)
        center_z = np.zeros(d)
        center_z[i] = c
        center_z[keep] = np.linalg.solve(
            lmat[np.ix_(keep, keep)], -lmat[keep, i] * c
        )
        a = m @ generators_z
        singular_values = np.linalg.svd(a, compute_uv=False)
        covariance = a @ a.T / 3.0
        interventions.append({
            'i': i, 'c': c, 'keep': keep, 'A': a,
            'generators_z': generators_z, 'center_z': center_z,
            'center': m @ center_z, 'Sigma': covariance,
            'singular_values': singular_values,
            'r': singular_values[-1],
            'R_upper': np.sqrt(d - 1) * singular_values[0],
        })
    return {
        'd': d, 'B': b, 'L': lmat, 'M': m, 'normals': normals,
        'interventions': interventions,
        'permutations': np.array(list(itertools.permutations(range(d)))),
        'r_min': min(x['r'] for x in interventions),
        'R_max_upper': max(x['R_upper'] for x in interventions),
        'lambda_min_positive': min(x['singular_values'][-1] ** 2 / 3 for x in interventions),
        'lambda_max': max(x['singular_values'][0] ** 2 / 3 for x in interventions),
    }


def permutation_min(model, costs):
    values = costs[np.arange(model['d'])[None, :], model['permutations']].mean(axis=1)
    best = int(np.argmin(values))
    return float(values[best]), tuple(int(x) for x in model['permutations'][best])


def objectives(model, w):
    assert np.allclose(np.linalg.norm(w, axis=1), 1, atol=1e-12)
    # Rows are candidates, columns are intervention targets.
    projections = [w @ x['A'] for x in model['interventions']]
    widths = np.stack([2 * np.abs(x).sum(axis=1) for x in projections], axis=1)
    # Factorized covariance evaluation avoids cancellation near the true nullspace.
    covariance_costs = np.stack([(x * x).sum(axis=1) / 3 for x in projections], axis=1)
    minus = w[:, None, :] - model['normals'][None, :, :]
    plus = w[:, None, :] + model['normals'][None, :, :]
    distances_sq = np.minimum((minus * minus).sum(axis=2), (plus * plus).sum(axis=2))
    e_sq, p_e = permutation_min(model, widths * widths)
    esigma_sq, p_cov = permutation_min(model, covariance_costs)
    delta_sq, p_d = permutation_min(model, distances_sq)
    return {
        'E': np.sqrt(e_sq), 'Delta': np.sqrt(delta_sq), 'E_sigma_sq': esigma_sq,
        'permutation_width': p_e, 'permutation_delta': p_d,
        'permutation_covariance': p_cov,
    }


def model_geometry_checks(model, rng):
    d = model['d']
    residuals = []
    vertex_width_errors = []
    vertices_noise = np.array(list(itertools.product([-1., 1.], repeat=d - 1)))
    for x in model['interventions']:
        eps = rng.uniform(-1, 1, size=(300, d - 1))
        z = x['center_z'] + eps @ x['generators_z'].T
        residual = z @ model['L'].T
        residuals.append(np.max(np.abs(residual[:, x['keep']] - eps)))
        assert np.max(np.abs(z[:, x['i']] - x['c'])) < 1e-12
        y_vertices = x['center'] + vertices_noise @ x['A'].T
        directions = unit_rows(rng.normal(size=(100, d)))
        values = y_vertices @ directions.T
        width_vertices = values.max(axis=0) - values.min(axis=0)
        width_formula = 2 * np.abs(directions @ x['A']).sum(axis=1)
        vertex_width_errors.append(np.max(np.abs(width_vertices - width_formula)))
        assert np.linalg.norm(x['A'].T @ model['normals'][x['i']]) < 1e-12
        assert np.linalg.matrix_rank(x['A']) == d - 1
    return {
        'max_re_solved_scm_residual': float(max(residuals)),
        'max_vertex_vs_formula_width_error': float(max(vertex_width_errors)),
        'all_intervention_generator_ranks': [int(np.linalg.matrix_rank(x['A'])) for x in model['interventions']],
        'max_normal_annihilation_error': float(max(
            np.linalg.norm(x['A'].T @ model['normals'][x['i']]) for x in model['interventions']
        )),
    }


def trial_summary(model, rows):
    delta = np.array([x['Delta'] for x in rows])
    e = np.array([x['E'] for x in rows])
    cov = np.array([x['E_sigma_sq'] for x in rows])
    width_low = np.sqrt(2) * model['r_min'] * delta
    width_high = 2 * model['R_max_upper'] * delta
    cov_low = model['lambda_min_positive'] / 2 * delta ** 2
    cov_high = model['lambda_max'] * delta ** 2
    width_violations = (e + 1e-12 < width_low) | (e > width_high + 1e-12)
    cov_violations = (cov + 1e-14 < cov_low) | (cov > cov_high + 1e-14)
    assert not width_violations.any()
    assert not cov_violations.any()
    assert np.all(delta > 0)
    assert np.all(e > 0)
    return {
        'count': len(rows),
        'Delta_min': float(delta.min()), 'Delta_max': float(delta.max()),
        'E_over_Delta_min': float((e / delta).min()),
        'E_over_Delta_max': float((e / delta).max()),
        'E_sigma_sq_over_Delta_sq_min': float((cov / delta ** 2).min()),
        'E_sigma_sq_over_Delta_sq_max': float((cov / delta ** 2).max()),
        'E_over_width_lower_bound_min': float((e / width_low).min()),
        'E_over_width_upper_bound_max': float((e / width_high).max()),
        'cov_over_cov_lower_bound_min': float((cov / cov_low).min()),
        'cov_over_cov_upper_bound_max': float((cov / cov_high).max()),
        'width_bound_violations': int(width_violations.sum()),
        'covariance_bound_violations': int(cov_violations.sum()),
        'width_and_distance_optimal_assignment_disagreements': sum(
            x['permutation_width'] != x['permutation_delta'] for x in rows
        ),
    }


def run_trials(model, rng):
    d = model['d']
    planted = []
    for p in model['permutations']:
        signs = rng.choice([-1., 1.], size=(d, 1))
        planted.append(objectives(model, model['normals'][p] * signs))
    random_rows = [objectives(model, unit_rows(rng.normal(size=(d, d)))) for _ in range(N_RANDOM)]
    near_rows, by_scale = [], {}
    for scale in NEAR_SCALES:
        rows = []
        for _ in range(N_NEAR_PER_SCALE):
            perm = rng.permutation(d)
            signs = rng.choice([-1., 1.], size=(d, 1))
            w = unit_rows(model['normals'][perm] * signs + scale * rng.normal(size=(d, d)))
            rows.append(objectives(model, w))
        by_scale[str(scale)] = trial_summary(model, rows)
        near_rows.extend(rows)
    return {
        'planted_signed_permutation_count': len(planted),
        'planted_zero_set_max_E': float(max(x['E'] for x in planted)),
        'planted_zero_set_max_Delta': float(max(x['Delta'] for x in planted)),
        'planted_zero_set_max_E_sigma_sq': float(max(x['E_sigma_sq'] for x in planted)),
        'random': trial_summary(model, random_rows),
        'near_truth': trial_summary(model, near_rows),
        'near_truth_by_noise_scale': by_scale,
        'all': trial_summary(model, random_rows + near_rows),
    }


def partial_intervention_counterexample(model, rng):
    d = model['d']
    k = d - 1
    w = model['normals'].copy()
    while True:
        w[-1] = unit_rows(rng.normal(size=(1, d)))[0]
        full = objectives(model, w)
        if full['Delta'] > 0.15 and abs(np.linalg.det(w)) > 0.05:
            break
    # Min over injections from observed intervention labels to d candidate rows.
    assignments = list(itertools.permutations(range(d), k))
    values = []
    for assignment in assignments:
        widths = [2 * np.abs(model['interventions'][i]['A'].T @ w[assignment[i]]).sum() for i in range(k)]
        values.append(np.mean(np.square(widths)))
    partial_e = float(np.sqrt(min(values)))
    assert partial_e < 1e-12 and full['Delta'] > 0.15
    return {
        'observed_intervention_targets': list(range(k)), 'W': w,
        'det_W': float(np.linalg.det(w)),
        'partial_E_with_injective_matching': partial_e,
        'full_Delta': float(full['Delta']), 'full_E': float(full['E']),
        'interpretation': 'An invertible W fits every measured hyperplane but the missing normal is arbitrary; complete identification does not follow.',
    }


def gaussian_support_counterexample(model):
    x = model['interventions'][0]
    u, _, _ = np.linalg.svd(x['A'], full_matrices=False)
    w = u[:, 0]
    projected = x['A'].T @ w
    unit_noise = projected / np.linalg.norm(projected)
    scales = np.array([1., 10., 100., 1000.])
    separations = [float(w @ (x['A'] @ (2 * scale * unit_noise))) for scale in scales]
    return {
        'target': 0, 'unit_tangent_w': w,
        'support_noise_scales': scales, 'achievable_width_lower_witnesses': separations,
        'width_on_actual_normal': 0.0,
        'width_on_this_tangent_direction': 'infinity',
        'support_function_on_any_direction_with_A_transpose_w_nonzero': 'infinity',
        'interpretation': 'With Gaussian full support, K=center+range(A); these support points at arbitrarily large scale prove unbounded width. The compact-support width constants cannot be used.',
        'gaussian_population_covariance_eigenvalues': np.linalg.eigvalsh(x['A'] @ x['A'].T),
    }


def small_sample_counterexample(model, rng):
    d = model['d']
    n = d - 1  # N<d implies centered empirical rank <= N-1 < d-1.
    x = model['interventions'][0]
    eps = rng.uniform(-1, 1, size=(n, d - 1))
    y = x['center'] + eps @ x['A'].T
    centered = y - y.mean(axis=0)
    _, singular_values, vh = np.linalg.svd(centered, full_matrices=True)
    rank = int(np.linalg.matrix_rank(centered, tol=1e-12))
    null_basis = vh[rank:].T
    true_normal = model['normals'][0]
    candidate = null_basis[:, 0] - true_normal * (true_normal @ null_basis[:, 0])
    if np.linalg.norm(candidate) < 1e-8:
        candidate = null_basis[:, 1] - true_normal * (true_normal @ null_basis[:, 1])
    w = candidate / np.linalg.norm(candidate)
    sample_width = float(np.ptp(y @ w))
    sample_cov = centered.T @ centered / n
    sample_variance = float(np.mean((centered @ w) ** 2))
    population_variance = float(np.linalg.norm(x['A'].T @ w) ** 2 / 3)
    population_width = float(2 * np.abs(x['A'].T @ w).sum())
    assert sample_width < 1e-12 and sample_variance < 1e-24
    assert abs(w @ true_normal) < 1e-12
    assert population_width > 0.1 and population_variance > 0.01
    return {
        'd': d, 'N': n, 'target': 0, 'samples_Y': y,
        'centered_sample_rank': rank,
        'empirical_nullspace_dimension': d - rank,
        'population_nullspace_dimension': 1,
        'spurious_unit_normal': w,
        'spurious_dot_true_normal': float(w @ true_normal),
        'empirical_width': sample_width, 'empirical_variance_stable': sample_variance,
        'empirical_variance_direct_matrix': float(w @ sample_cov @ w),
        'population_width': population_width, 'population_variance': population_variance,
        'sign_invariant_distance_to_true_normal': float(np.sqrt(2)),
        'interpretation': 'Centered rank is at most N-1. When N<d, a rank d-1 population has at least one extra empirical null direction, regardless of optimizer.',
    }


def jsonable(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def main():
    rng = np.random.default_rng(SEED)
    report = {
        'seed': SEED, 'numpy_version': np.__version__,
        'dimensions': [3, 4], 'random_trials_per_dimension': N_RANDOM,
        'near_trials_per_scale_per_dimension': N_NEAR_PER_SCALE,
        'near_scales': NEAR_SCALES,
        'assumptions': ['M invertible', 'DAG linear SCM', 'independent Uniform[-1,1] exogenous noise',
                        'deterministic perfect single-coordinate interventions',
                        'all d targets for full identification', 'unit candidate normals',
                        'population supports/covariances', 'bijective assignment for full objectives'],
        'bounds': {
            'width': 'sqrt(2)*r_min*Delta <= E <= 2*R_max_upper*Delta',
            'covariance': '(lambda_min_positive/2)*Delta^2 <= E_sigma_sq <= lambda_max*Delta^2',
            'r_i': 'smallest nonzero singular value of A_i',
            'R_i_upper': 'sqrt(d-1)*largest singular value of A_i',
        },
        'models': {},
        'scope': 'Numerical checks and explicit counterexamples; numerical sampling is not a proof of universal claims.',
    }
    for d in report['dimensions']:
        model = build_model(d, rng)
        model_report = {
            'B': model['B'], 'M': model['M'], 'true_unit_normals': model['normals'],
            'mixing_condition_number': float(np.linalg.cond(model['M'])),
            'interventions': [{k: v for k, v in x.items() if k not in ['keep']} for x in model['interventions']],
            'constants': {k: model[k] for k in ['r_min', 'R_max_upper', 'lambda_min_positive', 'lambda_max']},
            'width_ratio_allowed_interval': [np.sqrt(2) * model['r_min'], 2 * model['R_max_upper']],
            'covariance_ratio_allowed_interval': [model['lambda_min_positive'] / 2, model['lambda_max']],
            'geometry_checks': model_geometry_checks(model, rng),
            'trials': run_trials(model, rng),
            'partial_interventions': partial_intervention_counterexample(model, rng),
            'gaussian_support': gaussian_support_counterexample(model),
            'small_sample': small_sample_counterexample(model, rng),
        }
        report['models'][str(d)] = model_report
        compact = {
            'd': d, 'geometry': model_report['geometry_checks'],
            'planted_max_E': model_report['trials']['planted_zero_set_max_E'],
            'all_trials': model_report['trials']['all'],
            'width_allowed': model_report['width_ratio_allowed_interval'],
            'covariance_allowed': model_report['covariance_ratio_allowed_interval'],
            'partial_E': model_report['partial_interventions']['partial_E_with_injective_matching'],
            'partial_full_Delta': model_report['partial_interventions']['full_Delta'],
            'sample_N': model_report['small_sample']['N'],
            'sample_null_dimension': model_report['small_sample']['empirical_nullspace_dimension'],
            'sample_spurious_width': model_report['small_sample']['empirical_width'],
            'sample_spurious_population_width': model_report['small_sample']['population_width'],
        }
        print(json.dumps(jsonable(compact), ensure_ascii=False))
    destination = Path(__file__).with_name('results.json')
    destination.write_text(json.dumps(jsonable(report), ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    print('Saved ' + str(destination.resolve()))


if __name__ == '__main__':
    main()
