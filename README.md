"Automate Post LinkedIn"

Une application Python pour automatiser la création de posts LinkedIn en scrapant et résumant des articles sur des thèmes d'actualité, via une interface graphique tkinter.

Fonctionnalités :

👉Scraping d'articles : Recherche et extraction d'articles basés sur un thème d'actualité avec newspaper3k.

👉Résumé automatique : Génère des résumés d'articles pour les posts, lorsque possible.

👉Interface utilisateur : Interface graphique intuitive avec tkinter.

👉Préparation de posts : Crée des posts prêts à être publiés manuellement ou via une API LinkedIn.


-Prérequis-

Python : Version 3.13 ou supérieure.

Système d'exploitation : Windows (testé), compatible Linux/Mac avec ajustements.

Connexion Internet : Requise pour le scraping d'articles.


-Installation-

Clonez le dépôt :

git clone https://github.com/DevBigDaddy/applinkedinpostautomatic.git
cd applinkedinpostautomatic


Créez un environnement virtuel :

python -m venv venv


Activez l'environnement virtuel :

Windows :.\venv\Scripts\activate


Linux/Mac :source venv/bin/activate




Installez les dépendances :
pip install -r requirements.txt



-Utilisation-

Lancez l'application :

python ui.py

Cela ouvre l'interface graphique tkinter.

Instructions dans l'interface :

Choisissez un thème d'actualité (par exemple, "intelligence artificielle", "économie").

L'application scrape des articles pertinents et génère un résumé ou un post.

Exportez ou publiez manuellement sur LinkedIn.



-Limitations-

Résumés impossibles dans certains cas : Certains sites détectent les bots (comme newspaper3k) et bloquent le scraping, rendant le résumé impossible. Dans ce cas, l'application peut ne pas trouver d'articles utilisables pour certains thèmes.
Publication LinkedIn : La publication automatique nécessite une intégration avec l'API LinkedIn (non implémentée par défaut).

-Structure du projet-

ui.py : Fichier principal pour l'interface graphique.

article_summarizer.py : Module pour le scraping et le résumé d'articles.

requirements.txt : Liste des dépendances.

.gitignore : Exclut les fichiers inutiles (.venv, __pycache__, etc.).

Dépendances

newspaper3k : Scraping d'articles.

lxml et lxml_html_clean : Parsing HTML.

tkinter : Interface graphique (inclus avec Python).Consultez requirements.txt pour la liste complète.

Développement

Améliorations possibles :

Intégration avec l'API LinkedIn pour une publication automatique.

Contournement des protections anti-bot pour plus de sites.

Amélioration des résumés avec des modèles IA.


Contribuer :

Forkez le dépôt.

Créez une branche : git checkout -b ma-fonctionnalite.

Poussez et soumettez une Pull Request.



-Problèmes courants-

Erreur tkinter : Vérifiez que Tcl/Tk est installé avec Python.

Erreur lxml.html.clean : Installez lxml_html_clean (pip install lxml_html_clean).

Échec du scraping : Certains sites bloquent les bots, essayez un autre thème ou vérifiez votre connexion.

Licence

MIT License (à ajouter si vous choisissez cette licence).

Contact

Auteur : DevBigDaddy
GitHub : DevBigDaddy
Pour des questions, ouvrez une issue sur ce dépôt.

