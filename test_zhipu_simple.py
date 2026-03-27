#!/usr/bin/env python3
"""
Simple test for Zhipu AI
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from langchain_openai import ChatOpenAI as ZhipuChatOpenAI

    # Test basic connection
    client = ZhipuChatOpenAI(
        model="glm-4",
        temperature=0.1,
        max_tokens=100,
        base_url="https://open.bigmodel.cn/api/paas/v4",
        api_key=os.getenv("ZHIPU_API_KEY")
    )

    print("=== Zhipu AI Test ===")
    print(f"API Key: {os.getenv('ZHIPU_API_KEY', 'Not set')}")

    # Simple test prompt
    response = client.invoke("What is 2+2?")
    print(f"Response: {response.content}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()