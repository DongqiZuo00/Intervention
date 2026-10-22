# -*- coding: utf-8 -*-
"""
论文二 v0 最小实验：自适应 vs 批量 vs 随机干预选址
设定：线性高斯 DAG（变量已知层），研究"选址"问题本身
- 观测 MEC（CPDAG）由真实 DAG 经 v-structure + Meek 规则得到（隔离估计误差，纯测选址）
- 完美干预节点 i => 所有与 i 相连的未定向边按真实图定向，然后 Meek 闭包传播
- 指标：完全定向整个 DAG 所需的干预次数
"""
import numpy as np
import itertools
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- 图工具 ----------
def random_dag(d, exp_degree, rng):
    """ER 随机 DAG：随机拓扑序 + 上三角 Bernoulli"""
    p = min(1.0, exp_degree / max(d - 1, 1) * 2)
    order = rng.permutation(d)
    adj = np.zeros((d, d), dtype=bool)
    for a in range(d):
        for b in range(a + 1, d):
            if rng.random() < p:
                adj[order[a], order[b]] = True
    return adj  # adj[i,j]=True 表示 i->j


def skeleton_adj(adj):
    return adj | adj.T


def meek_closure(dir_mask, und_mask):
    """Meek R1-R4 闭包。dir_mask[i,j]: i->j; und_mask[i,j]: i—j（对称）"""
    d = dir_mask.shape[0]
    adj_any = dir_mask | dir_mask.T | und_mask
    changed = True
    while changed:
        changed = False
        for b in range(d):
            # R1: a->b, b—c, a,c 不相邻 => b->c
            for a in np.where(dir_mask[:, b])[0]:
                for c in np.where(und_mask[b])[0]:
                    if not adj_any[a, c] and a != c:
                        und_mask[b, c] = und_mask[c, b] = False
                        dir_mask[b, c] = True
                        adj_any[b, c] = adj_any[c, b] = True
                        changed = True
            # R2: a->b->c, a—c => a->c  (枚举 a,c 对)
        for a in range(d):
            for c in np.where(und_mask[a])[0]:
                if a == c:
                    continue
                if np.any(dir_mask[a] & dir_mask[:, c].T):
                    und_mask[a, c] = und_mask[c, a] = False
                    dir_mask[a, c] = True
                    changed = True
        for a in range(d):
            # R3: a—b, a—c, a—d, c->b, d->b, c,d 不相邻 => a->b
            for b in np.where(und_mask[a])[0]:
                if a == b:
                    continue
                cand = [c for c in np.where(und_mask[a] & dir_mask[:, b].T)[0]]
                found = False
                for c, e in itertools.combinations(cand, 2):
                    if not adj_any[c, e]:
                        found = True
                        break
                if found:
                    und_mask[a, b] = und_mask[b, a] = False
                    dir_mask[a, b] = True
                    changed = True
        adj_any = dir_mask | dir_mask.T | und_mask
        for a in range(d):
            # R4: a—b, a—d, d->c, c->b, a,c 不相邻 => a->b
            for b in np.where(und_mask[a])[0]:
                if a == b:
                    continue
                for dd in np.where(und_mask[a])[0]:
                    if dd in (a, b):
                        continue
                    for c in np.where(dir_mask[dd])[0]:
                        if dir_mask[c, b] and not adj_any[a, c] and c != a and c != b:
                            und_mask[a, b] = und_mask[b, a] = False
                            dir_mask[a, b] = True
                            changed = True
                            break
                    else:
                        continue
                    break
        adj_any = dir_mask | dir_mask.T | und_mask
    return dir_mask, und_mask


def cpdag_from_dag(adj):
    """观测 MEC：v-structure 定向 + Meek 闭包"""
    d = adj.shape[0]
    dir_mask = np.zeros((d, d), dtype=bool)
    und_mask = skeleton_adj(adj).copy()
    for j in range(d):
        parents = np.where(adj[:, j])[0]
        for a, b in itertools.combinations(parents, 2):
            if not skeleton_adj(adj)[a, b]:  # 不相邻亲本 => collider
                und_mask[a, j] = und_mask[j, a] = False
                und_mask[b, j] = und_mask[j, b] = False
                dir_mask[a, j] = True
                dir_mask[b, j] = True
    und_mask = und_mask & ~dir_mask & ~dir_mask.T
    return meek_closure(dir_mask, und_mask)


def intervene(dir_mask, und_mask, true_adj, nodes):
    """完美干预 nodes：所有与干预节点相连的未定向边按真实图定向 + Meek 闭包"""
    und = und_mask.copy()
    dr = dir_mask.copy()
    for i in nodes:
        for j in np.where(und[i])[0]:
            if true_adj[i, j]:
                und[i, j] = und[j, i] = False
                dr[i, j] = True
            elif true_adj[j, i]:
                und[i, j] = und[j, i] = False
                dr[j, i] = True
    und = und & ~dr & ~dr.T
    return meek_closure(dr, und)


