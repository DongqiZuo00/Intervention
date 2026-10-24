# 论文一数学推导稿 线性确定性干预下的识别误差校准

初稿：2026 年 10 月 23 日。复核修订：2026 年 10 月 24 日。依据：Intervention 白皮书 v0.2 的论文一要求，以及中文研究计划第 1 节。本文建立一个可逐项审查的理论起点：在明确的线性混合与确定性干预条件下，把可计算的干预残差校准为表征恢复误差，并给出连续性、优化、噪声、有限样本和不可能性边界。以下命题附证明；它们不等同于已经确立的论文新颖性，也不覆盖一般非线性 CRL。

核心结果是两组双边界：

$$

\sqrt2\,r_{\min}\Delta(W)\le \mathcal E_{\rm width}(W)\le2R_{\max}\Delta(W),
\tag{1}

$$

$$

\frac{\alpha_{\min}}2\Delta(W)^2\le \mathcal C(W)\le\beta_{\max}\Delta(W)^2.
\tag{2}

$$

这里 $\Delta$ 是到正确线性解混方向的符号及排列等价类距离，$r,R$ 描述干预支撑的几何尺度，$\alpha,\beta$ 描述干预协方差的非零谱。目标函数只使用干预分布；真混合矩阵只出现在误差定义与理论解释中。

## 1 白皮书目标的数学拆分

白皮书希望将“部分可识别性”转化为连续、可微、可优化的量，并希望诊断模型误设与优化失败。必须先区分三个对象。

1. **模型可识别性**：给定全部可用分布，是否只剩一个允许的参数等价类。
2. **候选表征误差**：一个具体编码器离真实表征的等价类有多远。
3. **候选表征对可用证据的残差**：一个具体编码器是否满足当前干预揭示的约束。

只有在数据和模型假设足以识别时，第 3 项的零点才可以等价于第 2 项的零点。数据不足时，小残差不意味着完整恢复。把这三件事都叫作“纠缠度”，会使目标量的含义不确定。

本文以线性编码器 $W$ 为优化变量。白皮书使用解码器 $\hat g$ 的记号；在下述降维坐标中，当 $W$ 可逆时，解码器就是对应的仿射逆映射。本文不预设任意神经网络已被识别到仿射类，也不声称由恢复表征立即恢复因果图 $B$。

## 2 原始支撑函数路线的边界

### 2.1 满支撑下不是有限连续量

支撑函数定义为

$$

h_K(v)=\sup_{x\in K}v^\top x.

$$

若非退化高斯分布的支撑为 $\mathbb R^d$，则所有 $v\ne0$ 都有 $h_K(v)=+\infty$。确定性干预后的高斯分布支撑为仿射超平面，法向宽度为零，非正常向宽度通常为无穷。因此，“两个高斯环境支撑函数的差”不能直接作为有限、连续的恢复误差。

### 2.2 支撑函数只辨认闭凸包

对任意集合 $S$，

$$

h_S=h_{\overline{\operatorname{conv}}S}.

$$

例如完整正方形与去掉中央开孔的正方形环具有相同支撑函数，但后者的联合支撑不等于边缘支撑的笛卡尔积。因此，支撑函数相等一般不等价于原始支撑独立，更不等价于统计独立。两个满支撑、协方差不同的非退化高斯分布也有相同支撑。

本文的宽度方法只需要正确辨认**仿射张成空间**；取凸包不会损失这一信息。这比宣称从凸包恢复全部分布结构弱得多。

### 2.3 可微与凸不能由凸几何自动推出

有限样本宽度是最大值减最小值，通常分段光滑而非处处可微。排列匹配的最小值也可能产生不可微点。即使固定匹配后的损失在无约束向量空间内凸，单位行约束仍是非凸约束；若去掉尺度约束，$W=0$ 会成为无意义的零解。

## 3 模型假设与尺度规范

设 $d\ge2$，观测模型为

$$

X=HZ+b,\qquad H\in\mathbb R^{p\times d},\quad \operatorname{rank}H=d.

$$

假设观测支撑仿射张成 $b+\operatorname{col}H$。在此已知的 $d$ 维仿射空间内选定正交坐标，得到

$$

Y=MZ+a,\qquad M\in GL(d).
\tag{3}

$$

平移 $a$ 不影响宽度或协方差。后续误差均在这套固定观测坐标和欧氏范数下定义。任意非正交重参数化会改变数值常数，故不声称对所有观测坐标变换不变。带噪时估计观测子空间的误差另需分析，本文的噪声结果以坐标已经给定为条件。

