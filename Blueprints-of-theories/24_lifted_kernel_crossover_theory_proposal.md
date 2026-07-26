# 計画24: 持ち上げ核クロスオーバー理論（Lifted-Kernel Crossover Theory / LKCT）

## 一行サマリ

exact protected kernel を ε-持ち上げした2パラメータ族 `A(Γ,ε;z) = Γ(D₀+εD_L) + B(z)` の
クロスオーバー面には、**核持ち上げ補正と Schur 漏洩補正が厳密に相殺する余次元1曲線
（保護回復稜線 / restoration ridge）`Γ²ε = α_leak/κ_lift`** が現れうる。
その存在は**符号不変量 `sign(κ_lift·α_leak)` という係数レベルのデータ**で決まり、
両端点の漸近指数・Newton fan・tropical データからは**決定できない**
（fan-identical で稜線の有無だけが異なる対が明示構成できる）。
これは §6.3 未解決項目3「exact/approximate kernel crossover」の理論本体である。

**作成日:** 2026-07-26
**位置づけ:** ガイド §6.1 **P1「Exact-to-approximate kernel crossover」**
（壊す仮定：exact protected kernel）に対する Stage 0 理論設計図。
§6.3 未解決項目3（「裸の `Γε/γ₀` collapse は失敗。projected slow-loss jet は凍結模型で
成功したが、一般クラスの十分条件は未証明」）が空けたままの空白を占有する。
**型（§2）:** (B) 数学的定理型（分類＋条件付き還元定理）＋ (A) 現象論（稜線は観測可能量）。
統合型 (D) 寄り。対象系は有限次元・time-local GKSL 由来の resolvent 族（weak probe）。
想定読者は開放系・量子光学・漸近解析・スケーリング解析の利用者一般。
**判定:** **要判断（2026-07-26 A2内部監査後）。** 当初は「PRX候補として探索する価値がある／L2」
としていたが、`docs/lkct-fan-blindness-exact-audit.md` により
**C1・C2 は Exact へ昇格、C3 の広い版は否定**された。§6 stop condition 1 が
文字通りの読みでは発火している。**下の監査ブロックを必ず先に読むこと。**

> ## ⚠️ この文書を読む前に（2026-07-26 A2内部監査）
>
> **本文 §2.3 C3・§3.2・§4.1 の「fan／tropical データに盲目」という新規性の書き方は、
> 監査により維持できないと判定された。** 訂正は §2.3・§4.1 の errata ブロックにある。
>
> | 監査項目 | 判定 | 一次資料 |
> |---|---|---|
> | C1（2-jet 恒等式） | **Conditional → Exact へ昇格** | `docs/lkct-fan-blindness-exact-audit.md` §2 |
> | C2（稜線二分律） | **Conditional → Exact へ昇格**（陰関数定理＋Sturm 証明書） | 同 §3 |
> | C3（fan 盲目性） | **広い版は否定。**非署名トロピカル化には確かに不可視だが、角の initial form の根の**符号**が決定する。符号付き／実トロピカル幾何が扱う対象 | 同 §4 |
> | ν(θ) の折れ点数 | **本文の誤りを訂正。**1個ではなく2個（θ=1 と θ=2） | 同 §4.2 |
> | stop condition 1 | **文字通りの読みでは発火。** (a)却下 /(b)縮小継続 /(c)文献監査待ちの判断が必要 | 同 §5 |
>
> 検証は `scripts/lkct_exact_audit.py`（X0–X6、全PASS、浮動小数点を判定に不使用）で
> 再現でき、全出力は `certificates/lkct_fan_blindness_2026-07-26.txt` にある。
>
> **理論の数学的部分はむしろ強くなった**（近似だった 2-jet が恒等式の Taylor 展開と判明し、
> 稜線が厳密な解析曲線として存在することが証明された）。**失ったのは新規性の重心である。**

**既存草案との関係（重複回避の宣言）:**

