# 台灣即時新聞 Dashboard

Dashboard: https://claude.ai/artifact/K2K3VGmSuknBGFqps6N8Nw

- `scrape_news.py` — 抓取 ETtoday、聯合新聞、聯合新聞網即時、LINE TODAY、三立、TVBS、中時的即時標題，輸出 `news.json`（每家最多 25 則）。
  `python3 news-dashboard/scrape_news.py /path/to/news.json`
- `index.html` — Dashboard 頁面原始碼（存在 artifact 的 `files/index.html`）。

更新流程：執行 scraper → 將 news.json 上傳為 artifact asset → 更新 `datasets/news` 的 `source.url`、`updated`。
