from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Offre, Candidature
from .permissions import IsRecruteur, IsCandidat

User = get_user_model()
from .serializers import UserSerializer, OffreSerializer, CandidatureSerializer


class InscriptionAPIView(generics.CreateAPIView):
    """vue pour l'inscription d'un utilisateur"""

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class PersonnaliseeRafraichirTokenAPIView(TokenRefreshView):
    """Vue personnalisée pour rafraîchir un token JWT"""

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Surcharge de la méthode post pour récupérer le refresh token depuis les cookies
        """
        request._full_data = {"refresh": request.COOKIES.get("refresh")}
        reponse: Response = super().post(request, *args, **kwargs)
        return reponse


class ListerCreerOffreAPIView(generics.ListCreateAPIView):
    """Vue pour lister et créer des offres pour un recruteur"""

    permission_classes = [IsRecruteur]
    serializer_class = OffreSerializer

    def perform_create(self, serializer):
        serializer.save(recruteur=self.request.user)

    def get_queryset(self):
        return Offre.objects.filter(recruteur=self.request.user)


class ListerOffreAPIView(generics.ListAPIView):
    """Vue pour lister toutes les offres"""

    permission_classes = [IsAuthenticated]
    serializer_class = OffreSerializer
    queryset = Offre.objects.all()


class OffreAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer une offre"""

    permission_classes = [IsRecruteur]
    serializer_class = OffreSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Offre.objects.filter(recruteur=self.request.user)


class DetailOffreAPIView(generics.RetrieveAPIView):
    """Vue pour afficher les détails d'une offre"""

    permission_classes = [IsAuthenticated]
    serializer_class = OffreSerializer
    queryset = Offre.objects.all()
    lookup_field = "pk"


class ListerCreerCandidatureAPIView(generics.ListCreateAPIView):
    """Vue pour lister et créer des candidatures pour un candidat"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer


class CreerCandidatureAPIView(generics.CreateAPIView):
    """Vue pour créer une candidature"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer
    parser_classes = [MultiPartParser, FormParser]  # Pour gérer les fichiers

    def perform_create(self, serializer):
        offre_id = self.kwargs.get("offre_id")
        offre = get_object_or_404(Offre, id=offre_id)
        serializer.save(candidat=self.request.user, offre=offre)


class CandidatureAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer une candidature"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Candidature.objects.filter(candidat=self.request.user)


class SupprimerCandidatureAPIView(generics.DestroyAPIView):
    """Vue pour supprimer une candidature"""

    permission_classes = [IsCandidat]
    serializer_class = CandidatureSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Candidature.objects.filter(candidat=self.request.user)