| 草案 | 対象軸 | 本提案との分離 |
|---|---|---|
| **計画18（Newton fan）・SMRT polyhedral** | **指数**（valuation・fan・wall。壁の両側で valuation が変わる） | 本提案の稜線は**両側で valuation が等しく、曲線上でのみ跳ね上がる**係数レベルの相殺。fan-identical 対で稜線の有無が分かれること（スモーク T5）が分離の構成的証拠。**指数構造そのものは新規性として数えない**（§4.1） |
| 計画18 **N4**（universal wall crossover） | face-selection boundary の有限-Γ thickening、1変数 collapse `x=δθ·Γ^{Δν/m}` | N4 は**壁**の近傍、本提案は**壁ではない場所**（同一 valuation 領域の内部）に立つ曲線。座標も (機能空間の δθ, Γ) vs (物理パラメータ Γ, ε) で別物 |
| 計画22（RRT） | 非半単純核・分数 valuation（P2） | 本提案は **ε=0 で semisimple protected cluster を維持**する。Jordan 構造は扱わない（排他的） |
| 計画21（FRRG）・計画23（DIBT） | 観測者の資源制限・凍結 shot 予算（P0-2） | 本提案は資源制限を課さない。証明書仕様（Hankel 等）も使わない |
| DCIT・計画19 | dilation の共存可能性（P0-1） | 共通 dilation の存在は一切問わない |
| 計画20 | 熱力学的価格 | エントロピー生成・仕事の簿記を扱わない |

---

## 0. 結論

**中心の問い:**

> exact protected kernel（ガイド §4.2 no-go 6 の保護機構）と
> fixed kernel lifting no-go（同 no-go 7 の抑制機構）は、
> 二重極限 `(Γ→∞, ε→0)` の錐の**内部**でどう接続されるか。
> クロスオーバーの**形**は何個の数で決まり、そのうち
> 漸近指数（fan データ）から**決まらない**成分は何か。

**理論固有現象（boxed 命題・Conjecture）:**

> **保護回復稜線（protection restoration ridge）**
>
> `D₀` の kernel を保護ブロック `P`（ε=0 で semisimple、RISEI Schur–Zeno 条件成立）とし、
> `D_L` を `(D_L)_PP ≻ 0` なる核持ち上げとする。probe/readout を `P` に射影した応答
> `R(Γ,ε;z)` は、二重スケーリング錐の内部で 2-jet
>
> `R − R_∞ = −(Γε)·κ_lift + Γ^{-1}·α_leak + o(Γε, Γ^{-1})`
>
> に従う（`κ_lift, α_leak` は界面データから閉形式で計算可能、§2.3）。
> `sign(κ_lift·α_leak) = +1` のとき、かつそのときに限り、曲線
>
> `Γ_ridge(ε) = √(α_leak/(κ_lift·ε))`
>
> の上で両補正が**厳密に相殺**し、持ち上げられた核の応答が leading order で
> exact-kernel 値 `R_∞` へ回復する。この稜線の存在・位置は
> **両端点の漸近指数・Newton fan からは決定できず**（fan-identical 対の存在、§3.4）、
> 界面の**係数レベル**の符号不変量である。

3行で言えば：**(i)** クロスオーバー面は2つの数 `(κ_lift, α_leak)` で決まる（有限決定）。
**(ii)** その積の符号が、クロスオーバー面が「単調な劣化」か「途中で一度厳密回復する」かを
二分する（稜線二分律 / ridge dichotomy）。**(iii)** この二分は指数データに盲目である。

---

## 1. なぜこの方向を選ぶのか

### 1.1 既存理論から引き継ぐ事実（ガイド §4）

- **RISEI（凍結）:** semisimple response-relevant protected cluster + bounded fast resolvent の下で
  ε=0 の `Γ→∞` protected transfer は O(1)（Schur–Zeno）。`z_loss`, `z_jet`, `q_*` という
  有限窓クロスオーバー座標の存在。**projected slow-loss jet が凍結模型で成功した**という
  数値資産（§6.3 項目3）。
- **ガイド §4.2 no-go 7（fixed kernel lifting）:** 固定 `ε>0` では `Γ→∞` で保護は消え
  O(Γ^{-1}) 抑制。→ 本提案のもう一方の端点。**破らない。両端点として使う。**
- **SMRT polyhedral／計画18:** path 依存 valuation は区分アフィン（tropical）。
  → **指数構造は既知として引き継ぎ、新規性として数えない。**
- **§6.3 未解決項目3の記録:** 裸の1変数 collapse `Γε/γ₀` は**失敗**している。
  この失敗は本提案では「2-jet が一般に rank 2 だから collapse しない」ことの
  証拠として**再利用**される（失敗の資産化）。

### 1.2 壊す仮定（新規性の源泉、§4.4 予算申告）

- **外す仮定（1つ）:** exact protected kernel（`ker D₀ ≠ {0}` を厳密に保つこと）。
  代わりに `D(ε) = D₀ + εD_L`、`(D_L)_PP ≻ 0` の**持ち上げ族**を導入し、
  極限は宣言された二重スケーリング錐 `{(Γ,ε): Γ→∞, ε→0, Γε→有限 or 0}` 上でのみ取る
  （no-go 10 の極限交換禁止を遵守：錐と path を protocol data として宣言する）。
