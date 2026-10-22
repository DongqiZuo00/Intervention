# 主动干预因果表征学习：三篇论文研究计划

> 项目定位：以"主动干预"为主线的因果表征学习（CRL）研究项目。
> 三篇论文构成完整弧线：**识别性奠基 → 干预选址 → 最小干预闭环**。
> 两条外部工具线贯穿始终：**控制理论**（结构可控性 / Kalman 分解 / 对偶控制）与**凸优化**（最优实验设计 / 凸松弛 / 凸几何 / DRO）。

---

## 总览：三篇论文的逻辑关系

| | 论文一 | 论文二 | 论文三 |
|---|---|---|---|
| 核心问题 | 识别性为什么是问题？用什么解决？ | 为什么要干预？干预哪里才正确？ | 怎么做到最小干预？ |
| 性质 | 理论奠基 + 新框架 | 方法构建（算法） | 效率闭环（优化 + 复杂度） |
| 主要外部工具 | 凸几何（支撑函数、凸包） | 控制理论（可控性、Kalman 分解） | 凸优化（松弛、SDP、次模、DRO） |
| 一句话贡献 | 把"部分可识别性"从定性等价类变成可优化的连续量 | 给"干预哪里"一个有多项式时间算法和边界定理的答案 | 给"最少干预"一个带近似保证和样本复杂度账本的闭环 |

依赖关系：论文一提供**可微的"纠缠度"度量**（论文二、三的目标函数）；论文二提供**选址算法与可识别边界**（论文三要最小化的对象）；论文三反过来为论文一的度量提供**有限样本收敛保证**，形成闭环。

---

## 论文一：识别性——为什么是问题，用什么解决

**暂定标题**：*Partial Identifiability as a Convex-Geometric Quantity: Rethinking What Can Be Learned in Causal Representation Learning*

### 1.1 为什么识别性是问题（motivation 部分要讲透的）

- 纯观测 i.i.d. 数据下，潜在表征对任意可逆变换不可识别（Locatello et al. 2019 的不可能性结果）——任何 $\hat Z = h(Z)$（$h$ 可逆）产生同样的观测分布。
- 因此"学出因果变量"不是工程难题而是**数学上的不适定性**：不加额外结构，解空间是整个等价类。
- 现有出路都靠"额外结构"：辅助变量/弱监督（Hyvärinen et al. 2019; Khemakhem et al. 2020）、多环境/非平稳、稀疏性（Lachapelle et al. 2024; Zheng et al. 2022）、干预数据（Ahuja et al. 2023; von Kügelgen et al. 2023; Varıcı et al. 2025）。
- 但现有理论的语言是**定性的**："可识别到排列加缩放""块仿射等价类"。这没法回答实践问题：*我现在学到的东西离可识别还差多远？下一次数据采集应该优先消除哪部分纠缠？*

### 1.2 核心想法：凸几何化

- Ahuja 等人的识别机制本质是**支撑集在干预下的解耦**（完美干预切断被干预变量支撑与其祖先支撑的依赖）。
- 支撑集、支撑函数（support function）、凸包、Minkowski 和——全是凸分析的原生对象。
- **提议构造**：定义潜在表征的"纠缠度"为学到的支撑函数族与真实支撑函数族之间的偏差（例如 Hausdorff 距离或支撑函数包含关系的违背度），使部分可识别性成为**连续、可微、可优化的量**。
- 由此，可识别性定理从"是/否"命题升级为"度量 + 收敛"命题：度量趋零 ⇔ 识别达成。

### 1.3 技术路线

1. 形式化支撑集解耦的凸几何判据（完美/不完美干预两种情形）。
2. 定义纠缠度函数 $\mathcal{E}(\hat g, \mathcal{I})$（$\hat g$ 为学到的解码器，$\mathcal{I}$ 为已用干预集合），证明其与块仿射等价类的对应关系。
3. 证明 $\mathcal{E}$ 的可微性与下界性质（何时 $\mathcal{E}=0$ 蕴含识别）。
4. 实验：在 Causal3DIdent、Interventional Pong 等标准基准上，验证 $\mathcal{E}$ 与 MCC 等现有指标的一致性，并展示它能捕捉 MCC 捕捉不到的残余纠缠。

### 1.4 关键参考文献

