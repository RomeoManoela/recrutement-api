# Generated by Django 5.1.7 on 2025-03-22 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_candidat_email_recruteur_email"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidature",
            name="candidat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidatures",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name="recruteur",
            name="user",
        ),
        migrations.AlterField(
            model_name="offre",
            name="recruteur",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offres",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.RenameField(
            model_name="offre",
            old_name="competences",
            new_name="competences_requises",
        ),
        migrations.RemoveField(
            model_name="user",
            name="est_candidat",
        ),
        migrations.RemoveField(
            model_name="user",
            name="est_recruteur",
        ),
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="competences",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="experience",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("candidat", "Candidat"), ("recruteur", "Recruteur")],
                default="candidat",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.DeleteModel(
            name="Candidat",
        ),
        migrations.DeleteModel(
            name="Recruteur",
        ),
    ]
