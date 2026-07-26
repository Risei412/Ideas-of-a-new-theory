# 弱く壊れた dark state における吸収・分散回復点分裂
## 計算手順・生死判定ロードマップ

**作成日:** 2026-07-26  
**対象:** EIT・CPT・dark state・ATS に近接した次期研究路線  
**位置づけ:** 新理論を先に宣言するための文書ではない。最小モデルで現象の有無を判定し、論文化可能な限定問いへ閉じるための計算設計書である。  
**第一投稿先の想定:** Physical Review A  
**原則:** 三準位 Λ 系で判定し、必要な場合だけ一準位を追加する。最初から一般理論、PRL、PRXを目標にしない。

> ## この文書の位置づけ（2026-07-26 確定）
>
> **本文書は新規提案ではない。提案24（LKCT）§5.2-2 の Step 1–2（GKSL/CPTP 物理実現）の実行計画である。**
> 新規提案番号は消費しない。
>
> 根拠：`Blueprints-of-theories/24_lifted_kernel_crossover_theory_proposal.md` §6 が
> 「**最も不足している物理接続:** 全結果が線形代数レベル。GKSL/CPTP 実現（§5.2-2）…が未着手。
> **監査後はここが唯一残った新規性の重心候補である。**」と明記し、同 §4.1 が
> 「GKSL/CPTP 物理クラス内で `sign(κ_lift·α_leak)=+1` が実現可能かという分類問題
> （現時点で最も有望な重心）」を未検証項目として残している。
> `docs/lkct-codimension-reality-audit.md` §4 の稜線対分裂は**凍結インスタンス1件でのみ検証**され、
> しかもその例では Im 側稜線が `Γ²ε ≈ −0.18221` と**非物理（負）**であった。同 §8:「GKSL 実現は未着手。」
>
> したがって本計算の目的は、**新現象の宣言ではなく、既存提案24の重心に対する生死判定**である。
> 判定結果は `docs/dark-ridge-novelty-verdict.md` に記録する。

---

## 0. 結論

最初に解くべき問いを、次に限定する。

> **弱く壊れた dark state を持つ最小 Λ 型 GKSL 系において、吸収応答と分散応答が理想 dark-state 値へ戻る正の制御条件は存在するか。存在するなら、二つの回復条件は一般に分裂し、その位置を局所 Schur 係数だけから予測できるか。**

観測量は複素感受率

\[
\chi(\omega)=\chi_{\mathrm{disp}}(\omega)+i\chi_{\mathrm{abs}}(\omega)
\]

の二成分に固定する。

\[
\chi_{\mathrm{disp}}=\operatorname{Re}\chi,
\qquad
\chi_{\mathrm{abs}}=\operatorname{Im}\chi.
\]

基準応答を \(\chi_\infty\)（§6.2、無限強制御での理想 dark-state 応答）とし、

\[
F_{\mathrm{disp}}
:=
\operatorname{Re}\!\left(\chi-\chi_\infty\right),
\qquad
F_{\mathrm{abs}}
:=
\operatorname{Im}\!\left(\chi-\chi_\infty\right)
\]

の零点を別々に求める。

> **基準を \(\chi_{\mathrm{dark}}=\chi(s,\gamma_{12}=0)\) にしてはならない。**
> その定義では leakage 項 \(\alpha\) が差から落ち、相殺が起こらないため
> \(F=0\) は \(\gamma_{12}=0\) 以外に非自明根を持たない（§6.3 と同じ規約に統一すること）。

中心対象は

\[
F_{\mathrm{disp}}=0,
\qquad
F_{\mathrm{abs}}=0
\]

を満たす二本の回復曲線である。

---

## 1. 既存計算から再利用するもの

以下は新規性として再主張せず、計算基盤としてのみ使う。

### 1.1 EIT 凍結理論

出典は `Frozen-Theories/EIT_no_go_go_theory_v6_2_English.tex`（v6.2）。節番号つきで再利用する。

| 項目 | 出典 |
|---|---|
| dark-state rank `dim D_opt = N_g − rank Ω` | §3.2 Theorem 1A |
| stationary dark-state 条件（三段階の梯子） | §3.4 Theorem 1B・§3.5 |
| weak-probe susceptibility の Schur 補表示 `Ξ = S_1 − βK_12S_2K_21/(γ_g+βS_2)` | §9.3 Theorem 2A |
| protected projector \(P\)・singular damping 下の protected channel | §7・§6.1 |
| exact-zero / Krylov certificate | §5.6 Theorem 4 |
| full response と sector-cut response の比較規約 `δχ_S` | §2・§9.5・§10 |
| **標準Λ系感受率の閉形式** `ρ_eg1^(1)` | **§9.6（boxed）** |
| **クロスオーバー変数 `y=|βS_2/γ_g|` と二分岐・吸収コントラスト `C_abs`** | **§9.9** |