- **維持する仮定:** 有限次元／time-local GKSL 由来／ε=0 で semisimple protected cluster／
  bounded fast resolvent／weak probe／固定比較クラス（probe・readout・観測窓・正規化固定）。
- **代替する数学的構造:** 1パラメータ Schur–Zeno 展開 → (u,v) = (Γε, Γ^{-1}) の2変数 jet 展開。
- **失効する既存定理:** RISEI の O(1) protected transfer は錐の内部では leading order のみ有効。
- **継承できる既存定理:** 両端点（ε=0: Schur–Zeno ／ ε固定: no-go 7）、SMRT の指数分類。
- **元の理論を回収する極限:** `ε=0`（スモーク T1）および `θ=0` 固定 ε（スモーク T2）。
- **仮定変更がなければ現象が消える control:** `ε≡0` では u 軸が消え 2-jet が rank 1 に退化、
  稜線は定義不能（`D_L`-destroyed control）。スモーク実装済み。

---

## 2. 理論の定式化

### 2.1 対象族

`𝒱 ≅ ℝ^n`（または ℂ^n）、`n = k + n_f`。ブロック分解 `P ⊕ F`（`dim P = k`）。

- `D₀`: damping-shape operator（SMRT の `D` の意味、`D_damp` 側）。`(D₀)_PP = 0`、
  `(D₀)_FF = D_F ≻ 0`（ε=0 で `ker D₀ = P`、semisimple）。
- `D_L`: 持ち上げ operator。PSD、`(D_L)_PP ≻ 0`（ε>0 で核が完全に持ち上がる）。
- `B(z)`: 遅い／周波数依存ブロック。`B_PP` 可逆（観測窓内の正則点）。
- probe/readout: `c = (c_P, 0)`, `p = (p_P, 0)`（保護ブロック支持。RISEI の
  非零 projected source/readout 条件の最単純ケース）。
- 応答: `R(Γ,ε;z) = p† A(Γ,ε;z)^{-1} c`、`A = Γ(D₀+εD_L) + B(z)`。

### 2.2 クロスオーバー座標

`u := Γε`（持ち上げ強度）、`v := Γ^{-1}`（Schur 漏洩強度）。
二重スケーリング path: `ε = ε₀Γ^{-θ}` は `(u,v)` 平面の曲線 `u = ε₀ v^{θ-1}`。
θ=2 が両補正の均衡 path（既知の tropical/polyhedral 解析はこの**指数** 2 を与える。
そこまでは新規性として数えない）。

> **【2026-07-26 訂正】fan の折れ点は 2 個である。**
> 初版は暗黙に折れ点1個を仮定していたが、厳密計算により
> `ν(θ) = clamp(θ−1, 0, 1)`、折れ点は **θ=1 と θ=2** と判明した。
> `θ ≤ 1` では `u = Γε` が発散して 2-jet の適用域外に出る（no-go 7 側、`ν=0`）。
> 稜線が乗るのは θ=2 の折れ点のみ。出典 `docs/lkct-fan-blindness-exact-audit.md` §4.2。

### 2.3 主要主張（status 付き）

**C1（2-jet 恒等式）— status: 🆙 Exact**（2026-07-26 昇格。
gate: `B_PP` 可逆・`D_F` 可逆・原点の多重円板内）

`u := Γε`, `v := Γ^{-1}` の下で、**近似ではなく恒等式**として

```
R(Γ,ε) = p_P† S(u,v)^{-1} c_P                                       … (厳密)
S(u,v) = B_PP + u(D_L)_PP − v·B_PF (D_F + v·Ω_FF)^{-1} B_FP ,  Ω = B + u D_L
```

が成立する（完全記号 k=1 と有理数 k=2 で残差**厳密に 0**）。`S` は原点で解析的、
`S(0,0)=B_PP` 可逆ゆえ `R` も解析的であり、2-jet はその Taylor 展開である。

```
R − R_∞ = −u·κ_lift + v·α_leak + O(|u|², |v|²)   （剰余はコンパクト部分集合上で一様）
R_∞     = p_P† B_PP^{-1} c_P
κ_lift  = p_P† B_PP^{-1} (D_L)_PP B_PP^{-1} c_P
α_leak  = p_P† B_PP^{-1} (B_PF D_F^{-1} B_FP) B_PP^{-1} c_P
```

厳密認証（`scripts/lkct_exact_audit.py` X1–X2）: Schur 恒等式の残差 0、
方向微分は4方向×2モデルで厳密有理数が完全一致、閉形式との残差 0。
ランダム有理54例で反例 0 件（X6）。

