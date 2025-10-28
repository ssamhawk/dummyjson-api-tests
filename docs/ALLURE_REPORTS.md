# Allure Reports Guide

## 📊 Where to Find Allure Reports

### Option 1: GitHub Actions Artifacts (Current Setup)

After each CI/CD run, Allure reports are available as artifacts:

1. Go to your GitHub repository: https://github.com/ssamhawk/dummyjson-api-tests
2. Click on **Actions** tab
3. Select the latest workflow run
4. Scroll down to **Artifacts** section
5. Download:
   - **allure-results** - Raw test data
   - **allure-report** - HTML report (download and open `index.html`)

**Note:** Artifacts are stored for 30 days.

### Option 2: GitHub Pages (Recommended)

For easier access, enable GitHub Pages deployment:

#### Setup Steps:

1. **Enable GitHub Pages in repository settings:**
   ```
   Repository → Settings → Pages
   Source: Deploy from a branch
   Branch: gh-pages / (root)
   ```

2. **Use the enhanced workflow:**
   - File: `.github/workflows/test-with-pages.yml`
   - This workflow automatically deploys reports to GitHub Pages
   - Each run creates a persistent, accessible report

3. **Access reports:**
   ```
   https://ssamhawk.github.io/dummyjson-api-tests/
   ```

#### Workflow Differences:

| Feature | test.yml | test-with-pages.yml |
|---------|----------|---------------------|
| Artifacts | ✅ Yes | ✅ Yes |
| GitHub Pages | ❌ No | ✅ Yes |
| History | ❌ No | ✅ Last 20 runs |
| Direct URL | ❌ No | ✅ Yes |

### Option 3: Local Reports

When running tests locally:

```bash
# Generate and open Allure report
uv run python tools/run_with_allure.py dummyjson/tests/api/test_assignment.py --open
```

**Local report location:**
```
allure-report/YYYY-MM-DD/HH-MM-SS/index.html
```

## 🔧 Advanced Configuration

### Custom Report Retention

Modify workflow to keep more/fewer reports:

```yaml
- name: Allure Report action
  uses: simple-elf/allure-report-action@master
  with:
    keep_reports: 20  # Change this number
```

### Slack/Teams Notifications

Add notification step to workflow:

```yaml
- name: Send notification
  if: always()
  run: |
    curl -X POST YOUR_WEBHOOK_URL \
      -H 'Content-Type: application/json' \
      -d '{"text":"Tests completed: ${{ job.status }}"}'
```

## 📈 Report Features

Allure reports include:

- ✅ Test execution summary
- 📊 Test trend graphs (with history)
- 🔍 Detailed test steps with screenshots
- ⏱️ Execution time breakdown
- 📋 Categorized failures
- 🏷️ Test tags and features
- 📎 Attachments (logs, API responses)

## 🚀 Quick Access URLs

After enabling GitHub Pages:

- **Latest Report:** https://ssamhawk.github.io/dummyjson-api-tests/
- **Specific Run:** https://ssamhawk.github.io/dummyjson-api-tests/{run_number}
- **Repository:** https://github.com/ssamhawk/dummyjson-api-tests
- **Actions:** https://github.com/ssamhawk/dummyjson-api-tests/actions

## 🛠️ Troubleshooting

### Report not generated?

Check workflow logs:
```
Actions → Latest run → test job → Generate Allure report step
```

### Can't access GitHub Pages?

1. Verify Pages is enabled in Settings
2. Check `gh-pages` branch exists
3. Wait 1-2 minutes after deployment
4. Clear browser cache

### Empty report?

Ensure tests ran successfully:
```bash
# Run locally to debug
uv run pytest dummyjson/tests/api/test_assignment.py -v --alluredir=allure-results
```
