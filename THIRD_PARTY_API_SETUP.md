# 🔑 第三方 Claude API 配置指南

如果你使用第三方 Claude API 服务（而不是官方 Anthropic API），请按照以下步骤配置。

## 📝 你的 API 信息

根据你提供的信息：

- **API Base URL**: `https://code.newcli.com/claude`
- **API Key**: `sk-ant-oat01-W-If4jeJzaP2XuRzhq6onCFSNV1NstmXLSCuuWqV6LLMhxlT8F7Mv5Nl-DpypqNaPdO2pB9VHrV1ew3YL4KhAiJ1RuMO7AA`

## ⚙️ GitHub Secrets 配置

进入你的 GitHub 仓库：

1. 点击 `Settings`（设置）
2. 左侧菜单选择 `Secrets and variables` → `Actions`
3. 点击 `New repository secret`

### 必需配置的 Secrets

添加以下 **4 个** Secrets：

#### 1. ANTHROPIC_API_KEY
```
sk-ant-oat01-W-If4jeJzaP2XuRzhq6onCFSNV1NstmXLSCuuWqV6LLMhxlT8F7Mv5Nl-DpypqNaPdO2pB9VHrV1ew3YL4KhAiJ1RuMO7AA
```

#### 2. ANTHROPIC_BASE_URL
```
https://code.newcli.com/claude
```

#### 3. TIANAPI_KEY
```
4dfdf794141101d7bb8ece0294dbbc02
```
（项目已有的天行数据密钥，免费额度 100 次/天）

#### 4. SEARCH_API_KEY

你需要自己注册一个搜索 API：

**选项 A：SerpAPI（推荐）**
1. 访问 https://serpapi.com/
2. 注册账号
3. 在 Dashboard 复制 API Key
4. 免费配额：100 次搜索/月

**选项 B：Google Custom Search API**
1. 访问 https://console.cloud.google.com/
2. 创建项目并启用 Custom Search API
3. 创建凭据获取 API Key
4. 免费配额：100 次搜索/天

然后填入对应的 API Key。

---

## ✅ 配置完成检查清单

在推送代码到 GitHub 之前，确保：

- [ ] `ANTHROPIC_API_KEY` 已添加
- [ ] `ANTHROPIC_BASE_URL` 已添加（重要！）
- [ ] `TIANAPI_KEY` 已添加
- [ ] `SEARCH_API_KEY` 已添加
- [ ] 仓库权限设置为 "Read and write permissions"

## 🧪 测试配置

配置完成后：

1. 进入 `Actions` 标签
2. 选择 "Weibo Trends Analyzer" workflow
3. 点击 `Run workflow`
4. 选择分支为 `main`
5. 点击绿色的 `Run workflow` 按钮

等待约 5-10 分钟，查看是否成功生成报告。

## 🔍 验证第三方 API 是否生效

在 Actions 运行日志中，你应该看到：

```
✅ Using custom Claude API endpoint: https://code.newcli.com/claude
```

如果看到这行，说明第三方 API 配置成功！

## 💰 成本估算

使用第三方 API 后，成本取决于第三方服务的定价：

| 服务 | 成本 |
|------|------|
| 第三方 Claude API | 根据服务商定价 |
| 天行数据 API | 免费（100次/天） |
| SerpAPI | 免费（100次/月）或 $50/月 |
| GitHub Actions | 免费 |

**预估每月成本**：$0-50（取决于搜索 API 选择和第三方 Claude API 定价）

## ⚠️ 注意事项

1. **密钥安全**：
   - ❌ 永远不要将 API Key 提交到代码仓库
   - ✅ 只在 GitHub Secrets 中配置
   - ✅ 定期轮换密钥

2. **第三方服务可靠性**：
   - 确保第三方 API 服务稳定
   - 如果服务不稳定，考虑切换回官方 API

3. **合规性**：
   - 遵守第三方服务的使用条款
   - 不要滥用 API

## 🔄 切换回官方 API

如果想切换回 Anthropic 官方 API：

1. 进入 GitHub Secrets
2. 更新 `ANTHROPIC_API_KEY` 为官方密钥（`sk-ant-api03-...`）
3. **删除** `ANTHROPIC_BASE_URL` Secret
4. 重新运行 workflow

---

**配置完成后，参考主文档 [DEPLOYMENT.md](DEPLOYMENT.md) 继续部署流程！**
