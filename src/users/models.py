from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    

    def __str__(self) -> str:
        return self.username
    
    groups = models.ManyToManyField(
    'auth.Group',
    related_name='custom_user_set',  # Avoid clash with 'auth.User'
    blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set_permissions',  # Avoid clash with 'auth.User'
        blank=True
    )