def n_unoriented(und_mask):
    return int(und_mask.sum() // 2)


# ---------- 选址策略 ----------
def sel_random(dir_m, und_m, true_adj, rng):
    cnt = 0
    while n_unoriented(und_m) > 0 and cnt < 10 * dir_m.shape[0]:
        cand = np.where(und_m.any(axis=0))[0]
        i = int(rng.choice(cand))
        dir_m, und_m = intervene(dir_m, und_m, true_adj, [i])
        cnt += 1
    return cnt


def sel_adaptive(dir_m, und_m, true_adj, rng):
    """每步选"当前未定向关联边最多"的节点（熵准则的度近似），逐步利用上一步结果"""
    cnt = 0
    while n_unoriented(und_m) > 0 and cnt < 10 * dir_m.shape[0]:
        scores = und_m.sum(axis=0)
        i = int(np.argmax(scores))
        dir_m, und_m = intervene(dir_m, und_m, true_adj, [i])
        cnt += 1
    return cnt


def sel_batch(dir_m, und_m, true_adj, rng):
    """批量（公平版）：只能用初始 CPDAG，做未定向部分的贪心点覆盖（分离系统的近似），
    一次性全部干预。计划阶段不允许用真实图推演结果。"""
    uncovered = und_m.copy()
    plan = []
    while uncovered.any():
        scores = uncovered.sum(axis=0)
        i = int(np.argmax(scores))
        plan.append(i)
        uncovered[i, :] = uncovered[:, i] = False
    dir_m, und_m = intervene(dir_m, und_m, true_adj, plan)
    return len(plan)


def sel_oracle(dir_m, und_m, true_adj, rng):
    """下界参照：从同一个初始 CPDAG 出发，每步用真实图选"实际新增定向边最多"的节点。
    现实中不可得，仅作最优自适应轨迹的贪心近似。"""
    cnt = 0
    while n_unoriented(und_m) > 0 and cnt < dir_m.shape[0]:
        best, best_left = None, None
        for i in range(dir_m.shape[0]):
            d2, u2 = intervene(dir_m.copy(), und_m.copy(), true_adj, [i])
            left = n_unoriented(u2)
            if best_left is None or left < best_left:
                best, best_left = i, left
        dir_m, und_m = intervene(dir_m, und_m, true_adj, [best])
        cnt += 1
    return cnt


# ---------- 主实验 ----------
def main():
    rng = np.random.default_rng(20261021)
    ds = [5, 10, 15, 20, 30]
    n_graphs = 60
    exp_degree = 2.0
    strategies = {
        "oracle_lower_bound": sel_oracle,
        "adaptive_greedy": sel_adaptive,
        "batch_greedy": sel_batch,
        "random": sel_random,
    }
    results = {name: {d: [] for d in ds} for name in strategies}
    for d in ds:
        for g in range(n_graphs):
            true_adj = random_dag(d, exp_degree, rng)
            dir0, und0 = cpdag_from_dag(true_adj)
            for name, fn in strategies.items():
                c = fn(dir0.copy(), und0.copy(), true_adj, rng)
                results[name][d].append(c)
        print(f"d={d} done", flush=True)

    with open("results_v0.json", "w") as f:
        json.dump({k: {str(d): v for d, v in dd.items()} for k, dd in results.items()}, f)

    labels = {
        "oracle_lower_bound": ("Oracle adaptive (lower-bound ref)", "#888888", "--"),
        "adaptive_greedy": ("Adaptive (ours)", "#DD8452", "-"),
        "batch_greedy": ("Batch vertex-cover (fair)", "#4C72B0", "-"),
        "random": ("Random", "#55A868", "-"),
    }
    fig, ax = plt.subplots(figsize=(8, 5.2))
    for name, (lab, color, ls) in labels.items():
        means = [np.mean(results[name][d]) for d in ds]
        ses = [np.std(results[name][d]) / np.sqrt(n_graphs) for d in ds]
        ax.errorbar(ds, means, yerr=ses, label=lab, color=color, ls=ls,
                    marker="o", capsize=3, linewidth=2)
    ax.plot(ds, ds, "k:", alpha=0.4, label="One intervention per node (worst case)")
    ax.set_xlabel("Number of nodes d")
    ax.set_ylabel("Interventions until full identification")
    ax.set_title("Paper2 v0: adaptive vs batch vs random intervention selection")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("fig_v0_curve.png", dpi=160)
    print("saved fig_v0_curve.png")


if __name__ == "__main__":
    main()
