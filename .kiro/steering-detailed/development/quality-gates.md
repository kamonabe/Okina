# 品質ゲート標準ガイド

## 🎯 目的
開発プロセスの各段階で品質を保証するゲートを定義し、
一貫した高品質なソフトウェア開発を実現する。

## 🚪 品質ゲート一覧

### 1. コミット前ゲート（Pre-commit Gate）
```yaml
pre_commit_gate:
  trigger: "git commit"
  automated: true
  blocking: true
  
  checks:
    code_formatting:
      tool: "black"
      requirement: "100% compliance"
      auto_fix: true
    
    import_sorting:
      tool: "isort"
      requirement: "100% compliance"
      auto_fix: true
    
    linting:
      tool: "flake8"
      requirement: "0 errors"
      auto_fix: false
    
    type_checking:
      tool: "mypy"
      requirement: "0 errors"
      auto_fix: false
    
    secrets_scan:
      tool: "custom"
      requirement: "0 secrets detected"
      auto_fix: false
    
    basic_tests:
      tool: "pytest"
      requirement: "fast tests pass"
      timeout: "30 seconds"
```

### 2. プルリクエストゲート（PR Gate）
```yaml
pr_gate:
  trigger: "pull request creation/update"
  automated: true
  blocking: true
  
  checks:
    full_test_suite:
      requirement: "all tests pass"
      timeout: "10 minutes"
      retry_count: 1
    
    code_coverage:
      requirement: "≥ 90% overall, ≥ 80% new code"
      tool: "pytest-cov"
      report_format: "html"
    
    security_scan:
      tools: ["bandit", "safety", "pip-audit"]
      requirement: "0 high/critical issues"
    
    documentation:
      requirement: "docstrings for new public APIs"
      tool: "custom"
    
    spec_consistency:
      requirement: "specs updated if needed"
      tool: "custom"
    
    performance_regression:
      requirement: "no significant regression"
      threshold: "20% slowdown"
      baseline: "main branch"
  
  manual_checks:
    code_review:
      requirement: "≥ 1 approval from code owner"
      reviewers: ["tech_lead", "senior_dev"]
    
    design_review:
      requirement: "architecture approval for major changes"
      trigger: "files_changed > 10 OR new_modules > 0"
```

### 3. リリース前ゲート（Pre-release Gate）
```yaml
pre_release_gate:
  trigger: "release branch creation"
  automated: true
  blocking: true
  
  checks:
    comprehensive_testing:
      unit_tests: "100% pass"
      integration_tests: "100% pass"
      property_tests: "100% pass"
      performance_tests: "within SLA"
    
    quality_metrics:
      code_coverage: "≥ 95%"
      complexity_score: "≤ 10 average"
      maintainability_index: "≥ 70"
      technical_debt_ratio: "≤ 5%"
    
    security_validation:
      vulnerability_scan: "0 high/critical"
      dependency_audit: "all up-to-date"
      secrets_scan: "0 detected"
      license_compliance: "100%"
    
    documentation_completeness:
      changelog_updated: true
      version_bumped: true
      api_docs_current: true
      user_guide_updated: true
    
    spec_validation:
      all_specs_completed: true
      traceability_verified: true
      acceptance_criteria_met: true
  
  manual_checks:
    stakeholder_approval:
      product_owner: "required"
      tech_lead: "required"
      security_officer: "required for security changes"
    
    deployment_readiness:
      rollback_plan: "documented"
      monitoring_setup: "verified"
      support_documentation: "updated"
```

### 4. 本番デプロイゲート（Production Gate）
```yaml
production_gate:
  trigger: "production deployment"
  automated: true
  blocking: true
  
  pre_deployment:
    environment_validation:
      infrastructure_ready: true
      dependencies_available: true
      configuration_validated: true
    
    final_testing:
      smoke_tests: "100% pass"
      canary_deployment: "successful"
      rollback_test: "verified"
    
    monitoring_setup:
      alerts_configured: true
      dashboards_updated: true
      logging_verified: true
  
  post_deployment:
    health_checks:
      application_responsive: true
      all_endpoints_healthy: true
      performance_within_sla: true
    
    monitoring_validation:
      metrics_flowing: true
      alerts_functional: true
      logs_accessible: true
    
    business_validation:
      core_functionality: "verified"
      user_acceptance: "confirmed"
      performance_acceptable: true
```

## 🔧 ゲート実装

