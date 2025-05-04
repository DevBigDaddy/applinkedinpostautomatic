import requests
from datetime import datetime

class Article:
    def __init__(self, title, url, published_at, source):
        self.title = title
        self.url = url
        self.published_at = published_at
        self.source = source

    def __str__(self):
        return f"{self.title} ({self.source}) - {self.published_at.strftime('%Y-%m-%d')} - {self.url}"

class NewsFetcher:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Clé API NewsAPI manquante. Fournissez une clé via l'interface.")
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, query="artificial intelligence", limit=10):
        params = {
            "q": query,
            "apiKey": self.api_key,
            "sortBy": "publishedAt",
            "pageSize": limit
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            articles_data = response.json().get("articles", [])
            articles = []
            excluded_sources = ["Forbes", "Bloomberg"]
            for article in articles_data:
                source_name = article["source"].get("name", "Inconnue")
                if source_name in excluded_sources:
                    continue
                try:
                    published_at = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                    articles.append(Article(
                        title=article.get("title", "Sans titre"),
                        url=article.get("url", "#"),
                        published_at=published_at,
                        source=source_name
                    ))
                except (KeyError, ValueError) as e:
                    print(f"Erreur lors du traitement d'un article : {e}")
                    continue
            return articles
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Clé API NewsAPI invalide. Vérifiez votre clé sur newsapi.org.")
            print(f"Erreur lors de la récupération des actualités : {e}")
            return []
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des actualités : {e}")
            return []

    def sort_by_popularity(self, articles):
        return sorted(articles, key=lambda x: x.published_at, reverse=True)[:10]

class NewsApp:
    def __init__(self, news_api_key):
        self.news_fetcher = NewsFetcher(news_api_key)

    def display_articles(self, articles):
        print("\nTop 10 des articles récents :")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article}")

    def run(self, query="artificial intelligence"):
        articles = self.news_fetcher.fetch_news(query)
        if not articles:
            print("Aucun article récupéré. Vérifiez votre clé API NewsAPI ou connexion.")
            return

        articles = self.news_fetcher.sort_by_popularity(articles)
        if not articles:
            print("Aucun article valide trouvé.")
            return

        self.display_articles(articles)