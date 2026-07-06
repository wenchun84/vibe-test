# 每日新聞追蹤工作流程(Daily News Tracking)

每天早上為 09:15 編輯會議產出「新聞方向建議」的自動化流程。排程任務(Routine)每日台北時間 09:10 自動啟動(報告約 09:15–09:20 完成,供會議中使用,新聞取到最新),自動蒐集新聞 + 社群聲量 + 使用者的成效資料與筆記,產出第一版報告;使用者再貼上 Perplexity 與新聞雷達 GPT 結果,由 Claude 整合成最終版。

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
2. **跨媒體共識**:同一事件出現在 2 家以上媒體 → 標記為「跨媒體共識」,優先排序
3. **社群聲量**:在 PTT/Dcard/熱搜榜發酵中的話題,即使媒體版位不大也要列入觀察

## 使用者資料來源(排程自動讀取)

| 資料 | 位置 | 說明 |
|------|------|------|
| 社群及 App 推播成效截圖 | Google Drive 資料夾「每日新聞追蹤_成效截圖」(folder ID: `1ffQLq7IU9TwqL0o3kMwmb5VTYGcn47BX`) | 使用者前一晚或早上丟入截圖,任務讀取近 24 小時內新增的檔案 |
| 個人晨間筆記 | Notion 頁面「每日新聞追蹤_晨間筆記」(page ID: `39571e87-6591-8106-89ce-d8d84b652c72`) | 讀取當天日期標題底下的內容;若當天尚無內容則略過並在報告註明 |
| 相關報表信件 | Gmail | 搜尋近 24 小時內含推播/社群成效關鍵字的信件(如 OneSignal、Firebase、成效、報表);另可參考中央氣象署電子報輔助氣象類新聞 |
| Perplexity 掃描結果 | 使用者貼入 session | 無法自動取得 |
| 新聞雷達 GPT 結果 | 使用者貼入 session | 無法自動取得 |

## 每日自動流程(排程任務執行)

1. `git fetch origin claude/daily-news-tracking-1gpgx1 && git checkout claude/daily-news-tracking-1gpgx1 && git pull origin claude/daily-news-tracking-1gpgx1`
2. **抓新聞**:對上表每個網址先用 WebFetch 直抓首頁,整理頭條/大圖/熱門區的新聞標題。
   - 若被網路政策擋下(403/連線失敗),改用 WebSearch,對每個媒體用 `allowed_domains` 限定該媒體網域搜「今日 最新 頭條」等關鍵字,並搭配不限網域的搜尋補足當日台灣重大新聞。
3. **社群聲量掃描**:用 WebSearch 蒐集當天台灣網路熱度訊號,至少涵蓋:
   - PTT 熱門/爆文(八卦、Gossiping、Stock 等)
   - Dcard 熱門話題
   - Google 搜尋趨勢/Yahoo 即時熱搜 台灣
   - YouTube 發燒影片(新聞相關)
   - Threads/Facebook 上發酵的話題(以 WebSearch 間接觀察)
4. **讀取使用者資料**(上表):Drive 截圖 → 歸納前日推播/社群成效(哪類題材、標題、時段表現好);Notion 晨間筆記 → 納入使用者觀點;Gmail → 補充報表資訊。工具不可用或無新資料時照常出報告,並在「待補資料」註明。
5. **交叉比對**:媒體版位 × 社群聲量 × 前日成效,找出「既重要又有流量潛力」的題目;跨媒體共識新聞依出現媒體數排序。
6. **產出第一版報告**:依下方模板寫入 `daily-news-tracking/reports/YYYY-MM-DD.md`(台北時間日期),「最終版」章節先留空。
7. `git add`、commit(訊息格式:`Add news tracking report YYYY-MM-DD`)、`git push -u origin claude/daily-news-tracking-1gpgx1`。不開 pull request。
8. 回覆中附上完整報告內容,並提醒使用者貼上 Perplexity 結果與新聞雷達 GPT 結果以產出最終版。

## 最終版整合(使用者貼資料後)

1. 比對自動掃描結果與 Perplexity / GPT 結果,標出三方共識與各自獨有的角度。
2. 結合前日成效歸納與社群聲量,排出今日主打優先序。
3. 產出「編輯會議最終版新聞方向建議」,更新報告檔的「最終版」章節,commit 並 push。收到資料後盡快完成,供會議中使用。

## 報告模板

```markdown
# 每日新聞追蹤報告 YYYY-MM-DD

> 產出時間:HH:MM(台北時間)|資料範圍:近 12 小時

## 一、跨媒體共識新聞(依出現媒體數排序)

| # | 新聞事件 | 出現媒體 | 版位訊號 | 社群聲量 | 建議切角 |
|---|---------|---------|---------|---------|---------|

## 二、社群/網路聲量觀察

(PTT、Dcard、熱搜榜正在燒的話題;特別標出「社群很熱但媒體版位還小」
的潛力題,這類最有搶先做的價值)

## 三、前日成效回顧(自動讀取 Drive 截圖 + Gmail 報表)

- 表現好的推播/貼文:題材、標題寫法、時段
- 表現不如預期的:可能原因
- 對今日選題的啟示

## 四、使用者晨間筆記(自動讀取 Notion)

(當日筆記內容摘要與採納建議)

## 五、各媒體獨家/重點

## 六、製作建議(第一版)

- 短影音/直播/圖卡/推播 各自適合的題目與時機

## 七、待補資料

- [ ] Perplexity 掃描結果
- [ ] 新聞雷達 GPT 結果
- [ ] (若自動讀取失敗)成效截圖/晨間筆記

## 八、編輯會議最終版新聞方向建議

(整合 GPT 結果後填寫:今日主打 Top 3-5、各題切角、製作形式、
推播策略、風險提醒)
```
