# Token 消耗估算

## **每次实验的 Token 消耗分析**

### **1. 基本参数**
- **仿真时间**: 450 秒（默认）
- **时间步长**: 0.1 秒
- **总步数**: 4500 步
- **LLM 调用频率**: 每 200 步 = 每 20 秒
- **LLM 调用次数**: 4500 / 200 = 22-23 次

### **2. Token 消耗构成**

#### **A. 输入 Tokens（每次调用）**
```
系统提示词: ~50 tokens
船舶信息（2艘船）: ~150 tokens
时间描述: ~20 tokens
总计输入: ~220 tokens/次
```

#### **B. 输出 Tokens（每次调用）**
```
格式化响应: Rule X, Action: [...], Explanation: ...
平均响应长度: ~80 tokens
总计输出: ~80 tokens/次
```

#### **C. 总消耗（每次调用）**
```
输入 + 输出: 220 + 80 = 300 tokens/次
```

### **3. 完整实验的 Token 消耗**

#### **标准实验（450秒）**
```
LLM调用次数: 23次
每次消耗: 300 tokens
总计消耗: 23 × 300 = 6,900 tokens
```

#### **不同时长的实验**

| 仿真时长 | 调用次数 | 总消耗 |
|---------|---------|--------|
| 60秒    | 3次     | 900 tokens |
| 300秒   | 15次    | 4,500 tokens |
| 450秒   | 23次    | 6,900 tokens |
| 600秒   | 30次    | 9,000 tokens |
| 900秒   | 45次    | 13,500 tokens |

### **4. 各提供商的 Token 成本**

#### **智谱AI (glm-4)**
- 输入: ~¥0.01/千tokens
- 输出: ~¥0.02/千tokens
- **450秒实验成本**: 6.9k × ¥0.01 + 6.9k × ¥0.02 = ¥0.207

#### **OpenAI (gpt-4)**
- 输入: $0.03/千tokens
- 输出: $0.06/千tokens
- **450秒实验成本**: 6.9k × $0.03 + 6.9k × $0.06 = $0.621

#### **Claude (claude-sonnet)**
- 输入: $0.015/千tokens
- 输出: $0.075/千tokens
- **450秒实验成本**: 6.9k × $0.015 + 6.9k × $0.075 = $0.621

### **5. 优化建议**

#### **减少 Token 消耗的方法**

1. **降低调用频率**
   ```python
   # 改为每40秒调用一次（原来20秒）
   if i % 400 ==:  # dt=0.1时，400步=40秒
   ```

2. **简化提示词**
   ```python
   # 简化前的提示词: ~220 tokens
   # 简化后: ~100 tokens
   ```

3. **减少最大输出长度**
   ```python
   max_tokens=50  # 从100降到50
   ```

#### **优化后的消耗**
```
优化后每次调用: 150输入 + 50输出 = 200 tokens
450秒实验: 23 × 200 = 4,600 tokens（节省33%）
```

### **6. 实际计算示例**

#### **Python 代码估算**
```python
def estimate_tokens(sim_time=450, dt=0.1, call_interval=20):
    total_steps = int(sim_time / dt)
    num_calls = int(sim_time / call_interval)

    tokens_per_call = 300  # 估算值
    total_tokens = num_calls * tokens_per_call

    return {
        'total_steps': total_steps,
        'num_calls': num_calls,
        'total_tokens': total_tokens
    }

# 示例
print(estimate_tokens(sim_time=450))
# 输出: {'total_steps': 4500, 'num_calls': 22, 'total_tokens': 6600}
```

### **7. 监控实际消耗**

#### **添加 Token 计数**
```python
# 在 multi_llm_decision.py 中添加
import tiktoken  # OpenAI 的 tokenizer

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# 使用示例
tokens = count_tokens(prompt)
print(f"Input tokens: {tokens}")
```

### **8. 成本预算参考**

#### **每月实验预算（按450秒计算）**
| 实验次数 | 总消耗 | 智谱AI成本 | OpenAI成本 |
|---------|-------|-----------|-----------|
| 10次    | 69k   | ¥2.07     | $6.21     |
| 50次    | 345k  | ¥10.35    | $31.05    |
| 100次   | 690k  | ¥20.70    | $62.10    |

### **9. 注意事项**

1. **Token 数不是固定的**，会根据实际响应长度变化
2. **不同模型**的 tokenizer 不同，token 计数有差异
3. **网络传输**可能产生额外开销
4. **错误重试**会增加消耗

### **10. 结论**

- **标准实验（450秒）**: 约 7k tokens
- **成本极低**: 智谱AI约¥0.2/次，OpenAI约$0.6/次
- **可以安全运行**: 即使大量实验，成本也在可接受范围内

建议先运行少量实验测试，监控实际消耗，再调整参数。