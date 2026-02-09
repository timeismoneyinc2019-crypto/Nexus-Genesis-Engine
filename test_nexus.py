from nexus_full_build import NexusCore
import os
import json
import numpy as np

print('\n--- RUNNING UNIT TESTS FOR NEXUS CORE ---')

# Test A: Force commit by setting a very low threshold
n = NexusCore(threshold=-1000)
signals = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
success, res = n.process_transaction(signals, {"event": "UNIT_TEST_COMMIT"})
print('Test A - Forced commit:', 'PASS' if success else 'FAIL')

# Ensure ledger line written
ledger_exists = os.path.exists(n.ledger_path)
print('Ledger file exists:', ledger_exists)
if ledger_exists:
    with open(n.ledger_path, 'r') as f:
        lines = f.readlines()
    print('Ledger lines appended:', len(lines))

# Test B: Admissibility rejection for PRIVATE_KEY
n2 = NexusCore(threshold=-1000)
succ2, resp2 = n2.process_transaction(signals, {"PRIVATE_KEY": "abcd"})
print('Test B - Admissibility block:', 'PASS' if not succ2 else 'FAIL')

print('--- UNIT TESTS COMPLETE ---\n')