**C2（稜線二分律）— status: 🆙 Exact**（2026-07-26 昇格。gate: `κ_lift ≠ 0`, `α_leak ≠ 0`）

`g := R − R_∞` は原点で解析的、`g(0,0)=0`、`∇g(0,0) = (−κ_lift, α_leak) ≠ 0`。
陰関数定理により零集合は原点を通る**厳密な解析曲線**であり、接線は
`u = (α_leak/κ_lift)·v`、すなわち `Γ²ε → α_leak/κ_lift`。
この曲線が物理域（開第一象限 `u,v>0`）へ入るのは
**`sign(κ_lift·α_leak) = +1` のとき、かつそのときに限る。**
稜線は「leading order の相殺」ではなく厳密な零曲線で、2-jet 公式はその接線である。

厳密認証（X5、Sturm 法・浮動小数点不使用）: ridge 側は Γ=500/5000/50000 のすべてで
錐内ブラケットに根ちょうど1個＋符号反転、2-jet 予測との相対差は
`2.67×10⁻³ → 2.68×10⁻⁴ → 2.68×10⁻⁵`（**1 decade あたり厳密に 1/10**、予測 `O(Γ^{-1})` と整合）。
no-ridge 側は `ε>0` 全域で根 0 個（大域証明書）。
※ ridge 側の `ε>0` 全域には第2根（`u=Γε≈100`）があるが**錐の外**であり稜線ではない。

**C3（fan 盲目性）— status: ⚠️ 広い版は否定（2026-07-26）／狭い版のみ Exact**

`D₀`・`B`・`p`・`c`・両端点の漸近指数・ブロック次元・持ち上げの正定値性を
すべて共有し、**`sign(κ_lift)` だけが異なる**持ち上げ対 `(D_L⁺, D_L⁻)` が構成できる
（`(D_L)_PP = ww† + δI` の `w` を `[x y]†w = (1, ±1)` で解く。
`x = B_PP^{-†}p_P`, `y = B_PP^{-1}c_P`）。`α_leak` は `D_L` に依存しないため
対の間で厳密に一致する。

**厳密認証（X3–X4、全有理数）:** 凍結対
`κ_lift = +499/500 / −501/500`、`α_leak = 2/25`（共通）、`R_∞ = −1/5` について、
`R−R_∞` の分子・分母の Newton 指数台（11点・12点）が **± 対で完全一致**し、
valuation `ν(θ)` も有理 θ 格子 9 点で **完全一致**する。
**⇒ 非署名トロピカル化（Newton 多面体・valuation 関数）は稜線の存在を決定しない。**

> ## ⚠️ errata（2026-07-26）— C3 の広い版は維持できない
>
> 初版はここから「**fan／tropical データに盲目**」という新規性を導いていたが、
> 監査により**差が現れる場所が特定された**：角 θ=2 の **initial form**
> `−e₀κ_lift + α_leak` の根 `e₀ = α_leak/κ_lift` の**符号**である
> （ridge: `+40/499`、no-ridge: `−40/501`。厳密一致を X4 で確認）。
>
> initial form は標準的な**係数付きトロピカル対象**（initial degeneration）であり、
> さらに符号情報を保持する **符号付きトロピカル化／実トロピカル幾何**
> （Viro patchworking、hyperfield 上のトロピカル幾何）が正面から扱う対象である。
> **したがって §6 stop condition 1 は文字通りの読みでは発火している。**
>
> **生き残る狭い版（これのみ主張してよい）:** 稜線は
> **非署名のトロピカル化**（計画18 の Newton fan と SMRT の polyhedral valuation が
> 実際に計算している対象）に対して不可視であり、決定には角の initial form の根の
> **実符号**という実半代数的条件を要する。
> **この狭い版は単独では新規性が弱く、実トロピカル幾何の文献監査が未実施である。**
>
> 判断の選択肢（(a)却下 /(b)縮小継続 /(c)文献監査待ち）と監査者の読みは
> `docs/lkct-fan-blindness-exact-audit.md` §5 にある。

**C4（非退化性）— status: Numerical phenomenon（float）＋ 🆙 exact 側からも支持**

ランダム界面 500 例で稜線存在率 48.8%（float、T6）。
**厳密有理数のランダム 54 例では 27/54 = 1/2**（X6）。
現象は測度ゼロでも普遍でもなく、界面データの符号で二分される**開集合対**である
（fine-tuning ではない）。

### 2.4 一般クラスへの拡張（未証明・目標定理）