> **§9.9 は本計算の核心的な前提である。** そこでは既に
> `y ≃ |Ω_c|²/(4Γ_e γ_12)` が定義され、`y≪1` と `y≫1` の二分岐
> （`ΔΞ = O(Γ^{-4})` vs `O(Γ^{-3})`、`C_abs = O(Γ^{-3})` vs `O(Γ^{-2})`）が確立している。
> したがって §7 の強スケール決定は「未知の指数を探す」作業ではなく、
> **`s=|Ω_c|²/Γ_e`, `a=0, b=1` という凍結理論の予想を検証する**作業である。
> ここで新しい指数が出ないこと自体は新規性にならない（§21 停止条件3）。
>
> また §9.9 は `C_abs = Im ΔΞ / Im S_1` という**吸収側のみ**の結果である。
> `Re Ξ` に対応する結果は凍結理論に存在しない。**分散側が本計算の実質的な未踏部分である。**

比較間で必ず固定するもの：

- 初期状態
- probe source
- readout
- 観測周波数
- 正規化
- rate convention
- control-field convention

### 1.2 LKCT から再利用する項目

抽象応答族

\[
A(s,\epsilon;z)=s(D_0+\epsilon D_L)+B(z)
\]

に対して得られている局所構造：

\[
R-R_\infty
=
-u\,\kappa_{\mathrm{lift}}
+v\,\alpha_{\mathrm{leak}}
+O(u^2,uv,v^2),
\]

ここで標準形では

\[
u=s\epsilon,\qquad v=s^{-1}.
\]

また、

\[
\kappa_{\mathrm{lift}}
=
p_P^\dagger B_{PP}^{-1}
(D_L)_{PP}
B_{PP}^{-1}c_P,
\]

\[
\alpha_{\mathrm{leak}}
=
p_P^\dagger B_{PP}^{-1}
B_{PF}D_F^{-1}B_{FP}
B_{PP}^{-1}c_P
\]

が局所 Schur データから計算できる。

ただし、EITへの物理的 pullback では \(u=s\epsilon\) とは限らない。  
**EITでの強スケールと ground-state decoherence の結合次数は、計算して決める。**

既存資産：

- `Blueprints-of-theories/24_lifted_kernel_crossover_theory_proposal.md`
- `docs/lkct-fan-blindness-exact-audit.md`
- `docs/lkct-codimension-reality-audit.md`
- `scripts/lkct_exact_audit.py`
- `scripts/lkct_codim_audit.py`

---

## 2. 今回固定する物理範囲

### 2.1 最小系

三準位 Λ 系

\[
\{|g_1\rangle,\ |g_2\rangle,\ |e\rangle\}
\]

から始める。

- probe: \(|g_1\rangle\leftrightarrow|e\rangle\)
- control: \(|g_2\rangle\leftrightarrow|e\rangle\)
- dark coherence: \(\rho_{g_1g_2}\)
- lifting parameter: ground-state decoherence \(\gamma_{12}\)

### 2.2 維持する仮定

- 有限次元
- time-independent
- Markovian GKSL
- stationary rotating frame
- weak probe
- 一点または狭い固定周波数窓
- unique steady state、または trace-zero 部分空間上で well-defined な group inverse
- source/readout/normalization 固定

### 2.3 最初は扱わないもの

- probe saturation
- 非 Markov 浴
- 空間伝搬
- collective effect
- Doppler averaging
- 多光子過程
- NV の全 10 準位モデル
- 情報熱力学
- 一般の EIT–ATS 統一分類

これらを同時に入れると、現象の死因が判別できなくなる。

### 2.4 必須ゲート（範囲外にしてはならないもの）

- **EIT/ATS 判別**（ガイド L252–253）: transparency dip だけで EIT を同定しない。
  ground-coherence 依存・control-power scaling・pole/residue・two-photon linewidth・
  full-minus-cut 差分を確認する。Stage 8（§12）の必須条件とする。
- **`χ_full=0` を no-go 判定に使わない**（ガイド L223）: 凍結理論の no-go 対象は
  全応答の零点ではなく指定 sector による差分 `δχ_S` である。
  本計算の `F=0` は**回復条件であって no-go ではない**ことを、記述上つねに区別する。

---

## 3. 記号とスケール

混同を避けるため、次を使う。

| 記号 | 意味 |
|---|---|
| \(\Gamma_e\) | 励起状態の全崩壊率 |
| \(\gamma_{12}\) | ground-state coherence の減衰率 |
| \(\Omega_p\) | probe Rabi 周波数 |
| \(\Omega_c\) | control Rabi 周波数 |
| \(\Delta_p\) | probe 一光子離調 |
| \(\delta\) | 二光子離調 |
| \(s\) | 漸近展開に使う強制御スケール |
| \(\chi\) | weak-probe susceptibility |
| \(\chi_{\mathrm{dark}}\) | \(\gamma_{12}=0\) の理想 dark-state 基準応答 |

強スケール \(s\) は最初から固定しない。候補は

\[
s=|\Omega_c|,\qquad
s=\frac{|\Omega_c|^2}{\Gamma_e},
\qquad
s=\Gamma_{\mathrm{eng}}
\]

である。

三準位 Λ 系では、励起状態消去後の有効 ground-state dynamics を見て、

\[
s=\frac{|\Omega_c|^2}{\Gamma_e}
\]

が自然な場合が多い。しかし、これは導出して確認する。