对每个 $i\in[d]$，有一个可区分的环境，其干预是

$$

\operatorname{do}(Z_i=c_i).
\tag{4}

$$

这是把目标固定为常数的 **deterministic clamping**。它强于把目标替换为独立随机噪声的随机完美干预。允许不知道生物学变量的名字，但要求这 $d$ 个环境确实分别覆盖 $d$ 个不同目标；重复同一目标不算完整覆盖。各环境中的非目标潜变量必须仍具有 $d-1$ 维仿射变化。

令

$$

K_i=\overline{\operatorname{conv}}\operatorname{supp}(Y\mid\operatorname{do}(Z_i=c_i)),
\quad n_i=\frac{M^{-\top}e_i}{\|M^{-\top}e_i\|_2}.
\tag{5}

$$

因为 $e_i^\top M^{-1}(Y-a)=c_i$，且其他坐标充分变化，所以

$$

\operatorname{aff}(K_i)=a_i+n_i^\perp.
\tag{6}

$$

宽度定理额外要求紧支撑，并存在 $0<r_i\le R_i<\infty$ 使

$$

a_i+r_i B_{n_i^\perp}\subseteq K_i\subseteq a_i+R_i B_{n_i^\perp}.
\tag{7}

$$

这里的球位于 $(d-1)$ 维超平面内。协方差定理不要求紧支撑，只要求二阶矩有限及非目标变化不退化。

编码器写作 $\widehat Z=WY+t$，每个行向量满足

$$

\|w_j\|_2=1.
\tag{8}

$$

平移 $t$ 可忽略；归一化消除任意缩小编码器导致残差趋零的退化。不能普遍要求 $W$ 正交：例如 $M=\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)$，两个真实单位法向分别是 $(1,-1)/\sqrt2$ 和 $(0,1)$，并不正交。

## 4 宽度目标与完整校准证明

定义平移不变的投影宽度

$$

\omega_i(w)=h_{K_i}(w)+h_{K_i}(-w).

$$

令 $S_d$ 为排列集合，定义

$$

\mathcal E_{\rm width}(W)=
\min_{\pi\in S_d}\left[\frac1d\sum_{i=1}^d\omega_i(w_{\pi(i)})^2\right]^{1/2},
\tag{9}

$$

$$

\Delta(W)=\min_{\pi\in S_d,\,s_i\in\{-1,1\}}
\left[\frac1d\sum_{i=1}^d\|w_{\pi(i)}-s_i n_i\|_2^2\right]^{1/2}.
\tag{10}

$$

一一匹配不能替换为“每个环境独立选任意输出行”，否则同一编码行可能被重复使用。$\Delta$ 是用于分析的真值距离；$\mathcal E$ 的定义不使用 $M$。

**定理 1 宽度校准。** 在第 3 节假设下，式 (1) 对任意单位行矩阵 $W$ 成立，其中 $r_{\min}=\min_i r_i$，$R_{\max}=\max_i R_i$。

**证明。** 令 $P_i=I-n_in_i^\top$，对单位 $w$ 定义

$$

\delta_i(w)=\min_{s=\pm1}\|w-sn_i\|_2,\qquad c=|w^\top n_i|.

$$

直接计算得

$$

\delta_i(w)^2=2(1-c),\qquad
\|P_iw\|_2^2=1-c^2=\frac{1+c}{2}\delta_i(w)^2.

$$

因而

$$

\frac{\delta_i(w)}{\sqrt2}\le\|P_iw\|_2\le\delta_i(w).
\tag{11}

$$

宽度消去平移，且 $K_i-a_i\subset n_i^\perp$，因此只取决于 $P_iw$。内外接球给出

$$

2r_i\|P_iw\|_2\le\omega_i(w)\le2R_i\|P_iw\|_2.
\tag{12}

$$

合并可得逐配对界

$$

\sqrt2 r_i\delta_i(w)\le\omega_i(w)\le2R_i\delta_i(w).

$$

对任意固定排列平方、平均、开方，便得到同一排列下的界。下界对全部排列成立；上界选取使 $\Delta$ 最小的排列。分别取最小值即得式 (1)。无需假设两个目标的最优排列相同。证毕。

**推论 1 零集与收敛。** 记 $N$ 的第 $i$ 行为 $n_i^\top$，则

$$

N=DM^{-1},\qquad D_{ii}=\|M^{-\top}e_i\|_2^{-1}>0.