**目標定理（Conjecture）:** RISEI admissible class（semisimple protected cluster・
bounded fast resolvent・非零 projected source/readout）＋ PD 持ち上げの下で、
C1 の 2-jet 還元は錐の内部で一様に成立し、`k ≥ 2` では `(κ_lift, α_leak)` は
行列値 jet `(K_lift, A_leak)`（`k×k`）に昇格、稜線は
`det(B_PP + u K̂ − v Â) の実零点集合` として一般化される。
これが §6.3 項目3の「一般クラスの十分条件」の候補形である。

---

## 3. 理論固有現象（ガイド §3.1 の5項目）

### 3.1 固有現象の定義

§0 の boxed 命題（保護回復稜線）。1文で：**核を持ち上げられた系の応答が、
2パラメータ面内の予測可能な余次元1曲線上で、leading order で exact-kernel 値へ
厳密に回復する。** 曲線の**両側で** valuation は等しく（どちらも同じ抑制次数）、
曲線の**上でのみ** `R−R_∞` の valuation が跳ね上がる。
これは wall（両側で valuation が変わる、tropical で見える）と対照的な
**anti-wall 型**の構造である。

### 3.2 非還元性の論拠（詳細は §4）

- 稜線の存在は `sign(κ_lift·α_leak)` — **係数データ**。tropical/fan/polyhedral の
  対象（指数データ）に載らない（C3 の fan-identical 対が構成的証拠）。
- 両端点理論（Schur–Zeno と no-go 7）はそれぞれ 1 パラメータ極限であり、
  錐の内部の相殺は**どちらの端点からも見えない**（両端点とも単調劣化を予言する）。
- 既知の非単調現象（anti-Zeno、ENAQT）との差分は §4.2 に脅威として申告。

### 3.3 観測可能量（observable signature）

- **どの量に:** 保護ブロック応答 `R(Γ,ε;z)` の `R_∞` からの偏差。固定 z 窓で
  `(Γ,ε)` を掃引したときの**符号反転を伴うゼロ交差**（発散でも閾値でもなく nodal curve）。
- **形:** `(log Γ, log ε)` 平面内の直線 `2logΓ + logε = log(α_leak/κ_lift)` 上での
  偏差の消失（傾き −2 は既知の指数、**切片が理論固有の係数データ**）。
- **検出手段:** 数値では resolvent 評価のみ（O(n³) per point、コスト極小）。
  実験では散逸レートの独立制御が2軸必要（例: EIT 系で bath 結合 Γ と
  ground-state coherence への意図的持ち上げ ε — 実験翻訳は P3 相当の別工程）。
- **有限サイズ・有限精度:** 稜線位置は leading order。有限 (u,v) では次数2補正で
  ゼロ交差が `O(u,v)` だけずれる — スモーク T4b はこのずれが ε→0 で縮むことを実測。
  ただしゼロ交差検出は cancellation そのものであり、`C_cancel` 型の精度監査必須（§6）。

### 3.4 反証条件

1. admissible class 内で、稜線位置が jet 予測から次数2補正で説明できない系統偏差を示す
   → C1/C2 の一様性が偽。中心命題撤回。
2. **GKSL/CPTP 物理実現が `sign(κ_lift·α_leak)=+1` を構造的に禁止する**
   （物理クラスで稜線側が空集合）→ 現象は線形代数の産物。撤回（§6 stop 2）。
3. fan-identical 対の稜線の有無が、実は既知のより細かい tropical 不変量
  （secondary fan・係数付き tropical 等）で判別できる → C3 が偽。§6.4 却下表へ。

### 3.5 既存理論との一致領域（sanity check、実測済み）

- `ε = 0`: RISEI Schur–Zeno 回収。plateau `R_∞` と漏洩補正 `+α_leak/Γ`
  （スモーク T1、相対誤差 0.01%）。
- `ε > 0` 固定: no-go 7 回収。`R ∝ Γ^{-1}`（T2、比 10.03/decade）。
- `D_L`-destroyed control: `ε≡0` で u 軸消滅、稜線定義不能（§1.2 control）。

---

## 4. 非還元性の検討

### 4.1 新規性として数えないもの（自白）

- **指数構造の全部。** θ=2 が均衡 path であること、両端点の valuation、path ごとの
  抑制次数 — これらは SMRT polyhedral／計画18 の枠内（または単純な次数勘定）で出る。
- 2変数 jet 展開という**手法**。Schur 補元の摂動展開は標準技術（Kato・Bender–Orszag）。
- ~~新規性の重心は「稜線二分律という分類問題」と「盲予測可能な切片」に置く。~~

