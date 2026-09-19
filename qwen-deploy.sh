#!/bin/bash
# Qwen Model Kubernetes Deployment Script
# Complete automated deployment

set -e

echo "🚀 部署 Qwen 模型到 Kubernetes..."
echo ""

# 1. 检查依赖
echo "1️⃣ 检查依赖..."
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl 未安装"; exit 1; }
echo "   ✓ kubectl 已安装"

command -v helm >/dev/null 2>&1 || echo "   ⚠️ helm 未安装（可选）"

# 2. 创建命名空间
echo ""
echo "2️⃣ 创建命名空间..."
kubectl create namespace qwen-ai --dry-run=client -o yaml | kubectl apply -f -
echo "   ✓ 命名空间已创建"

# 3. 检查存储类
echo ""
echo "3️⃣ 检查存储类..."
STORAGE_CLASS=$(kubectl get storageclass | grep -i standard | head -1 | awk '{print $1}' || echo "standard")
echo "   ✓ 使用存储类: $STORAGE_CLASS"

# 4. 部署 Qwen
echo ""
echo "4️⃣ 部署 Qwen 服务..."
kubectl apply -f qwen-deployment.yaml
echo "   ✓ 部署配置已应用"

# 5. 等待部署完成
echo ""
echo "5️⃣ 等待部署完成（这可能需要 5-15 分钟）..."
kubectl wait --for=condition=ready pod \
  -l app=qwen \
  -n qwen-ai \
  --timeout=900s || echo "⚠️ 部署超时，检查 pod 日志"

# 6. 获取服务信息
echo ""
echo "6️⃣ 服务信息..."
echo ""
echo "Pod 状态:"
kubectl get pods -n qwen-ai -l app=qwen
echo ""
echo "服务端点:"
kubectl get svc qwen-service -n qwen-ai
echo ""

# 7. 获取外部 IP
EXTERNAL_IP=$(kubectl get svc qwen-service -n qwen-ai -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")

# 8. 显示访问信息
echo ""
echo "✅ 部署完成！"
echo ""
echo "📍 访问信息:"
echo "   API 端点: http://$EXTERNAL_IP:8080/v1"
echo "   内部端点: http://qwen-service.qwen-ai:8080/v1"
echo ""
echo "📊 管理命令:"
echo "   查看日志:     kubectl logs -n qwen-ai -l app=qwen -f"
echo "   查看状态:     kubectl get all -n qwen-ai"
echo "   删除部署:     kubectl delete namespace qwen-ai"
echo ""
echo "🧪 测试 API:"
echo "   curl http://$EXTERNAL_IP:8080/v1/chat/completions \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"model\": \"/models/Qwen1.5-4B-Chat/\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}'"
echo ""

# 9. 监视部署
echo ""
read -p "是否要监视部署日志？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kubectl logs -n qwen-ai -l app=qwen -f
fi