- Ahuja, Mahajan, Wang, Bengio. *Interventional Causal Representation Learning*, ICML 2023 (arXiv:2209.11924).
- von Kügelgen et al. *Nonparametric Identifiability of Causal Representations from Unknown Interventions*, NeurIPS 2023 (arXiv:2306.00542).
- Varıcı, Acartürk, Shanmugam, Kumar, Tajer. *Score-based Causal Representation Learning: Linear and General Transformations*, JMLR 2025.
- Locatello et al. *Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations*, ICML 2019.
- Squires, Seigal, Bhate, Uhler. *Linear Causal Disentanglement via Interventions*, ICML 2023.
- Yao, Rancati, Cadei, Fumero, Locatello. *Unifying CRL with the Invariance Principle*, ICLR 2025.

### 1.5 风险与备选

- 风险：支撑函数在高维不可计算。备选：用随机投影下的切片支撑函数（sliced support function）保持可微性。
- 风险：凸几何只覆盖"支撑"信息，丢失分布内部结构。备选：与 score-based 方法（Varıcı et al. 2025）的密度梯度信息联合建模。

---

## 论文二：干预选址——为什么干预，干预哪里才正确

**暂定标题**：*Where to Intervene: Structural Controllability as a Subroutine for Active Causal Representation Learning*

### 2.1 为什么要干预（要讲透的）

- 干预数据是当前已知**假设最弱、保证最强**的识别来源：无需对潜在分布/依赖结构做参数化假设（Ahuja et al. 2023）。
- 直觉：干预在潜在空间留下"几何签名"（支撑集解耦），观测数据永远没有。
- 现实契合：CRISPR 扰动、光遗传、机器人动作、推荐系统推送——干预数据是许多领域的日常产出。

### 2.2 干预哪里才是正确的（核心贡献）

现有 CRL 理论假设干预集合是给定的；"选址"是缺失的一层。本论文从**控制理论**借三件工具：

1. **结构可控性 / 最小驱动节点**（Lin 1974; Liu–Slotine–Barabási 2011）：
   控制理论问"最少驱动哪些节点系统可控"，答案由二分图最大匹配给出，多项式时间。
   与因果干预设计的同构关系：

   | 控制理论 | 因果学习 |
   |---|---|
   | 最少驱动节点使系统可控 | 最少干预集使结构可识别 |
   | 最大匹配、SCC 分解 | 分离系统、染色 |
   | 图已知 | **图未知（要学的就是它）** |

   **核心算法想法**：自适应循环——每轮用当前学到的部分结构运行最小驱动节点算法，计算"剩余不确定性下最优的下一个干预目标"；干预后更新结构与纠缠度（论文一的 $\mathcal{E}$），迭代。

2. **Kalman 分解 → 可识别边界定理**：
   控制理论把系统分解为可控/不可控、可观/不可观四个子空间。移植到 CRL：给出"**可识别子空间分解**"——在当前可用干预集下，哪些潜在方向原则上可识别、哪些**任何干预序列都识别不出**（例如不可达状态、不可逆混合的零空间方向）。这是因果学习社区目前缺失的**否定性定理**，也是论文三"最小化"的合法边界（不能要求识别原则上不可识别的部分）。

3. **持续激励（persistent excitation）判据**：
   系统辨识中"输入足够丰富才能辨识参数"的条件，对应 CRL 的"sufficient variability / 每潜变量至少一次干预"。PE 的**在线可检验性**给选址算法提供停止准则：当前干预历史是否已满足识别激励条件。

### 2.3 技术路线

1. 建立"干预选址 = 未知图上的最小驱动节点"的形式化问题，证明最坏情形复杂度。
2. 提出自适应选址算法 CTRL-CRL（暂名）：结构学习子程序 + 匹配/SCC 子程序 + 纠缠度目标。
3. 证明可识别子空间分解定理（Kalman 型）。
4. 基线对比：随机干预、信息增益贪心（Zhang et al., Nature MI 2023）、minimax/熵准则（He & Geng 2008）在合成 + 半真实（基因扰动）数据上的干预次数与识别精度。

### 2.4 关键参考文献

- Lin. *Structural controllability*, IEEE TAC 1974. / Liu, Slotine, Barabási. *Controllability of complex networks*, Nature 2011.
- He, Geng. *Active Learning of Causal Networks with Intervention Experiments*, JMLR 2008.
- Zhang, Cammarata, Squires, Sapsis, Uhler. *Active learning for optimal intervention design in causal models*, Nature Machine Intelligence 2023.
- Kocaoglu, Dimakis, Vishwanath. *Cost-optimal learning of causal graphs*, ICML 2017.
- Addanki et al. *Efficient Intervention Design for Causal Discovery with Latents*, AISTATS 2020.

