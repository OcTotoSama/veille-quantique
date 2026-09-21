# Veille informatique quantique

Cette application produit chaque semaine une veille documentée sur les ordinateurs et le calcul quantiques. Elle est conçue comme une réalisation de portfolio : les règles de sélection, les sources, le code et les rapports datés sont tous traçables.

## Architecture

```text
Inoreader (RSS/API) -> collect.py -> articles des 7 jours -> filter.py
-> OpenAI API (pertinence, nouveauté, importance, résumé, source)
-> rapport Markdown -> PDF -> reports/ -> GitHub
```

## Mise en route locale

1. Créer un environnement Python puis installer les dépendances :

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Avec un compte Inoreader gratuit, tu peux t'abonner aux mêmes flux pour ta lecture personnelle. L'automatisation utilise directement les flux RSS publics de `config/sources.yml` : aucune clé Inoreader n'est nécessaire.

3. Créer un fichier `.env` local (jamais versionné) avec :

   ```text
   OPENAI_API_KEY=...
   ```

   Dans PowerShell, charger les variables pour la session :

   ```powershell
   $env:OPENAI_API_KEY="..."
   ```

4. Lancer la veille :

   ```powershell
   python -m src.main --days 7 --limit 10
   ```

Les fichiers `reports/AAAA-MM-JJ.md` et `reports/AAAA-MM-JJ.pdf` sont créés. Sans clé OpenAI, le programme reste exécutable : il génère une analyse de secours, clairement moins qualitative, pratique pour tester l'installation.

## Configuration

- `config/sources.yml` : flux RSS publics utilisés gratuitement. L'API Inoreader est facultative et réservée aux comptes qui y ont accès.
- `config/keywords.yml` : termes principaux, secondaires et exclusions ; modifier ce fichier rend le filtrage explicable au jury.
- `prompts/analyse.txt` : consignes imposées au modèle ; les scores sont pondérés à 45 % pertinence, 25 % nouveauté et 30 % importance.

## Publication GitHub

1. Créer un dépôt GitHub vide nommé `veille-quantique`, puis pousser ce dossier.
2. Dans **Settings > Secrets and variables > Actions**, créer le secret `OPENAI_API_KEY`. Le secret `INOREADER_ACCESS_TOKEN` est facultatif et ne sert que pour les comptes Inoreader ayant accès à l'API.
3. Dans **Actions**, lancer une première fois le workflow **Veille quantique hebdomadaire** via `workflow_dispatch`.
4. Le workflow s'exécute ensuite chaque vendredi à 07:00 UTC et versionne les PDF dans `reports/`.

Ne déposer aucune clé dans un fichier suivi par Git. Pour une démonstration BTS, conserver au moins deux rapports datés, commenter les évolutions des mots-clés et expliquer les choix de sources.
