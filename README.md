# ScraDispage

> 📚 分布式爬虫系统 | Scrapy + DrissionPage + Redis + AI 反爬检测

---

## ⚠️ 项目声明

**本项目为个人练习项目，无版本控制。**

- 📌 这是一个用于学习和练习的项目
- 📌 无版本控制系统（如 Git）
- 📌 使用或修改本项目**无需向作者声明**
- 📌 可直接在个人项目中修改和使用
- 📌 代码仅供学习参考

---

## 👤 项目介绍

这是一个**工程化的分布式爬虫系统**，整合了 Scrapy、DrissionPage、Redis 和机器学习等技术，具备完整的反爬对抗能力。

**核心功能：**
- ✅ Scrapy + DrissionPage 混合渲染
- ✅ Redis 分布式队列 + 自动去重
- ✅ AI 知识蒸馏反爬检测
- ✅ Redis 代理池 + 自动换 IP
- ✅ PyQt5 图形化管理界面

---

## 🚀 快速开始

### 一键启动

```bash
# Windows
双击 start.bat

# 或命令行
python start.py
```

### 手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 训练模型
python -m src.train

# 3. 启动 GUI
python -m src.gui

# 或启动爬虫
scrapy crawl demo_spider
```

---

## 📁 工程化目录结构

```
ScraDispage/
├── src/                              # 源代码目录
│   ├── spider/                       # Scrapy 爬虫模块
│   │   ├── __init__.py
│   │   ├── settings.py               # 爬虫配置
│   │   ├── items.py                  # 数据结构
│   │   ├── middlewares.py            # 反爬中间件
│   │   ├── pipelines.py              # 数据管道
│   │   ├── spiders/                  # 爬虫脚本
│   │   │   ├── __init__.py
│   │   │   └── demo_spider.py        # 示例爬虫
│   │   └── proxy_pool/               # 代理池模块
│   │       ├── __init__.py
│   │       └── manager.py            # 代理池管理
│   ├── train/                        # AI 训练模块
│   │   ├── __init__.py
│   │   ├── train.py                  # 训练程序
│   │   └── data.json                 # 标注数据
│   ├── gui/                          # 图形化界面
│   │   ├── __init__.py
│   │   ├── main.py                   # 主界面
│   │   └── __main__.py               # 入口文件
│   └── utils/                        # 工具模块
│       ├── __init__.py
│       └── redis_client.py           # Redis客户端(含模拟)
├── config/                           # 配置文件
│   └── settings.yaml                 # YAML配置
├── models/                           # 训练好的模型
│   └── anti_detect_model.pkl         # 反爬检测模型
├── output/                           # 输出数据
├── logs/                             # 日志文件
├── tests/                            # 测试文件
│   └── test_spider.py                # 单元测试
├── scrapy.cfg                        # Scrapy配置
├── requirements.txt                  # 依赖清单
├── .env.example                      # 环境变量示例
├── start.py                          # 一键启动入口
├── start.bat                         # Windows启动脚本
└── README.md                         # 项目说明
```

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| Scrapy | 2.11+ | 爬虫框架 |
| DrissionPage | 4.0+ | 浏览器渲染 |
| Redis | 5.0+ | 分布式队列 |
| scikit-learn | 1.3+ | 机器学习 |
| PyQt5 | 5.15+ | 图形化界面 |
| pydantic | 2.0+ | 数据验证 |

---

## 📖 核心模块

### 1. 爬虫引擎 (`src/spider/`)
- **settings.py**: 全局配置（分布式+反爬）
- **middlewares.py**: 8大反爬中间件
- **pipelines.py**: Redis + 文件双存储
- **spiders/demo_spider.py**: 分布式爬虫示例

### 2. 代理池 (`src/spider/proxy_pool/`)
- **manager.py**: Redis代理池管理

### 3. AI训练 (`src/train/`)
- **train.py**: 知识蒸馏训练程序
- **data.json**: 反爬标注数据集

### 4. 图形化界面 (`src/gui/`)
- **main.py**: PyQt5主界面

### 5. 工具模块 (`src/utils/`)
- **redis_client.py**: Redis客户端（支持模拟模式）

---

## 🎯 反爬中间件

| 中间件 | 功能 |
|--------|------|
| UserAgentMiddleware | 随机User-Agent轮换 |
| HeadersMiddleware | 完整请求头伪装 |
| CookieMiddleware | Cookie池管理 |
| ProxyMiddleware | 代理自动轮换 |
| FingerprintMiddleware | 设备指纹生成 |
| AntiDetectMiddleware | AI反爬检测 |
| RetryMiddleware | 智能重试（指数退避） |
| DrissionPageMiddleware | 浏览器渲染 |

---

## ⚙️ 配置说明

### 环境变量

复制 `.env.example` 为 `.env`：

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 主要配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| CONCURRENT_REQUESTS | 16 | 并发请求数 |
| DOWNLOAD_DELAY | 2 | 下载延迟(秒) |
| RETRY_TIMES | 3 | 重试次数 |
| PROXY_ROTATE_INTERVAL | 10 | 代理轮换间隔 |
| DRISSION_PAGE_HEADLESS | True | 无头浏览器模式 |

---

## 🧪 运行测试

```bash
python -m pytest tests/
```

---

## 💡 学习收获

通过这个项目，你将学会：
- ✅ 构建工程化的分布式爬虫系统
- ✅ 实现完整的反爬对抗策略
- ✅ 使用 Redis 实现任务队列
- ✅ 训练和部署机器学习模型
- ✅ 开发图形化管理界面（PyQt5）