> **【2026-07-26 訂正】重心の置き直しが必要。**
> 初版は「稜線二分律が fan データに盲目であること」を新規性の重心にしていたが、
> A2 内部監査（`docs/lkct-fan-blindness-exact-audit.md`）により、
> 二分律は角 θ=2 の initial form の根の**符号**で完全に決まると判明した。
> initial form および符号付き／実トロピカル幾何は既存の枠組みであり、
> **「fan に盲目だから固有」という論法は成立しない。**
>
> **追加で新規性として数えられなくなったもの:**
> - 「非署名トロピカル化に不可視」という性質そのもの（実トロピカル幾何が扱う層に落ちる）
> - 稜線の**存在判定**（initial form の符号テストで足りる）
>
> **なお生き残っている候補（未監査）:**
> - 稜線の**位置**が界面データ `(κ_lift, α_leak)` から**閉形式で盲予測できる**こと
>   （符号付きトロピカル化は存在を判定するが位置の閉形式は与えない）
> - **GKSL/CPTP 物理クラス内で `sign(κ_lift·α_leak)=+1` が実現可能か**という分類問題
>   （§5.2-2、stop condition 2 に直結。これが現時点で最も有望な重心）
>
> どちらも未検証であり、**現時点でこの提案は L2 のまま、むしろ L2 の下限側にある。**

### 4.2 既知機構への還元脅威（重要度順・すべて未監査）

| # | 脅威 | 内容 | 生死の分かれ目 |
|---|---|---|---|
| A1 | **2パラメータ特異摂動論／合成漸近展開**（Bender–Orszag、GSPT/Fenichel、Kato） | 2-jet と相殺曲線は「2小パラメータの摂動論の標準演習」と判定されうる。**最大の脅威** | 「機構の言い換え」なら死。生き残りは (i) 稜線二分律が**分類問題として未提出**であること、(ii) GKSL 物理クラス内での符号実現可能性が非自明であること、の2点に依存 |
| A2 | **SMRT polyhedral／計画18 fan**（内部還元） | 稜線が実は係数付き tropical（secondary fan 等）で見える | C3 の fan-identical 対を exact arithmetic 化して判定。**Claude 単独で実行可能・最短** |
| A3 | **anti-Zeno 効果**（Kofman–Kurizki 型） | 「散逸を強めると一度良くなる」非単調性は既知 | 対象が decay rate vs sector-resolved protected transfer で異なるが、写像の有無を文献監査。**位置の閉形式盲予測**が差分候補 |
| A4 | **ENAQT／dephasing-assisted transport** | 輸送効率の noise 非単調性（最適 dephasing）は有名 | ENAQT は**最適点**（滑らかな極値）、稜線は**厳密相殺の nodal curve**（符号反転を伴う）。この構造差が写像を阻むかを監査 |
| A5 | **Fano 干渉** | 応答ゼロ＝干渉相殺は古典的 | 稜線は `R` のゼロではなく `R−R_∞` のゼロ（no-go 3 遵守）。差分応答の nodal 構造として区別できるか監査 |
| A6 | **EP／Lidskii**（計画22 RRT の軸） | 非半単純性由来の非解析性 | ε=0 semisimple を維持しており排他的。ただし持ち上げ族が途中で EP を横切らないことの確認は必要 |

### 4.3 Frozen-Theories への非還元性

- **RISEI:** 両端点を与えるが、錐の内部の 2-jet と相殺は扱っていない（no-go 7 が
  「fixed ε」で止まっているのがまさに空白の証拠）。z_jet の凍結模型成功は
  本提案の C1 の**先行証拠**であり、一般化が本提案の追加分。
- **SMRT:** valuation は path の指数のみに依存する分類。稜線切片は係数データで対象外。
- **EIT no-go/go:** 対象外（configuration 分類）。ただし実験翻訳の候補プラットフォーム。

### 4.4 競合理論族（context-pack §6 の A–N）への対応

本提案は資源制限・多時間統計・群同期のいずれも使わないため、
族 A/B/C/D/E/F（ancilla・FCS・同期・HMM・process tensor・実験計画）の
null identity とは直交する見込み。ただし**族 G（解析的還元 gate: Schur/Zeno/adiabatic
elimination）が A1 と同内容**であり、ここが主戦場になる。

---

## 5. 検証計画

### 5.1 実施済み（Stage 0 スモーク）

`scripts/crossover_ridge_smoke.py`（seed 20260726、判定基準は実行前固定、全 PASS）:

| test | 内容 | 実測 |
|---|---|---|
| T1 | ε=0 端点で Schur–Zeno 回収＋漏洩勾配 α_leak | 相対誤差 0.01% |
| T2 | 固定 ε 端点で no-go 7 回収 | R(10⁵)/R(10⁶) = 10.03 |
| T3 | 2-jet 恒等式の精度と収束次数 | 0.10%、次数 2.00 |
| T4b | 稜線位置の盲予測 vs ゼロ交差 | \|log 偏差\| 0.0004→0.0000（ε→0） |
| T5 | fan-identical 対の稜線二分（α_leak 厳密共通） | κ = +0.988/−1.012 で二分 |
| T6 | ランダム界面 500 例の稜線存在率 | 48.8% |