---

## 4. Stage 0: 規約の凍結

計算前に以下を一つの設定ファイルへ固定する。

### 4.1 Hamiltonian

回転枠で、例えば

\[
H_0
=
-\Delta_p |e\rangle\langle e|
-\delta |g_2\rangle\langle g_2|
+
\frac{\Omega_c}{2}|e\rangle\langle g_2|
+
\frac{\Omega_c^*}{2}|g_2\rangle\langle e|.
\]

probe 摂動は

\[
V_p
=
\frac{1}{2}|e\rangle\langle g_1|,
\qquad
H=H_0+\Omega_p V_p+\Omega_p^*V_p^\dagger.
\]

### 4.2 Jump operators

励起状態崩壊：

\[
L_1=\sqrt{\Gamma_1}|g_1\rangle\langle e|,
\qquad
L_2=\sqrt{\Gamma_2}|g_2\rangle\langle e|,
\]

\[
\Gamma_e=\Gamma_1+\Gamma_2+\Gamma_{\mathrm{other}}.
\]

ground-state pure dephasing は、\(\rho_{g_1g_2}\) が正確に \(\gamma_{12}\) で減衰する規約を使う。

一例：

\[
L_\phi
=
\sqrt{\frac{\gamma_{12}}{2}}
\left(
|g_1\rangle\langle g_1|
-
|g_2\rangle\langle g_2|
\right).
\]

実装後に必ず

\[
\left.\frac{d}{dt}\rho_{g_1g_2}\right|_{\phi}
=
-\gamma_{12}\rho_{g_1g_2}
\]

を単体テストする。

### 4.3 規約テスト

- Hermiticity preservation
- trace preservation
- 全 jump rate 非負
- \(\Omega_p=0\) で定常状態が得られる
- \(\gamma_{12}=0,\delta=0\) で dark state が回収される
- 感受率の符号規約を一つに固定する
- \(\operatorname{Im}\chi>0\) が吸収になるかを確認する

**Gate S0:** 上記が全て通らなければ次へ進まない。

---

## 5. Stage 1: weak-probe 応答の厳密構築

### 5.1 Liouvillian

\[
\mathcal L(\Omega_p)
=
\mathcal L_0
+
\Omega_p\mathcal V
+
\Omega_p^*\bar{\mathcal V}.
\]

密度行列を

\[
\rho_{\mathrm{ss}}
=
\rho^{(0)}
+
\Omega_p\rho^{(1)}
+
\Omega_p^*\bar{\rho}^{(1)}
+
O(|\Omega_p|^2)
\]

と展開する。

零次：

\[
\mathcal L_0\rho^{(0)}=0,
\qquad
\operatorname{Tr}\rho^{(0)}=1.
\]

一次：

\[
\mathcal L_0\rho^{(1)}
=
-\mathcal V\rho^{(0)},
\qquad
\operatorname{Tr}\rho^{(1)}=0.
\]

### 5.2 解法

優先順位：

1. trace-one 行を置換した constrained linear solve
2. trace-zero 部分空間での逆行列
3. group inverse
4. 数値 pseudo-inverse

symbolic 段階では 1 または 2 を使う。  
pseudo-inverse は検算用に限定する。

### 5.3 感受率

probe coherence から

\[
\chi
=
C_\chi
\frac{\rho^{(1)}_{eg_1}}{\Omega_p}
\]

を定義する。定数 \(C_\chi\) は零点位置に影響しないため、最初は \(C_\chi=1\) でもよい。

### 5.4 既知式との照合

標準 Λ 系の解析式と、

- 極位置
- \(\gamma_{12}\to0\)
- \(\Omega_c\to0\)
- \(|\Delta_p|\to\infty\)

の極限を照合する。

**Gate S1:** symbolic 式と直接 Liouvillian solve が複数の有理パラメータ点で一致すること。

---

## 6. Stage 2: 理想 dark-state 基準の定義

基準応答を曖昧にしてはならない。

### 6.1 第一基準

\[
\chi_{\mathrm{dark}}(s,z)
:=
\chi(s,\gamma_{12}=0,z).
\]

この定義は有限 \(s\) の exact-kernel 基準である。

### 6.2 第二基準

必要なら

\[
\chi_\infty(z)
:=
\lim_{s\to\infty}
\chi(s,\gamma_{12}=0,z)
\]

も計算する。

### 6.3 主解析で使う差分

まず

\[
\Delta\chi(s,\gamma_{12};z)
=
\chi(s,\gamma_{12};z)
-
\chi(s,0;z)
\]

を調べる。

ただし、LKCT型の「lifting と leakage の相殺」を見るには

\[
\widetilde{\Delta\chi}
=
\chi(s,\gamma_{12};z)-\chi_\infty(z)
\]

も必要である。

二つを混同しない。

- \(\Delta\chi\): decoherence が加えた純粋な差
- \(\widetilde{\Delta\chi}\): 有限制御漏洩と decoherence lifting の競合

回復点分裂の中心対象は \(\widetilde{\Delta\chi}\) とする。

---

## 7. Stage 3: EIT版二変数 jet の抽出

