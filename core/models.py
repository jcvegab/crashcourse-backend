from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

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
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="courses")
    subcategory = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="subcourses")

    def __str__(self):
        return self.name
