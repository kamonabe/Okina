# Okina（翁）システム仕様書

## 1. プロジェクト概要

**プロジェクト名**: Okina（翁）  
**目的**: ファームウェア・ソフトウェア更新の変化検知と通知  
**哲学**: 静かに見守り、前と違えば知らせ、判断は人に委ねる

## 2. システム設計原則

### 2.1 基本哲学
- Okinaは **主役ではない**
- Okinaは **判断しない**
- Okinaは **自動適用しない**
- Okinaは **人や運用を置き換えない**

### 2.2 責務分離
```
① 取得（サイト依存）        ← Input Provider
② 正規化アウトプット生成     ← Input Provider
③ 変化検知                 ← Okina
④ 差分抽出                 ← Okina
⑤ 通知                    ← Okina
```

## 3. 正規化データ仕様

### 3.1 フォーマット
- JSON Lines（`.jsonl`）
- 1行 = 1アイテム
- UTF-8エンコーディング

### 3.2 スキーマ（v1）
```json
{
  "schema": "okina.item.v1",
  "source": "fortinet-docs",
  "id": "fortinet:fortios:7.6.6:release",
  "type": "release",
  "title": "FortiOS 7.6.6 Release Notes",
  "version": "7.6.6",
  "url": "https://docs.fortinet.com/...",
  "observed_at": "2025-12-22T14:30:00+09:00",
  "payload": {
    "major": "7.6",
    "pdf_url": "https://..."
  }
}
```

### 3.3 必須フィールド
- `schema`: スキーマバージョン
- `source`: データソース識別子
- `id`: 一意識別子
- `type`: アイテムタイプ
- `title`: 人間が読める名前
- `url`: 参照URL
- `observed_at`: 観測日時（ISO 8601）

### 3.4 任意フィールド
- `version`: バージョン情報
- `payload`: 追加データ
- `content_hash`: 内容ハッシュ（差分検知高速化）

## 4. ID設計ルール

### 4.1 設計原則
- 同一の論理対象は常に同じID
- URL変更に極力影響されない
- 人間が見て意味が分かる

### 4.2 推奨形式
```
vendor:product:version:type
```

### 4.3 例
- `fortinet:fortios:7.6.6:release`
- `cisco:ios-xe:17.12.01:advisory`
- `vmware:vcenter:8.0.2:patch`

## 5. 処理フロー

### 5.1 メイン処理
1. 正規化データ（今回分）を読み込む
2. 前回データをロードする
3. 差分を検出する
   - 新規追加（added）
   - 削除（removed）
   - 内容変更（changed）
4. 差分があれば通知
5. 正常終了時のみ「今回データ」を保存

### 5.2 エラーハンドリング
以下は必ず通知する：
- 取得結果が0件
- 正規化データが読めない
- 前回データが存在しない
- 例外終了

## 6. 通知仕様

### 6.1 通知方針
- 通知先はSlack等（Webhook）
- 重要度分類はしない
- メンションは行わない
- 夜間通知は受信側の設定に委ねる

### 6.2 通知内容
- 種別（added / removed / changed）
- 件数
- 対象の要約（version / title / url）

## 7. 実行モデル

### 7.1 実行方式
- cron等による定期実行
- 想定頻度：1日1回〜毎時
- 検知頻度と通知の重要度は分離しない

### 7.2 コマンドライン
```bash
okina check                    # 変化検知実行
okina status                   # 状態確認
okina history                  # 履歴表示
okina config validate          # 設定検証
```

## 8. 非目標（明示）

以下は意図的に実装しない：
- 完全性の保証
- SLA
- ベンダー公式APIの代替
- 構成管理ツール（CM）への昇格
- 自動アップデート機能
- 重要度判定機能