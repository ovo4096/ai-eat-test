#!/bin/bash
# 食谱生成器启动脚本 (macOS/Linux)

# 检查 Python 版本
python_cmd=""
if command -v python3.8 &> /dev/null; then
    python_cmd="python3.8"
elif command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "❌ 错误: 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo "使用 Python: $python_cmd"
$python_cmd --version

# 检查依赖
echo "检查依赖..."
$python_cmd -c "import volcenginesdkarkruntime" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 正在安装依赖..."
    $python_cmd -m pip install -r requirements.txt
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️ 未找到 .env 文件，正在创建..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的 API Key"
    exit 1
fi

# 运行程序
echo "🚀 启动食谱生成器..."
$python_cmd src/test_menu_batch.py
