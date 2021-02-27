from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class Course(models.Model):
    LEVEL_NAMES_CHOICES = [
        (1, "Introductorio"),
        (2, "Intermedio"),
        (3, "Avanzado"),
        (4, "Completo"),
    ]
    name = models.CharField(max_length=255, unique=True)
    real_price = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    level = models.IntegerField(
        choices=LEVEL_NAMES_CHOICES,
        default=1,
    )
    score = models.DecimalField(max_digits=3, decimal_places=2)
    tutor_username = models.CharField(max_length=255)
    users = models.IntegerField()
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)

    def __str__(self):
        return self.name
