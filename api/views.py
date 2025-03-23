"""Vues pour les API"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Offre, Candidature
from .permissions import IsRecruteur, IsCandidat

User = get_user_model()
from .serializers import UserSerializer, OffreSerializer, CandidatureSerializer


# POUR LES AUTHENTICATIONS
@extend_schema(
    tags=["Authentification"],
    description="Inscription d'un nouvel utilisateur",
    request=UserSerializer,
    responses={201: UserSerializer},
)
class InscriptionAPIView(generics.CreateAPIView):
    """vue pour l'inscription d'un utilisateur"""

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# JWTs
@extend_schema(
    tags=["Authentification"],
    description="Obtention d'un token JWT",
    request=TokenObtainPairSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {"access": {"type": "string"}},
        }
    },
)
class PersonnaliseeObtenirTokenAPIView(TokenObtainPairView):
    """Vue personnalisée pour obtenir un token JWT"""

    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Surcharge de la méthode post pour stocker le refresh token dans un cookie http only
        pour plus de sécurité et ne renvoyer que l'access token dans le corps de la réponse
        """
        reponse: Response = super().post(request, *args, **kwargs)
        token_rafraichissement = reponse.data.pop("refresh")
        reponse.set_cookie(
            key="refresh",
            value=token_rafraichissement,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600 * 24 * 30,  # 30 jours
        )
        return reponse


@extend_schema(
    tags=["Authentification"],
    description="Rafraîchissement d'un token JWT",
    request=TokenRefreshSerializer,
    responses={200: {"type": "object", "properties": {"access": {"type": "string"}}}},
)
class PersonnaliseeRafraichirTokenAPIView(TokenRefreshView):
    """Vue personnalisée pour rafraîchir un token JWT"""

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Surcharge de la méthode post pour récupérer le refresh token depuis les cookies
        """
        request._full_data = {"refresh": request.COOKIES.get("refresh")}
        reponse: Response = super().post(request, *args, **kwargs)
        return reponse


# POUR LES UTILISATEURS
@extend_schema(
    tags=["Utilisateurs"],
    description="Consulter et modifier son profil",
    responses={200: UserSerializer},
)
class ProfileInfoModifierAPIView(generics.RetrieveUpdateAPIView):
    """Vue pour modifier les informations du profil d'un utilisateur"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# recruteurs
@extend_schema(
    tags=["Statistiques"],
    description="Statistiques pour le recruteur",
    responses={
        200: {
            "type": "object",
            "properties": {
                "total_offres": {"type": "integer"},
                "total_candidatures": {"type": "integer"},
                "candidatures_par_offre": {"type": "object"},
            },
        }
    },
)
class StatistiquesRecruteurAPIView(generics.RetrieveAPIView):
    """Vue pour obtenir des statistiques sur les offres d'un recruteur"""

    permission_classes = [IsRecruteur]

    def retrieve(self, request, *args, **kwargs):
        offres = Offre.objects.filter(recruteur=request.user)
        total_offres = offres.count()
        total_candidatures = Candidature.objects.filter(offre__in=offres).count()
        candidatures_par_offre = {
            offre.titre: offre.candidatures.count() for offre in offres
        }

        return Response(
            {
                "total_offres": total_offres,
                "total_candidatures": total_candidatures,
                "candidatures_par_offre": candidatures_par_offre,
            }
        )


@extend_schema(
    tags=["Candidatures"],
    description="Mettre à jour le statut d'une candidature",
    request=CandidatureSerializer,
    responses={200: CandidatureSerializer},
)
class MettreAJourStatutCandidatureAPIView(generics.UpdateAPIView):
    """Vue pour mettre à jour le statut d'une candidature"""

    permission_classes = [IsRecruteur]
    serializer_class = CandidatureSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Candidature.objects.filter(offre__recruteur=self.request.user)


@extend_schema(
    tags=["Candidatures"],
    description="Liste des candidatures pour une offre spécifique",
    responses={200: CandidatureSerializer(many=True)},
)
class ToutCandidaturesPostuleRecruteurAPIView(generics.ListAPIView):
    """Vue pour lister toutes les candidatures pour l'une de ses offres"""

    permission_classes = [IsRecruteur]
    serializer_class = CandidatureSerializer

    def get_queryset(self):
        offre_id = self.kwargs.get("offre_id")
        offre = get_object_or_404(Offre, id=offre_id, recruteur=self.request.user)
        return offre.candidatures.all()


@extend_schema(
    tags=["Candidats"],
    description="Liste des candidats ayant postulé à une offre",
    responses={200: UserSerializer(many=True)},
)
class ToutCandidatSurOffreRecruteurAPIView(generics.ListAPIView):
    """Vue pour lister tous les candidats qui ont postulé sur l'une offre de ses offres"""

    permission_classes = [IsRecruteur]
    serializer_class = UserSerializer

    def get_queryset(self):
        offre_id = self.kwargs.get("offre_id")
        offre = get_object_or_404(Offre, id=offre_id, recruteur=self.request.user)

        candidat_ids = offre.candidatures.values_list("candidat", flat=True)
        return User.objects.filter(id__in=candidat_ids)


