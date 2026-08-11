#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
scripts=[
    ROOT/'code/W0_response_fibre_reachable_region.py',
    ROOT/'code/W1_no_internal_gauge_noise_information_fibre.py',
    ROOT/'code/W3_same_response_noise_different_qfi.py',
]
for script in scripts:
    print(f'\n=== {script.name} ===')
    subprocess.run([sys.executable, str(script)], check=True)
print('\nW2 is a written blocking/collapse gate: gates/W2_GAUSSIAN_COLLAPSE_GATE.md')
