import requests
from newspaper import Article as NewspaperArticle
from playwright.sync_api import sync_playwright


class ArticleSummarizer:
    def __init__(self, hf_api_key):
        if not hf_api_key:
            raise ValueError("Clé API Hugging Face manquante.")
        self.api_key = hf_api_key
        self.api_url = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def extract_article_content(self, url):
        # Méthode 1 : newspaper3k
        try:
            article = NewspaperArticle(url)
            article.download()
            article.parse()
            content = article.text[:2000]
            source = article.meta_data.get('source', article.source_url or 'Source inconnue')
            if content.strip():
                return content, source
        except Exception as e:
            print(f"Erreur newspaper3k : {e}")

        # Méthode 2 : requests
        try:
            response = requests.get(url, headers=self.request_headers, timeout=10)
            response.raise_for_status()
            article = NewspaperArticle(url)
            article.set_html(response.text)
            article.parse()
            content = article.text[:2000]
            source = article.source_url or 'Source inconnue'
            if content.strip():
                return content, source
        except Exception as e:
            print(f"Erreur requests : {e}")

        # Méthode 3 : playwright
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                content = page.content()
                browser.close()
                article = NewspaperArticle(url)
                article.set_html(content)
                article.parse()
                content = article.text[:2000]
                source = article.source_url or 'Source inconnue'
                if content.strip():
                    return content, source
        except Exception as e:
            print(f"Erreur playwright : {e}")
            return None, None

        return None, None

    def summarize_article(self, text, source):
        if not text:
            return f"Impossible de résumer : aucun contenu extrait. Source : {source}"

        payload = {
            "inputs": text,
            "parameters": {"max_length": 300, "min_length": 200}
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            summary = response.json()[0]["summary_text"]
            return f"{summary}\n\nSource : {source}"
        except requests.exceptions.HTTPError as e:
            print(f"Erreur API Hugging Face : {e}")
            return f"Erreur lors de la génération du résumé. Source : {source}"
        except (KeyError, IndexError) as e:
            print(f"Erreur de traitement de la réponse : {e}")
            return f"Erreur lors de la génération du résumé. Source : {source}"

    def get_article_summary(self, article_url):
        content, source = self.extract_article_content(article_url)
        if content:
            return self.summarize_article(content, source)
        return f"Impossible de résumer : contenu non extrait. Source : {source or 'Inconnue'}"