$$

因此

$$

\mathcal E_{\rm width}(W)=0
\iff \Delta(W)=0
\iff PW=SN
\tag{13}

$$

对某个置换矩阵 $P$ 和对角符号矩阵 $S$ 成立。于是 $PWY=SDZ+SNa$，恢复潜变量至排列、非零逐坐标缩放和平移。对固定且满足 $r_{\min}>0,R_{\max}<\infty$ 的环境族，$\mathcal E(W_m)\to0\iff\Delta(W_m)\to0$。该结论不是在任意退化的环境序列上的统一收敛保证。

**推论 2 从方向误差到解混误差。** 选择实现 $\Delta$ 的符号与排列，有

$$

\|PWM-SD\|_F\le\sqrt d\,\|M\|_{\rm op}\Delta(W)
\le\frac{\sqrt d\,\|M\|_{\rm op}}{\sqrt2r_{\min}}\mathcal E(W).
\tag{14}

$$

零解自动满秩。若

$$

\mathcal E(W)<\frac{\sqrt2r_{\min}\sigma_{\min}(N)}{\sqrt d},
\tag{15}

$$

则 $W$ 与某个满秩零解的算子距离小于其最小奇异值，所以 $W$ 也可逆。近零的可逆性需要混合条件数信息，不能仅由“小于一个固定数”的损失断言。

**连续性。** 式 (7) 蕴含 $|\omega_i(w)-\omega_i(v)|\le2R_i\|w-v\|$。对排列分支应用均方范数的三角不等式，再取有限最小值得

$$

|\mathcal E(W)-\mathcal E(V)|\le\frac{2R_{\max}}{\sqrt d}\|W-V\|_F.
\tag{16}

$$

这证明全局 Lipschitz 连续；不证明处处可微。

## 5 优化景观与可微替代

**命题 2 没有非零局部极小值。** 在仅有单位行约束的可行域上，$\mathcal E_{\rm width}$ 的所有局部极小值都是零点。

**证明。** 取当前最优匹配 $\pi$。若损失非零，存在对应的 $w$ 不平行于 $n_i$。选择最近的符号，写成

$$

w=\cos\theta\,\widetilde n_i+\sin\theta\,u,
\quad u\perp n_i,\quad \|u\|=1,\quad 0<\theta\le\pi/2.

$$

将该行替换为 $w(t)=\cos(\theta-t)\widetilde n_i+\sin(\theta-t)u$，其中 $0<t<\theta$。宽度严格按比例 $\sin(\theta-t)/\sin\theta$ 缩小。其他行不变，所以

$$

\mathcal E(W(t))\le\mathcal E_\pi(W(t))<\mathcal E_\pi(W)=\mathcal E(W).

$$

任意小的 $t$ 都成立，排除了非零局部极小值。证毕。

可逆性是开条件，因此在可逆单位行矩阵内也成立。此证明不适用于额外的正交约束、条件数硬约束或 softmin 替换；它也不是任意梯度算法的收敛保证。非光滑点、驻点、有限精度和模型不满足假设仍可能影响算法。

对有限样本投影 $u_1,\ldots,u_m$，可定义光滑宽度

$$

s_\tau(u)=\tau\log\left(\frac1m\sum_a e^{u_a/\tau}\right)
+\tau\log\left(\frac1m\sum_a e^{-u_a/\tau}\right),\quad\tau>0.
\tag{17}

$$

Cauchy–Schwarz 给出 $s_\tau\ge0$，且等号成立当且仅当所有 $u_a$ 相同。它保留样本宽度的零点，并且

$$

\max u-\min u-2\tau\log m\le s_\tau(u)\le\max u-\min u.

$$

但是固定 $\tau$ 时，$s_\tau(tu)=t^2\operatorname{Var}_{\rm emp}(u)/\tau+O(t^4)$，近零是二次而非线性行为，不能照搬式 (1)。样本不张成真实超平面时，还会存在额外零方向。

若省略 $1/m$，正确方向处也会留下 $2\tau\log m$ 的偏置。对排列损失做 softmin 则是另一个问题：即使配对零集正确，softmin 通常也改变全局零集。例如两个排列损失为 $0,4$，未归一化 softmin 为负，归一化 softmin 为正，均不等于零。严格版本应保留精确匹配，或固定输出行与环境的对应。

## 6 协方差目标与可计算恢复证书

