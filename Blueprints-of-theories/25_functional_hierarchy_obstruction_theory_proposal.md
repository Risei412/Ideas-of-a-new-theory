# 提案25: 機能階層障害理論（Functional Hierarchy Obstruction Theory / FHOT）

## 一行サマリ

有限次元 time-local GKSL 系の sector `S` について、**線形応答差分 `δχ_S` が全周波数で exact zero
かつ全次数の counting cumulant 差分も weak-probe 極限で消えていながら**、同一 probe・同一比較規約の
下で **量子 Fisher 情報（QFI）の sector 分解応答差分 `δF_S` が非零かつ `Γ→∞` で O(1) 保護される**
という現象（Φ階層排他ゼロ / functional-graded exact-zero splitting）を狙う。
成立条件は、symmetric logarithmic derivative（SLD）作用素と sector 射影の**非可換性の rank**で
分類されると予想する（未証明・Stage 0仮説）。

**作成日:** 2026-07-26
**位置づけ:** ガイド §6.1 **P1「Nonlinear functional hierarchy」**（壊す仮定：linear response
functional）に対する Stage 0 理論設計図。この空白地帯は現時点で他提案に占有されていない。
**型（§2）:** (A) 現象論的理論（sector 分解 QFI 応答という新しい観測可能量）＋ (B) 数学的定理型
（非可換 rank による分類・条件付き還元定理）の複合。対象系は有限次元・time-local GKSL・weak probe。
想定読者は量子計測（quantum metrology）、開放系、量子情報の交差領域。
**判定:** **⚠️ 内部監査により中心命題は現行の書き方では維持できないと判定された（2026-07-26）。
下の監査ブロックを必ず先に読むこと。** 判断（撤回／縮小継続）は所有者待ち。

> ## ⚠️ この文書を読む前に（2026-07-26 Stage 0 内部監査）
>
> 検証器 `scripts/fhot_smoke.py`（F0–F8、判定に浮動小数点を不使用）、
> 証明書 `certificates/fhot_smoke_2026-07-26.txt`、評価 `docs/fhot-stage0-internal-audit.md`。
> **結果は両面である。**
>
> | 監査項目 | 判定 | 一次資料 |
> |---|---|---|
> | (i) `δχ_S(Δ) ≡ 0` の全周波数 exact zero | **PASS**（分子多項式の係数がすべて 0） | 同 §2 F2 |
> | (iii) `δF_S ≠ 0` | **PASS**（厳密有理数 `−1216/(52260Δ²+2939625)`） | 同 §2 F4 |
> | QFI の2独立実装の一致 | **PASS**（固有分解公式 ⟷ SLD Lyapunov 解） | 同 §2 F3 |
> | **中心命題の書き方** | **⚠️ VACUOUS。**現象は自明な機構に完全に帰着する | **同 §3** |
> | **分類予想（`r_nc>0` が必要条件）** | **⚠️ 反証。**`r_nc=0` かつ `δF_S≠0` の明示的反例 | **同 §4** |
> | 正値性による一般判定 | **PASS**（生き残った唯一の非自明な結果） | 同 §5 |
>
> **🆙 得たもの:** 最小模型（4準位、厳密有理数レート）で (i)(iii) の**同時成立を厳密に構成できた。**
> さらに閉形式 `F_Q = 4|χ|²/Σ_A`、`χ = D_A·g(Δ)` が残差 0 で成立する。
> 副産物として `scripts/` に初めて GKSL superoperator 層・SLD/QFI の2独立実装が入った。
>
> **⚠️ 失ったもの:** `δχ_S≡0` は population 差 `D_A` の不変性に、`δF_S≠0` は population 和
> `Σ_A` の変化に**完全に**帰着する。そして **`Σ_A = tr(ρΠ_A)` は線形汎関数である**
> （`Π_A=|g1><g1|+|e1><e1|`）。sector は「ある線形汎関数には見えている」。
> より一般に、**有限次元でトモグラフィが可能な設定では状態の任意の汎関数は線形汎関数の
> 全体から決まるため、「線形汎関数に盲目・非線形汎関数に可視」という枠組みそのものが
> 原理的に空である。** §6 の stop condition 2 が発火した。
>
> **✅ 生き残った結果（模型に依存しない）:** population の正値性 `|D_A| ≤ Σ_A` から
> **任意の scaling path** について
> `ν(F_Q) < ν(χ) ⟺ ν(g) < ν(Σ_A) − ν(D_A) ≤ 0`。
> **すなわち QFI が線形応答を漸近的に追い越すには、probe optical coherence の減衰
> `Γ_coh` 自体が `Γ→∞` で消えること（保護された coherence）が必要であり、
> population の再配分だけでは決して達成できない。** 保護の源泉は非線形性ではなく
> あくまで線形理論側の kernel 構造であるという否定的だが明確な指針。
>
> **推奨は (a) 撤回**（§6.4 へ記録し番号25 を欠番化）。理由と代替案 (b)(c) は
> `docs/fhot-stage0-internal-audit.md` §6。**最終判断は所有者が行う。**

