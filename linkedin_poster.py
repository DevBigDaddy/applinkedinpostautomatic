from playwright.sync_api import sync_playwright
import time


class LinkedInPoster:
    def __init__(self, email, password):
        if not email or not password:
            raise ValueError("Identifiants LinkedIn manquants.")
        self.email = email
        self.password = password

    def post_article(self, article_title, article_summary, article_url):
        post_content = (
            f"📢 Nouvelle découverte intéressante : {article_title}\n\n"
            f"{article_summary}\n\n"
            f"Lisez l'article complet ici : {article_url}\n"
            f"#Actualité #Technologie #IA"
        )

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                print("Navigation vers la page de connexion LinkedIn...")
                page.goto("https://www.linkedin.com/login", timeout=60000)

                print("Remplissage des identifiants...")
                page.fill('input[name="session_key"]', self.email)
                page.fill('input[name="session_password"]', self.password)
                page.click('button[type="submit"]')
                time.sleep(5)

                print("Vérification de la connexion...")
                if "feed" not in page.url:
                    raise ValueError(
                        "Échec de la connexion à LinkedIn. Vérifie tes identifiants ou la présence d'une authentification à deux facteurs.")

                print("Navigation vers la page de flux...")
                page.goto("https://www.linkedin.com/feed/", timeout=60000)
                time.sleep(2)

                print("Clic sur le champ de publication...")
                page.click('div[class*="share-box-feed-entry"]', timeout=10000)
                time.sleep(1)

                print("Remplissage du contenu du post...")
                page.fill('div[role="textbox"]', post_content)
                time.sleep(1)

                print("Clic sur le bouton Publier...")
                page.click('button[class*="share-actions__primary-action"]', timeout=10000)
                time.sleep(5)

                print("Post publié avec succès sur LinkedIn !")
                return True

            except Exception as e:
                print(f"Erreur lors de la publication sur LinkedIn : {str(e)}")
                return False
            finally:
                browser.close()