# Mise en place pas à pas

## 1. Créer le dépôt GitHub

1. Connecte-toi à GitHub et crée un dépôt vide nommé `veille-quantique`.
2. Ne coche pas l'ajout automatique d'un README : ce projet en contient déjà un.
3. Copie l'adresse HTTPS du dépôt.

## 2. Installer et tester sur ton ordinateur

Depuis le dossier du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.main --days 7 --limit 10
```

Le premier essai crée deux fichiers dans `reports/` : un rapport Markdown et son PDF. Sans clés, il utilise les flux RSS de secours et un mode de test sans analyse IA.

## 3. Utiliser Inoreader gratuitement

1. Dans Inoreader, abonne-toi à des sources sur le calcul quantique.
2. Regroupe-les dans un dossier ou avec un tag `Quantum`.
3. Ne crée pas de jeton API : l'API Inoreader n'est pas disponible avec le compte gratuit.
4. Le programme récupère gratuitement les flux RSS directs renseignés dans `config/sources.yml`. Tu peux en ajouter d'autres depuis les sites des organismes ou entreprises suivis.

## 4. Configurer OpenAI

1. Crée une clé API OpenAI avec un projet ayant une facturation active.
2. Pour un test PowerShell ponctuel, définis les deux variables :

```powershell
$env:OPENAI_API_KEY="ta_cle"
```

3. Relance `python -m src.main --days 7 --limit 10`.

Le programme donne à chaque article des scores de pertinence, nouveauté et importance, un résumé, une catégorie et une indication de qualité de source. Les liens d'origine restent dans le rapport pour que tu puisses vérifier chaque information.

## 5. Publier sur GitHub

```powershell
git init
git add .
git commit -m "Initialisation de la veille quantique"
git branch -M main
git remote add origin https://github.com/TON_COMPTE/veille-quantique.git
git push -u origin main
```

Dans GitHub, ouvre `Settings > Secrets and variables > Actions` et ajoute :

- `OPENAI_API_KEY`

`INOREADER_ACCESS_TOKEN` est uniquement nécessaire si tu passes plus tard à une offre incluant l'API.

Ouvre ensuite l'onglet `Actions`, sélectionne **Veille quantique hebdomadaire**, puis **Run workflow**. Si le test est bon, le workflow s'exécutera ensuite chaque vendredi. Il ajoutera les rapports au dépôt.

## 6. Préparer la preuve pour le portfolio

Conserve au moins deux PDF de semaines différentes. Dans ton portfolio, explique : le besoin de suivre les technologies émergentes, les sources sélectionnées, les mots-clés et exclusions, l'automatisation hebdomadaire, et un exemple de conclusion tirée d'un rapport. L'annexe fournie demande notamment une veille régulière, des outils de recherche approfondis et un environnement d'apprentissage expliqué.
