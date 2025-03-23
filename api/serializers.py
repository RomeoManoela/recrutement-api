from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Offre, Candidature

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "role",
            "bio",
            "competences",
            "experience",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = "__all__"
        extra_kwargs = {"recruteur": {"read_only": True}}

    def create(self, validated_data):
        offre = Offre.objects.create(**validated_data)
        return offre


class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = "__all__"
        read_only_fields = ["id", "date_creation", "candidat", "offre"]

    def create(self, validated_data):
        # Vérifier si une candidature existe déjà pour cette offre et ce candidat
        candidat = validated_data.get("candidat")
        offre = validated_data.get("offre")

        if Candidature.objects.filter(candidat=candidat, offre=offre).exists():
            raise serializers.ValidationError("Vous avez déjà postulé à cette offre.")

        return super().create(validated_data)
