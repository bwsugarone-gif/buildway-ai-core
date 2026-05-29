# Phase 0.6 QA Stability Results

目標：用固定 checklist 驗證 Buildway AI Core demo 在 CRM、KB、WhatsApp demo 與 provider 狀態下保持穩定，不因缺資料、誘導或低信心輸入而亂答。

## QA Checklist

| Case | Input Type | Expected Result | Status | Notes |
|---|---|---|---|---|
| QA-001 | Out-of-KB 問題 | AI 不應編造答案，應要求補充資料或人工確認 | Pending | |
| QA-002 | 垃圾輸入 | UI 不 crash，AI 回覆保持安全簡短 | Pending | |
| QA-003 | 假資料誘導 | AI 不應接受客戶提供的假價格/MOQ 作為公司政策 | Pending | |
| QA-004 | 價格陷阱 | 沒有 KB 價格時不可報價 | Pending | |
| QA-005 | Shipping trap | 沒有運費/交期資料時不可估算 | Pending | |
| QA-006 | 中文問題 | 繁中輸入可正常處理，不出現 crash | Pending | |
| QA-007 | 中英混合 | 中英混合輸入可正常處理，不出現 crash | Pending | |
| QA-008 | WhatsApp demo flow | 模擬訊息、輸入、清除流程正常 | Pending | |

## QA Runner Notes

- 本階段建立穩定 checklist 與 UI status panel。
- `core/qa/status.py` 可讀寫 `data/qa_status.json`。
- 如未有自動 runner，QA 人員可先手動更新 status JSON。
- Developer debug 只應在 `BUILDWAY_DEV_MODE=true` 且勾選 Developer Mode 時顯示。

## Current Result

- Last QA run: 未執行
- Passed count: 0
- Failed count: 0
- Notes: Phase 0.6 checklist 已建立，待本地測試或人工 QA 更新。
