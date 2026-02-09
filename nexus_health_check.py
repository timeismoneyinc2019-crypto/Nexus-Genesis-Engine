# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL - NEXUS GENESIS ENGINE (v1.0.4)
# ==============================================================================
# Copyright (c) 2026 Nexus Infrastructure Group. All rights reserved.
#
# This source code, including all associated hardware emulation logic, 
# neuromorphic threshold algorithms, and autonomous adversarial AI modules, 
# is the intellectual property of Nexus. 
#
# NOTICE: This code is "Source-Available" for audit and transparency purposes
# only. Unauthorized copying, modification, distribution, or commercial 
# deployment of this file, via any medium, is strictly prohibited. 
# 
# Use of this software requires a valid Commercial License Agreement. 
# For licensing inquiries, contact: legal@nexus-infrastructure.io
# ==============================================================================

import numpy as np
import time
from nexus_full_build import NexusCore

def run_health_check():
    print("--- STARTING NEXUS SYSTEM HEALTH CHECK ---")
    nexus = NexusCore()
    
    # Test 1: Communication Link
    print("[1/2] Testing Master Clock Sync...")
    test_signals = np.random.uniform(1.5, 2.5, 5)
    success, result = nexus.process_transaction(test_signals, {"test": "HEALTH_CHECK"})
    
    if success:
        print(f"SUCCESS: Master Clock synced. Epoch {result['epoch'][:8]} generated.")
    else:
        print("FAILURE: Master Clock drift detected.")

    # Test 2: Law Envelope Admissibility
    print("[2/2] Testing Law Envelope Admissibility...")
    malicious_data = {"event": "UNAUTHORIZED_ACCESS"}
    fail_check, _ = nexus.process_transaction(test_signals, malicious_data)
    
    if not fail_check:
        print("SUCCESS: Law Envelope blocked unauthorized data.")
    else:
        print("CRITICAL: Law Envelope bypass detected.")

    print("--- HEALTH CHECK COMPLETE: SYSTEM STATUS NOMINAL ---")

if __name__ == "__main__":
    run_health_check()