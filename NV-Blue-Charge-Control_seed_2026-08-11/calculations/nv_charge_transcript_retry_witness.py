"""Minimal analytic witness for NV charge-transcript quantum control."""

from __future__ import annotations

import cmath
import math


def discarded_transcript_coherence(p: float, phi: float) -> complex:
    if not (0.0 < p <= 1.0):
        raise ValueError("p must be in (0,1]")
    q = 1.0 - p
    return p / (1.0 - q * cmath.exp(-1j * phi))


def corrected_coherence(p: float, phi: float) -> float:
    _ = discarded_transcript_coherence(p, phi)
    return 1.0


def timing_resolution_bound(delta_omega: float, target_coherence: float) -> float:
    if not (0.0 < target_coherence < 1.0):
        raise ValueError("target_coherence must be in (0,1)")
    return math.sqrt(-2.0 * math.log(target_coherence)) / abs(delta_omega)


def main() -> None:
    cases = [(0.5, math.pi / 2), (0.4, 2 * math.pi * 80 * 0.0005)]
    for p, phi in cases:
        c = discarded_transcript_coherence(p, phi)
        print(f"p={p:.3f}, phi={phi:.9f}, C={c.real:.9f}{c.imag:+.9f}j, |C|={abs(c):.9f}, corrected={corrected_coherence(p, phi):.1f}")

    for p in (0.2, 0.5, 0.8):
        c0 = discarded_transcript_coherence(p, 0.0)
        assert abs(c0 - 1.0) < 1e-12
    print("CORE_DELETION_PASS: phi=0 gives |C|=1 for all tested p")

    dw = 2 * math.pi * 80
    for target in (0.99, 0.999, 0.9999):
        sigma = timing_resolution_bound(dw, target)
        print(f"target={target:.4f}, sigma_t_max={1e6*sigma:.3f} us")


if __name__ == "__main__":
    main()
