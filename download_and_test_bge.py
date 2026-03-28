from sentence_transformers import SentenceTransformer
import time

print("正在下载并加载模型（仅首次需要联网）...")
# 加载模型并指定在 CPU 上运行
model = SentenceTransformer('BAAI/bge-large-en-v1.5', device='cpu')

print("模型加载完成！正在测试推理延迟...")
test_sentence = "Rule 14: Head-on situation. When two power-driven vessels are meeting on reciprocal or nearly reciprocal courses so as to involve risk of collision each shall alter her course to starboard."

# 预热一次（PyTorch 首次计算会稍微慢一点）
_ = model.encode([test_sentence])

# 测试真实延迟
start_time = time.time()
vector = model.encode([test_sentence], normalize_embeddings=True)
end_time = time.time()

print(f"向量维度: {len(vector[0])}") # BGE-large 应该是 1024 维
print(f"单句编码耗时: {(end_time - start_time) * 1000:.2f} ms")