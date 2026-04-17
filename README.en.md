# ScraDispage

> 📚 Distributed Crawler System | Scrapy + DrissionPage + Redis + AI Anti-Detection

---

## ⚠️ Project Declaration

**This is a personal practice project without version control.**

- 📌 This is a project for learning and practice purposes
- 📌 No version control system (e.g., Git) required
- 📌 **No need to notify the author** when using or modifying this project
- 📌 Can be directly modified and used in personal projects
- 📌 Code is for learning reference only

---

## 👤 Project Introduction

This is an **engineered distributed crawler system** that integrates Scrapy, DrissionPage, Redis, and machine learning technologies, with complete anti-crawling capabilities.

**Core Features:**
- ✅ Scrapy + DrissionPage hybrid rendering
- ✅ Redis distributed queue + automatic deduplication
- ✅ AI knowledge distillation anti-detection
- ✅ Redis proxy pool + automatic IP rotation
- ✅ PyQt5 graphical management interface

---

## 🚀 Quick Start

### One-click Start

```bash
# Windows
Double-click start.bat

# Or via command line
python start.py
```

### Manual Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python -m src.train

# 3. Start GUI
python -m src.gui

# Or start crawler directly
scrapy crawl demo_spider
```

---

## 📁 Project Structure

```
ScraDispage/
├── src/                              # Source code directory
│   ├── spider/                       # Scrapy spider module
│   │   ├── __init__.py
│   │   ├── settings.py               # Crawler configuration
│   │   ├── items.py                  # Data structures
│   │   ├── middlewares.py            # Anti-crawling middlewares
│   │   ├── pipelines.py              # Data pipelines
│   │   ├── spiders/                  # Spider scripts
│   │   │   ├── __init__.py
│   │   │   └── demo_spider.py        # Demo spider
│   │   └── proxy_pool/               # Proxy pool module
│   │       ├── __init__.py
│   │       └── manager.py            # Proxy pool manager
│   ├── train/                        # AI training module
│   │   ├── __init__.py
│   │   ├── train.py                  # Training program
│   │   └── data.json                 # Labeled data
│   ├── gui/                          # Graphical interface
│   │   ├── __init__.py
│   │   ├── main.py                   # Main interface
│   │   └── __main__.py               # Entry file
│   └── utils/                        # Utility modules
│       ├── __init__.py
│       └── redis_client.py           # Redis client (with mock support)
├── config/                           # Configuration files
│   └── settings.yaml                 # YAML configuration
├── models/                           # Trained models
│   └── anti_detect_model.pkl         # Anti-detection model
├── output/                           # Output data
├── logs/                             # Log files
├── tests/                            # Test files
│   └── test_spider.py                # Unit tests
├── scrapy.cfg                        # Scrapy configuration
├── requirements.txt                  # Dependencies
├── .env.example                      # Environment variables example
├── start.py                          # One-click start entry
├── start.bat                         # Windows start script
└── README.md                         # Project documentation
```

---

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming language |
| Scrapy | 2.11+ | Crawler framework |
| DrissionPage | 4.0+ | Browser rendering |
| Redis | 5.0+ | Distributed queue |
| scikit-learn | 1.3+ | Machine learning |
| PyQt5 | 5.15+ | Graphical interface |
| pydantic | 2.0+ | Data validation |

---

## 📖 Core Modules

### 1. Crawler Engine (`src/spider/`)
- **settings.py**: Global configuration (distributed + anti-crawling)
- **middlewares.py**: 8 anti-crawling middlewares
- **pipelines.py**: Redis + file dual storage
- **spiders/demo_spider.py**: Distributed spider example

### 2. Proxy Pool (`src/spider/proxy_pool/`)
- **manager.py**: Redis-based proxy pool management

### 3. AI Training (`src/train/`)
- **train.py**: Knowledge distillation training program
- **data.json**: Anti-detection labeled dataset

### 4. Graphical Interface (`src/gui/`)
- **main.py**: PyQt5 main interface

### 5. Utility Module (`src/utils/`)
- **redis_client.py**: Redis client (with mock mode support)

---

## 🎯 Anti-Crawling Middlewares

| Middleware | Function |
|------------|----------|
| UserAgentMiddleware | Random User-Agent rotation |
| HeadersMiddleware | Complete request header spoofing |
| CookieMiddleware | Cookie pool management |
| ProxyMiddleware | Automatic proxy rotation |
| FingerprintMiddleware | Device fingerprint generation |
| AntiDetectMiddleware | AI anti-detection |
| RetryMiddleware | Intelligent retry (exponential backoff) |
| DrissionPageMiddleware | Browser rendering |

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env`:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### Main Configuration Items

| Configuration | Default | Description |
|---------------|---------|-------------|
| CONCURRENT_REQUESTS | 16 | Number of concurrent requests |
| DOWNLOAD_DELAY | 2 | Download delay (seconds) |
| RETRY_TIMES | 3 | Number of retries |
| PROXY_ROTATE_INTERVAL | 10 | Proxy rotation interval |
| DRISSION_PAGE_HEADLESS | True | Headless browser mode |

---

## 🧪 Running Tests

```bash
python -m pytest tests/
```

---

## 💡 Learning Outcomes

Through this project, you will learn:
- ✅ Building engineered distributed crawler systems
- ✅ Implementing complete anti-crawling strategies
- ✅ Using Redis for task queues
- ✅ Training and deploying machine learning models
- ✅ Developing graphical management interfaces (PyQt5)

---

**Project Status**: Under active development 🚀