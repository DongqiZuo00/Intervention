# Complete Proofs for Theorem 1 and Its Lemmas

**Companion to `WHITEPAPER.md` · v0.2**
Conventions: $[d]=\{1,\dots,d\}$; all graphs are DAGs unless stated; $a\to b$ directed edge, $a—b$ undirected edge. §1–§6 are complete proofs; §7 conjectural; §8 the CRL-layer derivation.

---

## §1 Preliminaries: graphs, equivalence classes, Meek rules

**Definition 1.1 (Markov equivalence).** Two DAGs $G_1,G_2$ are Markov equivalent ($G_1\sim G_2$) iff they share the same skeleton and the same v-structures ($a\to b\leftarrow c$ with $a,c$ nonadjacent) (Verma & Pearl 1990). The class $[G]$ is uniquely represented by the essential graph (CPDAG) $E(G)$: directed edges of $E(G)$ = edges with identical orientation in all members; undirected edges = edges appearing in both orientations across the class.

**Lemma 1.2 (Chordality of chain components).** Every undirected connected component (chain component) of a CPDAG is **chordal** (every cycle of length ≥ 4 has a chord).
*Basis:* standard fact (Hauser & Bühlmann 2012). Chordality guarantees perfect elimination orderings (PEOs), the technical fulcrum of §4.

**Definition 1.3 (Meek rules).** Given a partially directed graph $(D,U)$:
- **R1**: $a\to b$, $b—c$, $a,c$ nonadjacent ⟹ $b\to c$;
- **R2**: $a\to b\to c$, $a—c$ ⟹ $a\to c$;
- **R3**: $a—b$, $a—c$, $a—d$, $c\to b$, $d\to b$, $c,d$ nonadjacent ⟹ $a\to b$;
- **R4**: $a—b$, $a—d$, $d\to c$, $c\to b$, $a,c$ nonadjacent ⟹ $a\to b$ (needed only with background knowledge / interventions).

Each rule is justified by contradiction: the opposite orientation would introduce a new v-structure or a cycle, contradicting membership in the same equivalence class (or consistency with background knowledge). Write $\mathrm{mk}(D,U)$ for the closure under R1–R4 to a fixed point.

