from django.urls import path

from . import views

urlpatterns = [
    # pour les utilisateurs
    path("profil/", views.ProfileInfoModifierAPIView.as_view(), name="profil"),
    path("candidats/", views.ToutCandidatAPIView.as_view(), name="candidats"),
    path("candidats/<int:pk>/", views.CandidatInfoAPIView.as_view(), name="candidat"),
    path(
        "recruteur/statistiques/",
        views.StatistiquesRecruteurAPIView.as_view(),
        name="statistiques",
    ),
    # pour les authentications
    path("inscription/", views.InscriptionAPIView.as_view(), name="inscription"),
    path(
        "token-obtain/", views.PersonnaliseeObtenirTokenAPIView.as_view(), name="token"
    ),
    path(
        "token-refresh/",
        views.PersonnaliseeRafraichirTokenAPIView.as_view(),
        name="refresh",
    ),
    # pour les offres
    path(
        "recruteur/offres/<int:offre_id>/candidatures/",
        views.ToutCandidaturesPostuleRecruteurAPIView.as_view(),
        name="candidats-postule",
    ),
    path(
        "recruteur/offres/<int:offre_id>/candidats/",
        views.ToutCandidatSurOffreRecruteurAPIView.as_view(),
        name="candidats-offre",
    ),
    path("offres/rechercher/", views.ChercherOffreAPIView.as_view(), name="recherche"),
    path(
        "offres/", views.ListerToutesOffreAPIView.as_view(), name="offres"
    ),  # toutes les offres
    path(
        "offres/<int:pk>/",
        views.DetailToutesOffreAPIView.as_view(),
        name="offre-detail",
    ),  # toutes les offres
    path(
        "recruteur/offres/",
        views.ListerCreerOffreRecruteurAPIView.as_view(),
        name="recruteur-offres",
    ),
    path(
        "recruteur/offres/<int:pk>/",
        views.RetrouverOffreRecruteurAPIView.as_view(),
        name="recruteur-offre-detail",
    ),
    # pour les candidatures
    path(
        "offres/<int:offre_id>/candidater/",
        views.CreerCandidatureCandidatAPIView.as_view(),
        name="creer-candidature",
    ),
    path(
        "candidatures/<int:pk>/mettre-a-jour-statut/",
        views.MettreAJourStatutCandidatureAPIView.as_view(),
        name="mettre-a-jour-statut",
    ),
    path(
        "candidatures/<int:pk>/",
        views.DetailCandidatureCandidatAPIView.as_view(),
        name="candidature-detail",
    ),
    path(
        "candidatures/",
        views.ListerCandidatureCandidatAPIView.as_view(),
        name="list-candidatures",
    ),
]
