import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Union
from enum import Enum
import numpy as np
from abc import ABC, abstractmethod

# Import LLM clients
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts.prompt import PromptTemplate
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from langchain_openai import ChatOpenAI as ZhipuChatOpenAI
    ZHIPU_AVAILABLE = True
except ImportError:
    ZHIPU_AVAILABLE = False

@dataclass
class VesselState:
    """Represents the state of a vessel encounter"""
    risk: float
    distance: float
    bearing: float
    dcpa: float
    tcpa: float


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM provider is available"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation"""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.1, max_tokens: int = 1000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None

        if OPENAI_AVAILABLE and self.is_available():
            self.client = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY") is not None
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        if not self.client:
            return "OpenAI not available"
        
        try:
            response = self.client.invoke(prompt)
            return response.content
        except Exception as e:
            return f"OpenAI error: {str(e)}"

class ClaudeProvider(LLMProvider):
    """Claude/Anthropic LLM provider implementation"""

    def __init__(self, model: str = "claude-sonnet-4-20250514", temperature: float = 0.1, max_tokens: int = 1000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None

        if ANTHROPIC_AVAILABLE and self.is_available():
            self.client = anthropic.Anthropic(
                api_key=os.getenv("CLAUDE_API_KEY")
            )

    def is_available(self) -> bool:
        """Check if Claude is available"""
        return ANTHROPIC_AVAILABLE and os.getenv("CLAUDE_API_KEY") is not None

    def generate_response(self, prompt: str) -> str:
        """Generate response using Claude"""
        if not self.client:
            return "Claude not available"

        try:
            response = self.client.messages.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude error: {str(e)}"

class ZhipuProvider(LLMProvider):
    """智谱AI GLM provider implementation (OpenAI-compatible protocol)"""

    def __init__(self, model: str = None, temperature: float = 0.1, max_tokens: int = 1000):
        # 从环境变量读取模型，如果没有设置则使用默认值
        self.model = model or os.getenv("ZHIPU_MODEL", "glm-4")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None

        if ZHIPU_AVAILABLE and self.is_available():
            base_url = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
            print(f"[DEBUG] Initializing Zhipu client with model: {self.model}")
            print(f"[DEBUG] Using ZHIPU_MODEL from env: {os.getenv('ZHIPU_MODEL')}")
            self.client = ZhipuChatOpenAI(
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=base_url,
                api_key=os.getenv("ZHIPU_API_KEY")
            )

    def is_available(self) -> bool:
        """Check if Zhipu is available"""
        return ZHIPU_AVAILABLE and os.getenv("ZHIPU_API_KEY") is not None

    def generate_response(self, prompt: str) -> str:
        """Generate response using Zhipu"""
        if not self.client:
            print(f"[DEBUG] Zhipu client not available")
            return "Zhipu not available"

        try:
            print(f"[DEBUG] Zhipu provider using model: {self.model}")
            print(f"[DEBUG] API key available: {bool(os.getenv('ZHIPU_API_KEY'))}")
            print(f"[DEBUG] Base URL: {os.getenv('ZHIPU_BASE_URL', 'default')}")

            # Make the API call
            response = self.client.invoke(prompt)

            if response and hasattr(response, 'content'):
                content = response.content
                print(f"[DEBUG] Response type: {type(content)}")
                print(f"[DEBUG] Response content: {repr(content)}")
                return content
            else:
                print(f"[DEBUG] Unexpected response format: {response}")
                return f"Zhipu error: Unexpected response format - {str(response)}"

        except Exception as e:
            print(f"[DEBUG] Zhipu API error: {str(e)}")
            print(f"[DEBUG] Error type: {type(e)}")
            import traceback
            print(f"[DEBUG] Full traceback: {traceback.format_exc()}")
            return f"Zhipu error: {str(e)}"

class MultiLLMCOLREGSInterpreter:
    """COLREGs interpreter that can use multiple LLM providers"""
    
    def __init__(self, provider: str = None):
        self.provider_name = provider or os.getenv("LLM_PROVIDER", "openai")
        self.provider = self._initialize_provider()
        
        self.system_prompt = """You are a ship navigation officer. Based on the situation, give a simple decision in this format:
Action: [Stand on / Give-way, turn to starboard / Give-way, turn to port]

Situation:"""
    
    def _initialize_provider(self) -> Optional[LLMProvider]:
        """Initialize the appropriate LLM provider"""
        if self.provider_name.lower() == "openai":
            provider = OpenAIProvider(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
            )
            if provider.is_available():
                return provider

        elif self.provider_name.lower() == "claude":
            provider = ClaudeProvider(
                model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
                temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
            )
            if provider.is_available():
                return provider

        elif self.provider_name.lower() == "zhipu":
            provider = ZhipuProvider(
                model=os.getenv("ZHIPU_MODEL", "glm-4"),
                temperature=float(os.getenv("ZHIPU_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("ZHIPU_MAX_TOKENS", "1000"))
            )
            if provider.is_available():
                return provider

        # Fallback logic
        if self.provider_name.lower() == "openai":
            fallbacks = [
                ClaudeProvider(
                    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
                    temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
                ),
                ZhipuProvider(
                    model=os.getenv("ZHIPU_MODEL", "glm-4"),
                    temperature=float(os.getenv("ZHIPU_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("ZHIPU_MAX_TOKENS", "1000"))
                )
            ]
        elif self.provider_name.lower() == "claude":
            fallbacks = [
                OpenAIProvider(
                    model=os.getenv("OPENAI_MODEL", "gpt-4"),
                    temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
                ),
                ZhipuProvider(
                    model=os.getenv("ZHIPU_MODEL", "glm-4"),
                    temperature=float(os.getenv("ZHIPU_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("ZHIPU_MAX_TOKENS", "1000"))
                )
            ]
        elif self.provider_name.lower() == "zhipu":
            fallbacks = [
                OpenAIProvider(
                    model=os.getenv("OPENAI_MODEL", "gpt-4"),
                    temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
                ),
                ClaudeProvider(
                    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
                    temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
                )
            ]
        else:
            fallbacks = [
                OpenAIProvider(
                    model=os.getenv("OPENAI_MODEL", "gpt-4"),
                    temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
                ),
                ClaudeProvider(
                    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
                    temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
                ),
                ZhipuProvider(
                    model=os.getenv("ZHIPU_MODEL", "glm-4"),
                    temperature=float(os.getenv("ZHIPU_TEMPERATURE", "0.1")),
                    max_tokens=int(os.getenv("ZHIPU_MAX_TOKENS", "1000"))
                )
            ]

        for fallback in fallbacks:
            if fallback.is_available():
                fallback_name = fallback.__class__.__name__.replace("Provider", "")
                print(f"{fallback_name} unavailable, falling back to {fallback_name}")
                return fallback

        return None
    
    
    
    def _format_situation_description(self, vessels: List[VesselState]) -> str:
        """Format situation description for LLM"""
        if not vessels:
            return "No vessels detected."

        highest_risk_vessel = max(vessels, key=lambda v: v.risk)

        # Add more context about the situation
        if highest_risk_vessel.tcpa < 0:
            time_status = "vessel is astern (already passed)"
        elif highest_risk_vessel.tcpa > 300:
            time_status = "vessel is far, no immediate action needed"
        else:
            time_status = f"vessel will reach CPA in {highest_risk_vessel.tcpa:.1f} seconds"

        description = f"""
Maritime Situation Analysis:
- Number of vessels: {len(vessels)}
- Highest risk vessel details:
* Risk Level: {highest_risk_vessel.risk:.3f}
* Distance: {highest_risk_vessel.distance:.2f} nautical miles
* Relative Bearing: {highest_risk_vessel.bearing:.1f}°
* DCPA (Closest Point of Approach): {highest_risk_vessel.dcpa:.2f} nautical miles
* TCPA (Time to CPA): {highest_risk_vessel.tcpa:.1f} seconds ({time_status})

Based on COLREGs rules, what action should be taken?"""

        return description.strip()
    
    def make_decision(self, vessels: List[VesselState], time_idx: int = 0) -> str:
        """Make a COLREGs-compliant decision"""
        if not self.provider:
            return "No LLM provider available"

        if not vessels:
            return "No vessels detected - maintain course and speed"

        # Format the situation
        situation_description = self._format_situation_description(vessels)

        # Create full prompt
        full_prompt = f"{self.system_prompt}\n\n{situation_description}"

        # Debug: Print the prompt being sent to LLM
        print(f"\n[DEBUG] Full prompt sent to {self.provider_name.upper()}:")
        print("=" * 60)
        print(full_prompt)
        print("=" * 60)

        # Get response from LLM
        response = self.provider.generate_response(full_prompt)

        # Debug: Print the raw response
        print(f"\n[DEBUG] Raw response received from {self.provider_name.upper()}:")
        print("=" * 60)
        print(repr(response))  # repr shows special characters
        print("-" * 60)
        print(response)  # Normal display
        print("=" * 60)

        # Ensure response is properly formatted
        if not response or len(response.strip()) == 0:
            response = "Error: Empty response from LLM"

        # Add provider information
        provider_info = f"[{self.provider_name.upper()}] "

        return f"{provider_info}{response}"
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers"""
        providers = []

        if OpenAIProvider().is_available():
            providers.append("openai")

        if ClaudeProvider().is_available():
            providers.append("claude")

        if ZhipuProvider().is_available():
            providers.append("zhipu")

        return providers

# Backward compatibility with original interface
COLREGSInterpreter = MultiLLMCOLREGSInterpreter