令 $\Sigma_i=\operatorname{Cov}(Y\mid\operatorname{do}_i)$。只要求二阶矩有限及仿射变化充分，就有

$$

\ker\Sigma_i=\operatorname{span}(n_i).

$$

令其非零特征值处于 $[\alpha_i,\beta_i]$，$\alpha_i>0$。定义

$$

\mathcal C(W)=\min_{\pi\in S_d}\frac1d\sum_i w_{\pi(i)}^\top\Sigma_iw_{\pi(i)}.
\tag{18}

$$

**定理 3 协方差校准。** 式 (2) 成立，其中 $\alpha_{\min}=\min_i\alpha_i$、$\beta_{\max}=\max_i\beta_i$。

**证明。** 每个单位向量满足

$$

\alpha_i\|P_iw\|^2\le w^\top\Sigma_iw\le\beta_i\|P_iw\|^2.

$$

代入式 (11) 的平方，逐排列求和再取最小值即可。证毕。

这个目标可以处理高斯 clamping 环境，因为协方差仍有限。它与常数拟合有精确关系：

$$

\min_c\mathbb E[(w^\top Y-c)^2]=w^\top\Sigma_iw.
\tag{19}

$$

固定匹配后，它是可微二次函数；第 $j=\pi(i)$ 行的梯度为 $2\Sigma_iw_j/d$。未知匹配下的有限最小值仍可能不可微。若直接让第 $i$ 个输出对应第 $i$ 个环境，匹配可固定，恢复目标本来就允许最终的潜变量置换。

全局求解不需要神经网络训练：分别取各 $\Sigma_i$ 的最小特征向量即可。在正确模型内，这些行构成可逆的 $N$。命题 2 的下降证明也适用于 $\mathcal C$，因为投影的平方二次型会随切向分量收缩而严格减小。

## 7 噪声基线与诊断能证明什么

对任意 PSD 矩阵 $Q_i$，定义

$$

\mathcal C_Q(W)=\min_\pi\frac1d\sum_iw_{\pi(i)}^\top Q_iw_{\pi(i)},
\qquad m_Q=\frac1d\sum_i\lambda_1(Q_i),
\tag{20}

$$

其中特征值按升序排列。

**命题 4 可计算的全局基线。**

$$

\min_{\|w_j\|=1}\mathcal C_Q(W)=m_Q.
\tag{21}

$$

证明：每一项的 Rayleigh 商至少是对应最小特征值；分别选各矩阵的最小特征向量作为各行即可取等。

故 $G_Q(W)=\mathcal C_Q(W)-m_Q\ge0$ 是这个**允许编码行重复或相关的目标**相对全局最小值的精确差距。它不是任意 CRL 训练目标的优化间隙。若强制满秩，极小值未必达到；存在重特征值时，要检查能否从各最小特征子空间中选出线性独立的行，而不能依赖一次特征分解任意返回的向量。

无噪信号仍记为 $Y_i$，实际采样变量记为 $\widetilde Y_i=Y_i+\xi_i$。假设测量噪声 $\xi_i$ 在这套固定观测坐标中与信号独立、均值为零、协方差为 $\sigma_i^2 I$，允许各环境的方差不同。记 $Q_i=\operatorname{Cov}(\widetilde Y_i)$，则

$$

Q_i=\Sigma_i+\sigma_i^2I,\quad m_Q=\frac1d\sum_i\sigma_i^2,
\quad G_Q(W)=\mathcal C(W).
\tag{22}

$$

这里无需知道噪声方差，总体协方差的最小特征值就是它。潜变量坐标中的各向同性噪声经过一般 $M$ 后通常不再各向同性，不能混用。

**推论 3 总体恢复误差区间。** 令

$$

\alpha_{\min}=\min_i[\lambda_2(Q_i)-\lambda_1(Q_i)],\quad
\beta_{\max}=\max_i[\lambda_d(Q_i)-\lambda_1(Q_i)].

$$

在上述模型与噪声条件下，所有量 $G_Q,\alpha,\beta$ 均由观测分布计算，并满足

$$

\boxed{\sqrt{G_Q(W)/\beta_{\max}}\le\Delta(W)
\le\min\{\sqrt2,\sqrt{2G_Q(W)/\alpha_{\min}}\}.}
\tag{23}

$$

这给出了无需输入真混合矩阵的恢复误差证书，但其解释以模型和激励条件成立为前提。证书约束编码方向，不声称从每个带噪样本精确恢复潜变量取值。未知各向异性噪声一般可能改变最小特征向量，不能无额外条件直接使用本结论。

