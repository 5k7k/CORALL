#!/usr/bin/env python3
"""
Test script to verify environment variables are being read correctly
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_env_variables():
    print("=== Environment Variables Test ===")

    # Test Zhipu variables
    print(f"\nZhipu Configuration:")
    print(f"  ZHIPU_API_KEY: {'SET' if os.getenv('ZHIPU_API_KEY') else 'NOT SET'}")
    print(f"  ZHIPU_MODEL: {os.getenv('ZHIPU_MODEL', 'NOT SET')}")
    print(f"  ZHIPU_BASE_URL: {os.getenv('ZHIPU_BASE_URL', 'NOT SET')}")
    print(f"  ZHIPU_TEMPERATURE: {os.getenv('ZHIPU_TEMPERATURE', 'NOT SET')}")
    print(f"  ZHIPU_MAX_TOKENS: {os.getenv('ZHIPU_MAX_TOKENS', 'NOT SET')}")

    # Test other variables
    print(f"\nOther LLM Variables:")
    print(f"  LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'NOT SET')}")
    print(f"  OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'NOT SET')}")
    print(f"  CLAUDE_MODEL: {os.getenv('CLAUDE_MODEL', 'NOT SET')}")

    # Test Zhipu provider
    print(f"\n=== Testing Zhipu Provider ===")
    try:
        from src.decision_making.multi_llm_decision import ZhipuProvider

        # Test with explicit model
        provider1 = ZhipuProvider(model="glm-4.5-air")
        print(f"  Provider 1 model: {provider1.model}")

        # Test with env var
        provider2 = ZhipuProvider()
        print(f"  Provider 2 model: {provider2.model}")
        print(f"  Provider 2 max_tokens: {provider2.max_tokens}")

    except Exception as e:
        print(f"  Error creating ZhipuProvider: {e}")

if __name__ == "__main__":
    test_env_variables()