### 7.1 強スケールの決定

候補変数について asymptotic series を比較する。

\[
x=\frac{1}{|\Omega_c|},
\qquad
x=\frac{\Gamma_e}{|\Omega_c|^2},
\qquad
x=\frac{1}{\Gamma_{\mathrm{eng}}}.
\]

\(\widetilde{\Delta\chi}\) が原点 \((x,\gamma_{12})=(0,0)\) で解析的になる変数を採用する。

### 7.2 最低次数の抽出

一般形を

\[
\widetilde{\Delta\chi}
=
-\gamma_{12}s^{a}\kappa
+
s^{-b}\alpha
+
\text{higher order}
\]

と置く。

ここで

- \(a\): lifting 項の強スケール次数
- \(b\): finite-control leakage の減衰次数
- \(\kappa,\alpha\in\mathbb C\): 局所係数

である。

**重要:** \(a=b=1\) を仮定しない。

EITへの pullback では例えば

\[
a=0,\qquad b=1
\]

となり、

\[
s\gamma_{12}=\mathrm{const.}
\]

が回復則になる可能性がある。

### 7.3 weighted-path 法

\[
\gamma_{12}=e_0s^{-q}
\]

を代入し、各 \(q\) に対する leading power を exact arithmetic で取得する。

- breakpoint
- dominant monomial
- cancellation angle
- initial form

を記録する。

これにより \(a+b\) を独立に確認する。

### 7.4 係数の抽出

\[
\kappa
=
-\lim
\frac{\widetilde{\Delta\chi}_{\mathrm{lifting}}}
{\gamma_{12}s^a},
\qquad
\alpha
=
\lim
s^b\widetilde{\Delta\chi}_{\mathrm{leakage}}.
\]

可能なら Schur 補ブロックから閉形式で導出する。

数値微分だけで係数を決めてはならない。

**Gate S2:** symbolic series、Schur 係数、有限差分の三者が一致すること。

---

## 8. Stage 4: 吸収・分散回復点の予測

実汎関数を

\[
\Phi_{\mathrm{disp}}(z)=\operatorname{Re}z,
\qquad
\Phi_{\mathrm{abs}}(z)=\operatorname{Im}z
\]

とする。

### 8.1 回復条件

一次予測は

\[
-\gamma_{12}s^a\Phi(\kappa)
+
s^{-b}\Phi(\alpha)=0.
\]

したがって

\[
\boxed{
\gamma_{12}s^{a+b}
=
\frac{\Phi(\alpha)}{\Phi(\kappa)}
}
\]

である。

### 8.2 存在条件

正の物理領域に回復曲線が入る条件：

\[
\Phi(\kappa)\Phi(\alpha)>0.
\]

よって

\[
r_{\mathrm{disp}}
=
\frac{\operatorname{Re}\alpha}
{\operatorname{Re}\kappa},
\qquad
r_{\mathrm{abs}}
=
\frac{\operatorname{Im}\alpha}
{\operatorname{Im}\kappa}
\]

を計算し、

\[
r_{\mathrm{disp}}>0,
\qquad
r_{\mathrm{abs}}>0
\]

を別々に判定する。

### 8.3 分裂幅

自然な無次元分裂量：

\[
\Delta_{\mathrm{split}}
=
r_{\mathrm{disp}}-r_{\mathrm{abs}}.
\]

標準 LKCT 形では

\[
\Delta_{\mathrm{split}}
=
\frac{\operatorname{Im}(\kappa\alpha^*)}
{\operatorname{Re}\kappa\,\operatorname{Im}\kappa}.
\]

EIT pullback でも同じ形が出るかを確認する。  
異なる正規化を使う場合は、観測可能な \(s\) または \(|\Omega_c|^2\) の差へ戻す。

### 8.4 完全回復の余次元

複素応答全体の回復

\[
\widetilde{\Delta\chi}=0
\]

は二本の実方程式である。

Jacobian

\[
J=
\frac{\partial
(\operatorname{Re}\widetilde{\Delta\chi},
 \operatorname{Im}\widetilde{\Delta\chi})}
{\partial
(\gamma_{12}s^a,s^{-b})}
\]

の rank を計算する。

- rank 2: 完全回復は孤立点
- rank 1: 二本の回復曲線が一致しうる
- rank 0: 一次係数が消失し、高次解析が必要

**完全回復曲線を一般に主張してはならない。**

---

## 9. Stage 5: exact root による検証

### 9.1 固定 \(s\) での零点

各 \(s\) に対して

\[
F_{\mathrm{disp}}(\gamma_{12})=0,
\qquad
F_{\mathrm{abs}}(\gamma_{12})=0
\]

を解く。

### 9.2 推奨グリッド

最初のスモーク：

\[
s\in\{10^2,10^3,10^4\}
\]

または物理単位へ戻した同等の3 decade。

本番：

- 20–40 log points
- \(\gamma_{12}\) は予測点の \(10^{-2}\) から \(10^2\) 倍
- detuning は固定一点から開始

### 9.3 根の認証

優先順位：

