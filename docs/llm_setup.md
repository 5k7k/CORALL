# LLM Setup Guide

## 🔑 Setting Up LLM API Keys (OpenAI & Claude)

### **Method 1: .env File (Recommended)**

1. **Create .env file** in the project root:
```bash
# Copy the template
cp .env.example .env

# Edit with your actual API key
nano .env
```

2. **Add your API keys**:
```
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Claude Configuration
CLAUDE_API_KEY=sk-ant-your-actual-claude-key-here

# Zhipu AI Configuration (智谱AI)
ZHIPU_API_KEY=your-zhipu-api-key-here

# Choose default provider
LLM_PROVIDER=openai
# Options: openai, claude, zhipu
```

3. **Run simulation**:
```bash
source simEnv/bin/activate

# Use default provider from .env
python main.py --llm 1 --case_number 1

# Or specify provider explicitly
python main.py --llm 1 --llm_provider claude --case_number 1
python main.py --llm 1 --llm_provider openai --case_number 1
python main.py --llm 1 --llm_provider zhipu --case_number 1
```

### **Method 2: Environment Variable**

#### Temporary (current session):
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
source simEnv/bin/activate
python main.py --llm 1 --case_number 1
```

#### Permanent:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export OPENAI_API_KEY="sk-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### **Method 3: Configuration File**

1. **Edit config/api_keys.json**:
```json
{
  "openai": {
    "api_key": "sk-your-actual-openai-key-here",
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 200
  },
  "zhipu": {
    "api_key": "your-zhipu-api-key-here",
    "model": "glm-4",
    "base_url": "https://open.bigmodel.cn/api/paas/v4",
    "temperature": 0.1,
    "max_tokens": 200
  }
}
```

2. **Load in code** (advanced users can modify the LLM module to read from this file)

## 🔐 Security Best Practices

### **DO:**
- ✅ Use .env file for local development
- ✅ Keep API keys in environment variables for production
- ✅ Add .env to .gitignore (already done)
- ✅ Use different keys for development/production
- ✅ Rotate keys regularly

### **DON'T:**
- ❌ Never commit API keys to git
- ❌ Don't share keys in plain text
- ❌ Don't use production keys for testing
- ❌ Don't hardcode keys in source code

## 🚀 Quick Start

1. **Get your API keys**:
   - OpenAI: https://platform.openai.com/api-keys
   - Zhipu AI (智谱): https://open.bigmodel.cn/console/usercenter/apikeys
   - Claude: https://console.anthropic.com/
2. **Choose your method** (we recommend .env file)
3. **Set the key**:
```bash
# For Zhipu AI
echo "ZHIPU_API_KEY=your-zhipu-key-here" >> .env

# For OpenAI
echo "OPENAI_API_KEY=sk-your-openai-key-here" >> .env
```
4. **Test it**:
```bash
source simEnv/bin/activate
python main.py --llm 1 --llm_provider zhipu --case_number 1 --sim_time 60
```

## 🔧 Configuration Options

### **Model Settings**
You can customize the LLM behavior by setting these environment variables:

```bash
# In .env file
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.1              # 0.0 to 1.0
OPENAI_MAX_TOKENS=200               # Response length

# Zhipu AI Configuration
ZHIPU_API_KEY=your-zhipu-key-here
ZHIPU_MODEL=glm-4                   # glm-4, glm-4v, glm-3-turbo
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_TEMPERATURE=0.1              # 0.0 to 1.0
ZHIPU_MAX_TOKENS=200               # Response length

# Claude Configuration
CLAUDE_API_KEY=sk-ant-your-claude-key-here
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_TEMPERATURE=0.1              # 0.0 to 1.0
CLAUDE_MAX_TOKENS=50                # Response length
```

