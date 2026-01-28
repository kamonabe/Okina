# Okina ステアリングルール

## 📁 ファイル構成

### 共通ルール（ワークスペースレベル）
以下のルールは `../../../.kiro/steering/` から自動同期：
- `essential-rules.md`: 必須ルール
- `development-standards.md`: 開発標準
- `git-ssh-setup.md`: Git/SSH設定

### Okina固有ルール
- `okina-customizations.md`: Okina固有のカスタマイズ
- `development-workflow.md`: Okina開発ワークフロー

---

## 🔗 ルールの参照方法

Kiroは自動的にワークスペースレベルのルールを読み込みます。
プロジェクト固有のルールは追加で読み込まれます。

### 読み込み順序
```
1. ワークスペース/.kiro/steering/essential-rules.md
2. ワークスペース/.kiro/steering/development-standards.md
3. ワークスペース/.kiro/steering/git-ssh-setup.md
4. Okina/.kiro/steering/okina-customizations.md
5. Okina/.kiro/steering/development-workflow.md
```

---

## 📝 ルール追加時の注意

新しいルールを追加する場合：

### 全プロジェクト共通のルール
1. `../../../.kiro/steering/` に追加
2. 同期スクリプトを実行:
   ```bash
   ../../../.kiro/scripts/sync-steering-rules.sh
   ```

### Okina固有のルール
1. このディレクトリに直接追加
2. ファイル名は `okina-*.md` を推奨
3. 同期スクリプトの対象外なので自由に編集可能

---

## ⚠️ 編集してはいけないファイル

以下のファイルは**直接編集しないでください**（同期で上書きされます）:
- `essential-rules.md`
- `development-standards.md`
- `git-ssh-setup.md`

これらを変更したい場合は、ワークスペースルートの `.kiro/steering/` にあるマスターファイルを編集してください。

---

## 🔄 同期の仕組み

### 自動同期
管理者がワークスペースルートの共通ルールを更新すると、同期スクリプトが実行され、各プロジェクトに自動的に反映されます。

### 手動同期
開発者は `git pull` するだけで最新のルールが取得できます。

---

## 🎯 Okina開発者へ

### 開発環境
Okinaプロジェクトフォルダをルートとして開発してください：
```bash
cd Okina
# ここで開発作業
```

### ルールの確認
```bash
# 共通ルールを確認
cat .kiro/steering/essential-rules.md

# Okina固有ルールを確認
cat .kiro/steering/okina-customizations.md
```

### 最新ルールの取得
```bash
git pull
# 共通ルールも自動的に最新になります
```

---

## 📚 関連ドキュメント

- [ワークスペース管理スクリプト](../../../.kiro/scripts/README.md)
- [Okina固有のカスタマイズ](okina-customizations.md)
- [Okina開発ワークフロー](development-workflow.md)

---

**最終更新**: 2025-01-28
**管理者**: kamonabe
