# PHASE 0.5D — UI/UX Polish QA Checklist

**Branch:** dev  
**Date:** 2026-05-27  
**Phase:** 0.5D — Full UI/UX Polish + WhatsApp Hotfix  

---

## QA Checklist

### A. Streamlit Chrome 隱藏

| 項目 | 狀態 | 備註 |
|---|---|---|
| `[data-testid="stToolbar"]` 隱藏 | ✅ 已加入 | app.py + whatsapp_demo.py |
| `[data-testid="stDecoration"]` 隱藏 | ✅ 已加入 | display: none !important |
| `[data-testid="stHeader"]` 隱藏 | ✅ 已加入 | display: none !important |
| `.stDeployButton` 隱藏 | ✅ 已加入 | display: none !important |
| `button[kind="header"]` 隱藏 | ✅ 已加入 | Fork / GitHub 按鈕 |
| `#MainMenu` 隱藏 | ✅ 已加入 | |
| `footer` 隱藏 | ✅ 已加入 | |
| `header` 隱藏 | ✅ 已加入 | |
| Sidebar navigation 不受影響 | ✅ 確認 | CSS 不影響 sidebar |
| config.toml toolbarMode = minimal | ✅ 已設定 | Phase 0.5C 已加入 |

**已知限制：**  
Streamlit 新版本可能更改 `data-testid` selector 名稱，導致 Fork/GitHub 按鈕重新出現。  
若仍可見，需以瀏覽器 DevTools 確認最新 selector 再更新 CSS。

---

### B. 全繁體中文化

| 頁面 | 項目 | 狀態 |
|---|---|---|
| Home | 標題、說明、3 個入口卡片按鈕 | ✅ 繁中 |
| Home (Dev Mode) | Login Portal、Platform Summary、Cost Model | ✅ 繁中（只在 Developer Mode 顯示） |
| Tenant 設定 | 所有 label、button | ✅ 繁中（透過 LABELS dict） |
| AI Model 設定 | 供應商、模型名稱、儲存、測試連線 | ✅ 繁中 |
| Database 設定 | 資料庫模式、URL、API Key | ✅ 繁中 |
| Knowledge Base | 上載文件、建立索引、搜尋知識庫、狀態 | ✅ 繁中 |
| CRM | 客戶訊息、生成 AI 回覆、清除、回覆草稿、複製回覆 | ✅ 繁中 |
| 使用記錄 | 表格標題、說明 | ✅ 繁中 |
| WhatsApp Demo | 所有 UI 文字 | ✅ 繁中（Phase 0.5C 已完成） |

---

### C. WhatsApp Demo

| 項目 | 狀態 | 備註 |
|---|---|---|
| UI 全繁體中文 | ✅ | 已確認 |
| Chat container 置中 | ✅ | max-width: 520px; margin: 0 auto |
| Desktop max-width ~520px | ✅ | .wa-container 設定 |
| Mobile width 100% | ✅ | @media (max-width: 600px) |
| 客戶 bubble 左邊 | ✅ | .wa-bubble-row-customer justify-content: flex-start |
| AI bubble 右邊 | ✅ | .wa-bubble-row-ai justify-content: flex-end |
| AI bubble 綠色 (#dcf8c6) | ✅ | .wa-bubble-ai background |
| 客戶 bubble 白色 (#ffffff) | ✅ | .wa-bubble-customer background |
| Timestamp 顯示 | ✅ | 每個 bubble 右下角 |
| AI 正在輸入... 動畫 | ✅ | _render_typing_indicator() |
| Loading spinner 發送時 | ✅ | st.spinner("AI 正在生成回覆...") |
| 清空對話 按鈕 | ✅ | |
| 發送 按鈕 | ✅ | |
| 模擬客戶訊息 按鈕 | ✅ | |
| 輸入訊息... placeholder | ✅ | |
| Toolbar CSS 隱藏 | ✅ | Phase 0.5D 新增 |

**預設模擬訊息：**
1. MOQ 幾多？ ✅
2. Shipping terms 係點？ ✅
3. 200 件可唔可以落單？ ✅
4. FOB 定 EXW？ ✅

---

### D. Knowledge Base

| 項目 | 狀態 | 備註 |
|---|---|---|
| 標題：Knowledge Base（公司知識庫） | ✅ | |
| 說明文字（上載 FAQ...） | ✅ | |
| Progress bar 在 indexing | ✅ | |
| Current file name 顯示 | ✅ | status_text.text(...) |
| indexed / failed / total chunks summary | ✅ | 4 欄 metric |
| Debug 只在 Developer Mode | ✅ | dev_mode gate |
| 單一文件失敗不中斷整批 | ✅ | try/except per file |

---

### E. Developer Mode Debug Gate

| 項目 | 狀態 |
|---|---|
| AI request debug JSON | ✅ 只在 dev_mode 顯示 |
| Retrieved KB Context (chunk ids, similarity, weighted score) | ✅ 只在 dev_mode 顯示 |
| KB indexing temp path debug | ✅ 只在 dev_mode 顯示 |
| KB indexing result debug | ✅ 只在 dev_mode 顯示 |
| Error traceback details | ✅ 只在 dev_mode 顯示 |
| Client mode 完全無 debug leak | ✅ |

---

### F. Core Logic 保護

| 項目 | 狀態 |
|---|---|
| core/rag/retriever.py 未修改 | ✅ |
| provider_router 未修改 | ✅ |
| Gemini provider 未修改 | ✅ |
| confidence logic 未修改 | ✅ |
| source weighting logic 未修改 | ✅ |

---

### G. 修改檔案清單

| 檔案 | 修改內容 |
|---|---|
| `apps/streamlit_demo/app.py` | 加強 CSS 隱藏、LABELS 擴展（繁中/簡中/英）、所有頁面繁中化、KB debug gate、CRM debug gate |
| `apps/streamlit_demo/pages/whatsapp_demo.py` | 加入 Streamlit chrome 隱藏 CSS |
| `apps/streamlit_demo/.streamlit/config.toml` | toolbarMode = minimal（Phase 0.5C） |
| `docs/PHASE_0_5D_UI_QA.md` | 本文件（新建） |

---

### H. 手動測試指引

1. **啟動 App：**
   ```
   cd buildway-ai-core/apps/streamlit_demo
   streamlit run app.py
   ```

2. **測試項目：**
   - [ ] 右上角無 Fork / GitHub / Deploy 按鈕
   - [ ] 所有頁面文字為繁體中文（預設語言）
   - [ ] Knowledge Base：上載 4 個文件，indexing 穩定完成
   - [ ] CRM：問「MOQ 幾多？」，生成回覆正常
   - [ ] WhatsApp Demo：問「FOB 定 EXW？」，bubble 正確顯示
   - [ ] 手機寬度（< 600px）：layout 不爆版
   - [ ] Developer Mode 開啟後：可見 debug expander
   - [ ] Developer Mode 關閉：無任何 debug / JSON 顯示
   - [ ] Sidebar navigation 正常運作

---

### I. 已知限制 / 後續工作

- Streamlit selector 可能在新版本更改，Fork/GitHub 按鈕需重新確認
- `st.page_link()` 跨頁跳轉需要正確的多頁架構（目前 whatsapp_demo 為 pages/ 子頁面）
- 手機 clipboard 複製功能將在 Phase 0.5 推出
- Customer Memory 欄位為 placeholder，Phase 1 接 Supabase