1. 有理係数化できる場合は Sturm 列
2. interval arithmetic
3. 高精度 mpmath + 符号ブラケット
4. 通常の root finder

通常の root finder 単独では認証としない。

### 9.4 収束判定

予測値を \(\gamma_{12}^{\mathrm{pred}}(s)\)、厳密根を \(\gamma_{12}^{\mathrm{root}}(s)\) とし、

\[
E(s)
=
\left|
\frac{\gamma_{12}^{\mathrm{root}}
-\gamma_{12}^{\mathrm{pred}}}
{\gamma_{12}^{\mathrm{pred}}}
\right|
\]

を計算する。

期待する挙動：

\[
E(s)\propto s^{-c},
\qquad c>0.
\]

少なくとも3 decadeで傾きを確認する。

### 9.5 錐内一意性

予測点の周囲

\[
\left[
\frac{1}{2}\gamma_{12}^{\mathrm{pred}},
2\gamma_{12}^{\mathrm{pred}}
\right]
\]

に根がちょうど一つあることを確認する。

遠方根が存在してもよい。  
ただし、それを回復稜線の根と混同しない。

**Gate S3:** 錐内一意根、符号反転、漸近収束の三つが通ること。

---

## 10. Stage 6: 物理実現可能領域の探索

### 10.1 探索パラメータ

最初は4軸以内に制限する。

- branching ratio \(\Gamma_1/\Gamma_e\)
- 一光子離調 \(\Delta_p/\Gamma_e\)
- 二光子離調 \(\delta/\Gamma_e\)
- control phase または dipole relative phase

必要なら5軸目として追加する：

- excited-state pure dephasing

### 10.2 判定量

各点で記録する。

\[
\operatorname{Re}\kappa,\quad
\operatorname{Im}\kappa,\quad
\operatorname{Re}\alpha,\quad
\operatorname{Im}\alpha,
\]

\[
r_{\mathrm{disp}},\quad
r_{\mathrm{abs}},\quad
\Delta_{\mathrm{split}}.
\]

クラス：

| class | 条件 |
|---|---|
| D+A | 分散・吸収とも正の回復曲線 |
| D only | 分散のみ |
| A only | 吸収のみ |
| none | どちらもなし |
| degenerate | 係数が零または Jacobian rank 低下 |

### 10.3 微調整判定

候補点の周囲を

- ±1%
- ±5%
- ±10%

で摂動する。

採用条件：

- 正の回復曲線が有限体積領域に存在
- \(\Delta_{\mathrm{split}}\) の符号が安定
- 根が観測可能な範囲に残る
- susceptibility contrast が数値ノイズより十分大きい

**Gate S4:** 少なくとも一つの回復曲線が開集合で存在すること。

---

## 11. Stage 7: destruction controls

現象の担い手を特定するため、以下を一つずつ壊す。

### C0: exact dark state

\[
\gamma_{12}=0.
\]

lifting 項が消え、回復曲線の概念が退化することを確認する。

### C1: leakage 除去

Schur coupling

\[
B_{PF}=0
\quad\text{または}\quad
B_{FP}=0
\]

に対応する物理結合を切る。

\[
\alpha=0
\]

となり、有限制御 leakage との相殺が消えることを確認する。

### C2: 実応答化

全位相を実に固定し、

\[
\operatorname{Im}(\kappa\alpha^*)=0
\]

となる対照を作る。

吸収・分散分裂が消えるか、片方が自明化することを確認する。

### C3: ground coherence 破壊

\(\gamma_{12}\) を EIT window より十分大きくし、long-lived dark coherence を消す。

回復曲線が残るなら、dark-state固有という主張を撤回する。

### C4: 位相反転

relative phase を変え、

\[
\Phi(\kappa)\Phi(\alpha)
\]

の符号が反転するとき、回復曲線の有無も反転するか確認する。

**Gate S5:** 少なくとも一つの destruction control で現象が消えること。

---

## 12. Stage 8: ATS 対照

ATSは主問題ではなく、dark-state機構を検証する対照群として使う。

### 12.1 ATS 対照の定義

単なる「二つのピーク」をATSと呼ばない。次を使う。

- ground-state coherence を消す
- dressed poles は残す
- 二つの resolved poles が支配
- 可能なら pole-residue decomposition で interference zero がないことを確認

### 12.2 比較規約

EIT側とATS側で固定するもの：

- probe observable
- 周波数点または窓
- 総 optical linewidth
- peak separation
- probe normalization

### 12.3 判定

ATS側でも

\[
F_{\mathrm{disp}}=0,\qquad F_{\mathrm{abs}}=0
\]

の分裂回復曲線が出るか。

#### 結果A: ATS側では消える

主張：

> 回復点分裂は、dark-state lifting と finite-control leakage の競合に依存する。

#### 結果B: ATS側にも残る

dark-state固有という表現を撤回する。  
問いを

> 複素 resolvent 応答における汎関数別回復点分裂

へ格下げする。

この場合、EITは最小実験場であり、理論対象そのものではない。

---

## 13. Stage 9: 三準位で死んだ場合の最小四準位拡張

三準位で回復曲線が物理領域に存在しない場合だけ、一準位を追加する。

