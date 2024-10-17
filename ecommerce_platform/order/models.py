from django.db import models
from user.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserCart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    class Meta:
        verbose_name = "User's Cart"
        verbose_name_plural = "Users' Carts"

@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
