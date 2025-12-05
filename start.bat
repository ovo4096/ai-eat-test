@echo off
REM 食谱生成器启动脚本 (Windows)

echo 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

python --version

echo 检查依赖...
python -c "import volcenginesdkarkruntime" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    python -m pip install -r requirements.txt
)

if not exist .env (
    echo 未找到 .env 文件，正在创建...
    copy .env.example .env
    echo 请编辑 .env 文件，填入你的 API Key
    pause
    exit /b 1
)

echo 启动食谱生成器...
python src\test_menu_batch.py
pause