# candidat
@extend_schema(
    tags=["Candidats"],
    description="Liste de tous les candidats",
    responses={200: UserSerializer(many=True)},
)
class ToutCandidatAPIView(generics.ListAPIView):
    """Vue pour lister tous les candidats"""

    permission_classes = [IsRecruteur]
    serializer_class = UserSerializer
    queryset = User.objects.filter(role="candidat")


@extend_schema(
    tags=["Candidats"],
    description="Détails d'un candidat spécifique",
    responses={200: UserSerializer},
)
class CandidatInfoAPIView(generics.RetrieveAPIView):
    """Vue pour afficher les informations d'un candidat"""

    permission_classes = [IsRecruteur]
    serializer_class = UserSerializer
    queryset = User.objects.filter(role="candidat")
    lookup_field = "pk"


# vues pour les offres
@extend_schema(
    tags=["Offres"],
    description="Liste et création des offres pour un recruteur",
    request=OffreSerializer,
    responses={200: OffreSerializer(many=True), 201: OffreSerializer},
)
class ListerCreerOffreRecruteurAPIView(generics.ListCreateAPIView):
    """Vue pour lister ou créer des offres pour un recruteur"""

    permission_classes = [IsRecruteur]
    serializer_class = OffreSerializer

    def perform_create(self, serializer):
        serializer.save(recruteur=self.request.user)

    def get_queryset(self):
        return Offre.objects.filter(recruteur=self.request.user)


@extend_schema(
    tags=["Offres"],
    description="Détail, modification et suppression d'une offre pour une offre d'un recruteur",
    request=OffreSerializer,
    responses={200: OffreSerializer, 204: None},
)
class RetrouverOffreRecruteurAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer une offre pour un recruteur"""

    permission_classes = [IsRecruteur]
    serializer_class = OffreSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Offre.objects.filter(recruteur=self.request.user)


@extend_schema(
    tags=["Offres"],
    description="Liste de toutes les offres disponibles",
    responses={200: OffreSerializer(many=True)},
)
class ListerToutesOffreAPIView(generics.ListAPIView):
    """Vue pour lister toutes les offres"""

    permission_classes = [IsAuthenticated]
    serializer_class = OffreSerializer
    queryset = Offre.objects.all()


@extend_schema(
    tags=["Offres"],
    description="Détail d'une offre spécifique",
    responses={200: OffreSerializer},
)
class DetailToutesOffreAPIView(generics.RetrieveAPIView):
    """Vue pour afficher les détails d'une offre pour tout le monde"""

    permission_classes = [IsAuthenticated]
    serializer_class = OffreSerializer
    queryset = Offre.objects.all()
    lookup_field = "pk"


@extend_schema(
    tags=["Offres"],
    description="Recherche avancée d'offres",
    responses={200: OffreSerializer(many=True)},
)
class ChercherOffreAPIView(generics.ListAPIView):
    """Vue pour chercher des offres par mot-clé"""

    permission_classes = [IsAuthenticated]
    serializer_class = OffreSerializer
    queryset = Offre.objects.all()
    search_fields = ["titre", "description"]
    filter_backends = [SearchFilter, DjangoFilterBackend]


# vues pour les candidatures
@extend_schema(
    tags=["Candidatures"],
    description="Postuler à une offre",
    request=CandidatureSerializer,
    responses={201: CandidatureSerializer},
)
class CreerCandidatureCandidatAPIView(generics.CreateAPIView):
    """Vue pour créer une candidature"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer
    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]  # Pour gérer les fichiers

    def perform_create(self, serializer):
        offre_id = self.kwargs.get("offre_id")
        print(offre_id)
        offre = get_object_or_404(Offre, id=offre_id)
        serializer.save(candidat=self.request.user, offre=offre)

    def get_queryset(self):
        return Candidature.objects.filter(candidat=self.request.user)


@extend_schema(
    tags=["Candidatures"],
    description="Liste des candidatures de l'utilisateur connecté",
    responses={200: CandidatureSerializer(many=True)},
)
class ListerCandidatureCandidatAPIView(generics.ListAPIView):
    """Vue pour lister les candidatures d'un candidat"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer

    def get_queryset(self):
        return Candidature.objects.filter(candidat=self.request.user)


@extend_schema(
    tags=["Candidatures"],
    description="Détail d'une candidature spécifique",
    responses={200: CandidatureSerializer},
)
class DetailCandidatureCandidatAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer une candidature pour un candidat"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Candidature.objects.filter(candidat=self.request.user)
