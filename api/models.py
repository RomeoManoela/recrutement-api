from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):

    CHOIX_ROLES = (
        ("candidat", "Candidat"),
        ("recruteur", "Recruteur"),
    )

    role = models.CharField(max_length=100, choices=CHOIX_ROLES, default="candidat")
    bio = models.TextField(blank=True, null=True)
    competences = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)  # optionel pour des recruteurs


class Offre(models.Model):

    titre = models.CharField(max_length=100)
    description = models.TextField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    competences_requises = models.TextField(blank=True, null=True)
    recruteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offres")
    date_creation = models.DateTimeField(auto_now_add=True)


class Candidature(models.Model):

    candidat = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="candidatures"
    )
    offre = models.ForeignKey(
        Offre, on_delete=models.CASCADE, related_name="candidatures"
    )
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)  # optionel
    lettre_motivation = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
