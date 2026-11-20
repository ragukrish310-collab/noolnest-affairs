# NoolNest Current Affairs — zero-cost publisher

This public repository publishes a UTF-8 `current-affairs.json` feed for the NoolNest Android reader.

## One-time setup
1. In repository **Settings → Pages**, select **GitHub Actions** as the Build and deployment source.
2. The `Validate and publish NoolNest feed` workflow runs on changes to main (or can be triggered manually).
3. Once deployed, the feed URL is **https://ragukrish310-collab.github.io/noolnest-affairs/current-affairs.json**
4. In NoolNest Android: **Current Affairs → Feed settings**. Save the URL and refresh.

## Publishing an actual lesson
Edit `current-affairs.json` and add dated UPSC/TNPSC content, with full Tamil and English fields. The validation workflow rejects missing bilingual fields and malformed records. Verify every factual claim against authoritative primary sources; include source URLs and dates. Do **not** copy copyrighted articles wholesale or publish made-up daily news.

Each date requires both `upsc` and `tnpsc`, each with bilingual `title`, `summary`, `background`, `conclusion`, `modelEssay`. Optional bilingual arrays include `facts`, `outline`, `pros`, `cons`, `questions`. The app merges new records by date and stores an offline cache. This feed intentionally starts empty and does not automatically create or verify news.

## Privacy
This repository is **public**. Never place personal information, passwords, API keys, or private reading notes in feed files.
