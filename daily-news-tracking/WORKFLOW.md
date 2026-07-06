# 每日新聞追蹤工作流程(Daily News Tracking)

每天早上為編輯會議產出「新聞方向建議」的自動化流程。由排程任務(Routine)每日自動啟動,先產出第一版報告;使用者再貼上自己的資料(Perplexity 結果、推播成效截圖、個人筆記、新聞雷達 GPT 結果),由 Claude 整合成最終版。

## 監測媒體清單

| 媒體 | 網址 |
|------|------|
| ETtoday | https://www.ettoday.net/ |
| 聯合新聞網 | https://udn.com/news/index |
| 聯合新聞網(即時) | https://udn.com/news/breaknews/1 |
| LINE TODAY | https://today.line.me/tw/v3/tab |
| 三立新聞網 | https://www.setn.com/ |
| TVBS 新聞 | https://news.tvbs.com.tw/ |
| 中時新聞網 | https://www.chinatimes.com/realtimenews/?chdtv |

## 重要性判準

近 12 小時內,符合以下任一條件即列入:

1. **版位訊號**:有跑馬、掛大圖、當頭條、或在熱門新聞區佔重要版位
2. **跨媒體共識**:同一事件出現在 2 家以上媒體 → 標記為「跨媒體共識」,代表重要或有流量的新聞,優先排序

## 每日自動流程(排程任務執行)

1. `git checkout claude/daily-news-tracking-1gpgx1 && git pull origin claude/daily-news-tracking-1gpgx1`
2. **抓新聞**:對上表每個網址先用 WebFetch 直抓首頁,整理頭條/大圖/熱門區的新聞標題。
   - 若被網路政策擋下(403/連線失敗),改用 WebSearch,對每個媒體用 `allowed_domains` 限定該媒體網域搜「今日 最新 頭條」等關鍵字,並搭配不限網域的搜尋補足當日台灣重大新聞。
3. **交叉比對**:找出跨媒體共同出現的新聞,依出現媒體數排序。
4. **產出第一版報告**:依下方模板寫入 `daily-news-tracking/reports/YYYY-MM-DD.md`(台北時間日期),「最終版」章節先留空。
5. `git add`、commit(訊息格式:`Add news tracking report YYYY-MM-DD`)、`git push -u origin claude/daily-news-tracking-1gpgx1`。
6. 回覆中附上完整報告內容,並提醒使用者貼上以下資料以產出最終版:
   - Perplexity 跨媒體掃描結果
   - 前一天社群及 App 推播成效截圖
   - 自己早上看新聞寫的重點
   - 新聞雷達 GPT 的第一份追蹤與製作建議

## 最終版整合(使用者貼資料後)

收到使用者貼上的資料後:

1. 比對自動掃描結果與 Perplexity / GPT 結果,標出三方共識與各自獨有的角度。
2. 從推播成效截圖歸納:哪類題材、標題寫法、推播時段成效好,回饋到今日選題。
3. 納入使用者個人筆記的觀點。
4. 產出「編輯會議最終版新聞方向建議」,更新報告檔的「最終版」章節,commit 並 push。

## 報告模板

```markdown
# 每日新聞追蹤報告 YYYY-MM-DD

> 產出時間:HH:MM(台北時間)|資料範圍:近 12 小時

## 一、跨媒體共識新聞(依出現媒體數排序)

| # | 新聞事件 | 出現媒體 | 版位訊號 | 建議切角 |
|---|---------|---------|---------|---------|

## 二、各媒體獨家/重點

(每家媒體 1-3 則值得注意但未跨媒體的新聞)

## 三、製作建議(第一版)

- 短影音/直播/圖卡/推播 各自適合的題目與時機

## 四、待補資料

- [ ] Perplexity 掃描結果
- [ ] 前日社群與 App 推播成效截圖
- [ ] 使用者晨間筆記
- [ ] 新聞雷達 GPT 結果

## 五、編輯會議最終版新聞方向建議

(整合 GPT 結果與使用者資料後填寫:今日主打 Top 3-5、各題切角、
製作形式、推播策略、風險提醒)
```
