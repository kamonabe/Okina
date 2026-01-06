# Okina固有カスタマイズ

## 🎭 プロジェクト哲学

### 翁（Okina）らしさ
```yaml
okina_philosophy:
  core_principle: "静かに見守り、変化を知らせ、判断は人に委ねる"
  behavior:
    - "主役ではない - あくまで補助的な存在"
    - "判断しない - 変化を知らせるだけ"
    - "自動適用しない - 自動更新は一切行わない"
    - "人や運用を置き換えない - 既存の運用を補完"
  
  messaging_tone:
    style: "静かで簡潔"
    approach: "事実のみを伝える"
    personality: "縁側に座って世界を見ている翁"
```

## 🔍 Okina固有の品質基準

### 変化検知精度
```yaml
change_detection_quality:
  accuracy: "≥ 99.5%"  # 変化検知の正確性
  false_positive_rate: "≤ 0.1%"  # 誤検知率
  false_negative_rate: "≤ 0.1%"  # 見逃し率
  processing_time: "≤ 1秒/1000アイテム"
```

### 通知品質
```yaml
notification_quality:
  message_clarity: "翁らしい静かで簡潔なメッセージ"
  delivery_reliability: "≥ 99.9%"
  response_time: "≤ 30秒"
  tone_consistency: "常に控えめで事実ベース"
```

### 差分抽出品質
```yaml
diff_analysis_quality:
  completeness: "全変化を漏れなく検出"
  categorization: "追加・削除・変更の正確な分類"
  content_preservation: "元データの完全性保持"
  performance: "大量データでも高速処理"
```

## 📋 Okina固有のテスト戦略

### 変化検知テスト
```python
# 翁らしさを検証するプロパティテスト
@given(st.lists(st.text(), min_size=1))
def test_okina_message_tone_property(items):
    """翁らしいメッセージトーンが保たれることを検証"""
    message = format_okina_message(items)
    
    # 翁らしさの検証
    assert is_quiet_and_humble(message)
    assert is_factual_only(message)
    assert not contains_judgment(message)
    assert not suggests_automatic_action(message)

@given(st.data())
def test_change_detection_accuracy(data):
    """変化検知の正確性を検証"""
    old_data = data.draw(generate_normalized_data())
    new_data = data.draw(modify_data(old_data))
    
    changes = detect_changes(old_data, new_data)
    
    # 検知精度の検証
    assert all_changes_detected(changes, old_data, new_data)
    assert no_false_positives(changes, old_data, new_data)
```

### 翁らしさテスト
```python
class TestOkinaBehavior:
    """翁らしい振る舞いのテスト"""
    
    def test_never_suggests_automatic_action(self):
        """自動アクションを提案しないことを確認"""
        message = generate_change_notification(sample_changes)
        assert "自動的に" not in message
        assert "自動更新" not in message
        assert "自動適用" not in message
    
    def test_always_defers_to_human_judgment(self):
        """常に人間の判断に委ねることを確認"""
        message = generate_change_notification(sample_changes)
        assert "確認してください" in message or "ご確認ください" in message
        assert not contains_recommendations(message)
    
    def test_quiet_and_humble_tone(self):
        """静かで控えめなトーンを確認"""
        message = generate_change_notification(sample_changes)
        assert is_humble_tone(message)
        assert not is_assertive_tone(message)
```

## 🎯 Okina固有のメトリクス

### 翁らしさメトリクス
```yaml
okina_metrics:
  message_tone_score: "翁らしさスコア (0-100)"
  humility_index: "控えめさ指数"
  factual_accuracy: "事実性の正確度"
  judgment_avoidance: "判断回避率"
  
  change_detection_metrics:
    precision: "検知精度"
    recall: "検知網羅率"
    f1_score: "総合検知品質"
    processing_efficiency: "処理効率"
```

## 🔧 Okina固有の設定

### メッセージテンプレート
```yaml
okina_message_templates:
  change_notification:
    prefix: "🏮 Okina（翁）からのお知らせ"
    tone: "静かで簡潔"
    format: "事実のみ、判断なし"
    suffix: "詳細は okina history で確認できます"
  
  error_notification:
    approach: "継続性を重視"
    message: "問題が発生しましたが、監視は継続しています"
    escalation: "重大な問題のみ人間に報告"
```

### 処理方針
```yaml
okina_processing:
  error_handling:
    philosophy: "完璧を求めず、継続性を重視"
    approach: "部分的な失敗でも可能な限り処理を継続"
    reporting: "エラーは記録するが、過度に警告しない"
  
  performance:
    priority: "正確性 > 速度"
    approach: "確実な処理を優先、速度は二の次"
    monitoring: "静かに見守る、過度な監視はしない"
```

## 📚 Okina固有のドキュメント

### 必須ドキュメント拡張
```yaml
okina_documentation:
  philosophy_guide: "翁の哲学と振る舞い指針"
  message_style_guide: "翁らしいメッセージ作成ガイド"
  change_detection_manual: "変化検知の仕組みと精度"
  integration_guide: "既存運用との統合方法"
```

## 🎯 適用範囲

この Okina 固有カスタマイズは以下に適用されます：

- ✅ 変化監視システム
- ✅ 差分抽出システム  
- ✅ 通知システム
- ✅ メッセージフォーマット
- ✅ エラーハンドリング
- ✅ ユーザーインターフェース

---

**最終更新**: 2025-01-06
**翁らしさ**: 最重要原則