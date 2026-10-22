# -*- coding: utf-8 -*-
"""
定理 1(b) 验证：路径族 P_n 上的批量 vs 自适应分离
预言：batch = floor(n/2)，adaptive = Theta(log n)
"""
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from exp_v0 import meek_closure, cpdag_from_dag, intervene, n_unoriented


def path_dag(n, rng):
    """有向路径，节点标签随机打乱（结构不变，防实现捷径）"""
    perm = rng.permutation(n)
    adj = np.zeros((n, n), dtype=bool)
    for k in range(n - 1):
        adj[perm[k], perm[k + 1]] = True
    return adj


def und_components_centers(und):
    """返回每个未定向连通分量（路径段）的中心节点"""
    seen = np.zeros(und.shape[0], dtype=bool)
    centers = []
    for s in range(und.shape[0]):
        if seen[s] or not und[s].any():
            continue
        comp, stack = [s], [s]
        seen[s] = True
        while stack:
            u = stack.pop()
            for v in np.where(und[u])[0]:
                if not seen[v]:
                    seen[v] = True
                    comp.append(v)
                    stack.append(v)
        # 段内 BFS 找偏心距最小的节点（中心）
        comp = sorted(comp)
        sub = und[np.ix_(comp, comp)]
        best, best_ecc = comp[0], None
        for idx, u in enumerate(comp):
            dist = {u: 0}
            q = [u]
            while q:
                x = q.pop(0)
                for j, v in enumerate(comp):
                    if sub[idx][j] and v not in dist:
                        dist[v] = dist[x] + 1
                        q.append(v)
            ecc = max(dist.values())
            if best_ecc is None or ecc < best_ecc:
                best, best_ecc = u, ecc
        centers.append((best, len(comp)))
    return centers


def sel_adaptive_bisect(dir_m, und_m, true_adj, rng):
    """定理 1(b) 的策略：对最长未定向段取中点干预"""
    cnt = 0
    while n_unoriented(und_m) > 0 and cnt < 4 * dir_m.shape[0]:
        centers = und_components_centers(und_m)
        node = max(centers, key=lambda t: t[1])[0]
        dir_m, und_m = intervene(dir_m, und_m, true_adj, [node])
        cnt += 1
    return cnt


def sel_batch_cover(dir_m, und_m, true_adj, rng):
    uncovered = und_m.copy()
    plan = []
    while uncovered.any():
        scores = uncovered.sum(axis=0)
        i = int(np.argmax(scores + rng.random(len(scores)) * 1e-9))
        plan.append(i)
        uncovered[i, :] = uncovered[:, i] = False
    dir_m, und_m = intervene(dir_m, und_m, true_adj, plan)
    return len(plan)


def sel_random(dir_m, und_m, true_adj, rng):
    cnt = 0
    while n_unoriented(und_m) > 0 and cnt < 4 * dir_m.shape[0]:
        cand = np.where(und_m.any(axis=0))[0]
        i = int(rng.choice(cand))
        dir_m, und_m = intervene(dir_m, und_m, true_adj, [i])
        cnt += 1
    return cnt


def main():
    rng = np.random.default_rng(7)
    ns = [8, 16, 32, 64, 128, 256]
    reps = 40
    res = {"adaptive_bisect": {}, "batch_cover": {}, "random": {}}
    for n in ns:
        for name in res:
            res[name][n] = []
        for r in range(reps):
            true_adj = path_dag(n, rng)
            dir0, und0 = cpdag_from_dag(true_adj)
            assert n_unoriented(und0) == n - 1, "路径的 CPDAG 应完全未定向"
            res["adaptive_bisect"][n].append(sel_adaptive_bisect(dir0.copy(), und0.copy(), true_adj, rng))
            res["batch_cover"][n].append(sel_batch_cover(dir0.copy(), und0.copy(), true_adj, rng))
            res["random"][n].append(sel_random(dir0.copy(), und0.copy(), true_adj, rng))
        print(f"n={n} done", flush=True)

    with open("results_path.json", "w") as f:
        json.dump({k: {str(n): v for n, v in dd.items()} for k, dd in res.items()}, f)

    fig, ax = plt.subplots(figsize=(8, 5.2))
    styles = {"adaptive_bisect": ("Adaptive bisection (Thm.1b)", "#DD8452", "o"),
              "batch_cover": ("Batch = vertex cover", "#4C72B0", "s"),
              "random": ("Random", "#55A868", "^")}
    for name, (lab, color, mk) in styles.items():
        means = [np.mean(res[name][n]) for n in ns]
        ses = [np.std(res[name][n]) / np.sqrt(reps) for n in ns]
        ax.errorbar(ns, means, yerr=ses, label=lab, color=color, marker=mk, capsize=3, linewidth=2)
    ax.plot(ns, [n // 2 for n in ns], "b--", alpha=0.5, label="floor(n/2) (Thm.1b batch)")
    ax.plot(ns, np.ceil(np.log2(ns)), color="#DD8452", ls="--", alpha=0.5, label="ceil(log2 n) (Thm.1b adaptive)")
    ax.set_xscale("log", base=2)
    ax.set_xticks(ns); ax.set_xticklabels(ns)
    ax.set_xlabel("Path length n (log2 scale)")
    ax.set_ylabel("Interventions until full identification")
    ax.set_title("Theorem 1(b): exponential separation on path graphs")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig("fig_path_separation.png", dpi=160)
    print("saved fig_path_separation.png")


if __name__ == "__main__":
    main()