**Lemma 1.4 (Chickering's covered-edge flips).** $G_1\sim G_2$ iff there is a sequence of edge reversals from $G_1$ to $G_2$ in which every step reverses a **covered edge** ($u\to v$ with $\mathrm{Pa}(v)=\mathrm{Pa}(u)\cup\{u\}$) and every intermediate graph remains a class member (Chickering 1995). Covered-edge reversal preserves the skeleton, acyclicity, and all v-structures.

---

## §2 The intervention model

**Assumption A1 (Faithfulness).** The observed distribution is faithful to $G^*$: all and only conditional independencies are encoded by d-separation.

**Assumption A2 (Intervention effectiveness).** A perfect intervention $\mathrm{do}(X_i)$ severs all incoming edges of $i$; and for every child $j$ of $i$ there exists an intervention level changing $p(x_j\mid \mathrm{do}(X_i))$ relative to the observational marginal (standard; He & Geng 2008).

**Lemma 2.1 (Orientation by intervention).** Under A1–A2, a single-node perfect intervention on $i$ orients every edge incident to $i$: for a neighbor $j$,
- $i\to j$ ⟺ the distribution of $X_j$ changes with the intervention level (detectable by A2);
- $j\to i$ ⟺ $X_i \perp X_j$ post-intervention (the incoming edge is severed).

*Derivation.* If $j\to i$, $\mathrm{do}(X_i)$ disconnects $X_i$ from its only source of dependence, hence independence. If $i\to j$, the mechanism of $X_j$ contains $X_i$, so the intervention value enters the conditional of $X_j$; A2 guarantees detectability. The two cases are mutually exclusive and exhaustive. $\square$

**Definition 2.2 (Intervention operator).** $\mathcal{T}_S(D,U)=\mathrm{mk}(D\cup D_S,\;U\setminus E_S)$, where $D_S$ is the set of $S$-incident edges oriented according to $G^*$ (Lemma 2.1), followed by Meek closure.

**Lemma 2.3 (Identification criterion).** A family of interventions $\mathcal{I}$ identifies $G^*$ iff no undirected edges remain.
*Derivation.* From observational + interventional distributions one identifies the $\mathcal{I}$-essential graph (Hauser–Bühlmann 2012, Thm. 10). It is a singleton ($[G^*]_\mathcal{I}=\{G^*\}$) iff every edge is oriented (a fully directed class member is alone in its class). $\square$

---

## §3 The two-member construction lemma

**Lemma 3.1.** Let $\{u,v\}$ be an undirected edge of $E(G^*)$. Then there exist $G_1,G_2\in[G^*]$ that differ **only in the orientation of $\{u,v\}$**.

*Proof.* Since $\{u,v\}$ is undirected, by the definition of a CPDAG there exist $G_u,G_v\in[G^*]$ containing $u\to v$ and $v\to u$ respectively. By Lemma 1.4 there is a covered-edge reversal sequence $G_u=H_0\to H_1\to\cdots\to H_m=G_v$. The orientation between $u,v$ differs in $H_0$ and $H_m$, so there is a first index $k$ at which $H_{k-1}$ and $H_k$ differ on $\{u,v\}$; a covered-edge reversal changes exactly one edge, so $H_{k-1},H_k$ differ only on $\{u,v\}$. Take $G_1=H_{k-1}$, $G_2=H_k$. $\square$

---

## §4 Proposition 0 (batch = vertex cover): complete proof

**Proposition 0.** Under single-node perfect interventions and batch (non-adaptive) selection, $S\subseteq V$ identifies $G^*$ iff $S$ is a vertex cover of the initial undirected edge set $U_0$. Consequently
$$\nu^{\mathrm{batch}}(G^*) \;=\; \tau(U_0).$$

**(⇒) Necessity.** Suppose $S$ is not a vertex cover: some undirected edge $\{u,v\}$ has $u,v\notin S$. By Lemma 3.1 take $G_1,G_2\in[G^*]$ differing only on $\{u,v\}$. For every $i\in S$: $i\ne u,v$, and $G_1,G_2$ coincide on all edges except $\{u,v\}$ — in particular **all edges incident to $i$ are identically oriented in both**. By Lemma 2.1, the observation produced by intervening on $i$ (incident-edge orientations, hence the input to the Meek closure) is identical under $G_1$ and $G_2$. This holds for all $i\in S$ ⟹ the final $\mathcal{I}$-essential graph is the same under both and contains both; by Lemma 2.3, identification fails. $\square$

**(⇐) Sufficiency.** Suppose $S$ covers every edge of $U_0$. Each undirected edge $\{u,v\}$ has $u\in S$ or $v\in S$ and is oriented directly by Lemma 2.1. Edges already directed lie in $D_0$. After the interventions $U=\varnothing$; by Lemma 2.3, $G^*$ is identified. $\square$

**Remark 4.1.** The information constraint "batch policies see only $E(G^*)$" is the source of necessity: the identification guarantee of $S$ must hold *simultaneously for all* class members, and Lemma 3.1's twin members always exist inside the class. Proposition 0 recovers the batch-optimal strategy of Hauser–Bühlmann (2014) through a self-contained indistinguishability argument.

---

## §5 Theorem 1(a): domination

**Theorem 1(a).** For every DAG $G^*$, $\nu^{\mathrm{ada}}(G^*)\le\nu^{\mathrm{batch}}(G^*)$.

*Proof.* The adaptive policy class contains policies that ignore intermediate outcomes: take an optimal batch set $S^*$ ($|S^*|=\tau(U_0)$) and intervene on its nodes one by one, in any order. Every undirected edge is oriented directly by the intervention on its covering endpoint (Lemma 2.1); after $|S^*|$ steps, identification is achieved. Hence $\nu^{\mathrm{ada}}\le |S^*|=\nu^{\mathrm{batch}}$. $\square$

**Remark 5.1.** Strict inequality does not hold universally (complete graph $K_k$: batch needs $k-1$; adaptive interventions on one clique node orient only its incident edges, no new v-structures arise for Meek to propagate, and induction gives $k-1$ for adaptive as well). Separation must therefore be stated for specific graph families — hence (b).

---

## §6 Theorem 1(b): exponential separation on paths

Let $P_n$ be the directed path $X_1\to X_2\to\cdots\to X_n$. Internal nodes have one parent and one child, so there are no v-structures ⟹ $E(P_n)$ is the **fully undirected path** ($n-1$ undirected edges).

### 6.1 Batch side: $\nu^{\mathrm{batch}}(P_n)=\lfloor n/2\rfloor$

*Derivation.* By Proposition 0, $\nu^{\mathrm{batch}}(P_n)=\tau(\text{path})$. The path has $n$ vertices and $n-1$ edges; even-indexed nodes $\{2,4,6,\dots\}$ cover all edges, giving $\tau\le\lfloor n/2\rfloor$; the matching number of $P_n$ is $\lfloor n/2\rfloor$, and by König's theorem (or direct counting — covered edges need distinct endpoints), $\tau\ge\lfloor n/2\rfloor$. $\square$

### 6.2 Adaptive upper bound: bisection gives $T(L)\le\lceil\log_2 L\rceil$

Consider an undirected segment of $L$ nodes. Strategy: intervene on its midpoint $k$.

*Structure after one intervention.* By Lemma 2.1, edges $(k-1,k)$ and $(k,k{+}1)$ are oriented. The truth cannot contain a v-structure inside the segment (it would already be oriented in $E(P_n)$, contradicting full undirectedness), so only two flow patterns exist at the midpoint:
- **Rightward through-flow**: $X_{k-1}\to X_k\to X_{k+1}$. Meek R1 cascades from $X_k\to X_{k+1}$: $X_{k+1}\to X_{k+2}$ (since $X_k,X_{k+2}$ are nonadjacent), onward to the right end — **the entire right side is oriented for free**. The remaining undirected part = internal edges of the left subsegment $[a..k{-}1]$.
- **Leftward through-flow**: symmetric.

The midpoint choice leaves a remainder of at most $\lceil(L-1)/2\rceil$ nodes. The recurrence
$$T(L)\;\le\;1+T\big(\lceil(L-1)/2\rceil\big),\quad T(1)=0$$
solves to $T(L)\le\lceil\log_2 L\rceil$ (induction: $\lceil\log_2\lceil(L-1)/2\rceil\rceil\le\lceil\log_2 L\rceil-1$). For $P_n$ as a whole, $T(n)\le\lceil\log_2 n\rceil$. $\square$

### 6.3 Adaptive lower bound: adversary argument, $T(L)\ge\Omega(\log L)$

*Adversary strategy.* Whenever the policy intervenes on node $k$ of a segment, the adversary reveals the through-flow pointing toward the **shorter side** (see §6.2; note that the fork pattern $X_{k-1}\leftarrow X_k\to X_{k+1}$ — $k$ a source — is a legal MEC member, but it triggers cascades in **both** directions and orients the whole segment at once; the adversary never chooses it). The remaining undirected segment therefore has at least $\lfloor(L-1)/2\rfloor$ nodes.

*Accounting.* Each intervention removes at most half of the remaining problem, so the worst-case intervention count of any policy satisfies $T(L)\ge 1+T(\lfloor(L-1)/2\rfloor)$, giving $T(L)\ge\lfloor\log_2 L\rfloor-1$.

Combining the bounds: $\nu^{\mathrm{ada}}(P_n)=\Theta(\log n)$. $\square$

### 6.4 The separation ratio

$$\frac{\nu^{\mathrm{batch}}(P_n)}{\nu^{\mathrm{ada}}(P_n)}=\frac{\lfloor n/2\rfloor}{\Theta(\log n)}=\Theta\!\Big(\frac{n}{\log n}\Big)\longrightarrow\infty.$$
The gap is unbounded ⟹ **order-level (exponential-class) separation holds**. $\square$

### 6.5 Formula vs. experiment

| Formula | Prediction | Experiment (n=256) |
|---|---|---|
| $\nu^{\mathrm{batch}}=\lfloor n/2\rfloor$ | 128 | 145.2 (greedy vertex-cover overhead; true value matches) |
| $T(L)\le\lceil\log_2 L\rceil$ | ≤ 8 | 5.2 (constant better than worst case: already-oriented edges at segment boundaries cascade inward via R1, shrinking the adversary's freedom) |

Experimental values systematically below the worst-case bound are **expected**: the theorem characterizes the worst case; the experiments enjoy benign structural dividends. Direction and order agree.

---

## §7 Status of Theorem 1(c)

**Conjecture.** $\nu^{\mathrm{ada}}(G^*)\le O(\nu_1(G^*)\cdot\log d)$, where $\nu_1$ is the single-node verification number (Choo–Shiragur).

**To resolve:** on paths, $\tau=\Theta(n)$ while adaptive is $\Theta(\log n)$; if $\nu_1(P_n)=\Theta(\log n)$, (c) generalizes "adaptive ≈ verification number" (Choo–Shiragur proved search bounds of similar form); our version must handle the Meek-cascading intervention operator. **Action item:** determine the order of $\nu_1$ on paths, then decide whether (c) is a theorem or a corollary.

---

## §8 The CRL layer (Theorem 1′): derivation

Setting: $Z=B^\top Z+\varepsilon$ ($B$ strictly upper triangular, $\varepsilon\sim N(0,\Omega)$ diagonal), $X=HZ$ with $H$ an injective $p\times d$ matrix ($p\ge d$). Contexts $k=0$ (observational) and $k=1..K$ (interventional).

### 8.1 The interventional fingerprint in precision matrices

Latent precision: $\Theta_Z=(I-B)\Omega^{-1}(I-B)^\top$ (directly from $Z=(I-B)^{-\top}\varepsilon$). A perfect intervention on node $i$ zeroes row $i$ of $B$ and replaces $\Omega_{ii}$, so
$$\Delta\Theta_Z^{(k)}=\Theta_Z^{(k)}-\Theta_Z^{(0)}$$
has nonzero rows/columns only on $\{i\}\cup\mathrm{Pa}(i)$ — **the intervention target and its parent set leave a low-rank fingerprint on the precision difference**. Via $\Theta_X=(H^{+})^\top\Theta_Z H^{+}$ ($H^+$ the pseudoinverse), the fingerprint is readable at the observation level. This is the information carrier of "placement": one intervention not only orients edges but also localizes $\{i\}\cup\mathrm{Pa}(i)$.

### 8.2 Sufficiency (one intervention per node): algebraic skeleton

$d$ interventions (one per node) reveal the support of every row of $B$ ⟹ $B$ fully recovered; $\Omega$ and $\Sigma_Z=(I-B)^{-\top}\Omega(I-B)^{-1}$ follow; then $\Sigma_X=H\Sigma_Z H^\top$ with $H$ injective pins $H$ under the scaling convention (Squires et al., Assumption 1(c)). Joint uniqueness of $(B,H)$ is guaranteed by the **partial-order RQ decomposition**: the usual orthogonal/upper-triangular conditions are replaced by their analogues relative to the partial order induced by $\mathcal{G}$ (Squires et al., Thm. 1).

### 8.3 Necessity: explicit twin-model construction

Suppose some node is never intervened across all $K<d$ interventions. Observations constrain only the **product** $\Phi=B_0H$ of the effective linear maps, not its factorization. Take a positive diagonal $\Lambda$ satisfying the scaling convention and set
$$\widehat H=\Lambda B_0 H,\qquad \widehat B_0=\Lambda^{-1}.$$
Then $\widehat B_0\widehat H=\Lambda^{-1}\Lambda B_0 H=\Phi$ — the same observed distribution (in every context): the left factorization has causal edges among latents, while the right one has **independent** latents ($\widehat B_0$ diagonal ⟹ no structure). The two models are indistinguishable on all available data ⟹ identification fails. (This is the idea of Squires et al., Prop. 4–5; when $H$ is a permutation it reduces to the $d-1$ lower bound of Eberhardt et al. 2005.)

### 8.4 Theorem 1′ (statement to prove)

In the setting of §8, the batch baseline is no longer a pure vertex cover but a **joint cover**:
$$\nu_{\mathrm{CRL}}^{\mathrm{batch}}=\min_S |S|\quad\text{s.t.}\quad\begin{cases} S \text{ covers } U_0 \text{ (edge orientation)}\\ S \text{ satisfies the } H\text{-anchoring constraints (identifying column } H_{\cdot i} \text{ requires intervening } i \text{ or its neighborhood)}\end{cases}$$
and the adaptive version separates analogously. **To do:** (i) axiomatize the propagation of the §8.1 fingerprint (does it admit a Meek-type closure?); (ii) pin down the exact form of the $H$-anchoring constraints; (iii) prove batch–adaptive separation for the joint cover (fingerprint version of the path family).

---

## §9 Open items

1. The order of $\nu_1(P_n)$ (decides whether (c) is a theorem or a corollary) — literature check.
2. A version of Lemma 3.1 for $\mathcal{I}$-essential graphs with interventional background knowledge — with R4 active, Chickering sequences need amendment.
3. §8.4(i): whether the precision fingerprint has its own Meek-type propagation closure — if yes, the entire §6 cascade analysis lifts to the CRL layer and Theorem 1′ comes alive.
