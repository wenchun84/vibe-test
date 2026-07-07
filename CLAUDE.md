# 專案說明

這個 repo 用於每日新聞追蹤自動化。

## 每日新聞追蹤

當使用者說「跑今日新聞追蹤」(或類似指令)時:

1. 切換到分支 `claude/daily-news-tracking-1gpgx1` 並 pull 最新
2. 完整依照 `daily-news-tracking/WORKFLOW.md` 的「每日自動流程」執行:掃描七家台灣媒體近 12 小時重要新聞、社群聲量掃描、用 Google Drive/Notion/Gmail 連接器自動讀取使用者的成效截圖與晨間筆記(位置與 ID 都在 WORKFLOW.md 中;連接器工具名稱前綴可能是隨機 UUID,用 ToolSearch 搜 drive / notion / gmail 載入)
3. 依模板產出報告寫入 `daily-news-tracking/reports/當天台北日期.md`,commit 並 push 到同一分支,不開 pull request
4. 回覆完整報告內容,並提醒使用者貼上 Perplexity 與新聞雷達 GPT 結果以整合「編輯會議最終版」
5. 全程用繁體中文回覆