### 5.1bis 実施済み（A2 内部監査・exact arithmetic）— **2026-07-26 完了**

`scripts/lkct_exact_audit.py`（seed 20260726、判定に浮動小数点不使用、X0–X6 全PASS）。
全出力は `certificates/lkct_fan_blindness_2026-07-26.txt`、
評価は `docs/lkct-fan-blindness-exact-audit.md`。

| test | 内容 | 結果 |
|---|---|---|
| X1 | 厳密 Schur 還元恒等式（完全記号 k=1 ＋有理数 k=2） | 残差**厳密に 0** |
| X2 | 2-jet 係数（4方向×2モデル） | 厳密有理数が**完全一致** |
| X3 | Newton 指数台（11/12点）と ν(θ)（有理9点） | ± 対で**完全一致** |
| X4 | 角 θ=2 の initial form と根の符号 | 予測と厳密一致。**差はここだけ** |
| X5 | 稜線の Sturm 根計数と収束 | 錐内1根＋符号反転、相対差 `2.67e-3→2.68e-5`（1/Γ） |
| X6 | ランダム有理54例 | 反例 **0 件**、二分律 **27/54 = 1/2** |

**成果:** C1・C2 が **Exact へ昇格**（2-jet は恒等式の Taylor 展開、稜線は陰関数定理による
厳密な解析曲線）。**代償:** C3 の広い版が否定され、**stop condition 1 が文字通りの読みで発火**
（§2.3 C3 の errata を参照）。判断の選択肢は監査文書 §5。

### 5.2 次工程（優先順・2026-07-26 更新）

1. ~~**A2 内部監査**~~ — **完了（§5.1bis）。結果は上記。**
1bis. **【新規・最優先】符号付き／実トロピカル幾何の文献監査。**
   Viro patchworking、hyperfield 上のトロピカル幾何、real tropicalization に対し、
   「角の initial form の根の実符号による分岐」がどこまで既出かを確認する。
   **これが提案24 の存続を決める。** egress が必要（`references.bib` の DOI 未解決と同じ制約）。
2. **GKSL 物理実現（stop condition 2 の判定・新しい重心の候補）:** custom Liouville 実装（QuTiP 不可）で
   Λ 型・4準位系の GKSL 族に `D₀, D_L` 構造を埋め込み、`sign(κ_lift·α_leak)=+1` が
   物理クラス（CPTP・レート非負・Hermiticity 監査つき）で実現可能かを系統探索。
   レート規約は §4.2 no-go 12 の監査表を添付。
3. **blind jet prediction ≥2 architectures:** §6.3 項目3が指定した最短検証そのもの。
   held-out は seed 20260726 系列から分割（20260723/20260725 は使用済みのため不使用）。
4. **Stage 1–2（赤チーム）:** A1（2パラメータ摂動論への還元）と A3/A4（anti-Zeno・
   ENAQT）を中立記法でシート化。1チャット1主張・3反復・1還元成功で死（§11 準拠）。
   シート化の際、`稜線` `ridge` `LKCT` `保護` 等の語は除去し、線形代数の命題のみ送る。

### 5.3 主張別の最低検証基準（§10.3 対応）

- ~~C1 は B（conditional theorem）~~ → **A（exact theorem）へ移行済み**（2026-07-26）。
  §10.3 A の5項目対応: (1) exact symbolic derivation = X1、(2) 仮定一覧 = `B_PP`/`D_F` 可逆・
  多重円板、(3) 有限証明書 = X4/X5 の Sturm 計数、(4) 小次元直接展開 = X1(a) の k=1 完全記号、
  (5) random substitution 反例探索 = X6（54例・反例0）。
- ~~C2/C3 は C（numerical phenomenon）~~ → **C2 は A（exact、陰関数定理＋Sturm 証明書）へ移行済み。**
  **C3 は広い版が否定され、狭い版のみ exact に確認**（§2.3 errata）。
- **未達:** 一般クラス（`k ≥ 2` 行列値 jet、`c_F, p_F ≠ 0`）と GKSL 物理実現は
  依然として未証明・未検証。本監査は凍結インスタンスと k=1 完全記号に対するものである。

---

## 6. 弱点と未解決点（§8 フォーマット）

