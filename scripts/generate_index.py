"""
Generate index.html for GitHub Pages
Lists all generated Weibo Trends Analysis reports
"""
import os
import json
from datetime import datetime
from pathlib import Path


def get_report_files(reports_dir="reports"):
    """Get all HTML and JSON report files"""
    reports_path = Path(reports_dir)

    if not reports_path.exists():
        return []

    html_files = sorted(reports_path.glob("weibo-trends-analysis-*.html"), reverse=True)

    reports = []
    for html_file in html_files:
        # Extract date from filename
        filename = html_file.name
        date_str = filename.replace("weibo-trends-analysis-", "").replace(".html", "")

        # Check if corresponding JSON exists
        json_file = reports_path / f"weibo-trends-data-{date_str}.json"

        # Get file size
        file_size = html_file.stat().st_size / 1024  # KB

        # Try to get metadata from JSON
        metadata = {}
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})
            except:
                pass

        reports.append({
            'date': date_str,
            'html_file': filename,
            'json_file': f"weibo-trends-data-{date_str}.json" if json_file.exists() else None,
            'file_size': round(file_size, 1),
            'metadata': metadata
        })

    return reports


def generate_index_html(reports, output_file="reports/index.html"):
    """Generate index.html listing all reports"""

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜创意产品分析 - 历史报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
            flex-wrap: wrap;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 5px;
        }

        .content {
            padding: 40px;
        }

        .intro {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            border-left: 5px solid #667eea;
        }

        .intro h2 {
            color: #667eea;
            margin-bottom: 15px;
        }

        .intro p {
            line-height: 1.8;
            color: #555;
            margin-bottom: 10px;
        }

        .reports-section {
            margin-top: 30px;
        }

        .section-title {
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            color: #333;
        }

        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }

        .report-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
            cursor: pointer;
        }

        .report-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }

        .report-date {
            font-size: 1.4em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }

        .report-meta {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
            font-size: 0.9em;
        }

        .meta-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
        }

        .meta-label {
            color: #666;
            font-size: 0.85em;
            margin-bottom: 3px;
        }

        .meta-value {
            color: #333;
            font-weight: bold;
            font-size: 1.1em;
        }

        .report-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        .btn {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 0.95em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            text-align: center;
            display: inline-block;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
            background: #f8f9fa;
            color: #667eea;
            border: 2px solid #667eea;
        }

        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }

        footer {
            background: #2c3e50;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }

        footer p {
            margin: 10px 0;
            opacity: 0.8;
        }

        footer a {
            color: #667eea;
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .reports-grid {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 2em;
            }

            .stats {
                flex-direction: column;
                gap: 20px;
            }

            .report-meta {
                grid-template-columns: 1fr;
            }
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
            margin-top: 10px;
        }

        .badge-new {
            background: #4caf50;
            color: white;
        }

        .badge-info {
            background: #2196f3;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 微博热搜创意产品分析</h1>
            <p class="subtitle">Weibo Trends Product Analysis - Historical Reports</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{{total_reports}}</div>
                    <div class="stat-label">历史报告</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{latest_date}}</div>
                    <div class="stat-label">最新更新</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">🤖</div>
                    <div class="stat-label">AI 驱动</div>
                </div>
            </div>
        </header>

        <div class="content">
            <div class="intro">
                <h2>📊 关于本项目</h2>
                <p>本项目基于 <strong>Claude Agent SDK</strong> 和 <strong>GitHub Actions</strong>，每天自动分析微博热搜话题，并通过 AI 生成创意小商品设计建议。</p>
                <p>🎯 <strong>100分评分系统</strong>：从可发展度、有趣度、生活有用度、生产容易度四个维度评估产品潜力。</p>
                <p>🚀 <strong>自动化流程</strong>：每天北京时间早上 9:00 自动运行，无需人工干预。</p>
            </div>

            <div class="reports-section">
                <h2 class="section-title">📁 历史报告列表</h2>

                {{#if reports}}
                <div class="reports-grid">
                    {{#each reports}}
                    <div class="report-card">
                        <div class="report-date">📅 {{date}}</div>
                        {{#if is_latest}}
                        <span class="badge badge-new">最新</span>
                        {{/if}}

                        <div class="report-meta">
                            {{#if metadata.total_analyzed}}
                            <div class="meta-item">
                                <div class="meta-label">分析数量</div>
                                <div class="meta-value">{{metadata.total_analyzed}}</div>
                            </div>
                            {{/if}}
                            {{#if metadata.average_score}}
                            <div class="meta-item">
                                <div class="meta-label">平均分数</div>
                                <div class="meta-value">{{metadata.average_score}}</div>
                            </div>
                            {{/if}}
                            {{#if metadata.excellent_count}}
                            <div class="meta-item">
                                <div class="meta-label">🏆 优秀产品</div>
                                <div class="meta-value">{{metadata.excellent_count}}</div>
                            </div>
                            {{/if}}
                            <div class="meta-item">
                                <div class="meta-label">文件大小</div>
                                <div class="meta-value">{{file_size}} KB</div>
                            </div>
                        </div>

                        <div class="report-actions">
                            <a href="{{html_file}}" class="btn btn-primary" target="_blank">📊 查看报告</a>
                            {{#if json_file}}
                            <a href="{{json_file}}" class="btn btn-secondary" download>📥 下载数据</a>
                            {{/if}}
                        </div>
                    </div>
                    {{/each}}
                </div>
                {{else}}
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <h3>暂无报告</h3>
                    <p>首次运行后将会生成报告</p>
                </div>
                {{/if}}
            </div>
        </div>

        <footer>
            <p>🤖 Powered by <a href="https://www.anthropic.com/" target="_blank">Claude Agent SDK</a> & GitHub Actions</p>
            <p>📊 数据来源：<a href="https://www.tianapi.com/" target="_blank">天行数据 - 微博热搜API</a></p>
            <p>🔗 项目源码：<a href="https://github.com/yitongcodes/weibo_trends_analyzer_web" target="_blank">GitHub Repository</a></p>
            <p style="margin-top: 15px; font-size: 0.9em;">生成时间：{{generated_time}}</p>
        </footer>
    </div>
</body>
</html>
"""

    # Prepare template data
    latest_date = reports[0]['date'] if reports else "N/A"

    # Mark the first report as latest
    if reports:
        reports[0]['is_latest'] = True

    # Simple template replacement (using Python string formatting)
    # For production, you might want to use Jinja2
    html = html_content.replace('{{total_reports}}', str(len(reports)))
    html = html.replace('{{latest_date}}', latest_date)
    html = html.replace('{{generated_time}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))

    # Build reports HTML
    if reports:
        reports_html = ""
        for report in reports:
            reports_html += f"""
                    <div class="report-card">
                        <div class="report-date">📅 {report['date']}</div>
                        {'<span class="badge badge-new">最新</span>' if report.get('is_latest') else ''}

                        <div class="report-meta">
                            {'<div class="meta-item"><div class="meta-label">分析数量</div><div class="meta-value">' + str(report['metadata'].get('total_analyzed', 'N/A')) + '</div></div>' if report['metadata'].get('total_analyzed') else ''}
                            {'<div class="meta-item"><div class="meta-label">平均分数</div><div class="meta-value">' + str(report['metadata'].get('average_score', 'N/A')) + '</div></div>' if report['metadata'].get('average_score') else ''}
                            {'<div class="meta-item"><div class="meta-label">🏆 优秀产品</div><div class="meta-value">' + str(report['metadata'].get('excellent_count', 0)) + '</div></div>' if report['metadata'].get('excellent_count') is not None else ''}
                            <div class="meta-item">
                                <div class="meta-label">文件大小</div>
                                <div class="meta-value">{report['file_size']} KB</div>
                            </div>
                        </div>

                        <div class="report-actions">
                            <a href="{report['html_file']}" class="btn btn-primary" target="_blank">📊 查看报告</a>
                            {'<a href="' + report['json_file'] + '" class="btn btn-secondary" download>📥 下载数据</a>' if report['json_file'] else ''}
                        </div>
                    </div>
"""

        # Replace template blocks
        html = html.replace('{{#if reports}}', '')
        html = html.replace('{{#each reports}}', '')
        html = html.replace('{{#if is_latest}}', '')
        html = html.replace('{{/if}}', '')
        html = html.replace('{{#if metadata.total_analyzed}}', '')
        html = html.replace('{{#if metadata.average_score}}', '')
        html = html.replace('{{#if metadata.excellent_count}}', '')
        html = html.replace('{{#if json_file}}', '')
        html = html.replace('{{/each}}', '')
        html = html.replace('{{else}}', '<!--')
        html = html.replace('{{/if}}', '-->')

        # Find and replace the reports grid section
        import re
        html = re.sub(r'<div class="reports-grid">.*?</div>\s*<!--',
                     f'<div class="reports-grid">{reports_html}</div><!--',
                     html, flags=re.DOTALL)
    else:
        # Show empty state
        html = html.replace('{{#if reports}}', '<!--')
        html = html.replace('{{#each reports}}', '')
        html = html.replace('{{/each}}', '')
        html = html.replace('{{else}}', '-->')
        html = html.replace('{{/if}}', '')

    # Write to file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Generated index.html with {len(reports)} report(s)")
    return output_file


if __name__ == "__main__":
    reports = get_report_files()
    generate_index_html(reports)
