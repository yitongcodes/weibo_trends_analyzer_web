#!/usr/bin/env python3
"""
Weibo Trends Analyzer - Main Script
Analyzes Weibo trending topics and generates creative product ideas
"""
import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.utils import (
    WeiboAPIClient,
    SearchAPIClient,
    format_timestamp,
    format_display_timestamp,
    validate_product_concept,
    calculate_score_tier,
    save_json_data
)

# Import Claude Agent SDK
try:
    from claude_agent_sdk import query
except ImportError:
    print("❌ Error: claude-agent-sdk not installed. Please run: pip install claude-agent-sdk")
    sys.exit(1)


class WeiboTrendsAnalyzer:
    """Main analyzer class"""

    def __init__(
        self,
        tianapi_key: str,
        search_api_key: str,
        anthropic_api_key: str,
        search_engine: str = "serpapi",
        anthropic_base_url: str = None
    ):
        self.weibo_client = WeiboAPIClient(tianapi_key)
        self.search_client = SearchAPIClient(search_api_key, search_engine)
        self.anthropic_api_key = anthropic_api_key
        self.anthropic_base_url = anthropic_base_url

        # Set environment variables for Claude SDK
        os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

        # Set custom API base URL if provided (for third-party APIs)
        if anthropic_base_url:
            os.environ["ANTHROPIC_BASE_URL"] = anthropic_base_url
            print(f"✅ Using custom Claude API endpoint: {anthropic_base_url}")

    async def analyze_single_topic(
        self,
        topic: Dict,
        research: Dict
    ) -> Dict:
        """
        Analyze a single trending topic using Claude Agent SDK

        Args:
            topic: Trending topic dictionary
            research: Research findings dictionary

        Returns:
            Product concept dictionary
        """
        keyword = topic["keyword"]
        rank = topic["rank"]
        heat_value = topic["heat_value"]

        # Construct prompt for Claude
        prompt = f"""
你是一位专业的产品设计师和市场分析师。请根据以下微博热搜话题，生成创意产品概念。

**热搜话题**：{keyword}
**排名**：第{rank}名
**热度值**：{heat_value:,}

**背景研究**：
社交媒体讨论：
{research['social_media']}

新闻背景：
{research['news_background']}

用户洞察：
{research['user_insights']}

市场潜力：
{research['market_potential']}

---

请基于以上信息，设计1个创意小商品，并按照以下格式返回JSON（仅返回JSON，不要其他文字）：

{{
  "product_name": "产品名称（简短、有吸引力）",
  "market_category": "市场赛道（如：文创、家居、科技配件、时尚饰品等）",
  "target_audience": "目标人群（具体描述年龄、兴趣、收入水平等）",
  "description": "详细产品描述（如何与热搜话题结合，解决什么问题，有什么特色）",
  "manufacturing_details": "生产特点（生产方式、材料、起订量、成本结构等）",
  "score_breakdown": {{
    "development_potential": <0-40分>,
    "interest_level": <0-20分>,
    "life_utility": <0-20分>,
    "production_ease": <0-20分>
  }},
  "total_score": <总分0-100>,
  "score_justification": "评分理由（简要说明各维度评分依据）"
}}

**评分标准**：
1. 可发展度 (40分)：市场规模15分 + 技术可行性10分 + 趋势持久性10分 + 竞争格局5分
2. 有趣度 (20分)：创意独特性10分 + 情感吸引力5分 + 传播潜力5分
3. 生活有用度 (20分)：日常整合度10分 + 解决问题能力5分 + 受众规模5分
4. 生产容易度 (20分)：制造复杂度10分 + 材料可得性5分 + 小批量成本5分
"""

        try:
            # Use Claude Agent SDK to generate product concept
            response_text = ""
            async for message in query(prompt=prompt):
                if hasattr(message, 'content'):
                    response_text += str(message.content)
                else:
                    response_text += str(message)

            # Parse JSON response
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                concept = json.loads(json_str)

                # Add topic information
                concept["keyword"] = keyword
                concept["rank"] = rank
                concept["heat_value"] = heat_value
                concept["tag"] = topic.get("tag", "")
                concept["category"] = topic.get("category", "")

                # Add research summary
                concept["research_summary"] = research

                # Validate concept
                if validate_product_concept(concept):
                    # Calculate tier
                    tier_name, tier_badge, tier_class = calculate_score_tier(
                        concept["total_score"]
                    )
                    concept["tier_name"] = tier_name
                    concept["tier_badge"] = tier_badge
                    concept["tier_class"] = tier_class

                    return concept
                else:
                    print(f"⚠️  Invalid product concept for '{keyword}'")
                    return self._create_fallback_concept(topic, research)

            else:
                print(f"⚠️  Failed to parse JSON for '{keyword}'")
                return self._create_fallback_concept(topic, research)

        except Exception as e:
            print(f"❌ Error analyzing topic '{keyword}': {e}")
            return self._create_fallback_concept(topic, research)

    def _create_fallback_concept(self, topic: Dict, research: Dict) -> Dict:
        """Create a basic fallback concept when AI analysis fails"""
        return {
            "keyword": topic["keyword"],
            "rank": topic["rank"],
            "heat_value": topic["heat_value"],
            "tag": topic.get("tag", ""),
            "category": topic.get("category", ""),
            "product_name": f"{topic['keyword']}主题商品",
            "market_category": "文创产品",
            "target_audience": "18-35岁年轻人群",
            "description": f"基于热搜话题'{topic['keyword']}'的创意产品",
            "manufacturing_details": "小批量生产，待进一步分析",
            "score_breakdown": {
                "development_potential": 20,
                "interest_level": 10,
                "life_utility": 10,
                "production_ease": 10
            },
            "total_score": 50,
            "score_justification": "⚠️ AI分析失败，使用默认评分",
            "research_summary": research,
            "tier_name": "其他",
            "tier_badge": "📋 其他",
            "tier_class": "other"
        }

    async def analyze_trends(self, limit: int = 10) -> Dict:
        """
        Main analysis workflow

        Args:
            limit: Number of trends to analyze

        Returns:
            Complete analysis results dictionary
        """
        print(f"🚀 Starting Weibo Trends Analysis...")
        print(f"📅 {format_display_timestamp()}\n")

        # Step 1: Fetch trending topics
        print("📊 Step 1: Fetching Weibo trending topics...")
        topics = self.weibo_client.fetch_trending_topics(limit=limit)

        if not topics:
            print("❌ No topics fetched. Exiting.")
            return {"error": "No topics available"}

        print(f"✅ Fetched {len(topics)} trending topics\n")

        # Step 2: Research and analyze each topic
        print("🔍 Step 2: Researching and analyzing topics...")
        product_concepts = []

        for idx, topic in enumerate(topics, 1):
            keyword = topic["keyword"]
            print(f"\n[{idx}/{len(topics)}] Analyzing: {keyword}")

            # Conduct web research
            print(f"  🔎 Researching background...")
            research = self.search_client.research_topic(keyword)

            # Analyze with Claude
            print(f"  🤖 Generating product concept with AI...")
            concept = await self.analyze_single_topic(topic, research)

            product_concepts.append(concept)
            print(f"  ✅ {concept['product_name']} - Score: {concept['total_score']}/100 ({concept['tier_badge']})")

        # Step 3: Sort and categorize
        print(f"\n📊 Step 3: Organizing results...")
        product_concepts.sort(key=lambda x: x["total_score"], reverse=True)

        # Categorize by tier
        excellent = [p for p in product_concepts if p["total_score"] >= 80]
        good = [p for p in product_concepts if 60 <= p["total_score"] < 80]
        other = [p for p in product_concepts if p["total_score"] < 60]

        # Calculate statistics
        avg_score = sum(p["total_score"] for p in product_concepts) / len(product_concepts) if product_concepts else 0

        results = {
            "metadata": {
                "generated_at": format_display_timestamp(),
                "total_analyzed": len(product_concepts),
                "average_score": round(avg_score, 1),
                "excellent_count": len(excellent),
                "good_count": len(good),
                "other_count": len(other)
            },
            "products": {
                "excellent": excellent,
                "good": good,
                "other": other
            },
            "all_products": product_concepts
        }

        print(f"\n✅ Analysis complete!")
        print(f"  🏆 Excellent (≥80): {len(excellent)}")
        print(f"  ⭐ Good (60-79): {len(good)}")
        print(f"  📋 Other (<60): {len(other)}")
        print(f"  📊 Average Score: {avg_score:.1f}/100")

        return results

    def generate_html_report(self, results: Dict, output_dir: str = "reports") -> str:
        """
        Generate HTML report from analysis results

        Args:
            results: Analysis results dictionary
            output_dir: Output directory

        Returns:
            Path to generated HTML file
        """
        print(f"\n📝 Generating HTML report...")

        # Load template
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("dashboard_template.html")

        # Render template
        html_content = template.render(
            metadata=results["metadata"],
            excellent_products=results["products"]["excellent"],
            good_products=results["products"]["good"],
            other_products=results["products"]["other"]
        )

        # Save HTML file
        os.makedirs(output_dir, exist_ok=True)
        filename = f"weibo-trends-analysis-{format_timestamp()}.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML report saved: {filepath}")
        return filepath


