import tkinter as tk
from tkinter import messagebox
import webbrowser
from linkedin_news_post_generator import NewsApp, Article
from article_summarizer import ArticleSummarizer
from linkedin_poster import LinkedInPoster


class NewsAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recherche d'Articles d'Actualité")
        self.news_app = None
        self.summarizer = None
        self.linkedin_poster = None
        self.articles = []
        self.current_query = "artificial intelligence"
        self.current_summary = ""

        # Configurer la fenêtre
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Pop-up pour la clé API Hugging Face
        messagebox.showinfo(
            "Clé API Hugging Face",
            "Pour obtenir votre clé API Hugging Face :\n1. Allez sur https://huggingface.co/\n2. Connectez-vous ou créez un compte\n3. Allez dans 'Settings' > 'Access Tokens'\n4. Créez un token avec l'option 'Read'\n5. Copiez et collez la clé ci-dessous."
        )

        # Frame pour les clés et identifiants
        self.credentials_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.credentials_frame.pack(pady=10)

        # Clé API NewsAPI
        tk.Label(
            self.credentials_frame,
            text="Clé API NewsAPI :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(anchor=tk.W, padx=5)
        self.api_key_entry = tk.Entry(
            self.credentials_frame,
            width=40,
            font=("Helvetica", 12),
            show="*"
        )
        self.api_key_entry.pack(anchor=tk.W, padx=5)

        # Clé API Hugging Face
        tk.Label(
            self.credentials_frame,
            text="Clé API Hugging Face :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(anchor=tk.W, padx=5)
        self.hf_api_key_entry = tk.Entry(
            self.credentials_frame,
            width=40,
            font=("Helvetica", 12),
            show="*"
        )
        self.hf_api_key_entry.pack(anchor=tk.W, padx=5)

        # Email LinkedIn
        tk.Label(
            self.credentials_frame,
            text="Email LinkedIn :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(anchor=tk.W, padx=5)
        self.linkedin_email_entry = tk.Entry(
            self.credentials_frame,
            width=40,
            font=("Helvetica", 12)
        )
        self.linkedin_email_entry.pack(anchor=tk.W, padx=5)

        # Mot de passe LinkedIn
        tk.Label(
            self.credentials_frame,
            text="Mot de passe LinkedIn :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(anchor=tk.W, padx=5)
        self.linkedin_password_entry = tk.Entry(
            self.credentials_frame,
            width=40,
            font=("Helvetica", 12),
            show="*"
        )
        self.linkedin_password_entry.pack(anchor=tk.W, padx=5)

        # Bouton pour valider les identifiants
        tk.Button(
            self.credentials_frame,
            text="Valider les identifiants",
            font=("Helvetica", 12),
            command=self.validate_credentials
        ).pack(anchor=tk.W, pady=5, padx=5)

        # Frame pour la recherche
        self.search_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.search_frame.pack(pady=10)

        tk.Label(
            self.search_frame,
            text="Rechercher un sujet :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(
            self.search_frame,
            width=30,
            font=("Helvetica", 12)
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.insert(0, "artificial intelligence")

        tk.Button(
            self.search_frame,
            text="Rechercher",
            font=("Helvetica", 12),
            command=self.search_articles
        ).pack(side=tk.LEFT, padx=5)

        # Titre
        tk.Label(
            self.root,
            text="Top 10 des articles récents",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)

        # Frame pour la liste
        self.list_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Liste des articles
        self.article_listbox = tk.Listbox(
            self.list_frame,
            width=80,
            height=10,
            font=("Helvetica", 12),
            selectmode=tk.SINGLE
        )
        self.article_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.article_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.article_listbox.yview)

        # Zone pour afficher le résumé
        self.summary_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.summary_frame.pack(pady=10, padx=10, fill=tk.BOTH)

        tk.Label(
            self.summary_frame,
            text="Résumé de l'article :",
            font=("Helvetica", 12),
            bg="#f0f0f0"
        ).pack(anchor=tk.W)

        self.summary_text = tk.Text(
            self.summary_frame,
            width=80,
            height=5,
            font=("Helvetica", 12),
            wrap=tk.WORD
        )
        self.summary_text.pack(fill=tk.BOTH)

        # Boutons d'action
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        tk.Button(
            self.button_frame,
            text="Ouvrir l'article sélectionné",
            font=("Helvetica", 12),
            command=self.open_article
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.button_frame,
            text="Résumer l'article",
            font=("Helvetica", 12),
            command=self.summarize_article
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.button_frame,
            text="Publier sur LinkedIn",
            font=("Helvetica", 12),
            command=self.post_to_linkedin
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.button_frame,
            text="Rafraîchir les articles",
            font=("Helvetica", 12),
            command=self.load_articles
        ).pack(side=tk.LEFT, padx=5)

    def validate_credentials(self):
        api_key = self.api_key_entry.get().strip()
        hf_api_key = self.hf_api_key_entry.get().strip()
        linkedin_email = self.linkedin_email_entry.get().strip()
        linkedin_password = self.linkedin_password_entry.get().strip()

        if not api_key:
            messagebox.showerror("Erreur", "Veuillez entrer une clé API NewsAPI valide.")
            return
        if not hf_api_key:
            messagebox.showerror("Erreur", "Veuillez entrer une clé API Hugging Face valide.")
            return
        if not linkedin_email or not linkedin_password:
            messagebox.showerror("Erreur", "Veuillez entrer un email et un mot de passe LinkedIn valides.")
            return

        try:
            self.news_app = NewsApp(api_key)
            self.summarizer = ArticleSummarizer(hf_api_key)
            self.linkedin_poster = LinkedInPoster(linkedin_email, linkedin_password)
            self.load_articles()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def search_articles(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Avertissement", "Veuillez entrer un mot-clé pour la recherche.")
            return
        self.current_query = query
        self.load_articles()

    def load_articles(self):
        if not self.news_app:
            messagebox.showerror("Erreur", "Veuillez valider les identifiants d'abord.")
            return

        self.article_listbox.delete(0, tk.END)
        articles = self.news_app.news_fetcher.fetch_news(self.current_query)
        if not articles:
            messagebox.showerror("Erreur",
                                 f"Aucun article trouvé pour '{self.current_query}'. Vérifiez votre clé API ou connexion.")
            return

        self.articles = self.news_app.news_fetcher.sort_by_popularity(articles)
        if not self.articles:
            messagebox.showerror("Erreur", "Aucun article valide trouvé.")
            return

        for i, article in enumerate(self.articles, 1):
            self.article_listbox.insert(tk.END,
                                        f"{i}. {article.title} ({article.source}) - {article.published_at.strftime('%Y-%m-%d')}")

    def open_article(self):
        selection = self.article_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aucun sélection", "Veuillez sélectionner un article.")
            return

        index = selection[0]
        article = self.articles[index]
        if article.url and article.url != "#":
            webbrowser.open(article.url)
        else:
            messagebox.showerror("Erreur", "URL invalide pour cet article.")

    def summarize_article(self):
        selection = self.article_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aucun sélection", "Veuillez sélectionner un article.")
            return

        index = selection[0]
        article = self.articles[index]
        try:
            self.current_summary = self.summarizer.get_article_summary(article.url)
        except Exception as e:
            self.current_summary = f"Erreur lors de la récupération du contenu : {str(e)}. Source : {article.source}"

        # Mettre à jour la zone de texte
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, self.current_summary)

    def post_to_linkedin(self):
        selection = self.article_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aucun sélection", "Veuillez sélectionner un article.")
            return

        index = selection[0]
        article = self.articles[index]
        if not self.current_summary:
            messagebox.showwarning("Aucun résumé", "Veuillez d'abord générer un résumé pour l'article.")
            return

        print("Tentative de publication sur LinkedIn...")
        try:
            success = self.linkedin_poster.post_article(article.title, self.current_summary, article.url)
            if success:
                messagebox.showinfo("Succès", "Article publié sur LinkedIn !")
            else:
                messagebox.showerror("Erreur", "Échec de la publication sur LinkedIn.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la publication : {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsAppUI(root)
    root.mainloop()