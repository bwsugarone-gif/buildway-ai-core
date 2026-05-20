# Buildway AI Core

**Buildway AI Core** 是一個通用 AI 工作流程底層框架，可用於多行業 AI 應用開發。

## 定位

本 repo 是 Buildway 旗下所有行業版本的共同核心，包括：

- 🏗️ **Construction** — 建築工地 AI 分析（HK-AICOS）
- 🤝 **CRM** — 客戶關係管理 AI
- 📄 **Document AI** — 文件智能處理

## 架構概覽

```
buildway-ai-core/
├── core/                    # 通用 AI 核心模組
│   ├── memory/              # Session 記憶管理
│   ├── rag/                 # RAG 文件檢索
│   ├── document_processing/ # 文件載入與解析
│   ├── ocr/                 # OCR 文字抽取
│   ├── agents/              # Agent 路由框架
│   ├── workflow/            # 工作流程工具
│   ├── actions/             # Action 追蹤
│   ├── reports/             # PDF 報告生成
│   └── security/            # 安全層（佔位）
│
├── verticals/               # 行業垂直模組
│   ├── construction/        # 建築行業（HK-AICOS）
│   ├── crm/                 # 客戶關係管理
│   └── document_ai/         # 文件 AI
│
├── apps/                    # 應用層
│   ├── streamlit_demo/      # Streamlit Demo App
│   └── api_server/          # API Server（佔位）
│
├── docs/                    # 文件
└── tests/                   # 測試
```

## 技術規格

- Python 3.11.x
- Streamlit（Demo App）
- ReportLab（PDF 生成）
- pypdf / pytesseract（文件處理）
- Anthropic / OpenAI（LLM）

## 快速開始

```bash
# 安裝依賴
pip install -r requirements.txt

# 運行 Demo App
cd apps/streamlit_demo
streamlit run app.py
```

## 版本

- v0.1.0 — 初始架構拆分（從 HK-AICOS 抽出通用核心）

## 授權

Buildway Tech (HK) Limited — 內部使用
