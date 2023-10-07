from django.db import models


# Create your models here.
class SavedTranslation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    english_text = models.CharField(max_length=255)
    newari_text = models.CharField(max_length=255)

    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