### 13.1 失敗原因による分岐

#### 原因A: \(\kappa,\alpha\) が常に同一直線上の複素数

一つの coherent leakage 経路を追加する。

候補：

- 第二励起状態 \(|e_2\rangle\)
- N 型四準位
- double-Λ の片側

目的は独立な複素位相を一つだけ導入すること。

#### 原因B: branching structure が符号を固定する

一つの shelving state \(|s\rangle\) を追加する。

目的は population return と coherence leakage の符号構造を分離すること。

#### 原因C: lifting 項が高次でしか現れない

ground-state population relaxation を一種類だけ追加する。

### 13.2 禁止

以下を同時に追加しない。

- 第二励起状態
- shelving
- 非 Markov memory
- strong probe
- propagation

一度に一仮定だけ壊す。

### 13.3 四準位での目標

最も価値が高い結果は

\[
\text{三準位では no-go}
\quad+\quad
\text{四準位で go}
\]

である。

この場合の論文の中心は、

> 吸収・分散回復点分裂を可能にする最小準位構造

となる。

---

## 14. 生死判定表

| 判定 | 結果 | 方針 |
|---|---|---|
| GO-1 | 三準位で正の回復曲線が開集合に存在 | PRA向け最短論文 |
| GO-2 | 三準位no-go、最小四準位でgo | より強いPRA論文 |
| GO-3 | dark-state側のみ分裂、ATS側では消失 | dark-state lifting機構として主張 |
| DOWNGRADE | ATS側にも同じ現象 | 一般resolvent現象へ格下げ |
| FREEZE-1 | 正の根が微調整点にしかない | 凍結 |
| FREEZE-2 | 三・四準位とも物理領域に根なし | 凍結 |
| FREEZE-3 | 既存EIT crossover式の単純な書換え | 新理論化しない |
| REDIRECT | 応答分裂より熱流差の方が非自明 | NV情報熱力学の限定問いへ移行 |

---

## 15. 論文化の最小経路

### 最小主張

> 弱く壊れた dark state の近傍では、有限制御漏洩と dark-state lifting が競合し、吸収と分散は一般に異なる制御条件で理想応答値へ戻る。その二つの回復位置と分裂幅は、局所 Schur 係数から予測できる。

### 必須結果

1. 最小 GKSL モデル
2. susceptibility の exact expression
3. EIT版二変数 jet
4. 吸収・分散回復条件
5. 分裂幅
6. exact root validation
7. 開集合での存在
8. destruction control
9. ATS対照

### 必須でないもの

- 一般有限次元定理
- 全材料への適用
- NV実験値への完全fit
- PRL級一般性
- 情報熱力学
- 非Markov一般化

### 推奨図

1. \((\log s,\log\gamma_{12})\) 平面の  
   \(F_{\mathrm{disp}}=0\) と \(F_{\mathrm{abs}}=0\)
2. 予測根と exact root の比較
3. \(r_{\mathrm{disp}},r_{\mathrm{abs}}\) の存在相図
4. EIT側とATS側の比較

---

## 16. 実装ファイル案

```text
scripts/
  dark_ridge_lambda_model.py
  dark_ridge_symbolic.py
  dark_ridge_asymptotics.py
  dark_ridge_root_certificate.py
  dark_ridge_parameter_scan.py
  dark_ridge_ats_control.py
  dark_ridge_four_level.py

results/dark_ridge/
  conventions.json
  symbolic_coefficients.json
  ridge_roots.csv
  convergence.csv
  parameter_classes.csv
  controls.csv
  ats_comparison.csv

certificates/
  dark_ridge_symbolic_certificate.txt
  dark_ridge_root_certificate.txt
  dark_ridge_controls_certificate.txt

docs/
  dark-ridge-stage-report.md
```

---

## 17. 各スクリプトの役割

### `dark_ridge_lambda_model.py`

- Hamiltonian
- jump operators
- Liouvillian
- weak-probe source
- readout
- trace constraint
- convention tests

### `dark_ridge_symbolic.py`

- \(\rho^{(0)}\)
- \(\rho^{(1)}\)
- \(\chi\)
- \(\chi_{\mathrm{dark}}\)
- \(\chi_\infty\)
- symbolic residual tests

### `dark_ridge_asymptotics.py`

- 強スケール候補の比較
- \(a,b\) の抽出
- \(\kappa,\alpha\) の抽出
- weighted-path valuation
- Jacobian rank
- \(\Delta_{\mathrm{split}}\)

### `dark_ridge_root_certificate.py`

- \(F_{\mathrm{disp}}\), \(F_{\mathrm{abs}}\) の零点
- Sturm または interval certificate
- 錐内一意性
- 符号反転
- 漸近収束

### `dark_ridge_parameter_scan.py`

- Sobol または Latin hypercube
- D+A / D only / A only / none 分類
- ±1%, ±5%, ±10% 摂動
- 開集合判定

### `dark_ridge_ats_control.py`

- dark coherence destruction
- pole/residue audit
- EITとATSの比較
- 同一規約での回復曲線判定

### `dark_ridge_four_level.py`

