from django.urls import path

from . import views

urlpatterns = [
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
    path("offres/", views.ListerOffreAPIView.as_view(), name="offres"),
    path("offres/<int:pk>/", views.DetailOffreAPIView.as_view(), name="offre-detail"),
    path(
        "recruteur/offres/",
        views.ListerCreerOffreAPIView.as_view(),
        name="recruteur-offres",
    ),
    path(
        "recruteur/offres/<int:pk>/",
        views.OffreAPIView.as_view(),
        name="recruteur-offre-detail",
    ),
    # pour les candidatures
    path(
        "candidat/offres/<int:offre_id>/candidatures/",
        views.ListerCreerCandidatureAPIView.as_view(),
        name="candidat-candidatures",
    ),
    path(
        "candidat/offres/<int:offre_id>/candidatures/creer/",
        views.CreerCandidatureAPIView.as_view(),
        name="candidat-candidature-creer",
    ),
    path(
        "candidat/offres/<int:offre_id>/candidatures/<int:pk>/",
        views.CandidatureAPIView.as_view(),
        name="candidat-candidature-detail",
    ),
    path(
        "candidat/offres/<int:offre_id>/candidatures/<int:pk>/supprimer/",
        views.SupprimerCandidatureAPIView.as_view(),
        name="candidat-candidature-supprimer",
    ),
]
