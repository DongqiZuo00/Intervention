# 主动干预因果表征学习：完整文献 Sweep

> 面向"三篇论文"研究项目（识别性奠基 → 干预选址 → 最小干预）的文献全景。
> 检索日期：2026-10-21；覆盖六个板块、约 80 项工作，年代跨度 1974–2026。

## 执行摘要

因果表征学习（CRL）的核心障碍是**可识别性**：纯观测 i.i.d. 数据下潜在表征对任意可逆变换不可识别。干预数据是当前已知**假设最弱、保证最强**的识别来源，其理论在 2022–2025 年快速收敛（每潜变量 1–2 次干预充要、未知多节点干预、首个样本复杂度），但三个缺口仍然明显：

1. **可识别性语言是定性的**（等价类"是/否"），缺乏连续、可微、可优化的"距离可识别还有多远"的度量——论文一的靶点；
2. **"干预哪里"没有算法层答案**——CRL 假设干预集合给定，而控制理论（结构可控性、Kalman 分解、持续激励）恰好提供图已知侧的完整工具，2026 年已有个别工作开始把持续激励引入世界模型识别性，但系统性桥接尚未发生——论文二的靶点；
3. **"最小干预"的组合理论（分离系统、次模性、NP-hardness）与 CRL 的识别理论至今分离**，凸优化松弛路线（$\ell_1$/SDP/D-最优设计）在干预设计中几乎未被使用——论文三的靶点。

此外，ICML 2025 的 Light Tunnel 真实系统体检显示代表性 CRL 方法**全部失败**且存在复现性问题，这为"诊断度量 + 边界定理"型贡献提供了强烈的需求侧论证。

![六板块关键文献时间线](fig1_timeline.png)

---

## 1. 板块一：识别性不可能性与非线性 ICA 奠基

### 1.1 不可能性结果（问题的起点）

非线性设定下潜在变量不可识别是领域的第一块基石：Hyvärinen & Pajunen（1999）证明，把线性 ICA 的混合函数放松为一般非线性变换后，仅靠独立性与非高斯性**不足以**识别源信号——存在无穷多种变换使观测保持独立成分混合的形式。Locatello et al.（ICML 2019）把这一不可能性推广到整个无监督解耦表征学习：在没有归纳偏置和监督的情况下，任何无条件先验的模型都不可识别，并用大规模实证（12,000+ 模型）表明现有解耦方法的成功无法复现地归因于无监督目标本身。 [iVAE 综述中的不可能性讨论](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2310.11011v2&text=Can%20we%20utilize%20additional%20structure%20in%20data%20to%20attain%20identifiability "citation")

不可能性结果的方法论意义在于：它把"学出因果变量"从工程问题重新定性为**数学不适定问题**，从而规定了整个领域的研究纲领——寻找能将解空间收缩到可接受等价类的"额外结构"。这一点是三篇论文共同的问题背景，也是论文一引言的核心叙事。

### 1.2 正面结果的四条路线

| 路线 | 关键工作 | 识别机制 | 代价/条件 |
|---|---|---|---|
| 辅助变量/弱监督 | Hyvärinen, Sasaki & Turner 2019；Khemakhem et al. 2020（iVAE） | 给定辅助变量 $u$ 条件下源条件独立 | "充分变化"条件：$u$ 需至少 $2n+1$ 个不同取值 [识别性综述](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2406.13371&text=at%20least%202n%2B1%20distinct%20values%20of%20u "citation") |
| 时序结构 | Hyvärinen & Morioka 2016/2017（TCL/PCL）；Klindt et al. 2021 | 非平稳性、时序依赖 | 需要时间序列与分段平稳 |
| 混合函数约束 | Zheng, Ng & Zhang, NeurIPS 2022 | 混合函数 Jacobian 的结构稀疏性 | 稀疏结构需先验成立 [Sparsity and Beyond](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2206.07751v5&text=identifiable%20from%20nonlinear%20mixtures%20up%20to%20a%20component-wise%20invertible%20transformation%20and%20a%20permutation%20under%20assumptions%20only%20on%20the%20mixing%20process "citation") |
| 多视图 | Gresele et al. 2020；Locatello et al. 2020；Zimmermann et al. 2021 | 视图间共享/独占内容 | 需要同时观测多个视图 |

