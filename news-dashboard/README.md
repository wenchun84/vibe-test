# 台灣即時新聞 Dashboard

Dashboard: https://claude.ai/artifact/K2K3VGmSuknBGFqps6N8Nw

- `scrape_news.py` — 抓取 ETtoday、聯合新聞、聯合新聞網即時、LINE TODAY、三立、TVBS、中時的即時標題，輸出 `news.json`（每家最多 25 則）。
  `python3 news-dashboard/scrape_news.py /path/to/news.json`
- `index.html` — Dashboard 頁面原始碼（存在 artifact 的 `files/index.html`）。

更新流程：下載目前的 news.json（上一版）→ `scrape_news.py new.json prev.json`（合併、保留 24 小時）→ 上傳 new.json 為 artifact asset → 更新 `datasets/news` 的 `source.url`、`updated` → 刪除舊 asset。

## 公開網站（GitHub Pages）

`.github/workflows/news-site.yml` 每 15 分鐘：從線上網站讀回上一版 `news.json` → 執行 `scrape_news.py` 合併（保留 24 小時）→ `build_site.py` 用 `site/shell.html` 包住 `index.html` → 部署到 GitHub Pages。

需要在 repo 的 Settings → Pages → Build and deployment → Source 選 **GitHub Actions**，且 workflow 要在 `main` 分支上才會依排程執行。