### 2.5 风险与备选

- 风险：可控性本质是线性/结构化理论，CRL 主打非线性非参数。应对：只借**图论子程序**（匹配、SCC）与**分解思想**，不直接搬秩判据；非线性情形用微分几何（Lie 括号）表述开放问题。
- 风险：潜在变量上"干预目标未知"使驱动节点对应关系模糊。应对：与未知干预目标下的识别结果（Varıcı et al. 2024, NeurIPS）对接。

---

## 论文三：最小干预——怎么做到最小

**暂定标题**：*Minimal Interventions for Causal Representation Learning: Convex Relaxations, Budgets, and Sample Complexity*

### 3.1 问题的三个"最小"

| 层面 | 问题 | 本文工具 |
|---|---|---|
| 干预**次数**最少 | 多少次干预够识别？ | 下界理论 + 凸松弛选址 |
| 单次干预**规模/强度**最小 | 每次最少动几个变量、多大强度？ | 连续松弛的最优实验设计 |
| **总成本 / 样本**最小 | 预算与样本账本 | 次模 + Lovász 扩展；样本复杂度 |

### 3.2 核心想法：凸优化三件套

1. **凸松弛打 NP-hard**：
   最小成本干预设计 NP-hard（Lindgren et al. 2018）。用 $\ell_1$ 松弛替代基数约束（LASSO 思想）、SDP 松弛替代离散设计（混合整数 D-最优设计的成熟路线），得到与现有贪心 $(2+\varepsilon)$ 近似**互补的近似保证**，并给出可计算的最优性间隙证书。

2. **连续松弛的干预分配 = 凸的最优实验设计**：
   把"干预哪些变量"松弛为预算单纯形上的权重向量 $w$，目标为 $\max_w \log\det \sum_i w_i M_i$（D-最优）或其变体。KKT 对偶变量给出**每个干预的影子价格**——边际信息价值的干净语义。Frank-Wolfe 级算法保证可扩展性。

3. **次模性与 Lovász 扩展做预算分配**：
   若识别收益（论文一的 $\mathcal{E}$ 削减量）作为干预集合的函数是次模的（信息增益类目标通常如此），贪心自动有 $(1-1/e)$ 保证；Lovász 扩展把次模函数延拓为凸函数，使**预算约束下的干预序列规划**可以用凸对偶理论完整刻画。

### 3.3 样本复杂度与 DRO 证书

- 承接 Acartürk et al.（NeurIPS 2024）的干预式 CRL 样本复杂度，给出**凸松弛选址下的有限样本保证**：松弛造成的损失 + 舍入损失 + 估计误差三本账。
- **DRO 视角的干预外推**：干预把分布推出支撑；"对未见过干预的预测"用分布鲁棒优化的凸对偶重新表述，给出**可计算的外推证书**（certificate），与 Saengkyongam et al.、von Kügelgen et al.（2025）的代数条件互补。

### 3.4 与论文一、二的闭环

- 目标函数 $\mathcal{E}$ 来自论文一；选址下界与合法性边界来自论文二。
- 论文三给出：在预算 $B$ 内，自适应凸选址算法达到 $\mathcal{E} \le f(B, d, \text{样本量})$ 的端到端保证——**整个项目的收官定理**。

### 3.5 关键参考文献

- Lindgren, Kocaoglu, Dimakis, Vishwanath. *Experimental design for cost-aware learning of causal graphs*, NeurIPS 2018.
- Acartürk, Varıcı, Shanmugam, Tajer. *Sample Complexity of Interventional Causal Representation Learning*, NeurIPS 2024.
- Varıcı et al. *Linear CRL from unknown multi-node interventions*, NeurIPS 2024.
- Boyd & Vandenberghe, *Convex Optimization*, §7.5（实验设计）.
- Krause & Singh 等传感器放置的次模性文献（迁移对象）。

### 3.6 风险与备选

- 风险：$\mathcal{E}$ 的次模性不成立。备选：证明弱次模/近似次模，或用 Lovász 扩展直接凸化而绕过次模性。
- 风险：SDP 松弛在大规模不可行。备选：一阶方法 + 只在小规模上给证书、大规模上给启发式。

---

