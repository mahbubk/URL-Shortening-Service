from django.db import models
import secrets
from django.utils import timezone

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.username


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    custom_short_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    @staticmethod
    def generate_short_code():
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        short_code = ''.join(secrets.choice(characters) for _ in range(8))
        while ShortenedURL.objects.filter(short_code=short_code).exists():
            short_code = ''.join(secrets.choice(characters) for _ in range(8))
        return short_code


    def save(self, *args, **kwargs):

        if not self.custom_short_code:
            self.custom_short_code = None

        if not self.short_code:
            self.short_code = self.generate_short_code()


        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
            self.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_url