async def main():
    """Main entry point"""
    # Load configuration from environment variables
    tianapi_key = os.getenv("TIANAPI_KEY")
    search_api_key = os.getenv("SEARCH_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    anthropic_base_url = os.getenv("ANTHROPIC_BASE_URL")  # Optional: for third-party APIs
    search_engine = os.getenv("SEARCH_ENGINE", "serpapi")  # serpapi or google
    analysis_limit = int(os.getenv("ANALYSIS_LIMIT", "10"))

    # Validate required environment variables
    if not all([tianapi_key, search_api_key, anthropic_api_key]):
        print("❌ Error: Missing required environment variables")
        print("Required: TIANAPI_KEY, SEARCH_API_KEY, ANTHROPIC_API_KEY")
        sys.exit(1)

    # Initialize analyzer
    analyzer = WeiboTrendsAnalyzer(
        tianapi_key=tianapi_key,
        search_api_key=search_api_key,
        anthropic_api_key=anthropic_api_key,
        search_engine=search_engine,
        anthropic_base_url=anthropic_base_url
    )

    # Run analysis
    results = await analyzer.analyze_trends(limit=analysis_limit)

    if "error" in results:
        print(f"❌ Analysis failed: {results['error']}")
        sys.exit(1)

    # Save JSON data (optional)
    json_filename = f"weibo-trends-data-{format_timestamp()}.json"
    json_path = save_json_data(results, "reports", json_filename)
    print(f"✅ JSON data saved: {json_path}")

    # Generate HTML report
    html_path = analyzer.generate_html_report(results)

    print(f"\n🎉 All done! Check the reports in the 'reports/' directory.")
    print(f"📄 HTML Report: {html_path}")
    print(f"📊 JSON Data: {json_path}")


if __name__ == "__main__":
    asyncio.run(main())
