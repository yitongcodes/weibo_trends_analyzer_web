# 🌐 GitHub Pages 部署指南

## 📖 概述

本项目已配置自动部署到 GitHub Pages，每次运行分析后，报告会自动发布到公开的网页上，你可以轻松分享给任何人！

---

## 🎯 最终效果

部署完成后，你将获得：

- 📊 **首页**: `https://yitongcodes.github.io/weibo_trends_analyzer_web/`
  - 显示所有历史报告列表
  - 精美的卡片式布局
  - 快速访问每个报告

- 📈 **详细报告**: `https://yitongcodes.github.io/weibo_trends_analyzer_web/weibo-trends-analysis-YYYY-MM-DD.html`
  - 完整的分析报告
  - 交互式数据展示
  - 可搜索和筛选

---

## ⚙️ 启用 GitHub Pages（一次性配置）

### 方式1：使用 GitHub Actions 部署（推荐，已配置）

**步骤：**

1. **进入仓库设置页面**
   - 访问: https://github.com/yitongcodes/weibo_trends_analyzer_web/settings/pages

2. **配置 Source（来源）**
   - 在 "Build and deployment" 部分
   - **Source**: 选择 `GitHub Actions` ✅
   - 这是最重要的一步！必须选择 GitHub Actions

   ![GitHub Pages Source](https://docs.github.com/assets/cb-122896/images/help/pages/publishing-source-drop-down.png)

3. **保存配置**
   - 配置会自动保存
   - 无需其他设置

4. **等待首次部署**
   - 下次运行 workflow 时会自动部署
   - 或者现在手动触发一次 workflow

**完成！** 🎉

---

## 🚀 手动触发首次部署

配置完成后，立即测试部署：

1. 进入 **Actions** 标签: https://github.com/yitongcodes/weibo_trends_analyzer_web/actions

2. 选择 **"Weibo Trends Analyzer"** workflow

3. 点击右侧 **"Run workflow"** 按钮

4. 选择 branch: **main**

5. 点击绿色的 **"Run workflow"** 确认

6. 等待约 5-10 分钟

7. 部署完成后，访问:
   ```
   https://yitongcodes.github.io/weibo_trends_analyzer_web/
   ```

---

## 📊 查看部署状态

### 方法1：在 Actions 中查看

1. 进入 Actions: https://github.com/yitongcodes/weibo_trends_analyzer_web/actions

2. 点击最近的 workflow 运行

3. 查看 **"🚀 Deploy to GitHub Pages"** 步骤

4. 成功后会显示部署 URL

### 方法2：在 Settings 中查看

1. 进入 Settings → Pages: https://github.com/yitongcodes/weibo_trends_analyzer_web/settings/pages

2. 顶部会显示:
   ```
   ✅ Your site is live at https://yitongcodes.github.io/weibo_trends_analyzer_web/
   ```

---

## 🔗 分享你的报告

部署成功后，你可以分享以下链接：

### 1. 首页（推荐）
```
https://yitongcodes.github.io/weibo_trends_analyzer_web/
```
- 显示所有历史报告
- 用户可以选择查看任何日期的报告

### 2. 直接分享最新报告
```
https://yitongcodes.github.io/weibo_trends_analyzer_web/weibo-trends-analysis-2026-01-17.html
```
- 替换日期为你想分享的报告日期

### 3. 下载数据
```
https://yitongcodes.github.io/weibo_trends_analyzer_web/weibo-trends-data-2026-01-17.json
```
- JSON 格式的原始数据
- 可用于二次分析

---

## 🎨 自定义域名（可选）

如果你想使用自己的域名（如 `weibo.yourdomain.com`）：

1. 购买域名

2. 在域名 DNS 设置中添加 CNAME 记录:
   ```
   CNAME: weibo
   目标: yitongcodes.github.io
   ```

3. 在 GitHub Pages 设置中添加自定义域名:
   - Settings → Pages → Custom domain
   - 输入: `weibo.yourdomain.com`
   - 勾选 "Enforce HTTPS"

4. 等待 DNS 生效（可能需要几分钟到几小时）

5. 访问你的自定义域名！

---

## 🔧 故障排除

### 问题1：Pages 显示 404

**原因**: GitHub Pages 未正确配置

**解决方案**:
1. 确认 Settings → Pages → Source 选择了 `GitHub Actions`
2. 确认 workflow 已成功运行
3. 等待几分钟让部署生效
4. 清除浏览器缓存后重试

### 问题2：Workflow 部署步骤失败

**原因**: 权限不足

**解决方案**:
1. 检查 Settings → Actions → General → Workflow permissions
2. 确保选择了 "Read and write permissions"
3. 确保勾选了 "Allow GitHub Actions to create and approve pull requests"
4. 重新运行 workflow

### 问题3：首页显示但报告链接 404

**原因**: 报告文件未生成或路径错误

**解决方案**:
1. 检查 GitHub 仓库的 `reports/` 目录是否有文件
2. 确认文件名格式: `weibo-trends-analysis-YYYY-MM-DD.html`
3. 重新运行 workflow 生成新报告

### 问题4：样式显示异常

**原因**: CSS 加载问题

**解决方案**:
1. 清除浏览器缓存
2. 使用无痕模式打开
3. 尝试不同浏览器（Chrome、Firefox、Safari）

---

## 📱 移动端访问

GitHub Pages 完全支持移动端访问：

- ✅ 响应式设计
- ✅ 触摸友好的交互
- ✅ 移动端优化的布局

直接在手机浏览器中打开链接即可！

---

## 🔐 隐私与安全

### 公开访问

- ⚠️ GitHub Pages 上的所有内容都是**公开可访问**的
- 任何人都可以通过 URL 访问你的报告
- 不要在报告中包含敏感信息

### 限制访问（如需要）

如果你想限制访问：

1. **方案 A**: 使用 Private 仓库 + GitHub Pro
   - GitHub Pro 支持私有仓库的 Pages
   - 只有仓库协作者可以访问

2. **方案 B**: 不使用 GitHub Pages
   - 只提交报告到仓库
   - 通过 Artifacts 下载查看
   - 或在本地运行脚本

3. **方案 C**: 添加密码保护
   - 使用第三方服务（如 Cloudflare Pages）
   - 部署时添加访问控制

---

## 📊 使用统计

想了解有多少人访问了你的报告？

### 使用 Google Analytics

1. 创建 Google Analytics 账号

2. 获取跟踪代码

3. 修改 `scripts/templates/dashboard_template.html` 和 `scripts/generate_index.py`

4. 在 `</head>` 前添加 GA 代码:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

5. 重新生成报告即可看到访问统计

---

## 🎓 进阶功能

### 添加搜索功能

可以集成第三方搜索服务（如 Algolia）来搜索历史报告。

### 添加评论功能

使用 Utterances 或 Giscus 为报告添加评论区。

### RSS 订阅

生成 RSS feed 让用户订阅更新。

---

## ✅ 配置检查清单

部署前确认：

- [ ] Settings → Pages → Source 设置为 `GitHub Actions`
- [ ] Settings → Actions → Workflow permissions 设置为 `Read and write`
- [ ] 已成功运行一次 workflow
- [ ] 可以访问 `https://yitongcodes.github.io/weibo_trends_analyzer_web/`
- [ ] 首页显示正常
- [ ] 可以点击查看详细报告
- [ ] 移动端访问正常

---

## 🎉 完成！

恭喜！你的微博热搜分析报告现在可以公开分享了！

**你的公开链接**:
```
https://yitongcodes.github.io/weibo_trends_analyzer_web/
```

每天早上 9:00，新报告会自动生成并发布 🚀

---

## 📞 需要帮助？

如有问题：

1. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 完整部署文档
2. 查看 [GitHub Pages 官方文档](https://docs.github.com/en/pages)
3. 在仓库提交 Issue

---

**最后更新**: 2026-01-17