**因果诊断反例。** 几何残差为零不证明共享因果机制正确。取二维观测环境为两个独立的 $U[10,11]$ 变量；环境 1 为 $Z_1=0,Z_2\sim U[1,2]$；环境 2 为 $Z_2=0,Z_1\sim U[3,4]$。两个干预协方差的核分别是 $e_1,e_2$，故 $m_Q=0$，$W=I$ 完全满足几何零残差。但任意两节点 DAG 至少有一个根节点，对另一个节点干预不能改变根的边缘分布；这里两种根选择都不成立。因此该指标检测几何不变量，不能单独诊断全部 SCM 模块性。

同样，$m_Q>0$ 只能说明至少一个未去噪的观测环境不具有超平面支撑，原因可能是测量噪声、随机目标干预、环境混合或模型误设。它不能据此否定底层无噪 clamping 模型，一个正数也不能自动区分这些原因。

## 8 有限样本稳定性与置信区间

### 8.1 确定性扰动界

设每个经验协方差满足

$$

\|\widehat Q_i-Q_i\|_{\rm op}\le\varepsilon_i,
\qquad\bar\varepsilon=\frac1d\sum_i\varepsilon_i.
\tag{24}

$$

对任意单位行 $W$ 和任意排列，配对损失的平均误差至多 $\bar\varepsilon$。取最小值保持此界。Weyl 特征值界又给出基线误差，所以同时有

$$

|\widehat{\mathcal C}_Q(W)-\mathcal C_Q(W)|\le\bar\varepsilon,
\quad|\hat m_Q-m_Q|\le\bar\varepsilon,
\quad|\widehat G_Q(W)-G_Q(W)|\le2\bar\varepsilon.
\tag{25}

$$

这是对全部单位行矩阵的统一界，允许 $W$ 使用同一批样本学习。

定义可计算谱界

$$

\underline\alpha=\min_i[\lambda_2(\widehat Q_i)-\lambda_1(\widehat Q_i)-2\varepsilon_i],
\quad
\overline\beta=\max_i[\lambda_d(\widehat Q_i)-\lambda_1(\widehat Q_i)+2\varepsilon_i].

$$

在式 (24) 同时成立的事件上，只要 $\underline\alpha>0$，式 (23) 可转化为

$$

\boxed{
\sqrt{\frac{\max(0,\widehat G_Q(W)-2\bar\varepsilon)}{\overline\beta}}
\le\Delta(W)\le
\min\left\{\sqrt2,\sqrt{\frac{2(\widehat G_Q(W)+2\bar\varepsilon)}{\underline\alpha}}\right\}.
}
\tag{26}

$$

证明：用式 (25) 上下夹住 $G_Q$，用 Weyl 界得到 $\alpha_{\min}\ge\underline\alpha$、$\beta_{\max}\le\overline\beta$，再代入式 (23)。若 $\underline\alpha\le0$，数据不能通过这个界认证方向稳定性，不能把它当作零误差。

### 8.2 直接估计法向的更强误差界

设 $Q_i$ 最小特征值为 $\sigma_i^2$，其余特征值至少大 $\alpha_i$，且 $\varepsilon_i<\alpha_i/2$。取 $\widehat Q_i$ 的单位最小特征向量 $\hat n_i$。则

$$

\min_{s=\pm1}\|\hat n_i-sn_i\|_2
\le\frac{\sqrt2\varepsilon_i}{\alpha_i-\varepsilon_i}
\le\frac{2\sqrt2\varepsilon_i}{\alpha_i}.
\tag{27}

$$

证明：写 $F_i=\widehat Q_i-Q_i$、$P_i=I-n_in_i^\top$，把特征方程投影到 $n_i^\perp$：

$$

\big[Q_i|_{n_i^\perp}-\hat\lambda_i I\big]P_i\hat n_i=-P_iF_i\hat n_i.

$$

由 $|\hat\lambda_i-\sigma_i^2|\le\varepsilon_i$，左侧算子的最小特征值至少是 $\alpha_i-\varepsilon_i$，故投影范数至多为 $\varepsilon_i/(\alpha_i-\varepsilon_i)$。再用式 (11) 即得。$\varepsilon_i<\alpha_i/2$ 还保证估计的最小特征值简单。