- 三準位で死んだ場合だけ使う
- 一回につき一準位・一機構のみ追加
- 三準位no-goの原因を破る最小構成

---

## 18. 簡易テスト

### T0: trace/Hermiticity

\[
\|\mathcal L^\dagger(I)\|=0,
\qquad
\mathcal L(\rho^\dagger)=\mathcal L(\rho)^\dagger.
\]

### T1: dephasing convention

\[
\dot\rho_{g_1g_2}=-\gamma_{12}\rho_{g_1g_2}.
\]

### T2: dark state

\[
\gamma_{12}=0,\quad \delta=0
\]

で dark vector が Hamiltonian coupling の kernel に入る。

### T3: weak-probe linearity

\[
\frac{\rho_{eg_1}(\Omega_p)}
{\Omega_p}
\]

が \(\Omega_p\) を10分の1にしても一定。

### T4: symbolic/numeric一致

有理パラメータ10点で相対残差

\[
<10^{-10}.
\]

### T5: coefficient recovery

symbolic \(\kappa,\alpha\) と有限差分が一致。

### T6: root bracket

予測根の半分と2倍で符号反転。

### T7: destruction control

少なくとも一つの control で回復根が消える。

---

## 19. 計算量の見積り

### 三準位

- Hilbert次元: 3
- Liouville次元: 9
- trace-zero 実効次元: 8
- symbolic solve: 軽量から中程度
- 数値scan: 軽量
- root certificate: 軽量

通常のノートPCで十分である。

### 四準位

- Hilbert次元: 4
- Liouville次元: 16
- trace-zero 実効次元: 15
- 完全symbolic逆行列は式膨張の恐れ
- Schur補と部分symbolic化を優先
- 数値scanは依然として軽量

### 本番scanの目安

- 4次元 Sobol: 2,000–10,000点
- 各点3–5個の \(s\)
- root solve 2汎関数
- 合計 \(10^4\)–\(10^5\) linear solves

行列が最大16×16なので現実的である。

---

## 20. 優先順位

### Priority 0: 生死判定

1. 三準位 Liouvillian
2. weak-probe \(\chi\)
3. 強スケール \(s\) の同定
4. \(a,b,\kappa,\alpha\)
5. 正の回復条件の有無

### Priority 1: 論文化可能性

6. exact root
7. 開集合
8. destruction controls
9. ATS対照

### Priority 2: 強化

10. 三準位no-go
11. 最小四準位go
12. NVパラメータへの写像

Priority 0 が失敗した段階で、Priority 1以降へ進まない。

---

## 21. 最終停止条件

次のいずれかが成立すれば、この路線を凍結する。

1. 三準位と最小四準位の両方で、正の回復曲線が存在しない
2. 根が余次元の高い微調整集合にしか存在しない
3. 分裂が単なる detuning shift または既知のEIT linewidth式へ完全還元される
4. ATS対照でも同一条件・同一係数式が成立し、dark-stateとの関係が消える
5. 実験的に必要な \(s\) または \(\gamma_{12}\) が非現実的
6. susceptibility差が観測ノイズ以下
7. source/readout規約を変えないと現象が出ない

停止条件が発火した場合、理論名を残さず、計算資産だけを保存する。

---

## 22. 情報熱力学への移行条件

この計算で応答回復点分裂が死んだ場合でも、直ちに広いNV情報熱力学へ移らない。

移行するなら問いを次に限定する。

> **同一の定常蛍光応答と同一のdark-state cut応答を与える二つのNV optical-pumping実装は、異なるentropy-production scalingを持ちうるか。**

必要計算：

- 同一応答を持つ二つのGKSL実装
- 各jumpへのreservoir assignment
- local detailed balance
- heat current
- entropy production
- 応答同値性と熱力学的非同値性

これは本ロードマップより計算距離が長い。  
したがって、まず dark-state 回復点分裂の Priority 0 を実行する。

---

## 23. 最初に実行する具体的な順序

```text
Step 1  三準位Λ Liouvillianを実装
Step 2  規約テスト S0
Step 3  weak-probe susceptibilityをsymbolic/numericで一致確認
Step 4  χ_dark と χ_infty を分離定義
Step 5  強スケール候補を比較し、解析的な変数を選ぶ
Step 6  a,b,κ,α を抽出
Step 7  Re/Im の正の回復条件を判定
Step 8  正の候補がなければ三準位no-goを調べる
Step 9  候補があれば exact root と収束を認証
Step 10 開集合scanとdestruction controls
Step 11 ATS対照
Step 12 必要な場合だけ最小四準位へ進む
Step 13 GO/FREEZEを決定
Step 14 GOの場合のみ論文構成へ移る
```

---

## 24. この計算で最初に答えるべき三問

**Q1（還元テスト・最優先）**
\(\operatorname{Re}/\operatorname{Im}\bigl(\chi(s,\gamma_{12})-\chi_\infty\bigr)\) の零点分裂は、
凍結EIT理論 §9.9 のクロスオーバー \(y=|\Omega_c|^2/(4\Gamma_e\gamma_{12})\) と、
標準的な ac-Stark シフトによる分散零点の移動へ代数的に還元されるか。
**還元されるなら §21 停止条件3 が発火し、この路線はそこで終了する。**

