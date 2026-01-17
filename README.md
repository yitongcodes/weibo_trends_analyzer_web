# 🔥 微博热搜创意产品分析器

> 基于 Claude Agent SDK 和 GitHub Actions 的自动化微博热搜分析工具

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Claude](https://img.shields.io/badge/Claude-Agent%20SDK-6B46C1?logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)

## 📖 项目简介

本项目将微博热搜分析自动化，每天定时获取热门话题，通过 AI 分析生成创意小商品设计建议，并自动生成精美的交互式 HTML 报告。

### ✨ 核心功能

- 🔄 **自动定时执行**：每天北京时间早上 9:00 自动运行
- 🤖 **AI 智能分析**：使用 Claude Agent SDK 进行产品创意生成
- 📊 **100 分评分系统**：从可发展度、有趣度、有用度、易生产四个维度评估
- 🎨 **可视化报告**：生成交互式 HTML Dashboard，支持搜索和筛选
- 🔍 **深度背景研究**：自动进行 Web 搜索，获取社交媒体和新闻背景
- 💾 **自动存档**：报告自动提交到 GitHub 仓库

### 🎯 适用场景

- 💼 创业选品参考
- 🎨 文创产品设计
- 📈 市场趋势分析
- 🛍️ 电商选品决策

## 🚀 快速开始

### 1. 准备 API 密钥

你需要获取以下 API 密钥：

- **Claude API Key**
  - 官方：[Anthropic Console](https://console.anthropic.com/)
  - 第三方：如果你有第三方 Claude API，请查看 [**第三方 API 配置指南**](THIRD_PARTY_API_SETUP.md)
- **天行数据 API Key** - [获取地址](https://www.tianapi.com/)（或使用项目内置密钥）
- **SerpAPI Key** - [获取地址](https://serpapi.com/)（或使用 Google Custom Search）

### 2. 部署到 GitHub Actions

详细步骤请参考 [**DEPLOYMENT.md**](DEPLOYMENT.md) 完整部署指南。

**简化版步骤**：

```bash
# 1. 创建 GitHub 仓库
# 2. 克隆本项目到本地
git clone <your-repo>

# 3. 配置 GitHub Secrets
# 进入仓库 Settings → Secrets → Actions
# 添加：ANTHROPIC_API_KEY, TIANAPI_KEY, SEARCH_API_KEY

# 4. 推送代码
git add .
git commit -m "Initial commit"
git push origin main

# 5. 查看 Actions 标签页，等待自动运行或手动触发
```

### 3. 查看报告

报告生成后会自动提交到 `reports/` 目录，可以：

- 🌐 **GitHub Pages 在线查看**（推荐）: `https://yitongcodes.github.io/weibo_trends_analyzer_web/`
- 📂 直接在 GitHub 浏览
- 📥 下载 Artifacts 查看

> 💡 **配置 GitHub Pages**: 查看 [**GitHub Pages 部署指南**](GITHUB_PAGES_SETUP.md)

## 📊 示例报告

![Dashboard Preview](.github/images/dashboard-preview.png)

**报告包含**：
- 🏆 优秀产品（≥80分）- 优先开发推荐
- ⭐ 良好产品（60-79分）- 可考虑开发
- 📋 其他产品（<60分）- 观望或需优化

## 🏗️ 项目架构

```
GitHub Actions (定时触发)
    ↓
获取微博热搜 (天行数据 API)
    ↓
Web 搜索背景研究 (SerpAPI)
    ↓
AI 分析生成产品创意 (Claude Agent SDK)
    ↓
生成 HTML 报告 (Jinja2 模板)
    ↓
生成首页索引 (index.html)
    ↓
提交到仓库 (Git) + 部署到 GitHub Pages 🌐
```

## 📁 项目结构

```
weibo-trends-analyzer/
├── .github/workflows/        # GitHub Actions 配置
├── scripts/                  # Python 脚本
│   ├── weibo_analyzer.py    # 主分析脚本
│   ├── utils.py             # 工具函数
│   ├── generate_index.py    # 生成首页索引
│   └── templates/           # HTML 模板
├── reports/                  # 生成的报告
│   ├── index.html           # GitHub Pages 首页
│   └── weibo-trends-*.html  # 每日报告
├── requirements.txt          # Python 依赖
├── DEPLOYMENT.md            # 详细部署指南
├── GITHUB_PAGES_SETUP.md    # GitHub Pages 配置指南
└── README.md                # 本文件
```

## 🔐 必需配置的 GitHub Secrets

| Secret 名称 | 说明 |
|------------|------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 |
| `TIANAPI_KEY` | 天行数据 API 密钥 |
| `SEARCH_API_KEY` | SerpAPI 或 Google API 密钥 |

**可选 Secrets**（使用第三方 Claude API 时需要）：

| Secret 名称 | 说明 |
|------------|------|
| `ANTHROPIC_BASE_URL` | 第三方 Claude API 地址 |

> 💡 使用第三方 API？查看 [**第三方 API 配置指南**](THIRD_PARTY_API_SETUP.md)

## 💰 成本估算

**每日运行成本**（分析 10 个话题）：

- Claude API: ~$0.10
- 天行数据: 免费（100 次/天）
- SerpAPI: 免费配额内（100 次/月）
- GitHub Actions: 免费

**每月约 $3-50**（取决于搜索 API 选择）

## 🎛️ 自定义配置

### 调整执行时间

编辑 `.github/workflows/weibo-trends-analyzer.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = 北京时间 9:00
```

### 调整分析数量

手动运行时在 Actions UI 设置，或修改环境变量 `ANALYSIS_LIMIT`。

## 🔧 故障排除

遇到问题？请参考：

1. [DEPLOYMENT.md - 故障排除章节](DEPLOYMENT.md#故障排除)
2. 查看 Actions 运行日志
3. 提交 GitHub Issue

## 📚 文档

- [📖 完整部署指南](DEPLOYMENT.md)
- [🔧 原 Skill 文档](.claude/skills/weibo-trends-analyzer/SKILL.md)
- [🔑 API 配置说明](.claude/skills/weibo-trends-analyzer/API_CONFIG.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📜 许可证

MIT License - 可自由使用和修改

---

**从本地 Skill 到云端自动化，让 AI 帮你发现热搜商机！** 🚀

Made with ❤️ using Claude Agent SDK