这是协方差估计误差除以谱间隙的稳定性保证。若 $\varepsilon=O(N^{-1/2})$，直接谱估计器的方向误差为 $O(N^{-1/2})$；对任意候选编码器使用通用残差区间 (26)，可能只给出较松的 $O(N^{-1/4})$ 近零上界，二者不能混称。

### 8.3 一个显式但保守的概率版本

每环境有 $N_i$ 个独立同分布样本，设实际采样变量的中心化值 $V_i=\widetilde Y_i-\mathbb E\widetilde Y_i$ 满足 $\|V_i\|_2\le L_i$ 几乎必然成立。无测量噪声时令 $\xi_i=0$。这个界必须约束实际样本，只有无噪信号有界还不够。经验协方差使用分母 $N_i$，并用样本均值中心化。给定失败概率 $\delta\in(0,1)$，置

$$

\ell=\log(4d^3/\delta),\qquad
\varepsilon_i=dL_i^2\sqrt{2\ell/N_i}+2dL_i^2\ell/N_i.
\tag{28}

$$

则所有 $d$ 个环境同时满足 (24) 的概率至少为 $1-\delta$。

证明：每个 $V_{ij}V_{ik}\in[-L_i^2,L_i^2]$。Hoeffding 不等式和对 $d\times d^2$ 个条目的 union bound，使真均值中心化的二阶矩误差各条目至多 $L_i^2\sqrt{2\ell/N_i}$，失败概率至多 $\delta/2$。算子范数不超过 $d$ 倍最大条目误差。对 $d\times d$ 个均值坐标同样应用 Hoeffding，得到 $\|\bar V_i\|^2\le2dL_i^2\ell/N_i$，失败概率至多 $\delta/2$。用 $\widehat Q_i=N_i^{-1}\sum_a V_{ia}V_{ia}^\top-\bar V_i\bar V_i^\top$ 合并即可。

此界使式 (26) 的证书以至少 $1-\delta$ 的概率对所有 $W$ 同时有效；这不是对“条件于经验谱间隙为正”的条件覆盖率声明。此界是自足的保守构造，没有声称维度依赖最优；未知 $L_i$ 不能直接以样本最大值替代。Gaussian 或其他无界分布须另用尾部条件和相应集中界，不能套用式 (28)。

### 8.4 无噪情形的特殊性和小样本反例

无噪、精确 clamping 且每环境分布相对于其 $(d-1)$ 维超平面上的 Lebesgue 测度绝对连续时，$d$ 个样本几乎必然仿射张成整个超平面。因此法向可以精确恢复。这说明该理想模型很强，真正需要稳定性分析的是噪声、退化或近似条件。

若 $N_i<d$，中心化样本矩阵秩至多为 $N_i-1<d-1$，经验协方差必有至少二维的零空间。可以找到远离真实法向、却具有零经验宽度和零经验方差的方向。故训练残差为零不等于有限样本识别。

对于支撑版本，若另外已知 $d_H(\widehat K_i,K_i)\le\eta_i$，则由单位方向的支撑函数误差界可得

$$

|\widehat{\mathcal E}_{\rm width}(W)-\mathcal E_{\rm width}(W)|
\le2\left(\frac1d\sum_i\eta_i^2\right)^{1/2}.
\tag{29}

$$

但仅凭内外接球条件不能给出统一的 $\eta_i(N)$ 速率：边界附近概率质量可以任意小，需要额外的概率质量下界。

## 9 部分识别性与不能删除的假设

### 9.1 部分环境只校准已覆盖的方向

若只有 $I\subset[d]$、$|I|=k<d$ 个不同目标，将式 (9) 的双射改为从 $I$ 到输出行的一一映射，定义 $\mathcal E_I$ 和相应的 $\Delta_I$。定理 1 的证明逐项仍成立，但只得到已覆盖方向的误差界。其零点不约束其余 $d-k$ 行。

例如 $M=I,d=2,I=\{1\}$，对任意 $0<\theta<\pi/2$，

$$

W_\theta=\begin{pmatrix}1&0\\\sin\theta&\cos\theta\end{pmatrix}

$$

单位行且可逆，环境 1 的残差为零，但第二输出仍混合两个潜变量。增加环境会增加约束；采用平均值后的数值损失本身未必随环境数量单调。

### 9.2 数据不足时不存在普遍有效的真值误差标量

下面的反例比“这个损失不能识别”更强，但只针对所述模型类，不排除额外的 ICA 或结构先验。

模型 A：$Z_1=\varepsilon_1,Z_2=\varepsilon_2$，噪声独立均匀于 $[-1,1]$，且 $X=Z$。