**当初の自己評価（監査前）:** L2（既存枠組みでは自然に出ないが、原理的には精製二重化を介して
既知の線形応答理論に還元される可能性が最大の脅威として残っている。§4 参照）。
**監査後の実効評価は L1 以下**（現象は存在するが自明な機構に帰着する）。

**既存草案との関係（重複回避の宣言）:**

| 草案 | 対象軸 | 本提案との分離 |
|---|---|---|
| 計画22（RRT） | 非半単純核・分数 valuation（P2） | 本提案は semisimple kernel を維持する。Jordan 構造は扱わない |
| 計画23（DIBT・欠番） | 認証盲点・脱出深さ（P0-2） | 本提案は資源制限や shot 予算を課さない |
| 計画24（LKCT） | exact/approximate kernel crossover（P1） | 本提案は kernel の持ち上げ・持ち上げパラメータ `ε` を扱わない。壊す仮定は functional の線形性であり、kernel の exactness ではない |
| 計画18・21・DCIT・計画19・計画20 | valuation構造／資源限界／dilation共存／熱力学 | いずれも本提案の非線形 functional 階層とは独立の軸 |
| WPOT（提案23・撤回済み） | 受動性の語領域実現 | 直接の後継ではないが、「片側正値性は語領域に降りない」という死因（§6.4）を踏まえ、本提案は QFI という**二次形式**を主軸に据え、ergotropy 系の片側判定は補助にとどめる（§6） |

---

## 0. 結論

> **【Stage 0 仮説・boxed命題】Φ階層排他ゼロ（functional-graded exact-zero splitting）:**
> 有限次元 GKSL 系に固定された比較クラス（初期状態・probe・readout・観測窓）の下で sector `S`
> が存在し、
>
> (i) 線形応答差分 `δχ_S ≡ 0`（全周波数で exact、Krylov moment certificate により証明可能）、
>
> (ii) probe の counting record の全次数 cumulant 差分も weak-probe 極限で 0（FCS 的に不可視）、
>
> にもかかわらず
>
> (iii) 同一 probe・同一比較規約下の QFI sector 応答差分 `δF_S := F_Q[full] − F_Q[cut^{(S)}]`
> が**非零かつ `Γ→∞` で O(1) に保護される**。
>
> この現象の成立・非成立は、SLD 作用素 `L_SLD`（状態 `ρ` に対する `∂_θρ = (1/2)(L_SLD ρ + ρ L_SLD)`
> の解）と sector 射影 `P_S` の非可換性の rank `r_{nc} := rank[L_SLD, P_S]` によって分類される
> （予想：`r_{nc}=0` なら `δF_S=0` へ帰着し、`δF_S≠0` は `r_{nc}>0` を必要とする）。

**この命題は現時点で証明されていない。** Stage 0 の役割は、この命題を検証可能な形に定式化し、
最初の kill test（§4・§5）を設計することである。

---

## 1. なぜこの方向を選ぶのか

### 1.1 既存理論から引き継ぐ事実（§4 参照）

- 有限次元・time-local GKSL・weak probe・固定比較クラス（RISEI/SMRT/EIT 共通の枠組み）はそのまま維持する。
- sector 切断 `cut^{(S)}`、full-minus-cut 差分 `δχ_S`（EIT no-go/go 記法）、Krylov moment による
  exact-zero certificate（SMRT・EIT 共通）を土台として再利用する。