### 自動化スクリプト
```python
# scripts/quality_gates.py
from enum import Enum
from typing import Dict, List, Optional, Tuple
import subprocess
import json

class GateResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"

class QualityGate:
    """品質ゲートの基底クラス"""
    
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.results: List[Tuple[str, GateResult, str]] = []
    
    def run_check(self, check_name: str, command: str) -> GateResult:
        """個別チェックを実行"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=self.config.get('timeout', 300)
            )
            
            if result.returncode == 0:
                self.results.append((check_name, GateResult.PASS, result.stdout))
                return GateResult.PASS
            else:
                self.results.append((check_name, GateResult.FAIL, result.stderr))
                return GateResult.FAIL
                
        except subprocess.TimeoutExpired:
            self.results.append((check_name, GateResult.FAIL, "Timeout"))
            return GateResult.FAIL
        except Exception as e:
            self.results.append((check_name, GateResult.FAIL, str(e)))
            return GateResult.FAIL
    
    def generate_report(self) -> Dict:
        """ゲート実行結果のレポートを生成"""
        pass_count = sum(1 for _, result, _ in self.results if result == GateResult.PASS)
        fail_count = sum(1 for _, result, _ in self.results if result == GateResult.FAIL)
        
        return {
            "gate_name": self.name,
            "total_checks": len(self.results),
            "passed": pass_count,
            "failed": fail_count,
            "success_rate": pass_count / len(self.results) if self.results else 0,
            "overall_result": "PASS" if fail_count == 0 else "FAIL",
            "details": [
                {
                    "check": check,
                    "result": result.value,
                    "message": message
                }
                for check, result, message in self.results
            ]
        }

class PreCommitGate(QualityGate):
    """コミット前品質ゲート"""
    
    def run(self) -> bool:
        """pre-commitゲートを実行"""
        checks = [
            ("code_formatting", "black --check src/ tests/"),
            ("import_sorting", "isort --check-only src/ tests/"),
            ("linting", "flake8 src/ tests/"),
            ("type_checking", "mypy src/"),
            ("secrets_scan", "python scripts/scan_secrets.py"),
            ("fast_tests", "pytest tests/ -m 'not slow' --tb=short")
        ]
        
        all_passed = True
        for check_name, command in checks:
            result = self.run_check(check_name, command)
            if result == GateResult.FAIL:
                all_passed = False
        
        return all_passed

class PRGate(QualityGate):
    """プルリクエスト品質ゲート"""
    
    def run(self) -> bool:
        """PRゲートを実行"""
        checks = [
            ("full_test_suite", "pytest tests/ -v"),
            ("code_coverage", "pytest --cov=src --cov-fail-under=90"),
            ("security_scan", "bandit -r src/ && safety check"),
            ("spec_consistency", "python scripts/check_spec_consistency.py"),
            ("performance_test", "pytest tests/performance/ --benchmark-only")
        ]
        
        all_passed = True
        for check_name, command in checks:
            result = self.run_check(check_name, command)
            if result == GateResult.FAIL:
                all_passed = False
        
        return all_passed

class ReleaseGate(QualityGate):
    """リリース前品質ゲート"""
    
    def run(self) -> bool:
        """リリースゲートを実行"""
        checks = [
            ("comprehensive_testing", "pytest tests/ --cov=src --cov-fail-under=95"),
            ("security_validation", "python scripts/comprehensive_security_scan.py"),
            ("documentation_check", "python scripts/validate_documentation.py"),
            ("spec_validation", "python scripts/validate_all_specs.py"),
            ("performance_regression", "python scripts/check_performance_regression.py")
        ]
        
        all_passed = True
        for check_name, command in checks:
            result = self.run_check(check_name, command)
            if result == GateResult.FAIL:
                all_passed = False
        
        return all_passed
```

### GitHub Actions統合
```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  pre-commit-gate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run Pre-commit Gate
      run: |
        python scripts/quality_gates.py --gate pre-commit
    
    - name: Upload Gate Report
      uses: actions/upload-artifact@v3
      with:
        name: pre-commit-gate-report
        path: reports/pre-commit-gate.json

  pr-gate:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run PR Gate
      run: |
        python scripts/quality_gates.py --gate pr
    
    - name: Comment PR with Results
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = JSON.parse(fs.readFileSync('reports/pr-gate.json'));
          
          const comment = `## 🚪 品質ゲート結果
          
          **総合結果**: ${report.overall_result === 'PASS' ? '✅ PASS' : '❌ FAIL'}
          **成功率**: ${(report.success_rate * 100).toFixed(1)}% (${report.passed}/${report.total_checks})
          
          ### 詳細結果
          ${report.details.map(d => 
            `- ${d.result === 'pass' ? '✅' : '❌'} ${d.check}: ${d.message}`
          ).join('\n')}`;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

## 📊 ゲート品質メトリクス

### 追跡指標
```yaml
gate_metrics:
  effectiveness:
    defect_escape_rate: "< 2%"  # ゲートを通過した欠陥の割合
    false_positive_rate: "< 5%"  # 誤検知の割合
    gate_pass_rate: "> 85%"     # ゲート通過率
  
  efficiency:
    average_gate_time: "< 10 minutes"
    automation_coverage: "> 90%"
    manual_intervention_rate: "< 10%"
  
  adoption:
    gate_bypass_rate: "< 1%"    # ゲート迂回率
    developer_satisfaction: "> 4.0/5"
    process_compliance: "> 95%"
```

### レポートダッシュボード
```python
# scripts/gate_dashboard.py
def generate_gate_dashboard():
    """品質ゲートダッシュボードを生成"""
    
    # 過去30日のゲート実行結果を収集
    gate_history = collect_gate_history(days=30)
    
    # メトリクス計算
    metrics = calculate_gate_metrics(gate_history)
    
    # HTMLダッシュボード生成
    dashboard_html = f"""
    <div class="gate-dashboard">
        <h2>品質ゲート ダッシュボード</h2>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>ゲート通過率</h3>
                <div class="metric-value">{metrics['pass_rate']:.1f}%</div>
                <div class="trend">{'↗' if metrics['pass_rate_trend'] > 0 else '↘'}</div>
            </div>
            
            <div class="metric-card">
                <h3>平均実行時間</h3>
                <div class="metric-value">{metrics['avg_time']:.1f}分</div>
                <div class="trend">{'↗' if metrics['time_trend'] > 0 else '↘'}</div>
            </div>
        </div>
        
        <div class="charts-section">
            <canvas id="gate-success-trend"></canvas>
            <canvas id="gate-time-distribution"></canvas>
        </div>
    </div>
    """
    
    return dashboard_html
```

## 🎯 適用プロジェクト

- ✅ Komon（既存CI/CDを品質ゲート化）
- ✅ Okina（新規導入）
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 最高（品質保証の要）