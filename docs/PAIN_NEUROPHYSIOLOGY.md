# Pain & Neurophysiology 個人設定

本 fork 新增 `pain_neurophysiology` profile，供疼痛、偏頭痛與神經生理研究的文獻初篩使用。
這是設定與檢索策略的第一版，尚未以實際文獻集合評估召回率或精確率，也不是系統性回顧搜尋策略。

## 第一版範圍

| 分類 | 內容與範圍 |
|---|---|
| 疼痛神經科學 | 痛覺傳入、中樞敏感化、疼痛調節、痛覺過敏與觸誘發痛 |
| 偏頭痛與頭痛 | migraine、headache、三叉血管系統與皮質擴散性去極化 |
| 神經生理與 EEG | EEG／神經振盪，搭配疼痛、體感、連結、coherence、PSD、靜息態或 ERP |
| 神經調節 | 正中神經／周邊神經刺激、TENS、tDCS、tACS、TMS、VNS 等完整術語，搭配疼痛、頭痛、復健或體感 |
| QST 與感覺處理 | 定量感覺測試、CPM、疼痛時間加成、壓痛／熱痛／機械痛閾值與感覺分型 |
| 復健與物理治療 | 物理治療、復健、運動治療、疼痛神經科學教育與漸進式動作意象，搭配疼痛或頭痛 |

所有查詢與 relevance terms 都位於 `config/radar_master.json` 的
`stream_routing.pain_reader_*`，不依賴 legacy query catalog。
查詢使用 Title/Abstract 欄位；Europe PMC adapter 會轉成 TITLE_ABS。
除 EEG 外，第一版優先使用完整術語，避免 MNS、CPM 等縮寫的跨領域歧義；
這也可能漏掉只寫縮寫的紀錄，首次實際執行後應檢視並調整。
未限定年齡、人類研究、研究設計、期刊或 OA，保留機制研究與方法研究。

## 來源、篇數與輸出

- 搜尋來源：PubMed、Europe PMC。兩者重疊紀錄沿用既有 publication identity 去重。
- 原始來源核實：沿用 `publisher` 有界核實來源。摘要或 OA 標記不等於全文已取得。
- 精選目標：每類 3 篇、最多 5 篇；合計目標 18 篇、最多 30 篇。
  精選是閱讀數量目標，不是保證；不足時不補足，完整候選紀錄仍保留。
- 每次查詢沿用 40 筆設定與既有分頁／截斷紀錄；不宣稱窮盡檢索。
- 沿用原始 verification limits：publisher 目標 10 次、最多 15 次、每 domain 最多 2 次。
- 沿用繁體中文標題與導覽摘要，保留英文原標題及可追溯來源。
- 沿用原始 daily 模式的 72 小時事件窗與 Asia/Tokyo 時區；尚未新增每週模式或排程。
  台灣比此時區慢一小時，閱讀報告時應留意時間標示。

分類以研究問題為主；跨領域論文可能符合多組查詢，仍需去重與人工檢視分類。
`min_relevance: 54` 是既有 metadata ranking 的初步路由門檻，
使具識別碼且摘要含一個明確術語的紀錄不會僅因缺乏 OA 加分被排除；
這個分數不是證據品質或治療效果的評分。

## 如何使用

本修改新增獨立 profile；未指定 profile 時仍會選到原作者的 `owner_daily`。
請在後續執行要求中明確指定：

```text
使用 yw-arch/EvidenceRadar 中包含個人化修改的已驗證 Work Pack，
選擇 profile_id: pain_neurophysiology，以 daily 模式執行。
完成來源搜尋、核實、繁中摘要、State 去重、canonical rendering 與完整 validation，
交付 HTML、State、Evidence、Run 四個檔案。
若 Work Pack 未包含這個 profile，請回報版本不符，不要改用 owner_daily。
```

第一次執行前，需由包含本修改的 source commit 重新建置並完成正式 Work Pack
發布與 provenance 驗證；原作者或修改前的 latest Release 不會自動包含本 profile。
本次建立設定不等於已執行文獻搜尋，也不會啟動 GitHub Actions、公開報告或自動排程。

維護者可先驗證與建置：

```sh
python3 -m unittest tests.test_pain_neurophysiology tests.test_radar_control tests.test_default_profile
python3 tools/build_work_pack.py --output-dir dist
```

本地建置通過不等於已完成簽署發布。請依 `docs/WORK_SETUP.md` 完成正式 package 驗證。
該文件的下載與簽署範例指向 upstream；本 fork 的正式版本必須改用
`yw-arch/EvidenceRadar` 的 Release，並將 attestation 的 `--repo` 設為
`yw-arch/EvidenceRadar`、`--signer-workflow` 設為
`yw-arch/EvidenceRadar/.github/workflows/work-pack-release.yml`，確保驗證的是本 fork。

## 保留的研究治理

搜尋、實際內容存取與 claim verification 保持分開；所有 source CHECK、executor
receipts、claim/source/locator binding、事件窗、State 去重與 fail-closed validators
皆沿用既有實作。Profile 不新增臨床結論，也不把分類或翻譯升格為已核實證據。
