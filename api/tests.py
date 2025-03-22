from decimal import Decimal

from django.test import TestCase

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
