# API de Recrutement

Une API RESTful pour la gestion des recrutements, offres d'emploi et candidatures, développée avec Django et Django REST Framework.

## Fonctionnalités

- Authentification JWT sécurisée
- Mise à jour du profil
- Gestion des utilisateurs (candidats et recruteurs)
- Publication et recherche d'offres d'emploi
- Retrouver, lister les candidats/candidatures pour une offre
- Gestion des candidatures avec upload de CV
- Documentation API interactive (Swagger/OpenAPI)

## Prérequis

- Python 3.8+
- PostgreSQL
- pip

## Installation

1. Cloner le dépôt
```bash
git clone https://github.com/RomeoManoela/recrutement-api.git
cd recrutement-api
```

2. Créer un environnement virtuel
```bash
python -m venv venv # ou python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt # ou pip3 install -r requirements.txt
```

4. Créer un fichier `.env` à la racine du projet avec les variables suivantes:
```
DB_NAME=nom_de_votre_base
DB_USER=utilisateur_postgres
DB_PASSWORD=mot_de_passe_postgres
DB_HOST=localhost
DB_PORT=5432
```

5. Appliquer les migrations
```bash
python manage.py migrate # ou python3 manage.py migrate
```

7. Lancer le serveur de développement
```bash
python manage.py runserver 8001 # ou python3 manage.py runserver 8001
```

## Utilisation

### Documentation API

Une fois le serveur lancé, vous pouvez accéder à:

- Documentation Swagger: http://localhost:8000/api/docs/


### Endpoints principaux

- `/api/inscription/` - Inscription d'un nouvel utilisateur
- `/api/token-obtain/` - Obtention d'un token JWT
- `/api/token-refresh/` - Rafraîchissement d'un token JWT
- `/api/profil/` - Consulter et modifier son profil
- `/api/offres/` - Liste des offres d'emploi
- `/api/offres/<id>/` - Détail d'une offre
- `/api/candidat/candidatures/` - Liste des candidatures (pour candidats)
- `/api/recruteur/offres/` - Gestion des offres (pour recruteurs)

## Développement

### Structure du projet

```
api-recrutement/
├── api/                # Application principale
│   ├── migrations/     # Migrations Django
│   ├── __init__.py     # Fichier d'initialisation de l'application
│   ├── admin.py        # Interface d'administration Django
│   ├── apps.py         # Configuration de l'application
│   ├── models.py       # Modèles de données
│   ├── permissions.py  # Permissions personnalisées
│   ├── serializers.py  # Sérialiseurs RES
│   ├── tests.py        # Tests Unitaires et Integrations
│   ├── urls.py         # Routes API
│   └── views.py        # Vues API
├── config/             # Configuration du projet
│   ├── __init__.py     # Fichier d'initialisation du projet
│   ├── asgi.py         # Configuration ASGI
│   ├── settings.py     # Paramètres Django
│   ├── urls.py         # Routes principales
│   └── wsgi.py         # Configuration WSGI
└── manage.py           # Script de gestion Django
└── media/              # Fichiers media: les cvs
```

### Tests

Pour exécuter les tests:
```bash
python manage.py test
```

## Licence

[MIT](LICENSE)