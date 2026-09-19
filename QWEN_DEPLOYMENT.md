# Qwen 模型 Kubernetes 部署指南

## 快速开始

### 一键部署

```bash
chmod +x qwen-deploy.sh
./qwen-deploy.sh
```

### 手动部署

```bash
# 1. 应用配置
kubectl apply -f qwen-deployment.yaml

# 2. 等待部署
kubectl wait --for=condition=ready pod -l app=qwen -n qwen-ai --timeout=900s

# 3. 获取服务端点
kubectl get svc qwen-service -n qwen-ai
```

---

## 前置要求

- **Kubernetes 集群** (1.20+)
  - Aliyun ACK
  - AWS EKS
  - GCP GKE
  - 本地 Minikube (需要 GPU)

- **GPU 节点**
  - NVIDIA GPU (V100/A100 推荐)
  - 驱动程序已安装
  - nvidia-device-plugin 部署完成

- **工具**
  ```bash
  kubectl version --client
  helm version  # 可选
  ```

- **存储**
  - 50GB 持久化存储用于模型
  - StorageClass 已配置

---

## 部署架构

```
┌─────────────────────────────────────┐
│   Kubernetes Cluster                │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Service: qwen-service       │  │
│  │  Type: LoadBalancer          │  │
│  │  Port: 80 → 8080            │  │
│  └──────────────────────────────┘  │
│            ↓                         │
│  ┌──────────────────────────────┐  │
│  │  Pod: vllm-qwen              │  │
│  │  - Port: 8080                │  │
│  │  - GPU: 1x NVIDIA            │  │
│  │  - Memory: 32-64Gi           │  │
│  │  - Model: Qwen1.5-4B-Chat    │  │
│  └──────────────────────────────┘  │
│            ↓                         │
│  ┌──────────────────────────────┐  │
│  │  PVC: qwen-model             │  │
│  │  Size: 50Gi                  │  │
│  │  Path: /models/Qwen1.5-4B    │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

## API 使用

### Chat Completion

```bash
curl http://your-endpoint:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models/Qwen1.5-4B-Chat/",
    "messages": [
      {
        "role": "user",
        "content": "你好，请自我介绍一下"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

### Completions

```bash
curl http://your-endpoint:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models/Qwen1.5-4B-Chat/",
    "prompt": "Hello, my name is",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

---

## 管理命令

### 查看状态

```bash
# 查看所有资源
kubectl get all -n qwen-ai

# 查看 Pod 详情
kubectl describe pod -n qwen-ai -l app=qwen

# 查看服务端点
kubectl get svc qwen-service -n qwen-ai -o wide
```

### 查看日志

```bash
# 实时日志
kubectl logs -n qwen-ai -l app=qwen -f

# 获取最近 100 行
kubectl logs -n qwen-ai -l app=qwen --tail=100

# 获取前面的日志
kubectl logs -n qwen-ai -l app=qwen --previous
```

### 性能监控

```bash
# 查看 Pod 资源使用
kubectl top pod -n qwen-ai -l app=qwen

# 查看节点资源
kubectl top node

# 监视 HPA
kubectl get hpa -n qwen-ai -w
```

### 扩缩容

```bash
# 手动扩展
kubectl scale deployment qwen --replicas=3 -n qwen-ai

# 查看 HPA 状态
kubectl get hpa qwen-hpa -n qwen-ai -w

# 修改 HPA 范围
kubectl edit hpa qwen-hpa -n qwen-ai
```

---

## 故障排除

### Pod 未启动

```bash
# 查看 Pod 事件
kubectl describe pod -n qwen-ai -l app=qwen

# 查看完整日志
kubectl logs -n qwen-ai -l app=qwen --previous

# 可能原因：
# - GPU 不可用: kubectl get nodes -o wide | grep gpu
# - 存储不足: kubectl get pvc -n qwen-ai
# - 镜像拉取失败: kubectl describe pod ... 查看 Events
```

### 服务无法访问

```bash
# 检查 Service
kubectl get svc qwen-service -n qwen-ai

# 检查 Endpoints
kubectl get endpoints qwen-service -n qwen-ai

# 测试内部连接
kubectl run -it --image=curlimages/curl test --restart=Never -- \
  curl http://qwen-service.qwen-ai:8080/v1/health
```

### 内存不足

```bash
# 查看内存使用
kubectl top pod -n qwen-ai

# 减少 max_tokens 或 max_num_seqs
kubectl edit deployment qwen -n qwen-ai

# 检查节点内存
kubectl describe node | grep -A 5 "Allocated resources"
```

---

## 性能优化

### GPU 优化

```yaml
# 在 deployment 中调整：
resources:
  requests:
    nvidia.com/gpu: "1"  # 使用 GPU
  limits:
    nvidia.com/gpu: "1"

# 环境变量
env:
- name: CUDA_VISIBLE_DEVICES
  value: "0"
```

### 并发优化

```bash
# 调整服务并发目标
annotations:
  autoscaling.knative.dev/target: "10"  # 增加并发
  autoscaling.knative.dev/max-scale: "5"  # 最大副本数
```

### 模型优化

```bash
# 启用缓存
--enable-prefix-caching
--enable-chunked-prefill

# 调整精度
--dtype half  # 使用 FP16 节省内存
--dtype float16  # 另一种写法

# 调整 GPU 内存利用率
--gpu-memory-utilization 0.95  # 0-1 之间
```

---

## 升级和更新

### 更新镜像版本

```bash
# 编辑部署
kubectl set image deployment/qwen \
  vllm-qwen=ac2-registry.cn-hangzhou.cr.aliyuncs.com/ac2/vllm:0.5.0-ubuntu22.04 \
  -n qwen-ai

# 或直接编辑
kubectl edit deployment qwen -n qwen-ai
```

### 更新配置

```bash
# 编辑配置映射
kubectl edit configmap qwen-config -n qwen-ai

# 重启 Pod 使配置生效
kubectl rollout restart deployment/qwen -n qwen-ai
```

---

## 清理和卸载

```bash
# 删除整个命名空间（包括所有资源）
kubectl delete namespace qwen-ai

# 或逐个删除
kubectl delete deployment qwen -n qwen-ai
kubectl delete svc qwen-service -n qwen-ai
kubectl delete pvc qwen-model -n qwen-ai
kubectl delete namespace qwen-ai
```

---

## 与 Claude 聊天机器人集成

### 配置集成点

```python
# 在 claude_chatbot.py 中添加
import requests

QWEN_ENDPOINT = "http://qwen-service.qwen-ai:8080/v1"

def query_qwen(messages, model="/models/Qwen1.5-4B-Chat/"):
    response = requests.post(
        f"{QWEN_ENDPOINT}/chat/completions",
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 512
        }
    )
    return response.json()
```

### 多模型路由

```bash
# 启用模型选择
/model qwen  # 使用 Qwen
/model claude-opus-5  # 使用 Claude

# 需要在聊天机器人中添加模型路由逻辑
```

---

## 成本估算

| 资源 | 用量 | 成本 (AWS) |
|------|------|-----------|
| GPU (p3.2xlarge) | 1 个 | $3.06/小时 |
| 内存 (64GB) | 固定 | 包含在 GPU 中 |
| 存储 (50GB) | 持久 | $5/月 |
| 网络 | 可变 | $0.02/GB |
| **月成本** | - | **~$2,300** |

---

## 支持和资源

- [vLLM 文档](https://docs.vllm.ai/)
- [Qwen 官方](https://github.com/QwenLM/Qwen)
- [Kubernetes 文档](https://kubernetes.io/docs/)
- [Knative 文档](https://knative.dev/)

---

**部署完成后**：Qwen 模型将在 Kubernetes 中 24/7 运行！🎉