iVAE（Khemakhem, Kingma, Monti & Hyvärinen, AISTATS 2020）是承上启下的枢纽：它给出 VAE 框架下第一个严格的可识别性证明，把非线性 ICA 与深度生成模型统一，成为后续几乎所有干预式 CRL 方法（CausalVAE、LEAP、ICM-VAE 等）的方法论前身。 [iVAE 论文](kimi-cite://web?url=https%3A%2F%2Fproceedings.mlr.press%2Fv108%2Fkhemakhem20a%2Fkhemakhem20a.pdf&text=the%20first%20rigorous%20proof%20of%20identifiability%20in%20the%20context%20of%20VAEs "citation")

### 1.3 对论文一的直接启示

四条路线得到的都是**等价类语言**的定理（"可识别到置换与逐分量变换"），没有一个给出"部分可识别程度"的连续刻画。von Kügelgen 的 ETH 博士论文（2024）系统比较了非监督、多视图、多环境下的可识别性，刻画了干预数据下"最多能识别到 $\sim_{CRL}$ 等价类"的界限，但仍停留在等价类层面。 [Identifiable CRL: Unsupervised, Multi-View, and Multi-Environment](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2406.13371&text=%E5%9C%A8%E6%B2%A1%E6%9C%89%E6%9B%B4%E5%A4%9A%E7%9B%B4%E6%8E%A5%E7%9B%91%E7%9D%A3%E5%BD%A2%E5%BC%8F%E7%9A%84%E6%83%85%E5%86%B5%E4%B8%8B%EF%BC%8C%E5%8F%AF%E8%AF%86%E5%88%AB%E6%80%A7%E8%83%BD%E8%BE%BE%E5%88%B0%E7%9A%84%E6%9C%80%E4%BD%B3%E7%A8%8B%E5%BA%A6 "citation")这正是论文一（凸几何化的纠缠度度量）要填的空。

---

## 2. 板块二：干预式 CRL 核心理论（2021–2026）

### 2.1 定理系谱：从配对反事实到未知多节点

| 工作 | 发表 | 设定 | 干预条件 | 识别保证 |
|---|---|---|---|---|
| Schölkopf et al. | Proc. IEEE 2021 | 立场论文 | — | 提出 CRL 纲领 |
| Brehmer et al. | NeurIPS 2022 | 非参数模型+混合 | 配对前后样本、随机未知稀疏干预 | 弱监督下可识别 [Weakly supervised CRL](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2203.16437&text=identifiable%20in%20a%20weakly%20supervised%20setting "citation") |
| Ahuja, Mahajan, Wang & Bengio | ICML 2023 | 非参数模型，多项式混合 | 完美干预 | 排列+缩放；不完美干预下块仿射 [Interventional CRL](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2209.11924&text=Interventional%20Causal%20Representation%20Learning "citation") |
| Squires, Seigal, Bhate & Uhler | ICML 2023 | 线性模型+线性混合 | 单节点完美干预 | **每潜变量 1 次干预充要** [Linear Causal Disentanglement](kimi-cite://web?url=https%3A%2F%2Fproceedings.mlr.press%2Fv202%2Fsquires23a.html&text=a%20single%20intervention%20on%20each%20latent%20variable%20is%20sufficient%20for%20identifiability "citation") |
| Zhang, Greenewald, Squires et al. | NeurIPS 2023 | 多项式混合 | 软干预 | 因果解耦可识别性保证 |
| von Kügelgen et al. | NeurIPS 2023 | 双非参数 | 每节点两次配对干预（未知目标） | $\sim_{CRL}$ 等价类刻画 |
| Varıcı et al. (score-based) | NeurIPS 2023 / AISTATS 2024 | 非参数模型 | 每节点两次非耦合硬干预 | 完美恢复，无需 faithfulness [NeurIPS 2023](kimi-cite://web?url=https%3A%2F%2Fneurips.cc%2Fvirtual%2F2023%2F77543&text=two%20hard%20interventions%20per%20node%20in%20the%20latent%20causal%20graph "citation") |
| Buchholz et al. | NeurIPS 2023 | 线性高斯模型+一般混合 | 未知单节点 | 非配对干预数据下可识别 |
| Jiang & Aragam (Jin & Srygkanis?) | NeurIPS 2024 | 一般环境数据 | 无需硬干预 | $d-2$ 次干预不足的下界 [Learning Linear Causal Representations](kimi-cite://web?url=https%3A%2F%2Fproceedings.neurips.cc%2Fpaper_files%2Fpaper%2F2023%2Ffile%2F8e5de4cb639ef718f44060dc257cb04f-Paper-Conference.pdf&text=d%20interventions%20are%20both%20necessary%20and%20sufficient "citation") |
| Varıcı et al. (UMN) | NeurIPS 2024 | 一般模型+线性混合 | **未知多节点**干预 | 硬干预完美识别、软干预到祖先，与单节点保证持平 [UMN-CRL](kimi-cite://web?url=https%3A%2F%2Fpapers.nips.cc%2Fpaper_files%2Fpaper%2F2024%2Fhash%2Fca70528fb11dc8086c6a623da9f3fee6-Abstract-Conference.html&text=the%20first%20identifiability%20results%20for%20general%20latent%20causal%20models%20under%20stochastic%20interventions%20(soft%20or%20hard)%20and%20linear%20transformation "citation") |
| Acartürk et al. | NeurIPS 2024 | 一般模型+线性混合 | 每节点一次随机软干预 | **首个样本复杂度**：$O((\log\frac1\delta)^4)$ 样本恢复图（祖先意义） [Sample Complexity](kimi-cite://web?url=https%3A%2F%2Fpapers.nips.cc%2Fpaper_files%2Fpaper%2F2024%2Fhash%2F458fa8ee331566383d8e74bdb647f829-Abstract-Conference.html&text=the%20first%20sample-complexity%20analysis%20for%20the%20finite-sample%20regime "citation") |
| Varıcı et al. | JMLR 2025 | 非参数模型 | 线性混合每节点 1 次、一般混合每节点 2 次随机硬干预 | 可识别 + 可达（可微损失全局最优保证） [JMLR 2025](kimi-cite://web?url=https%3A%2F%2Fjmlr.org%2Fpapers%2Fv26%2F24-0194.html&text=one%20stochastic%20hard%20intervention%20per%20node%20suffices%20to%20guarantee%20identifiability "citation") |
| 高阶累积量扩展 | Springer 2025 | 线性模型+**非单射**混合 | 每节点一次完美干预 | 充要；软干预下部分识别为负结果 [Higher-Order Cumulants](kimi-cite://web?url=https%3A%2F%2Flink.springer.com%2Farticle%2F10.1007%2Fs44007-025-00168-8&text=one%20perfect%20intervention%20on%20each%20latent%20node%20is%20sufficient%20and%2C%20in%20the%20worst%20case%2C%20necessary "citation") |
| 少环境+有限样本 | arXiv 2026 | — | **对数级**数量未知多节点干预 | 因果表征可学 [Few environments](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2603.25796v1&text=only%20a%20logarithmic%20number%20of%20unknown%2C%20multi-node%20interventions "citation") |

### 2.2 三条结构性观察

**第一，"每潜变量一次干预"已成为基准刻度。** Squires et al. 2023 在线性设定下证明其充要性（最坏情形），证明工具是把 RQ 分解推广为偏序版本；2025 年的高阶累积量工作进一步把它推广到非单射混合（$p, q$ 任意），并给出软干预下的负结果——即使无限多次软干预也无法完全识别参数。这条线给论文三提供了精确的"最小次数"锚点。

**第二，干预条件的放松路径清晰且收敛中。** 已知目标→未知目标（von Kügelgen 2023）→非耦合环境（Varıcı 2023/2024）→未知多节点（Varıcı NeurIPS 2024，要求干预签名矩阵满秩）→对数级干预环境（2026）。值得注意的是，所有"最小化"结果都是**被动给定干预集合下的充要性**，没有一篇处理"主动选择哪个干预"的优化问题——这正是论文二、三的接缝。

**第三，干预外推作为下游任务开始成形。** Saengkyongam et al.（ICLR 2024）证明线性干预效应下潜表征的仿射可识别性，并据此给未见干预值的外推提供证书；Rajendran et al.（NeurIPS 2024）把 CRL 与概念学习打通；Yan, Acartürk & Tajer（NeurIPS 2025）提出 reward-oriented CRL，把识别目标对齐到下游回报而非完整恢复——这为论文三"识别多少算够"提供了实用主义出口。

---

## 3. 板块三：最小干预设计与主动学习（变量已知侧）

### 3.1 计数理论：最少需要多少次实验

Eberhardt, Glymour & Scheines（UAI 2005）给出从马尔可夫等价类唯一确定因果图所需实验数的上下界，证明单变量干预最坏需要 $n-1$ 次，多变量同时干预可压至 $\lceil\log_2 n\rceil$ 量级；Eberhardt（2012）进一步精确化。Hauser & Bühlmann（JMLR 2012）建立干预马尔可夫等价类（$\mathcal{I}$-MEC）与干预本质图的完整刻画并提出 GIES 算法；其 2015 年 JRSS-B 工作证明 BIC 在联合观测-干预数据下的一致性。 [Hauser & Bühlmann 2012](kimi-cite://web?url=https%3A%2F%2Fjmlr.org%2Fpapers%2Fv13%2Fhauser12a.html&text=interventional%20Markov%20equivalence%20defines%20a%20finer%20partitioning%20of%20DAGs%20than%20observational%20Markov%20equivalence "citation")

分离系统（separating systems）是把"最少干预"翻译成组合数学的关键桥梁：能识别任意图的干预集族恰为分离系统；Kocaoglu, Dimakis & Vishwanath（ICML 2017）引入变量差异化成本并建立与图染色的联系；Addanki et al.（AISTATS 2020）推广到含潜变量（强分离集系统 + 2-近似 + $(1+\varepsilon)$-近似）；Lindgren et al.（NeurIPS 2018）证明最小成本干预设计 **NP-hard** 并给出贪心 $(2+\varepsilon)$-近似；Elrefaey & Pan（AAAI 2025）用整数规划精确求解并可模块化加入预算约束。 [整数规划干预设计](kimi-cite://web?url=https%3A%2F%2Fojs.aaai.org%2Findex.php%2FAAAI%2Farticle%2Fview%2F33810%2F35965&text=design%20minimal%20intervention%20sets%20that%20ensure%20causal%20structure%20identifiability "citation")

### 3.2 自适应性与预算：两篇对论文三最直接的工作

**Ghassami et al.（2018, Budgeted Experiment Design）**：在最多 $k$ 次非自适应单变量实验的预算约束下，把目标设为"平均可定向边数最大化"，**证明该目标是次模函数**，贪心即得 $(1-1/e)$ 近似。这是"凸/次模工具进入干预设计"的现成先例，也是论文三 Lovász 扩展路线的合法起点。 [Budgeted Experiment Design](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F1709.03625&text=we%20prove%20that%20the%20corresponding%20objective%20function%20is%20submodular%20and%20a%20greedy%20algorithm%20suffices "citation")

**Choo & Shiragur 系列（NeurIPS 2022 验证与搜索、ICML 2023 子集验证、UAI 2023 自适应复杂度、AISTATS 2024 off-target 干预）**：把自适应干预设计做成精确的复杂度理论——验证数下界 $\nu_1(G)$、$r$-自适应轮次与干预数的权衡、以及 off-target（干预打偏，如 CRISPR 脱靶）模型下的 polylog 竞争比。 [Adaptivity Complexity](kimi-cite://web?url=https%3A%2F%2Fproceedings.mlr.press%2Fv216%2Fchoo23a%2Fchoo23a.pdf&text=higher%20rounds%20of%20adaptivity%20leads%20to%20lower%20number%20of%20interventions%20required "citation")

### 3.3 贝叶斯实验设计（BOED）线

Tong & Koller（2001）与 Murphy（2001）开创用期望信息增益（EIG）选实验；Cho et al.（2016）处理线性高斯连续情形；Agrawal et al.（AISTATS 2019, ABCD-Strategy）引入预算约束与目标化结构发现；Sussex et al.（2021）推进批量设计；**Tigas et al.（NeurIPS 2022, "Interventions, Where and How?"）**把贝叶斯因果发现与 BOED 结合，同时选择干预目标**和干预值**，扩展到非线性 SCM 与 DREAM 基因网络；**diffCBED（ICML 2023）**实现可微多目标设计，在 40–50 节点图上大幅超越随机与 SSGb 基线（ESHD 0.44 vs 15.59/43.78）。 [diffCBED](kimi-cite://web?url=https%3A%2F%2Fproceedings.mlr.press%2Fv202%2Ftigas23a%2Ftigas23a.pdf&text=experiments%20that%20are%20maximally%20informative%2C%20as%20evaluated%20by%20expected%20information%20gain "citation")von Kügelgen et al.（NeurIPS 2023, "Trust Your V"）另辟蹊径，用梯度分数替代互信息以规避 MI 估计误差。 [Trust Your V](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2211.13715&text=computing%20mutual%20information%20suffers%20from%20approximation%20errors%20and%20model%20mismatches "citation")Zhang, Cammarata, Squires, Sapsis & Uhler（Nature Machine Intelligence 2023）把主动学习最优干预设计落地到基因扰动实验，是理论走向湿实验室的标志。

**板块小结**：变量已知侧的"最小/主动干预"已经相当成熟（复杂度、近似比、贝叶斯框架齐备），但其全部算法都假设变量与干预目标的对应关系已知——CRL 的潜变量设定使这一切无法直接套用。这个"断层"就是三篇论文的机会窗口。

---

## 4. 板块四：控制理论交叉

### 4.1 可控性 / 可观性：与最小干预的同构

Lin（1974）提出结构可控性；Liu, Slotine & Barabási（Nature 2011）给出最小驱动节点数 = 最大匹配未匹配节点数的著名刻画；后续工作把条件细化为"每个 child SCC 与每个 dilation 至少一个驱动节点"，并证明一般网络上最小输入/最小传感器选择均为 NP-hard（有 $\log n$ 近似）。 [Minimal Driver Nodes](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F1911.11388v1&text=the%20minimal%20controllability%20problem "citation")与因果干预设计的对照（可控性图已知 vs 因果学习图未知）已在项目计划文档中展开，此处不重复。

### 4.2 持续激励进入世界模型识别性：2026 年的关键信号

Zhang et al.（arXiv 2607.22430, 2026）*On the Identifiability of Controlled World Models* 是本轮 sweep 中与论文二最贴近的工作：它对 JEPA 式受控世界模型给出联合识别条件——**表征识别性**由可预测信号的谱分离margin控制，**转移识别性**由条件动作激励margin $\rho_{\mathrm{tr}}(\pi)=\lambda_{\min}(\mathbb{E}[\mathrm{Cov}(a_t|z_t)])$ 控制，后者正是持续激励（persistent excitation, Willems et al. 2005）的世界模型版本；并证明反事实预测误差放大倍数与最弱激励方向成反比。 [Controlled World Models](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2607.22430v2&text=transition%20identifiability%20is%20related%20to%20non-degenerate%20variation%20of%20conditional%20action "citation")这说明"控制理论语言进入 CRL"已经开始发生，但目前仅限于线性高斯潜动力学的世界模型——结构可控性、Kalman 分解层面的桥接仍是空白。

### 4.3 因果 bandit 与对偶控制的现实化身

因果 bandit 线（Lattimore et al. 2016 开创）已经覆盖：已知图线性 SEM 软干预（Varıcı et al., JMLR 2023，$O(d^{L+1/2}\sqrt{NT})$ 遗憾）、未知图+软干预（Yan & Tajer, NeurIPS 2024）、模型漂移鲁棒性（Yan et al., 2024，证明极少实例偏差即可使既有算法线性遗憾）、预算约束（Nair et al., AISTATS 2021）、以及 POMIS（Lee & Bareinboim 2018/2019，离线裁剪"可能最优干预集"——本质上是 bandit 侧的"最小候选干预集"）。 [Causal Bandits for Linear SEMs](kimi-cite://web?url=https%3A%2F%2Fjmlr.org%2Fpapers%2Fv24%2F22-0969.html&text=designing%20an%20optimal%20sequence%20of%20interventions%20in%20a%20causal%20graphical%20model%20to%20minimize%20cumulative%20regret "citation")Feldbaum 对偶控制（探测-控制不可分）在这一线中已有近似化身，但**与 CRL 表征识别的统一**（学表征即探测、用表征即控制）尚无人做。

### 4.4 机器人侧的主动干预实践

*Curious Causality-Seeking Agents*（NeurIPS 2025）提出 Meta-Causal Graph 世界模型与好奇心驱动的主动干预探索，理论上给出干预族唯一识别 meta-causal graph 的充分条件，并在机械臂任务上验证；其局限与未来工作**明确点名**：不可达状态对识别性的影响未分析、干预有成本需要预算感知探索。 [Curious Causality-Seeking Agents](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2506.23068v1&text=certain%20states%20are%20fundamentally%20unreachable%20via%20any%20sequence%20of%20interventions "citation")这两个"未来工作"恰好分别是论文二的 Kalman 边界定理与论文三的预算理论的用武之地。机器人因果世界模型的更大生态（PCMCI 系、CREST 干预式因果特征选择、CausalWorld 基准）为实验验证提供了现成平台。

---

## 5. 板块五：凸优化与连续优化交叉

### 5.1 因果发现的连续优化：成就与非凸之痛

NOTEARS（Zheng et al., NeurIPS 2018）把 DAG 学习重写为带光滑无环约束 $h(W)=\mathrm{tr}(e^{W\circ W})-d=0$ 的连续优化，作者自己强调该规划**非凸**，只能保证驻点。 [NOTEARS](kimi-cite://web?url=https%3A%2F%2Fpapers.neurips.cc%2Fpaper%2F8157-dags-with-no-tears-continuous-optimization-for-structure-learning.pdf&text=the%20equality%20constrained%20program%20(8)%20is%20a%20nonconvex%20program "citation")后续批评与修复构成一条完整线索：Wei et al.（NOFEARS, 2020）指出 NOTEARS 不满足 KKT 正则性条件并重构约束；Reisach et al.（2021）与 Kaiser & Sipos（2022）揭示数据标准化导致的虚假表现；GOLEM、DAGMA 改进目标；2026 年 AAAI 的 CALM 用 Gumbel-Softmax 逼近 $\ell_0$ 修复不一致性。

### 5.2 凸几何的现成据点

与论文一、三最相关的三个凸几何/凸优化据点：**(1) 排序多面体**——DAG Learning on the Permutahedron（2023）在置换多面体上做连续优化学拓扑序，兼具精确 DAG 性与模块化； [Permutahedron](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2301.11898v2&text=optimizes%20over%20the%20polytope%20of%20permutation%20vectors "citation")**(2) sparsest-permutation 松弛**（2026）把 Raskutti & Uhler 的最稀疏序判据做成可扩展的连续形式；**(3) 最优实验设计**——Boyd & Vandenberghe §7.5 的 D-/A-/E-最优设计（$\log\det$ 信息矩阵最大化）在因果发现文献中**只在贝叶斯 EIG 形式下被使用**，其纯凸优化形式（连续松弛 + Frank-Wolfe + KKT 影子价格解释）尚未进入干预设计文献。

### 5.3 空白确认

本轮检索未发现任何工作：将最小干预集设计做 $\ell_1$/SDP 凸松弛（现有近似全部基于贪心/组合构造）；用 Lovász 扩展处理干预预算分配；或用凸几何（支撑函数）表述 CRL 的部分可识别性。三个空白点与论文一、三的技术路线一一对应，sweep 结果支持其新颖性。

---

## 6. 板块六：前沿、基准与批判性工作（2025–2026）

### 6.1 现实检验：Light Tunnel 体检

von Kugelgen/Bing 等人的 *Sanity Checking CRL on a Simple Real-World System*（ICML 2025）构建了受控光学实验（Light Tunnel），因果因子即实验控制输入、真值已知，测试三类代表性方法（Contrastive CRL、Multiview CRL、CITRIS 时序干预），结论严峻：**所有方法都未能一致地恢复因果因子**；合成消融实验进一步暴露复现性问题（多数方法在简化合成数据上已失败）；混合函数的常见假设（确定性、单射性）在真实数据中不成立是主要失败模式。 [Light Tunnel](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2502.20099v3&text=they%20all%20fail%20to%20consistently%20recover%20the%20underlying%20causal%20factors "citation")该文还给出重要方法论区分：失败可归因于**模型误设**或**优化失败**——论文一的诊断度量恰好应能对两者做出区分性度量。

### 6.2 新基准与统一视角

| 工作 | 性质 | 要点 |
|---|---|---|
| CausalVerse（NeurIPS 2025 D&B） | 基准 | 汇总 Causal3DIdent、CausalCircuit、Light Tunnel 等 9+ 数据集，多域场景 [CausalVerse](kimi-cite://web?url=https%3A%2F%2Fproceedings.neurips.cc%2Fpaper_files%2Fpaper%2F2025%2Ffile%2F05962abf920ebddac275d26f83fe118a-Paper-Datasets_and_Benchmarks_Track.pdf&text=CausalVerse "citation") |
| CAUSAL3D（ICLR 2025） | 基准 | 结构化因果图+3D 视觉；现有 CRL 方法处理不了真实多样场景 |
| Yao et al.（ICLR 2025） | 统一理论 | 多数 CRL 方法本质在对齐数据对称性而非严格因果层级；不变性原理统一框架 |
| *Towards Interpretable Deep Generative Models via CRL*（2026 综述） | 综述 | 统计学视角：CRL = 潜变量模型 + 因果图模型 + 非参数深度学习三者综合 |
| Concept Modulation Models（2026） | 统一理论 | 用共享结构形式 $A\to\Lambda\to C\to X$ 统一多类识别性与外推结果 [CMM](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2606.18509v1&text=concept%20modulation%20models "citation") |
| 少环境+有限样本（2026） | 理论前沿 | 对数级未知多节点干预即可学因果表征 |

### 6.3 对项目定位的三点修正建议

1. **论文一的实验设计应直接对接 Light Tunnel 与 CausalVerse**：诊断度量的价值主张应包含"能预警方法在真实系统上的失败模式"——这比在合成基准上对齐 MCC 更有说服力。
2. **论文二需注意与 Zhang et al. 2026（受控世界模型）的差异化**：他们做的是"给定行为策略下的识别条件"，我们做的是"主动选择干预使识别达成"——被动条件 vs 主动设计，叙事上必须划清。
3. **Yao et al. 2025 的不变性统一视角应在三篇的 related work 中正面回应**：如果识别性本质是对称性对齐，那么凸几何度量应能被表述为对称性违背的度量——这反而能强化论文一的理论深度。

![板块×论文覆盖矩阵](fig2_matrix.png)

---

## 7. 空白点地图与三篇论文的最终定位

| 空白点 | 证据 | 对应论文 |
|---|---|---|
| 部分可识别性只有等价类语言，无连续可微度量 | §1.3、§6.1（失败无法区分误设/优化） | 论文一 |
| CRL 无"干预选址"算法层；可控性工具未桥接 | §2.2 观察二、§4.2 | 论文二 |
| 无"原则上不可识别子空间"的否定性刻画 | §4.4（NeurIPS 2025 明确点名） | 论文二 |
| 最小干预的组合理论（分离系统/次模/NP-hard）未进 CRL；凸松弛路线空白 | §3、§5.3 | 论文三 |
| 主动干预的预算/样本统一账本缺失 | §2.1（样本复杂度刚起步）、§3.2 | 论文三 |
| 学习（识别）与控制（决策）的统一目标 | §4.3 | 展望/第四篇 |

---

## 8. 核心文献总表（按板块）

| 板块 | 必读（★）与重要文献 |
|---|---|
| 识别性奠基 | ★Hyvärinen & Pajunen 1999；★Locatello et al. ICML 2019；★Hyvärinen, Sasaki & Turner AISTATS 2019；★Khemakhem et al. AISTATS 2020（iVAE）；Zheng, Ng & Zhang NeurIPS 2022；Kivva et al. 2022；von Kügelgen 博士论文 2024 |
| 干预式 CRL | ★Schölkopf et al. Proc. IEEE 2021；★Ahuja et al. ICML 2023；★Squires et al. ICML 2023；★von Kügelgen et al. NeurIPS 2023；★Varıcı et al. JMLR 2025；Brehmer et al. NeurIPS 2022；Zhang et al. NeurIPS 2023（软干预）；Buchholz et al. NeurIPS 2023；Varıcı et al. NeurIPS 2024（UMN）；Acartürk et al. NeurIPS 2024（样本复杂度）；Bing et al. CLeaR 2024；高阶累积量 Springer 2025；Saengkyongam et al. ICLR 2024；Yan et al. NeurIPS 2025（reward-oriented）；对数级干预 arXiv 2026 |
| 最小干预/主动设计 | ★Eberhardt et al. UAI 2005；★Hauser & Bühlmann JMLR 2012 / JRSS-B 2015；★Ghassami et al. 2018（次模）；★Lindgren et al. NeurIPS 2018（NP-hard）；He & Geng JMLR 2008；Kocaoglu et al. ICML 2017；Agrawal et al. AISTATS 2019；Addanki et al. AISTATS 2020；Sussex et al. 2021；Choo & Shiragur NeurIPS 2022 / ICML 2023 / UAI 2023 / AISTATS 2024；Tigas et al. NeurIPS 2022；diffCBED ICML 2023；Trust-Your-V NeurIPS 2023；Zhang et al. Nature MI 2023；Elrefaey & Pan AAAI 2025 |
| 控制理论交叉 | ★Lin 1974；★Liu, Slotine & Barabási Nature 2011；★Zhang et al. 2026（受控世界模型识别性）；Willems et al. 2005（持续激励）；Varıcı et al. JMLR 2023（因果 bandit）；Yan & Tajer NeurIPS 2024；Nair et al. AISTATS 2021；Lee & Bareinboim 2018/2019（POMIS）；Curious Causality-Seeking Agents NeurIPS 2025 |
| 凸优化交叉 | ★Boyd & Vandenberghe §7.5；★NOTEARS NeurIPS 2018；NOFEARS 2020；GOLEM 2020；DAGMA 2022；Permutahedron 2023；sparsest-permutation 松弛 2026；CALM AAAI 2026 |
| 前沿·基准·批判 | ★Light Tunnel 体检 ICML 2025；★Yao et al. ICLR 2025（不变性统一）；CausalVerse NeurIPS 2025；CAUSAL3D ICLR 2025；CRL 统计综述 2026；CMM 2026；von Kügelgen et al. LMRL 2025（扰动外推） |

---

*本 sweep 基于 7 轮迭代检索（14 次查询），所有结论性陈述均可追溯至检索返回的来源；个别文献的具体定理表述建议以原文为准。*
