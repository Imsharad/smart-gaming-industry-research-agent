"""
Knowledge Retrieval Tool - Database abstraction for UDA-Hub knowledge base operations
"""
import os
import json
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain_core.tools import tool
import sys

# Add the parent directory to the path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data.models.udahub import Knowledge


class KnowledgeRetrievalTool:
    """Tool for retrieving information from the UDA-Hub knowledge base"""
    
    def __init__(self, db_path: str = None, articles_path: str = None):
        if db_path is None:
            from utils.path_utils import get_core_db_path
            db_path = get_core_db_path()

        if articles_path is None:
            from utils.path_utils import find_project_root
            project_root = find_project_root()
            articles_path = os.path.join(project_root, 'data', 'external', 'cultpass_articles.jsonl')
        
        # Ensure we have absolute paths
        db_path = os.path.abspath(db_path)
        articles_path = os.path.abspath(articles_path)
        
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.articles_path = articles_path
        self._articles_cache = None
    
    def load_articles(self) -> List[Dict[str, Any]]:
        """Load articles from JSONL file"""
        if self._articles_cache is not None:
            return self._articles_cache
        
        articles = []
        try:
            if os.path.exists(self.articles_path):
                with open(self.articles_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            articles.append(json.loads(line))
            self._articles_cache = articles
        except Exception as e:
            print(f"Error loading articles: {e}")
            self._articles_cache = []
        
        return self._articles_cache
    
    def search_articles_by_keywords(self, keywords: List[str], max_results: int = 3) -> List[Dict[str, Any]]:
        """Search articles by keywords in title, content, or tags"""
        articles = self.load_articles()
        
        if not articles:
            return []
        
        # Convert keywords to lowercase for case-insensitive matching
        keywords = [kw.lower() for kw in keywords]
        
        matches = []
        for article in articles:
            score = 0
            title = article.get('title', '').lower()
            content = article.get('content', '').lower()
            tags = article.get('tags', '').lower()
            
            # Score based on keyword matches
            for keyword in keywords:
                # Higher score for title matches
                if keyword in title:
                    score += 3
                # Medium score for content matches
                if keyword in content:
                    score += 2
                # Lower score for tag matches
                if keyword in tags:
                    score += 1
            
            if score > 0:
                article_copy = article.copy()
                article_copy['relevance_score'] = score
                matches.append(article_copy)
        
        # Sort by relevance score and return top results
        matches.sort(key=lambda x: x['relevance_score'], reverse=True)
        return matches[:max_results]
    
    def search_articles_by_category(self, category: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search articles by category/tag"""
        articles = self.load_articles()
        category = category.lower()
        
        matches = []
        for article in articles:
            tags = article.get('tags', '').lower()
            if category in tags:
                matches.append(article)
        
        return matches[:max_results]
    
    def get_all_categories(self) -> List[str]:
        """Get all unique categories/tags from articles"""
        articles = self.load_articles()
        categories = set()
        
        for article in articles:
            tags = article.get('tags', '')
            if tags:
                # Split tags by comma and clean up
                article_tags = [tag.strip().lower() for tag in tags.split(',')]
                categories.update(article_tags)
        
        return sorted(list(categories))
    
    def get_article_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get specific article by exact title match"""
        articles = self.load_articles()
        
        for article in articles:
            if article.get('title', '').lower() == title.lower():
                return article
        
        return None


# Initialize the tool instance
knowledge_tool = KnowledgeRetrievalTool()


@tool
def search_knowledge_base(query: str, max_results: str = "3") -> str:
    """
    Search the CultPass knowledge base for relevant articles.
    
    Args:
        query: Search query containing keywords to find relevant articles
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        Formatted string with relevant knowledge base articles
    """
    try:
        max_results_int = int(max_results)
        max_results_int = min(max_results_int, 10)  # Cap at 10 for performance
    except ValueError:
        max_results_int = 3
    
    # Extract keywords from query
    keywords = [word.strip() for word in query.lower().split() if len(word.strip()) > 2]
    
    if not keywords:
        return "Please provide specific keywords to search for in the knowledge base."
    
    articles = knowledge_tool.search_articles_by_keywords(keywords, max_results_int)
    
    if not articles:
        return f"No articles found matching your query: '{query}'. Try different keywords or check available categories."
    
    response = f"Found {len(articles)} relevant article(s) for '{query}':\n\n"
    
    for i, article in enumerate(articles, 1):
        response += f"{i}. {article['title']}\n"
        response += f"   Relevance Score: {article.get('relevance_score', 0)}\n"
        response += f"   Content: {article['content'][:200]}...\n"  # First 200 chars
        response += f"   Tags: {article.get('tags', 'N/A')}\n\n"
    
    return response


@tool
def get_knowledge_categories() -> str:
    """
    Get all available categories/tags from the knowledge base.
    
    Returns:
        List of all available knowledge base categories
    """
    categories = knowledge_tool.get_all_categories()
    
    if not categories:
        return "No categories found in the knowledge base."
    
    response = "Available knowledge base categories:\n\n"
    
    # Group categories for better readability
    for i, category in enumerate(categories):
        if i % 3 == 0 and i > 0:
            response += "\n"
        response += f"• {category.title():<20} "
    
    response += f"\n\nTotal categories: {len(categories)}"
    response += "\n\nUse 'search_knowledge_by_category' to find articles in a specific category."
    
    return response


@tool
def search_knowledge_by_category(category: str, max_results: str = "5") -> str:
    """
    Search knowledge base articles by category/tag.
    
    Args:
        category: Category or tag to search for
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Articles in the specified category
    """
    try:
        max_results_int = int(max_results)
        max_results_int = min(max_results_int, 10)  # Cap at 10
    except ValueError:
        max_results_int = 5
    
    articles = knowledge_tool.search_articles_by_category(category, max_results_int)
    
    if not articles:
        available_categories = knowledge_tool.get_all_categories()
        return f"No articles found in category '{category}'. Available categories: {', '.join(available_categories[:10])}..."
    
    response = f"Found {len(articles)} article(s) in category '{category}':\n\n"
    
    for i, article in enumerate(articles, 1):
        response += f"{i}. {article['title']}\n"
        response += f"   {article['content'][:150]}...\n"  # First 150 chars
        response += f"   All tags: {article.get('tags', 'N/A')}\n\n"
    
    return response


@tool
def get_full_article(title: str) -> str:
    """
    Get the full content of a specific knowledge base article by title.
    
    Args:
        title: Exact title of the article to retrieve
        
    Returns:
        Full article content with all details
    """
    article = knowledge_tool.get_article_by_title(title)
    
    if not article:
        return f"Article not found: '{title}'. Use 'search_knowledge_base' to find similar articles."
    
    response = f"Article: {article['title']}\n"
    response += "=" * (len(article['title']) + 9) + "\n\n"
    response += f"{article['content']}\n\n"
    response += f"Tags: {article.get('tags', 'N/A')}\n"
    
    return response