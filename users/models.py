from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class UserProfile(AbstractUser):
    # Extra fields
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(300)],  # cm range
        help_text="Height in centimeters"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(500)],  # kg range
        help_text="Weight in kilograms"
    )
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # The AbstractUser email field is not unique by default, so I make it unique here
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Keep username as a required field for user creation

    def __str__(self):
        return self.username

    @property
    def age(self):
        """Calculate age from date_of_birth"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