模型 B：$Z'_1=\varepsilon_1,Z'_2=aZ'_1+\varepsilon_2$，$a\ne0$，观测混合为

$$

X=\begin{pmatrix}1&0\\-a&1\end{pmatrix}Z'.

$$

两个模型的观测分布完全相同；对任意常数 $c$ 的目标 1 干预，两者也都产生 $X=(c,\varepsilon_2)$。固定候选编码器 $f_0(X)=X$，它在模型 A 中正确，在模型 B 中相对于 $Z'$ 含有不可由排列和逐坐标缩放消除的剪切混合。

因此，任何只依赖这些观测及干预分布与同一候选编码器的标量，都不可能在两个模型中分别输出“正确为零”和“错误严格为正”。这阻止了白皮书原始目标在不可识别模型类上的普遍实现。

在兼容模型集合 $\mathfrak M(\mathcal Q,I)\ne\varnothing$ 时，模型本身的歧义可以另定义为其直径：

$$

\mathcal U(\mathcal Q,I)=\sup_{M_1,M_2\in\mathfrak M(\mathcal Q,I)}
d_{\rm quot}([N_{M_1}],[N_{M_2}]),
\tag{30}

$$

其中 $d_{\rm quot}$ 为单位行法向矩阵在符号与排列商空间中的均方距离。$\mathcal U=0$ 表示该表征等价类可识别；$\mathcal E_I(W)=0$ 仅表示候选编码器符合已测几何约束。兼容集合为空时应单列为模型类与数据不兼容，不能以空集直径零解释为已识别。这里给出的是概念定义，没有给出一般情况下计算 $\mathcal U$ 的高效算法。

### 9.3 任意非线性编码器破坏零点定理

取 $d=2$、真实混合为恒等映射，并只有每变量一次固定为零的干预。映射

$$

f(z_1,z_2)=(z_1e^{az_2},z_2),\qquad a\ne0,

$$

具有全局光滑逆 $f^{-1}(u_1,u_2)=(u_1e^{-au_2},u_2)$，Jacobian 行列式为 $e^{az_2}>0$。干预 $Z_1=0$ 使第一输出恒为零，干预 $Z_2=0$ 使第二输出恒为零，但第一输出混合了两个变量。因此所有目标都覆盖、重建可逆、对应坐标干预残差为零，仍不保证任意非线性表征逐坐标恢复。多个不同干预值或额外的函数类约束需要新的证明。

### 9.4 没有谱间隙就没有统一稳定性

二维矩阵 $Q_1=\operatorname{diag}(0,\eta)$ 与 $Q_2=\operatorname{diag}(\eta,0)$ 的算子距离为 $\eta\to0$，但最小特征向量分别是 $e_1,e_2$，符号不变距离始终为 $\sqrt2$。因此方向恢复的连续稳定性需要正的激励或谱间隙，不能把 $r_{\min}$ 或 $\alpha_{\min}$ 从误差界中删除。

## 10 可复现数值排错

代码、依赖和命令见 [复现说明](../experiments/paper1/README.md)。三个验证脚本位于 `experiments/paper1/`，本次复跑的参考结果位于 [reference_results](../experiments/paper1/reference_results/)。后续统计验证的协议见 [实验计划](../docs/paper1_experiments_zh.md)。

验证使用 $d=3,4$ 的线性 DAG、独立均匀外生噪声及非正交混合。每次 clamping 后重新求解剩余结构方程，构造精确的干预平行多面体 $K_i=a_i+A_i[-1,1]^{d-1}$，而非仅覆盖原样本的一列。其宽度为 $2\|A_i^\top w\|_1$，总体协方差为 $A_iA_i^\top/3$。

每个维度检查 2,000 个随机候选和 1,200 个近真解候选，共 6,400 组。三个目标分别穷举排列，没有假定其最优排列相同。

| 维度 | 实测宽度误差比值 E/Delta | 理论允许范围 | 宽度界违反数 | 协方差界违反数 |
|---|---|---|---|---|
| 3 | 1.593241 至 6.507441 | 1.001018 至 6.605027 | 0 | 0 |
| 4 | 2.103123 至 6.846183 | 0.929857 至 8.120138 | 0 | 0 |

