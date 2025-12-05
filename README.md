# 食谱生成器

基于火山引擎 Ark API 的批量食谱生成工具，支持深度思考模式生成高质量食谱内容。

## 功能特点

- ✅ 批量生成多种类型的食谱
- ✅ 使用深度思考模式提升内容质量
- ✅ **支持并发请求，加快处理速度**
- ✅ 实时保存进度，支持中断恢复
- ✅ 双格式输出（CSV + Excel）
- ✅ 记录 AI 思考过程和生成结果
- ✅ 自动跳过已完成的食谱
- ✅ 可自定义提示词模板

## 环境要求

- Python 3.8 或更高版本（推荐 3.8-3.12）
- 火山引擎 Ark API Key

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像加速：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置 API Key

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
ARK_API_KEY=your_actual_api_key_here
```

> 💡 如何获取 API Key：请访问 [火山引擎文档](https://www.volcengine.com/docs/82379/1399008)

### 3. 运行程序

**方式一：使用启动脚本（推荐）**

macOS/Linux:
```bash
./start.sh
```

Windows:
```bash
start.bat
```

**方式二：直接运行**

```bash
python src/test_menu_batch.py
```

## 项目结构

```
ai-eat-test/
├── src/
│   ├── test_menu_name.txt       # 食谱名称列表
│   ├── test_menu_batch.py       # 批量生成脚本（主程序）
│   ├── test_ark_api.py          # API 测试脚本
│   └── test_thinking.py         # 深度思考测试脚本
├── outputs/
│   ├── recipe_results.csv       # CSV 格式结果（实时保存）
│   └── recipe_results.xlsx      # Excel 格式结果（完成后生成）
├── requirements.txt              # Python 依赖
├── .env.example                 # 环境变量示例
├── .env                         # 环境变量配置（需自行创建）
├── .python-version              # Python 版本配置（pyenv）
├── start.sh                     # macOS/Linux 启动脚本
├── start.bat                    # Windows 启动脚本
└── README.md                    # 项目说明
```

## 使用说明

### 食谱配置

编辑 `src/test_menu_name.txt` 文件，每行一个食谱名称，例如：

```
补血养颜的食谱
清热解毒的食谱
健脾养胃的食谱
```

### 自定义提示词

在 `.env` 文件中配置提示词模板（可选）：

```env
RECIPE_PROMPT=请生成3天的{menu_name}，每天至少包含8种不同的食物。食物的选择必须严格符合需求
```

> 注意：提示词中必须包含 `{menu_name}` 占位符

### 并发配置

在 `.env` 文件中配置并发请求数量（可选）：

```env
MAX_CONCURRENT_REQUESTS=5
```

- **默认值**：5（同时发送 5 个请求）
- **推荐范围**：5-10 个
- **注意事项**：
  - 并发数过大可能触发 API 限流
  - 根据您的 API 配额和网络情况调整
  - 并发处理会显著提升批量生成速度

### 中断恢复

- 程序运行时按 `Ctrl+C` 可以随时中断
- 已完成的食谱会保存到 CSV 文件
- 下次运行时会自动跳过已完成的食谱，继续未完成的部分

### 输出说明

程序会生成两个文件：

1. **recipe_results.csv**
   - 实时保存，每完成一条立即写入
   - 包含列：食谱名、AI思考过程、AI结果、状态、请求耗时(秒)
   - 可随时查看进度

2. **recipe_results.xlsx**
   - 程序结束时自动生成
   - 格式更友好，便于查看和分享

## 常见问题

### 1. ModuleNotFoundError: No module named 'xxx'

确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

### 2. Python 版本不兼容

本项目需要 Python 3.8-3.12 版本。如果使用 Python 3.13+ 会出现兼容性问题。

使用 pyenv 切换版本：

```bash
pyenv install 3.8.20
pyenv local 3.8.20
```

### 3. API 请求失败

检查：
- `.env` 文件中的 API Key 是否正确
- 网络连接是否正常
- 是否有足够的 API 配额

### 4. 程序运行缓慢

- 深度思考模式需要较长时间（单个请求约 60-120 秒）
- 已支持并发请求，可通过 `MAX_CONCURRENT_REQUESTS` 调整并发数
- 默认并发数为 5，可根据需要提升至 10 以加快速度
- 可以查看控制台输出的实时进度

## API 参数说明

- **model**: `deepseek-v3-1-terminus` - 使用的模型
- **thinking**: `enabled` - 启用深度思考能力
- **timeout**: `1800` - 超时时间（30分钟）

## 依赖说明

- `volcengine-python-sdk[ark]`: 火山引擎 Python SDK
- `python-dotenv`: 环境变量管理
- `openpyxl`: Excel 文件处理

## 注意事项

- ⚠️ 请勿将 `.env` 文件提交到版本控制系统
- 🔒 请妥善保管您的 API Key
- 📊 批量处理大量数据时，请注意 API 配额限制
- ⏱️ 深度思考模式耗时较长，建议分批次运行

## 技术支持

如有问题，请参考：
- [火山引擎官方文档](https://www.volcengine.com/docs/82379/1399008)
- 项目 Issues

## License

MIT
