from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import User, Offre, Candidature


class UserModelTest(TestCase):
    def setUp(self):
        self.candidat = User.objects.create_user(
            username="candidat1",
            email="candidat1@example.com",
            password="password123",
            role="candidat",
            bio="Développeur Python",
            competences="Django, Flask, Python",
        )

        self.recruteur = User.objects.create_user(
            username="recruteur1",
            email="recruteur1@example.com",
            password="password123",
            role="recruteur",
        )

    def test_user_creation(self):
        self.assertEqual(self.candidat.username, "candidat1")
        self.assertEqual(self.candidat.role, "candidat")
        self.assertEqual(self.recruteur.role, "recruteur")


class OffreModelTest(TestCase):
    def setUp(self):
        self.recruteur = User.objects.create_user(
            username="recruteur1",
            email="recruteur1@example.com",
            password="password123",
            role="recruteur",
        )

        self.offre = Offre.objects.create(
            titre="Développeur Django",
            description="Poste de développeur Django senior",
            salaire=Decimal("60000.00"),
            competences_requises="Django, Python, JavaScript",
            recruteur=self.recruteur,
        )

    def test_offre_creation(self):
        self.assertEqual(self.offre.titre, "Développeur Django")
        self.assertEqual(self.offre.recruteur, self.recruteur)
        self.assertEqual(Offre.objects.count(), 1)


class CandidatureModelTest(TestCase):
    def setUp(self):
        self.candidat = User.objects.create_user(
            username="candidat1",
            email="candidat1@example.com",
            password="password123",
            role="candidat",
        )

        self.recruteur = User.objects.create_user(
            username="recruteur1",
            email="recruteur1@example.com",
            password="password123",
            role="recruteur",
        )

        self.offre = Offre.objects.create(
            titre="Développeur Django",
            description="Poste de développeur Django senior",
            salaire=Decimal("60000.00"),
            recruteur=self.recruteur,
        )

        self.candidature = Candidature.objects.create(
            candidat=self.candidat, offre=self.offre
        )

    def test_candidature_creation(self):
        self.assertEqual(self.candidature.candidat, self.candidat)
        self.assertEqual(self.candidature.offre, self.offre)
        self.assertTrue(hasattr(self.candidature, "date_creation"))


class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.inscription_url = reverse("inscription")
        self.token_url = reverse("token")

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "role": "candidat",
        }

    def test_inscription(self):
        response = self.client.post(self.inscription_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_obtenir_token(self):
        # Créer un utilisateur
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            role="candidat",
        )

        # Obtenir un token
        response = self.client.post(
            self.token_url,
            {"username": "testuser", "password": "testpassword123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.cookies)


class OffreAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Créer un recruteur
        self.recruteur = User.objects.create_user(
            username="recruteur",
            email="recruteur@example.com",
            password="password123",
            role="recruteur",
        )

        # Créer un candidat
        self.candidat = User.objects.create_user(
            username="candidat",
            email="candidat@example.com",
            password="password123",
            role="candidat",
        )

        # Créer une offre
        self.offre = Offre.objects.create(
            titre="Développeur Full Stack",
            description="Poste de développeur Full Stack",
            salaire=Decimal("70000.00"),
            competences_requises="React, Django, Python",
            recruteur=self.recruteur,
        )

        # URLs
        self.liste_offres_url = reverse("offres")
        self.detail_offre_url = reverse("offre-detail", kwargs={"pk": self.offre.pk})
        self.recruteur_offres_url = reverse("recruteur-offres")

    def test_liste_offres_non_authentifie(self):
        response = self.client.get(self.liste_offres_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_liste_offres_authentifie(self):
        self.client.force_authenticate(user=self.candidat)
        response = self.client.get(self.liste_offres_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_offre_recruteur(self):
        self.client.force_authenticate(user=self.recruteur)
        nouvelle_offre = {
            "titre": "Développeur Backend",
            "description": "Poste de développeur backend",
            "salaire": "65000.00",
            "competences_requises": "Django, Python, PostgreSQL",
        }
        response = self.client.post(
            self.recruteur_offres_url, nouvelle_offre, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offre.objects.count(), 2)

    def test_creation_offre_candidat_interdit(self):
        self.client.force_authenticate(user=self.candidat)
        nouvelle_offre = {
            "titre": "Développeur Backend",
            "description": "Poste de développeur backend",
            "salaire": "65000.00",
            "competences_requises": "Django, Python, PostgreSQL",
        }
        response = self.client.post(
            self.recruteur_offres_url, nouvelle_offre, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CandidatureAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Créer un recruteur
        self.recruteur = User.objects.create_user(
            username="recruteur",
            email="recruteur@example.com",
            password="password123",
            role="recruteur",
        )

        # Créer un candidat
        self.candidat = User.objects.create_user(
            username="candidat",
            email="candidat@example.com",
            password="password123",
            role="candidat",
        )

        # Créer une offre
        self.offre = Offre.objects.create(
            titre="Développeur Full Stack",
            description="Poste de développeur Full Stack",
            salaire=Decimal("70000.00"),
            competences_requises="React, Django, Python",
            recruteur=self.recruteur,
        )

        # URLs
        self.creer_candidature_url = reverse(
            "creer-candidature", kwargs={"offre_id": self.offre.pk}
        )
        self.liste_candidatures_url = reverse("list-candidatures")

    def test_creer_candidature(self):
        self.client.force_authenticate(user=self.candidat)
        response = self.client.post(self.creer_candidature_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidature.objects.count(), 1)

    def test_creer_candidature_recruteur_interdit(self):
        self.client.force_authenticate(user=self.recruteur)
        response = self.client.post(self.creer_candidature_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_candidatures_candidat(self):
        # Créer une candidature
        Candidature.objects.create(candidat=self.candidat, offre=self.offre)

        self.client.force_authenticate(user=self.candidat)
        response = self.client.get(self.liste_candidatures_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_candidature_double_impossible(self):
        # Créer une première candidature
        Candidature.objects.create(candidat=self.candidat, offre=self.offre)

        # Tenter de créer une seconde candidature pour la même offre
        self.client.force_authenticate(user=self.candidat)
        response = self.client.post(self.creer_candidature_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Candidature.objects.count(), 1)
