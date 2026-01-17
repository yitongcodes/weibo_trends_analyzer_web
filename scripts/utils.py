"""
Utility functions for Weibo Trends Analyzer
"""
import os
import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class WeiboAPIClient:
    """Client for fetching Weibo trending topics"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://apis.tianapi.com/weibohot/index"

    def fetch_trending_topics(self, limit: int = 15) -> List[Dict]:
        """
        Fetch trending topics from Weibo API

        Args:
            limit: Maximum number of topics to return

        Returns:
            List of trending topic dictionaries
        """
        try:
            response = requests.get(
                self.base_url,
                params={"key": self.api_key},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            if data.get("code") != 200:
                raise Exception(f"API Error: {data.get('msg', 'Unknown error')}")

            topics = data.get("result", {}).get("list", [])

            # Parse and structure the data
            parsed_topics = []
            for idx, topic in enumerate(topics[:limit], 1):
                parsed_topics.append({
                    "rank": idx,
                    "keyword": topic.get("hotword", ""),
                    "heat_value": self._extract_heat_value(topic.get("hotwordnum", "")),
                    "tag": topic.get("hottag", ""),
                    "category": self._extract_category(topic.get("hotwordnum", ""))
                })

            return parsed_topics

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch Weibo trending topics: {e}")
            return self._load_mock_data(limit)
        except Exception as e:
            print(f"❌ Error processing API response: {e}")
            return self._load_mock_data(limit)

    def _extract_heat_value(self, hotwordnum: str) -> int:
        """Extract numeric heat value from hotwordnum field"""
        # Remove category prefix and extract numbers
        numbers = re.findall(r'\d+', str(hotwordnum))
        return int(numbers[0]) if numbers else 0

    def _extract_category(self, hotwordnum: str) -> str:
        """Extract category from hotwordnum field"""
        # Categories like "综艺", "剧集", "盛典", "演出"
        categories = re.findall(r'^[\u4e00-\u9fa5]+', str(hotwordnum).strip())
        return categories[0] if categories else ""

    def _load_mock_data(self, limit: int) -> List[Dict]:
        """Load mock data as fallback"""
        mock_file = os.path.join(
            os.path.dirname(__file__),
            "../.claude/skills/weibo-trends-analyzer/weibo-mock-data.json"
        )

        try:
            with open(mock_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                topics = data.get("result", {}).get("list", [])

                parsed_topics = []
                for idx, topic in enumerate(topics[:limit], 1):
                    parsed_topics.append({
                        "rank": idx,
                        "keyword": topic.get("hotword", ""),
                        "heat_value": self._extract_heat_value(topic.get("hotwordnum", "")),
                        "tag": topic.get("hottag", ""),
                        "category": self._extract_category(topic.get("hotwordnum", ""))
                    })

                print("⚠️  Using mock data as fallback")
                return parsed_topics
        except Exception as e:
            print(f"❌ Failed to load mock data: {e}")
            return []


class SearchAPIClient:
    """Client for web search API (SerpAPI or Google Custom Search)"""

    def __init__(self, api_key: str, search_engine: str = "serpapi"):
        self.api_key = api_key
        self.search_engine = search_engine

        if search_engine == "serpapi":
            self.base_url = "https://serpapi.com/search"
        elif search_engine == "google":
            self.base_url = "https://www.googleapis.com/customsearch/v1"
        else:
            raise ValueError(f"Unsupported search engine: {search_engine}")

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Perform web search

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search result dictionaries
        """
        try:
            if self.search_engine == "serpapi":
                return self._search_serpapi(query, num_results)
            elif self.search_engine == "google":
                return self._search_google(query, num_results)
        except Exception as e:
            print(f"❌ Search failed for query '{query}': {e}")
            return []

    def _search_serpapi(self, query: str, num_results: int) -> List[Dict]:
        """Search using SerpAPI"""
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results,
            "hl": "zh-cn",  # Chinese language
            "gl": "cn"      # China region
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get("organic_results", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", "")
            })

        return results

    def _search_google(self, query: str, num_results: int) -> List[Dict]:
        """Search using Google Custom Search API"""
        params = {
            "key": self.api_key,
            "cx": os.getenv("GOOGLE_SEARCH_ENGINE_ID"),  # Custom search engine ID
            "q": query,
            "num": min(num_results, 10),  # Max 10 per request
            "lr": "lang_zh-CN"
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get("items", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", "")
            })

        return results

    def research_topic(self, keyword: str) -> Dict[str, str]:
        """
        Conduct comprehensive research on a trending topic

        Args:
            keyword: Trending keyword to research

        Returns:
            Dictionary with research findings
        """
        research = {
            "social_media": "",
            "news_background": "",
            "user_insights": "",
            "market_potential": ""
        }

        # Search 1: Context & Background
        query1 = f"{keyword} 微博 新闻背景 讨论"
        results1 = self.search(query1, num_results=5)

        if results1:
            context = []
            for r in results1:
                context.append(f"{r['title']}: {r['snippet']}")

            research["social_media"] = "\n".join(context[:2])
            research["news_background"] = "\n".join(context[2:])
        else:
            research["social_media"] = "⚠️ 搜索结果受限"
            research["news_background"] = "⚠️ 搜索结果受限"

        # Search 2: User Insights & Market Potential
        query2 = f"{keyword} 用户需求 产品 市场"
        results2 = self.search(query2, num_results=5)

        if results2:
            insights = []
            for r in results2:
                insights.append(f"{r['title']}: {r['snippet']}")

            research["user_insights"] = "\n".join(insights[:3])
            research["market_potential"] = "\n".join(insights[3:])
        else:
            research["user_insights"] = "⚠️ 搜索结果受限"
            research["market_potential"] = "基于通用市场分析"

        return research


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for filenames and display"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


def format_display_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for display in reports"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y年%m月%d日 %H:%M:%S")


def validate_product_concept(concept: Dict) -> bool:
    """
    Validate that a product concept has all required fields

    Args:
        concept: Product concept dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "product_name",
        "market_category",
        "target_audience",
        "description",
        "manufacturing_details",
        "total_score",
        "score_breakdown"
    ]

    for field in required_fields:
        if field not in concept or not concept[field]:
            return False

    # Validate score ranges
    breakdown = concept.get("score_breakdown", {})
    if not (0 <= breakdown.get("development_potential", -1) <= 40):
        return False
    if not (0 <= breakdown.get("interest_level", -1) <= 20):
        return False
    if not (0 <= breakdown.get("life_utility", -1) <= 20):
        return False
    if not (0 <= breakdown.get("production_ease", -1) <= 20):
        return False

    return True


def calculate_score_tier(score: int) -> Tuple[str, str, str]:
    """
    Calculate score tier and styling

    Args:
        score: Total score (0-100)

    Returns:
        Tuple of (tier_name, tier_badge, tier_class)
    """
    if score >= 80:
        return ("优秀", "🏆 优秀", "excellent")
    elif score >= 60:
        return ("良好", "⭐ 良好", "good")
    else:
        return ("其他", "📋 其他", "other")


def save_json_data(data: Dict, output_dir: str, filename: str) -> str:
    """
    Save data as JSON file

    Args:
        data: Data to save
        output_dir: Output directory
        filename: Filename

    Returns:
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath
