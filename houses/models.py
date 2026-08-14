from django.db import models
from django.contrib.auth.models import User


class House(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="houses"
    )

    title = models.CharField(max_length=100)

    description = models.TextField(default="")

    location = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    bedrooms = models.PositiveIntegerField(default=1)

    bathrooms = models.PositiveIntegerField(default=1)

    guests = models.PositiveIntegerField(default=1)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )

    image = models.ImageField(
        upload_to="houses/"
    )

    def __str__(self):
        return self.title