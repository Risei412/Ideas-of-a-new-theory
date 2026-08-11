# DLA held-out benchmark: NV + blue charge control

Status: **ADOPT AS HELD-OUT BENCHMARK SEED; NOT YET DEVICE-LEVEL CLOSURE**.

Use the two-nuclear basis `|00>, |10>, |01>, |11>` with `H0 = diag(0,1,1,3)` and a Hermitian diamond control graph. The parameter `d_c` changes the relative strength/sign of one route to the marked target.

- `d_c=+1`: DLA dimension 15, `K2=3`, depth 2.
- `d_c=-1/2`: DLA dimension 15, `K2=0`, `K3=1.05`, depth 3.
- Weak-coupling transition-probability slopes are approximately 4 and 6.

Blue light is reserved for charge-state preparation / heralding. During the coherent DLA measurement window, blue illumination should be off and `epsilon V` should be implemented by MW/RF/electron-mediated coherent control.

### Device-level gate
PASS requires a reachable same-`su(4)` pair with robust `d=2 -> 3` cancellation using measured or credible NV hyperfine tensors, available MW/RF controls, realistic amplitudes, and decoherence.

FAIL if the depth-3 point requires unphysical independent matrix elements or unavoidable non-Hermitian charge dynamics during the coherent measurement window.
