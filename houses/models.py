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

class HouseImage(models.Model):

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="houses/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Image - {self.house.title}"


class Reservation(models.Model):

    class Status(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def nights(self):
        return(self.check_out - self.check_in).days

    @property
    def total_price(self):
        return self.nights * self.house.price

    def __str__(self):
        return f"{self.guest.username} - {self.house.title}"