# NV-Blue-Charge-Control seed

Seed package created 2026-08-11 JST for a proposed dedicated repository `NV-Blue-Charge-Control`.

## Scope
This package joins two connected but distinct programmes:

1. **DLA bridge:** a closed-Hamiltonian, two-nuclear-spin `su(4)` benchmark in which marked perturbative depth changes from `d=2` to `d=3` while the DLA remains full.
2. **Charge-trajectory bridge (TP-16):** a stochastic first-success / heralded charge-control witness linking charge transcript precision to nuclear-register coherence and feed-forward cost.

Blue light is treated as a **charge preparation / heralding control**, not as the coherent perturbation parameter `epsilon` of the DLA model.

## Reproduce
```bash
python -m pip install -r requirements.txt
python calculations/nv_blue_charge_two_nuclear_seed.py
python calculations/nv_charge_transcript_retry_witness.py
```

Expected outputs are stored in `results/`.

## Current verdict
- DLA held-out benchmark seed: **ADOPT**.
- Dedicated development/falsification repository for charge-trajectory control: **GO**.
- Device-level NV realization with measured hyperfine tensors: **not yet closed**.
- PRL/PRX novelty: **not certified by this seed package**.

## Next decisive gates
See `NEXT_GATES.md`.