- protected kernel の semisimple 性・response-relevant projected block の可逆性など、
  Frozen-Theories の protected response 必要条件（ガイド §4.2 no-go 6）はそのまま課す
  （非半単純核は計画22の占有領域であり、本提案では扱わない）。

### 1.2 壊す仮定 ← 新規性の源泉

**壊す仮定は1つ: linear response functional。** `δχ_S`（線形応答差分）ではなく、
状態の非線形 functional である QFI `F_Q[ρ_θ] = tr(ρ_θ L_SLD^2)` の sector 分解差分 `δF_S` を
中心対象とする。

**維持する仮定（§4.4 予算の遵守）:**

- 有限次元・time-local GKSL・weak probe・固定比較クラス
- protected kernel の semisimple 性（計画22との排他性）
- 資源制限なし（計画21・23との排他性）
- kernel exactness／持ち上げなし（計画24との排他性）

外す仮定は1つのみであり、ガイド §4.4 の「原則1つ、不可分な補助仮定を含め最大2つ」の予算内。
補助仮定として**追加で外すもの:「観測可能量は probe の counting record（FCS）に限る」という
暗黙の前提**も外すが、これは「線形応答から非線形 functional への一般化」という単一の中心仮定と
数学的に不可分である（線形応答も counting cumulant も、非線形 functional 階層の中の1点に過ぎない）。

---

## 2. 理論の定式化

**型:** (A) 現象論的理論（sector 分解 QFI 応答という新しい観測可能量の予言）＋ (B) 数学的定理型
（非可換 rank `r_{nc}` による分類、条件付き還元定理）の複合。

**対象系:** 有限次元 Hilbert 空間、time-local GKSL generator、stationary rotating frame、
weak probe（一次摂動パラメータ `θ` に対する量子計測シナリオ）。EIT の Λ系配置を最小模型として流用する
（`EIT_no_go_go_theory_v6_2_English.tex` §9.2）。

**定義（暫定・Stage 0）:**

- `F_Q[ρ_θ] := tr(ρ_θ L_SLD^2)`：probe 位相 `θ` に対する量子 Fisher 情報。`L_SLD` は
  `∂_θρ_θ = (1/2){L_SLD, ρ_θ}` の解（Lyapunov 方程式、有限次元では exact に解ける）。
- `F_Q^{full}`：full response（sector 切断なし）の QFI。
- `F_Q^{cut^{(S)}}`：sector `S` を切断した counterfactual protocol の QFI（EIT no-go/go の
  `χ_cut^{(S)}` 記法を踏襲）。
- `δF_S := F_Q^{full} − F_Q^{cut^{(S)}}`：sector 分解 QFI 応答差分（**新規記号**）。

**主定理（案、Stage 0時点では conjecture）:**

`δχ_S ≡ 0`（全周波数 exact）かつ `r_{nc} = rank[L_SLD, P_S] > 0` ならば、
weak-probe 極限で `δF_S ≠ 0` が genericに成立し、`Γ→∞` で `δF_S` は少なくとも一つの
semisimple protected sector で O(1) に保護される。

---

## 3. 理論固有現象

### 3.1 必須記述項目

**1. 固有現象の定義** — §0 の boxed 命題（Φ階層排他ゼロ）。

**2. 非還元性の論拠（Stage 0時点の仮説・未検証）**

- **FCS / tilted-GKSL 族に対して:** counting record の任意次 cumulant は tilted generator
  `L_χ` の主固有値の χ 微分として書ける（解析的母関数表示）。`δF_S` は counting record の
  functional ではなく**状態の二次形式**（SLD による）であるため、母関数表示に直接写らないと
  予想する。ただし QFI が classical Fisher information の quantum extension として
  tilted-generator の Hessian（Fisher information matrix）に一致する既知の関係
  （dynamical activity・quantum metrology の文脈）があるため、**この還元経路は最も精査が必要**。
- **精製二重化（purification doubling）族に対して（最大の脅威）:** QFI ≒ Bures計量 ≒
  fidelity susceptibility は、系を精製した二重化 Hilbert 空間上での**線形応答（Kubo形式）**
  に書き直せることが量子計測理論で知られている。もし `δF_S` が二重化 Liouvillian 上の
  線形応答差分 `δχ_S^{doubled}` に一致し、かつ sector 切断 `cut^{(S)}` が二重化空間上の
  GKSL-admissible な sector 切断に写るなら、本現象は **SMRT/EIT の既存定理の系**に還元される。
  **これが本提案の非還元性の要である**（§4・§6）。