符号排列真解的宽度残差不超过 $3.64\times10^{-16}$。额外检查包含部分目标残差为零但完整误差非零、高斯支撑无限宽、小样本额外零空间、各向同性噪声去偏、21 个特征向量扰动界、258 个候选矩阵的统一损失界、18 个平滑宽度检查，以及 96 步严格下降路径。另有 312 个候选矩阵检查式 (26) 在精确给定算子扰动预算下的区间代数；它不是随机置信覆盖率实验。全部断言通过。随机数值检查只用于排除实现与常数错误，不代替上文证明。

运行方式：

```bash
python3 experiments/paper1/validate_paper1_geometry.py
python3 experiments/paper1/validate_paper1_noise.py
python3 experiments/paper1/validate_paper1_certificate.py
```

## 11 与已有工作的关系和下一步定理目标

[Ahuja et al. ICML 2023](https://proceedings.mlr.press/v202/ahuja23a/ahuja23a.pdf) 的 Theorem 5.3 已利用确定性干预下编码坐标恒定来识别目标变量；Eq. (7) 已有常数拟合平方损失，Eq. (8) 使用 Hausdorff 支撑损失；附录 A.8、A.12 还涉及近似识别。因此不能将“连续损失”“零宽度识别”或所有定量化都声称为首创。本文可继续检验的候选价值在于明确尺度下的双边校准、统一置信证书与失败边界，仍须和相关稳定性文献逐项比较。

[Squires et al. ICML 2023](https://proceedings.mlr.press/v202/squires23a/squires23a.pdf) 的随机完美干预保留严格正的目标噪声方差，使用精度矩阵差等信息。本文单环境协方差零空间方法不能直接覆盖该设定。把 $\operatorname{do}(Z_i=c_i)$ 无说明替换为随机完美干预，会使主定理失效。

[Light Tunnel 最新 v3](https://arxiv.org/html/2502.20099v3) 通过合成消融检查失败来源，并在 2026 年勘误中修订了对图像映射单射性的判断。本文的谱基线只能区分几何目标的最低残差与候选编码器的额外残差；它不取代这类机制与噪声对照实验。

白皮书各项要求目前对应为：

| 要求 | 本稿提供的结果 | 尚未覆盖 |
|---|---|---|
| 凸几何判据 | 超平面宽度与法向距离的双边界 | 一般不完美及随机干预 |
| 零误差对应识别 | 完整 clamping 覆盖下的线性等价类 | 任意非线性混合与编码器 |
| 连续和可微目标 | 宽度 Lipschitz；固定匹配协方差可微；规范化平滑宽度 | 对全局精确匹配处处光滑的零集保持方案 |
| 部分可识别性 | 已覆盖方向校准、兼容模型歧义定义及反例 | 一般块仿射等价类的可计算歧义直径 |
| 优化与误设诊断 | 可计算谱基线、残差差距和因果解释反例 | 单指标判别全部真实系统失败原因 |
| 有限样本与噪声 | 算子扰动界、置信区间、保守有界样本集中界 | 未知各向异性噪声、估计观测子空间、最优维度依赖 |
| 实验 | 精确合成数学排错 | Light Tunnel、Causal3DIdent、MCC 对照 |

下一轮最有价值的定理目标，是选定一种明确的近似干预模型，例如 $Q_i=\Sigma_i+\sigma_i^2I+F_i$ 且 $\|F_i\|_{\rm op}\le\eta_i$，把模型偏离预算 $\eta_i$ 与采样误差 $\varepsilon_i$ 分别放入证书。已知预算时可用总扰动界控制恢复；未知预算时，二者无法仅靠同一残差自动区分，需要额外标定或对照数据。另一个目标是从单节点法向推广到块干预的法向子空间，并处理不同干预块之间的一致对齐。

## 12 来源

- [项目白皮书](https://github.com/DongqiZuo00/Intervention/blob/main/WHITEPAPER.md)，第 1.3 节及路线图。
- [中文研究计划](https://github.com/DongqiZuo00/Intervention/blob/main/docs/research_plan_zh.md)，论文一第 1.1 至 1.5 节。
- Ahuja, Mahajan, Wang, Bengio. [Interventional Causal Representation Learning](https://proceedings.mlr.press/v202/ahuja23a.html). ICML 2023.
- Squires, Seigal, Bhate, Uhler. [Linear Causal Disentanglement via Interventions](https://proceedings.mlr.press/v202/squires23a.html). ICML 2023.
- Gamella, Bing, Runge. [Sanity Checking Causal Representation Learning on a Simple Real-World System](https://arxiv.org/html/2502.20099v3). 最新核对版本为 arXiv v3，2026 年 9 月 14 日。
