# Weibo Trends Analyzer - GitHub Actions 部署指南

## 📋 目录

1. [项目概述](#项目概述)
2. [前置准备](#前置准备)
3. [API密钥获取](#api密钥获取)
4. [GitHub仓库配置](#github仓库配置)
5. [部署步骤](#部署步骤)
6. [使用说明](#使用说明)
7. [故障排除](#故障排除)
8. [进阶配置](#进阶配置)

---

## 📖 项目概述

本项目将原有的 Claude Code Skill `weibo-trends-analyzer` 迁移到 GitHub Actions，实现云端定时自动分析微博热搜并生成创意产品报告。

### 核心特性

- ✅ **定时自动执行**：每天北京时间早上 9:00 自动运行
- ✅ **手动触发**：支持随时手动运行分析
- ✅ **AI 驱动分析**：使用 Claude Agent SDK 进行智能产品创意生成
- ✅ **自动提交报告**：生成的 HTML 报告自动提交到仓库
- ✅ **多搜索引擎支持**：支持 SerpAPI 或 Google Custom Search
- ✅ **完整错误处理**：API 失败时自动使用备用数据

---

## 🔧 前置准备

### 必需工具

- GitHub 账号
- 以下 API 密钥：
  - Anthropic API Key（Claude）
  - 天行数据 API Key（微博热搜）
  - SerpAPI Key 或 Google Custom Search API Key（Web 搜索）

---

## 🔑 API密钥获取

### 1. Anthropic API Key

**用途**：调用 Claude Agent SDK 进行 AI 分析

**获取步骤**：
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 点击 "Create Key" 创建新密钥
5. 复制密钥（格式：`sk-ant-...`）

**定价参考**：
- Claude 3.5 Sonnet：$3/M tokens (input), $15/M tokens (output)
- 每次分析约消耗 5-10K tokens，成本约 $0.05-0.15

**重要提示**：
- ⚠️ 请妥善保管密钥，不要提交到代码仓库
- ⚠️ 定期检查使用量，设置消费限额

### 2. 天行数据 API Key

**用途**：获取微博实时热搜数据

**获取步骤**：
1. 访问 [天行数据官网](https://www.tianapi.com/)
2. 注册账号并登录
3. 在控制台找到"微博热搜"接口
4. 复制 API Key

**当前可用密钥**：
```
4dfdf794141101d7bb8ece0294dbbc02
```
（这是项目中已有的密钥，如需更高配额可自行注册）

**免费配额**：
- 每日 100 次请求
- 实时数据更新

**注意事项**：
- ⚠️ 每次运行消耗 1 次请求
- ⚠️ 如需高频使用，考虑升级付费版

### 3. Web 搜索 API Key

#### 选项 A：SerpAPI（推荐）

**用途**：进行网页搜索，获取热搜话题背景信息

**获取步骤**：
1. 访问 [SerpAPI](https://serpapi.com/)
2. 注册账号
3. 在 Dashboard 复制 API Key

**免费配额**：
- 每月 100 次免费搜索
- 每次分析消耗约 20-30 次搜索（分析 10 个话题）

**定价**：
- Free: 100 searches/month
- Paid: $50/month (5000 searches)

#### 选项 B：Google Custom Search API

**获取步骤**：
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建项目并启用 Custom Search API
3. 创建凭据（API Key）
4. 创建自定义搜索引擎并获取 Search Engine ID

**免费配额**：
- 每天 100 次免费搜索
- 超出后需付费

**配置要求**：
- API Key
- Search Engine ID（需额外配置）

---

## ⚙️ GitHub仓库配置

### 步骤 1：创建 GitHub 仓库

1. 在 GitHub 创建新仓库（public 或 private 均可）
2. 建议仓库名：`weibo-trends-analyzer`

### 步骤 2：配置 GitHub Secrets

进入仓库设置：`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**必需配置的 Secrets**：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 | `sk-ant-api03-...` |
| `TIANAPI_KEY` | 天行数据 API 密钥 | `4dfdf794141101d7bb8ece0294dbbc02` |
| `SEARCH_API_KEY` | SerpAPI 或 Google API 密钥 | `your-serpapi-key` |

**可选配置的 Secrets**：

| Secret 名称 | 说明 | 默认值 |
|------------|------|--------|
| `SEARCH_ENGINE` | 搜索引擎类型 | `serpapi` |
| `GOOGLE_SEARCH_ENGINE_ID` | Google 自定义搜索引擎 ID（仅在使用 Google 时需要） | - |

### 步骤 3：配置仓库权限

确保 GitHub Actions 有写入权限：

1. 进入 `Settings` → `Actions` → `General`
2. 滚动到 "Workflow permissions"
3. 选择 **"Read and write permissions"**
4. 勾选 **"Allow GitHub Actions to create and approve pull requests"**
5. 点击 Save

---

## 🚀 部署步骤

### 方法 1：克隆并推送（推荐）

```bash
# 1. 克隆本地项目
cd /path/to/your/project

# 2. 初始化 Git（如果尚未初始化）
git init

# 3. 添加所有文件
git add .

# 4. 创建初始提交
git commit -m "Initial commit: Weibo Trends Analyzer with GitHub Actions"

# 5. 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/weibo-trends-analyzer.git

# 6. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 方法 2：直接上传

1. 将整个项目文件夹压缩为 ZIP
2. 在 GitHub 仓库页面点击 "Add file" → "Upload files"
3. 上传 ZIP 并解压

### 步骤验证

推送后，检查以下内容：

```
✅ .github/workflows/weibo-trends-analyzer.yml 存在
✅ scripts/weibo_analyzer.py 存在
✅ scripts/utils.py 存在
✅ scripts/templates/dashboard_template.html 存在
✅ requirements.txt 存在
✅ GitHub Secrets 已配置完成
```

---

## 📖 使用说明

### 自动执行

GitHub Actions 会在每天 **北京时间早上 9:00**（UTC 1:00）自动运行分析。

**查看执行状态**：
1. 进入仓库 → `Actions` 标签
2. 查看 "Weibo Trends Analyzer" workflow
3. 点击最近的运行记录查看详情

### 手动执行

如需立即运行分析：

1. 进入仓库 → `Actions` 标签
2. 点击 "Weibo Trends Analyzer" workflow
3. 点击右侧 "Run workflow" 按钮
4. （可选）调整分析数量（默认 10 个话题）
5. 点击绿色 "Run workflow" 确认

### 查看报告

生成的报告会自动提交到 `reports/` 目录：

**查看方式**：
1. **GitHub 网页查看**：
   - 进入 `reports/` 目录
   - 点击最新的 HTML 文件
   - 点击 "Raw" 查看原始文件
   - 复制链接到浏览器打开（或使用 GitHub Pages）

2. **下载查看**：
   - 进入 `Actions` → 点击运行记录
   - 滚动到底部 "Artifacts"
   - 下载 `weibo-trends-reports-XXX.zip`
   - 解压后在本地浏览器打开 HTML

3. **GitHub Pages 部署**（推荐）：
   - 进入 `Settings` → `Pages`
   - Source 选择 "main" 分支和 `/reports` 目录
   - 访问 `https://YOUR_USERNAME.github.io/weibo-trends-analyzer/weibo-trends-analysis-YYYY-MM-DD.html`

---

## 🔧 故障排除

### 问题 1：Workflow 运行失败

**可能原因**：
- API 密钥未配置或错误
- API 配额已用尽
- 网络连接问题

**解决方案**：
1. 检查 GitHub Secrets 配置是否正确
2. 查看 Actions 运行日志中的错误信息
3. 验证 API 密钥在对应平台是否有效
4. 检查 API 剩余配额

### 问题 2：报告未生成

**检查步骤**：
1. 查看 Actions 日志中的错误信息
2. 确认 Python 脚本执行成功
3. 检查 `reports/` 目录是否有新文件
4. 确认 Git 提交步骤是否成功

### 问题 3：Claude API 响应慢或超时

**原因**：Claude API 处理大量文本需要时间

**解决方案**：
- 减少分析话题数量（默认 10 个）
- 手动触发时设置 `analysis_limit` 为更小值（如 5）
- 检查 API 服务状态

### 问题 4：搜索 API 配额不足

**临时解决**：
- 脚本会自动使用 mock 数据作为备用
- 报告中会标记 "⚠️ 搜索结果受限"

**长期解决**：
- 升级 SerpAPI 付费计划
- 切换到 Google Custom Search API
- 减少分析频率（如每周运行 1 次）

### 问题 5：中文显示乱码

**原因**：编码问题

**解决方案**：
- 确保浏览器使用 UTF-8 编码打开
- 检查 HTML 文件开头是否有 `<meta charset="UTF-8">`
- 使用现代浏览器（Chrome、Firefox、Safari）

---

## 🎯 进阶配置

### 调整定时执行时间

编辑 `.github/workflows/weibo-trends-analyzer.yml`：

```yaml
on:
  schedule:
    # 每天北京时间 21:00 (UTC 13:00)
    - cron: '0 13 * * *'

    # 每周一、三、五 9:00 (UTC 1:00)
    # - cron: '0 1 * * 1,3,5'

    # 每小时运行（不推荐，API 配额消耗快）
    # - cron: '0 * * * *'
```

**Cron 语法**：
```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日期 (1 - 31)
│ │ │ ┌───────────── 月份 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 6) (0=Sunday)
│ │ │ │ │
* * * * *
```

**时区转换**：
- 北京时间 = UTC + 8
- 例如：北京时间 9:00 = UTC 1:00

### 自定义分析数量

**方法 1：修改默认值**

编辑 `.github/workflows/weibo-trends-analyzer.yml`：

```yaml
env:
  ANALYSIS_LIMIT: '15'  # 修改为你想要的数量
```

**方法 2：手动触发时指定**

在 GitHub Actions UI 手动运行时，在输入框填写数量。

### 添加通知功能

可以在 workflow 中添加通知步骤（Slack、Discord、Email 等）：

```yaml
- name: 📧 Send notification
  if: always()
  uses: actions/github-script@v7
  with:
    script: |
      // 自定义通知逻辑
```

### 优化性能

**减少 API 调用**：
- 调整搜索次数（修改 `utils.py` 中的 `num_results` 参数）
- 使用缓存机制避免重复搜索

**加速执行**：
- 启用 pip 缓存（已配置）
- 使用并行处理（需修改代码）

---

## 📊 成本估算

### 每日运行成本（分析 10 个话题）

| 服务 | 消耗量 | 单价 | 每日成本 |
|------|--------|------|---------|
| Claude API | ~10K tokens | $3/M (input) + $15/M (output) | ~$0.10 |
| 天行数据 API | 1 次请求 | 免费（100次/天） | $0 |
| SerpAPI | 20 次搜索 | 免费（100次/月） | $0（前5天）|
| GitHub Actions | ~5 分钟 | 免费（2000分钟/月） | $0 |
| **总计** | - | - | **~$0.10/天** |

### 每月成本（每日运行）

- Claude API: ~$3/月
- SerpAPI: 需付费（$50/月）或减少频率
- 其他: $0

**节省成本建议**：
- 减少分析频率（每周 2-3 次）
- 使用 Google Custom Search（免费配额更高）
- 优化 prompt 减少 token 消耗

---

## 📝 项目结构

```
weibo-trends-analyzer/
├── .github/
│   └── workflows/
│       └── weibo-trends-analyzer.yml    # GitHub Actions 工作流
├── scripts/
│   ├── weibo_analyzer.py                # 主分析脚本
│   ├── utils.py                         # 工具函数
│   └── templates/
│       └── dashboard_template.html      # HTML 报告模板
├── reports/                              # 生成的报告存放目录
│   ├── weibo-trends-analysis-2026-01-XX.html
│   └── weibo-trends-data-2026-01-XX.json
├── requirements.txt                      # Python 依赖
├── DEPLOYMENT.md                         # 本文档
└── README.md                             # 项目说明

# 原 Skill 文件（保留供参考）
├── .claude/
│   └── skills/
│       └── weibo-trends-analyzer/
│           ├── SKILL.md
│           ├── API_CONFIG.md
│           └── ...
```

---

## 🎓 学习资源

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Claude Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview)
- [SerpAPI 文档](https://serpapi.com/docs)
- [天行数据 API 文档](https://www.tianapi.com/apiview/223)
- [Cron 表达式生成器](https://crontab.guru/)

---

## ⚠️ 安全注意事项

1. **永远不要将 API 密钥提交到代码仓库**
2. **使用 GitHub Secrets 管理敏感信息**
3. **定期轮换 API 密钥**
4. **监控 API 使用量和成本**
5. **设置 API 消费限额**
6. **私有仓库存放敏感数据**

---

## 🤝 支持与反馈

如有问题或建议：
1. 查看本文档的故障排除部分
2. 在 GitHub 仓库提交 Issue
3. 查阅官方文档和社区资源

---

## 📜 许可证

本项目基于 MIT License 开源，可自由使用和修改。

---

**祝你使用愉快！发现更多热搜商机！** 🚀

最后更新：2026-01-17