- **群同期／HMM実現族に対して:** 対象が word 確率や gauge 構造ではなく連続パラメータの
  Fisher情報であるため、原理的に射程外と考えるが、Stage 2 で形式的に確認する。

**3. 観測可能量（observable signature）**

- 物理量: probe 位相推定における QFI（EIT系なら制御光位相または探査光位相の Fisher 情報）。
- 現れ方: `δχ_S` が exact zero（不連続や閾値ではない）の sector で `δF_S` が有限値を持つという
  **functional 間の不一致**として現れる。
- 検出手段: 解析的（SLD の exact 構成、Lyapunov 方程式は有限次元で厳密に解ける）。数値検証は
  custom Liouville 実装（QuTiP 不可）で補強。
- 有限サイズ・有限精度での可視性: 最小模型（3–4準位）で exact arithmetic により判定可能と見込む。

**4. 反証条件**

- 二重化線形化によって `δF_S` が既存の `δχ_S^{doubled}` 定理へ厳密に帰着することが一般に
  証明されたら、本現象は棄却（§6.4 行き）。
- `r_{nc}=0` の場合にのみ `δF_S≠0` が起きる反例が構成されたら、分類定理は失効。
- 最小模型で `δχ_S≡0` かつ `δF_S=0`（非零にならない）が genericであれば、現象自体が存在しない。

**5. 既存理論との一致領域**

- SLD `L_SLD` と sector 射影 `P_S` が可換（`r_{nc}=0`）な極限では、`δF_S → 0` が
  `δχ_S≡0` から自明に従うことを sanity check として示す（線形応答と QFI が同じ保護構造を
  共有する退化極限）。

### 3.2 固有性の強さの自己評価

**L2**（既存枠組みでは自然に出ないが、原理的には精製二重化を介して導出可能である疑いが強い）。
**L3 を主張していない。** 非可換 rank 分類が二重化還元を生き延びることが確認できて初めて L3 への
昇格を検討する。

---

## 4. 非還元性の検討

**ガイド §6.4 末尾の確定方針に従い、以下の競合 null identity を先に固定した上で witness を
逆設計する方針を取る。** ただし本 Stage 0 文書の時点では、この逆設計・還元試行はまだ実行していない。

### 4.1 固定する null identity

1. **FCS / tilted-GKSL 族の null identity:** 「counting field `χ` の解析的母関数で書ける
   functional はすべて FCS 内」。過去の第2累積量 witness（§6.4 表）はこの経路で死んだ。
   → 逆設計条件: `δF_S` は record の functional ではなく、状態の非線形 functional
   （QFI／SLD 系）でなければならない。

2. **精製二重化族の null identity（最大の脅威）:** 「`δF_S` が二重化空間上の線形応答差分
   `δχ_S^{doubled}` に一致し、かつ `cut^{(S)}` が二重化空間の GKSL-admissible sector 切断に
   写るなら、SMRT/EIT の既存定理の適用例にすぎない」。
   → 逆設計条件: witness の成立には、二重化写像の下で **sector 切断が GKSL-admissible な
   切断に写らないこと**（SLD の非線形性が sector cut と可換でないこと、すなわち `r_{nc}>0`）
   を組み込む。

3. **群同期／HMM実現族:** 対象外と考えるが、Stage 2 で形式的確認を行う。

### 4.2 Frozen-Theories との整合

- RISEI/SMRT/EIT の protected response 必要条件（ガイド §4.2 no-go 6: semisimple kernel・
  非零 projected source/readout・可逆 protected block）はそのまま維持し、`δF_S` の保護構造にも
  同じ必要条件を課す。
- ガイド §4.2 no-go 14（熱力学拡張時の制約）は本提案では発動しない（entropy production を扱わない）。

**現時点でこの節は「還元監査の設計」であり、実際の還元試行（Stage 1〜2、赤チーム投入）は
未実施である。** 特に精製二重化経路は Stage 2 の最初の kill test として優先的に投入する。

---

## 5. 検証計画

1. **最小模型:** EIT §9.2 の Λ系（3–4準位）を流用し、probe 位相 `θ` を制御光または探査光の
   位相として導入する。