- **最も危険な既知還元:** 2パラメータ特異摂動論・合成漸近展開（A1）。
  「標準演習の再命名」判定が最有力の死因。
- **最も弱い仮定:** probe/readout の保護ブロック完全支持（`c_F = p_F = 0`）。
  fast 成分を許すと 2-jet に新しい項が入り、稜線公式が変形する
  （拡張は可能と見込むが未計算 — 「見込み」であり証明ではない）。
- ~~**最も脆い数値操作:** 稜線検出は cancellation そのもの…~~
  → **解消済み（2026-07-26）。** Sturm 法による厳密実根計数へ置換し、
  判定から浮動小数点を排除した（X5）。cancellation 由来の偽信号リスクは消えた。
- **最も不足している物理接続:** 全結果が線形代数レベル。GKSL/CPTP 実現（§5.2-2）と
  matched interface（比較クラス固定の物理 protocol）が未着手。
  ε の実験的意味（意図的核持ち上げ）の実装可能性も未検討。
  **監査後はここが唯一残った新規性の重心候補である。**
- **PRXを阻む一点:** ~~A1/A2 を生き延びない限り~~
  → **A2 で新規性の重心が壊れた（2026-07-26）。** 現状は L2 の下限側。
  §5.2-1bis の文献監査と §5.2-2 の GKSL 実現の両方を通らない限り PRX 候補ではない。
- **stop condition:**
  1. ~~A2 で稜線が係数付き tropical 不変量から決定できると判明~~
     → **⚠️ 2026-07-26 に発火（文字通りの読み）。** 角の initial form の根の符号が決定する。
     ただし C1/C2 が Exact へ昇格したため即時却下とはせず、
     **(a) 却下 /(b) 重心を GKSL 実現可能性へ移して縮小継続 /(c) 実トロピカル幾何の
     文献監査を待って決定** の判断待ちとする（`docs/lkct-fan-blindness-exact-audit.md` §5）。
     **(a) を選ぶ場合は番号24を欠番として残す。**
  2. GKSL 物理クラスで `sign(κ_lift·α_leak)=+1` が実現不能 → **撤回**（現象が非物理）
  3. A1 で「2小パラメータ摂動論の標準演習」への写像が具体的に与えられ、
     分類問題としての残差も既出 → **§6.4 却下表へ**
  4. A3/A4 で anti-Zeno または ENAQT の枠組みに稜線の**位置公式ごと**吸収される
     → 既知現象の例へ格下げ（固有現象としては死）
  5. fast 支持を許した途端に二分律が消える（開集合対でなくなる）→ 主張を
     「保護支持限定の模型現象」へ縮小し PRA/PRB 型へ降格
  6. 「まだ検討が必要」が3ラウンド継続 → §11.4 に従い打ち切り記録

---

## 7. 参考文献

> ⚠️ ガイド §11.2 Stage 3 に従い、**DOI/arXiv を実在確認するまで「未確認」フラグを付ける。**
> 現環境は egress 制限により resolver 検証不能（PROJECT_STATE の既知の残作業と同一制約）。

| # | 文献 | 用途 | 状態 |
|---|---|---|---|
| L-1 | C. M. Bender, S. A. Orszag, *Advanced Mathematical Methods for Scientists and Engineers*（matched asymptotics／合成展開） | 脅威 A1 の本体 | **未確認** |
| L-2 | N. Fenichel, *Geometric singular perturbation theory for ordinary differential equations*, J. Diff. Eq.（1979頃）；C. Kuehn, *Multiple Time Scale Dynamics* | 同上（GSPT） | **未確認** |
| L-3 | T. Kato, *Perturbation Theory for Linear Operators* | 2変数摂動展開の標準参照 | **未確認** |
| L-4 | A. G. Kofman, G. Kurizki, *Acceleration of quantum decay processes by frequent observations*, Nature 405, 546（2000頃） | 脅威 A3（anti-Zeno） | **未確認** |
| L-5 | P. Rebentrost et al.／M. B. Plenio, S. F. Huelga, *dephasing-assisted transport / ENAQT*, New J. Phys.（2008–09頃） | 脅威 A4 | **未確認** |
| L-6 | U. Fano, *Effects of configuration interaction on intensities and phase shifts*, Phys. Rev. 124, 1866 (1961) | 脅威 A5 | **未確認** |
| L-7 | 本リポジトリ: `Frozen-Theories/Generalized_RISEI_Theory_...tex`（z_loss/z_jet/q_* とslow-loss jet）、`SMRT_two_scale_polyhedral...tex`、ガイド §4.2 no-go 6/7/10、§6.3 項目3 | 端点定理・先行証拠・空白の特定 | リポジトリ内 |