**Q2（自己応答性テスト）**
source と readout が同一の probe coherence \(\rho_{eg_1}\) に乗る自己応答型の EIT pullback において、
\(\Phi(\kappa)\Phi(\alpha)>0\) は物理パラメータの開集合で実現するか。
それとも受動性（\(\operatorname{Im}\chi\ge0\)）が吸収側の回復曲線を構造的に禁じるか。

**Q3（指数と分裂）**
EIT pullback における \((a,b)\) は何か（\(s^2\gamma_{12}\)・\(s\gamma_{12}\)・それ以外）。
またそのとき \(r_{\mathrm{disp}}-r_{\mathrm{abs}}\) は有限体積の物理パラメータ領域で非零か。

---

> **Q1 を先頭に置いた理由。** 三準位Λ系の弱プローブ \(\chi\) には凍結理論 §9.6 の閉形式があり、
> 「回復点分裂」は既知式の Re/Im 零点位置の差に過ぎない可能性が最初から高い。
> リポジトリの最重要原則（理論固有現象と非還元性、ガイド §0・§3）からして、
> 還元テストは Priority 0 の第一問でなければならない。
>
> **Q2 が「存在するか」でない理由。** `docs/lkct-codimension-reality-audit.md` §6（Y7）は
> 「CPTP は符号を強制しない」を自己応答30例で示したが、そこでの反例は
> `B_PP` が複素（非共鳴）の場合であり、監査自身が
> 「**GKSL 由来の `B_PP` が追加の構造を持つ可能性は排除されていない。
> Step 1–2 で GKSL から `B_PP` を実際に導出するまで、no-go 分岐を捨ててはならない**」
> と留保している。EIT 弱プローブはまさに source と readout が同一 coherence に乗る自己応答型であり、
> 反例が出た側ではなく制約が効きうる側に落ちる危険がある。
>
> **この三問が解けるまで、新しい一般理論を宣言しない。**

### 24.1 手計算による事前予想（要検証、これ自体は結論ではない）

凍結理論 §9.6 の boxed 式

\[
\rho^{(1)}_{eg_1}=\frac{i\Omega_p}{2}\cdot\frac{\gamma_g}{D},
\qquad
D=(\gamma_{31}-i\Delta_p)\gamma_g+\beta,
\qquad
\gamma_g=\gamma_{12}-i\delta_2,
\qquad
\beta=\frac{|\Omega_c|^2}{4}
\]

を使う。この規約では \(\gamma_{12}=0,\delta_2=0\) で \(\chi\to0\) なので \(\chi_\infty=0\)、
すなわち \(\widetilde{\Delta\chi}=\chi\) である。\(\chi\propto i\gamma_g/D\) より
（\(i\) が Re と Im を入れ替えることに注意）

\[
\gamma_g\overline{D}
=(\gamma_{31}+i\Delta_p)|\gamma_g|^2+\beta\gamma_g,
\]

\[
\operatorname{Re}\bigl(\gamma_g\overline D\bigr)
=\gamma_{31}(\gamma_{12}^2+\delta_2^2)+\beta\gamma_{12},
\qquad
\operatorname{Im}\bigl(\gamma_g\overline D\bigr)
=\Delta_p(\gamma_{12}^2+\delta_2^2)-\beta\delta_2 .
\]

\(\chi_{\mathrm{abs}}\propto\operatorname{Re}(\gamma_g\overline D)\)、
\(\chi_{\mathrm{disp}}\propto-\operatorname{Im}(\gamma_g\overline D)\) であるから：

- **吸収回復点:** \(\gamma_{31}(\gamma_{12}^2+\delta_2^2)+\beta\gamma_{12}=0\)。
  \(\gamma_{31},\beta,\gamma_{12}>0\) では全項が正で**解なし**。
- **分散回復点:** \(\beta=\Delta_p(\gamma_{12}^2+\delta_2^2)/\delta_2\)。
  \(\Delta_p/\delta_2>0\) なら**正の解が存在する**。ただし \(\gamma_{12}\ll\delta_2\) では
  \(\beta\approx\Delta_p\delta_2\) となり \(\gamma_{12}\) に依存しない
  → 既知の ac-Stark シフトへの還元（Q1 発火）が強く疑われる。

⇒ 予想クラスは **D only**、\(\Delta_{\mathrm{split}}\) は片側が空のため定義されない。

**ただしこれは結論ではない。** §9.6 の式は \(\rho^{(0)}=|g_1\rangle\langle g_1|\) を前提とする。
実際の Λ 系では branching \(\Gamma_1,\Gamma_2\) と control による optical pumping で定常分布が
\(g_2\) 側へ移り、**population inversion による利得（\(\operatorname{Im}\chi<0\)）が起こりうる**。
その場合、吸収稜線を禁じていた正値性が破れる（§13.1 の「原因B」に対応）。
したがって**真の定常状態 \(\rho^{(0)}\) を含む完全な Liouvillian 解**でのみ判定する。
これは 9×9 の記号解1本で済み、Stage 0–3 で完結する。