2. **SLD の exact 構成:** 有限次元 Lyapunov 方程式 `∂_θρ_θ = (1/2){L_SLD, ρ_θ}` を
   SymPy による exact symbolic algebra で解く（QuTiP 不可のため）。
3. **`δχ_S` の Krylov moment certificate:** EIT/SMRT の既存手法（`scripts/` 内の関連実装）を
   踏襲し、exact zero を symbolic に証明する。
4. **`δF_S` の数値・symbolic スモーク:** custom NumPy/SciPy Liouville 実装で `F_Q^{full}` と
   `F_Q^{cut^{(S)}}` を独立に計算し、差分の非零性・`Γ→∞` での漸近を確認する。
5. **二重化還元テスト（最初の kill test）:** 系を精製した二重化 Liouvillian を構成し、
   `δF_S` が `δχ_S^{doubled}` に一致するかを exact arithmetic で判定する。**一致すれば
   本提案は §6.4 の却下リストへ即座に記録する。**
6. **destruction control:** `r_{nc}=0` となるよう sector を選び直し、`δF_S→0` を確認する
   （§3.1-5 の sanity check）。

**held-out の扱い:** 本提案は現時点で `docs/context-pack.md` §6.4 の held-out（seed 20260723）を
使用しない。数値検証は独立の最小模型パラメータで行う予定であり、使用する場合は seed と割当を
本節に追記する（ガイド §11.2）。

---

## 6. 弱点と未解決点

- **最も危険な既知還元:** 精製二重化による線形応答化（§4.1 の2番目）。QFI が Bures計量・
  fidelity susceptibility として二重化空間の線形応答に一般に書き直せることは量子計測理論の
  標準的知見であり、sector 切断が GKSL-admissible な形で二重化空間に持ち上がってしまえば
  本現象は SMRT/EIT の系に完全に吸収される。
- **次点の脅威:** dissipative quantum metrology の一般的な Fisher information 境界
  （Escher–Davidovich 系統の結果）との重複。文献監査未実施（egress 必要）。
- **最も弱い仮定:** weak-probe 極限での QFI 二次応答の well-definedness。ガイド §4.3 が
  「ergotropy・Fisher information 等の非線形 functional は滑らかさ・順序・整合性を別途証明する
  必要がある」と明記しており、この検証が未着手。
- **最も脆い数値操作:** SLD の Lyapunov 方程式を有限次元で解く際、退化固有値（`ρ_θ` の
  縮退スペクトル）付近での数値不安定性。
- **最も不足している物理接続:** QFI の実験測定は理想的な optimal measurement を要し、
  実際の位相推定プロトコルとの matched interface が未検討。
- **PRXを阻む一点:** 非還元性（Novelty ゲート）が現時点で全く検証されていない。
  精製二重化経路のkill testを通過しない限り、探索中の段階を出ない。
- **WPOT の教訓の適用:** 撤回された提案23（WPOT）は「source と readout を独立に選べる
  functional では受動性が片側正値性として語領域に降りない」という機構的必要条件を残した
  （§6.4）。QFI は二次形式であり片側正値性ではないため直接の抵触はないと考えるが、
  ergotropy 系の補助 witness を導入する場合は同じ罠に注意する。

**stop condition（案）:**

1. 二重化写像の下で sector cut が一般に GKSL-admissible sector cut に写ることが証明されたら、
   撤回し §6.4 へ記録する。
2. 逆に `δχ_S=0 ⇒ δF_S=0` が semisimple クラス全体で定理として成立してしまったら、
   それ自体を no-go 定理として反転し、PRL 型で論文化する方向へ切り替える。
3. 上記どちらでもなく、`r_{nc}>0` の下で `δF_S≠0` が genericに存在し、かつ二重化還元が
   失敗する具体例が構成できたら、Stage 1（主張抽出）へ進む。

---

## 7. 参考文献

*TODO — 文献監査未実施。DOI/arXiv番号の実在確認まで確定として引用しない（ガイド §11.2 Stage 3）。*

優先して監査すべき方向（暫定）:

- quantum Fisher information と Bures計量・fidelity susceptibility の二重化（purification）
  表示に関する文献
- dissipative quantum metrology における Fisher information 境界（Escher–Davidovich 系統）
- SLD 作用素と対称性・保存量の非可換性に関する量子計測理論の文献