## 贯穿两条工具线的对照总表

| 工具 | 论文一 | 论文二 | 论文三 |
|---|---|---|---|
| 凸几何（支撑函数） | 纠缠度定义 ★ | 目标函数输入 | 次模性分析对象 |
| 结构可控性 / 匹配 / SCC | — | 选址子程序 ★ | 松弛前的组合下界 |
| Kalman 分解 | — | 可识别边界 ★ | 最小化的合法域 |
| 持续激励 | — | 停止准则 | 样本充分性条件 |
| 最优实验设计（D-最优） | — | 对照基线 | 连续松弛 ★ |
| $\ell_1$/SDP 松弛 | — | — | NP-hard 近似 ★ |
| 次模 + Lovász | — | — | 预算分配 ★ |
| DRO 凸对偶 | — | — | 外推证书 ★ |
| 对偶控制（Feldbaum） | — | 讨论：学习与决策统一 | 展望：接因果 RL |

---

## 时间与里程碑建议（可按 24–30 个月排）

1. **0–6 月**：论文一。纠缠度定义 + 定理 + 基准实验。目标投 ICML/NeurIPS。
2. **4–14 月**：论文二。选址算法 + 可识别边界定理。与论文一并行启动，在论文一投稿后全力。目标投 NeurIPS/ICML 或 JMLR。
3. **12–24 月**：论文三。凸松弛 + 预算理论 + 样本复杂度收官。目标投 JMLR（理论完整版）或 NeurIPS（算法版）。
4. 全程维护统一代码库：结构学习子程序、纠缠度度量、选址算法、凸求解器接口。

---

*文档生成于 2026-10-21，基于当轮检索到的文献（Ahuja 2023、von Kügelgen 2023、Varıcı 2024–2025、Acartürk 2024、Squires 2023、He & Geng 2008、Lindgren 2018、Kocaoglu 2017、Addanki 2020、Zhang et al. Nature MI 2023、可控性文献 Lin 1974 / Liu et al. 2011 等）。*


---

# v2 修订（2026-10-21，文献 sweep 后）

## 顺序调整：论文二先行

原定顺序 1→2→3 调整为 **论文二（干预选址）先行，论文一并行低强度推进，论文三收官**。理由：

1. 竞争窗口：*On the Identifiability of Controlled World Models*（2026）已将持续激励引入世界模型识别性；Curious Causality-Seeking Agent（NeurIPS 2025）把"不可达状态""预算感知"列为未来工作——桥接首创权有时效。
2. 论文二故事最完整、实验门槛最低：算法骨架（匹配/SCC 子程序）、基线（随机、EIG、Trust-Your-V、diffCBED）、平台（Causal3DIdent、CausalVerse、Light Tunnel）均现成。
3. 解耦分析支持：论文二换用结构熵/MCC 作目标函数即自足，不依赖论文一的度量。

## 定位声明（对张坤"最小变化"纲领的差异化）

- 两个"最小"分属两条正交轴：张坤 program 最小化**假设**（minimal change / sufficient change，被动利用自然分布偏移）；本项目最小化**行动**（最少干预次数与成本，主动制造变化）。
- 统一视角：张坤线的充分变化条件（≥2n+1 环境、导数向量线性无关）≡ 被动版的持续激励（PE）。本项目命题：**当被动数据不满足充分变化时，用最小成本主动制造它**。
- 需求侧证据：CausalVerse 评测中所有方法 MCC < 0.6（4 视图远低于 2n+1 要求）；张坤本人（2026 keynote Q&A）承认潜变量上的干预落点是开放边界。
- 与张坤线的关系是递进而非竞争：其 ICML 2024 一般化结果刻画"纯被动最多恢复什么"，作为论文一的下界参照；我们量度"每次主动干预带来多少纠缠度下降"。
- 详见 [主动干预CRL文献综述](./主动干预CRL文献综述.md) §7 空白点地图。

## 差异化声明（对近邻工作）

- vs Zhang et al. 2026（受控世界模型）：他们给"给定行为策略下的识别条件"（被动），我们做"主动选择干预使识别达成"（主动设计）。
- vs Curious Causality-Seeking Agent（NeurIPS 2025）：他们做启发式好奇心探索，我们做带边界定理与最优性保证的选址。
- vs 经典干预设计（Choo–Shiragur、Ghassami、Tigas 等）：他们假设变量已知，我们处理潜变量 + 表征识别。
