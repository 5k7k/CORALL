#!/usr/bin/env python3
"""
Debug script for testing LLM responses
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.decision_making.multi_llm_decision import MultiLLMCOLREGSInterpreter, VesselState
import json

def test_llm_response():
    # Create interpreter
    interpreter = MultiLLMCOLREGSInterpreter(provider="zhipu")

    # Create test vessel states
    vessels = [
        VesselState(
            risk=0.345,
            distance=2.45,
            bearing=45.2,
            dcpa=1.23,
            tcpa=45.6
        )
    ]

    print("=== Testing LLM Response ===")
    print(f"Provider: {interpreter.provider_name}")
    print(f"Provider available: {interpreter.provider is not None}")

    # Make decision
    response = interpreter.make_decision(vessels)

    print("\n=== Final Response ===")
    print(response)

    # Test the extraction function
    from src.core.simulation import extract_kdir_from_response
    kdir = extract_kdir_from_response(response)
    print(f"\nExtracted Kdir: {kdir}")
    print(f"Action: {['Stand on', 'Turn Port', 'Turn Starboard'][kdir + 1]}")

if __name__ == "__main__":
    test_llm_response()