
# SportNews API SDK

Un SDK Python officiel pour l'API SportNews, offrant un accès simplifié aux actualités sportives en temps réel. Cette bibliothèque permet aux développeurs d'intégrer facilement des flux d'actualités sportives dans leurs applications Python.

## Installation

```bash
pip install sportnews-api
```

## Utilisation

```python
from sportnews import SportNewsAPI

# Initialisation du client avec votre clé API
api = SportNewsAPI('VOTRE_CLE_API')

# Récupération des dernières actualités
news = api.get_latest_news(
    limit=10,
    language='fr'
)

# Affichage d'un article
article = news[0]
print(f"Titre: {article.title}")
print(f"Date: {article.published}")
print(f"Description: {article.description}")
print(f"Sport: {article.sport}")
```

## Fonctionnalités principales

- Récupération des dernières actualités sportives
- Recherche d'articles avec filtres avancés
- Support multilingue (FR, EN, ES, IT, DE)
- Pagination des résultats
- Gestion des erreurs robuste
- Validation automatique des paramètres
- Support des dates pour la recherche temporelle

## Langues supportées

- Français (`fr`)
- Anglais (`en`)
- Espagnol (`es`)
- Italien (`it`)
- Allemand (`de`)

## Licence

Ce projet est sous licence MIT.

## Support

- Documentation : [https://docs.sportnews-api.com](https://docs.sportnews-api.com)
- Support email : support@sportnews-api.com

Développé et maintenu par l'équipe SportNews API.
