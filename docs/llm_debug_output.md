# LLM 推理过程查看指南

## **显示详细的 LLM 推理过程**

现在你可以看到大模型在决策过程中的详细推理信息了！

### **1. 基本使用**

运行时可以看到：
```bash
python main.py --llm 1 --llm_provider zhipu --case_number 1 --sim_time 60
```

### **2. 预期输出**

运行时会显示如下详细信息：

```
============================================================
[LLM Input at t=10.0s]
============================================================

🚢 Vessel 1:
  📏 Distance: 2.45 nmi
  🧭 Bearing: 45.2°
  ⏱️  DCPA: 1.23 nmi
  ⏱️  TCPA: 45.6 s
  ⚠️  Risk: 0.345

============================================================
[🤖 LLM Response]
============================================================
[Claude] Rule 14 (head-on situation), Action: [Give-way, turn to starboard], Explanation: Based on COLREGs Rule 14, when two vessels are approaching head-on, both shall alter course to starboard...

🎯 FINAL DECISION: Turn STARBOARD
   → Turn right to give way to other vessel

============================================================
```

### **3. 调试模式（显示更多信息）**

设置环境变量开启调试模式：
```bash
# 方法1：临时设置
export SHOW_LLM_DEBUG=true
python main.py --llm 1 --llm_provider zhipu

# 方法2：添加到 .env 文件
echo "SHOW_LLM_DEBUG=true" >> .env
```

调试模式下会显示：
```
[DEBUG] Full response parsing:
  Raw response length: 156 characters
  Extracted Kdir: 1
  Keywords found: 'starboard'=1, 'port'=0, 'stand on'=0
```

### **4. 显示的内容说明**

#### **输入信息（发送给LLM的数据）**
- 🚢 Vessel {n}: 第n艘目标船的信息
- 📏 Distance: 距离（海里）
- 🧭 Bearing: 相对方位（度）
- ⏱️ DCPA: 最近接近距离（海里）
- ⏱️ TCPA: 到达最近接近点的时间（秒）
- ⚠️ Risk: 风险值（0-1）

#### **LLM响应**
- 完整的LLM回复内容
- 包含引用的COLREGs规则
- 建议的行动（转向或保持）

#### **最终决策**
- 🎯 FINAL DECISION: 最终决定
  - Turn STARBOARD: 向右转向
  - Turn PORT: 向左转向
  - STAND ON: 保持航向

### **5. 决策频率**

- LLM每**10秒**（仿真时间）进行一次决策
- 决策基于当前所有船舶的位置和运动状态
- 决策结果影响船舶的转向方向

### **6. 故障排查**

#### **如果看不到LLM输出**
1. 确认使用了 `--llm 1` 参数
2. 检查API key是否正确设置
3. 确认网络连接正常

#### **如果输出显示"LLM not available"**
1. 检查依赖是否安装：`pip install langchain-openai`
2. 检查环境变量是否设置正确
3. 尝试使用不同的provider

#### **如果决策总是"Stand on"**
- 检查风险值是否过低
- 尝试增加仿真时间让船舶更接近
- 调整模型参数（temperature等）

### **7. 不同案例的观察**

#### **Case 1 - 对遇情况**
- 初始：两船相向而行
- 期望：LLM建议在合适时机转向
- 观察：何时开始转向，转向幅度

#### **Case 8 - 交叉相遇**
- 一船在前，一船从侧面接近
- 期望：判断谁让谁，转向方向
- 观察：是否符合COLREGs规则

#### **Case 12 - 追越情况**
- 快船追慢船
- 期望：追越船向右让路
- 观察：追越时机和行动

### **8. 高级技巧**

#### **保存输出到文件**
```bash
python main.py --llm 1 --llm_provider zhipu --case_number 1 > output.log
```

#### **查看特定时间段的决策**
```bash
# 只显示LLM决策部分（过滤掉进度信息）
python main.py --llm 1 --llm_provider zhipu --case_number 1 | grep -A 20 "LLM Input"
```

这样你就能清楚地看到大模型是如何根据COLREGs规则和当前船舶状态做出决策的了！