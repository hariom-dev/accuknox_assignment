from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    friends = models.ManyToManyField("self", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    @property
    def get_full_name(self) -> str:
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email

class FriendsRequest(models.Model):
    sent_from = models.ForeignKey(CustomUser, verbose_name=_(" Sent From"), on_delete=models.CASCADE, related_name='sent_from')
    sent_to = models.ForeignKey(CustomUser, verbose_name=_("Sent To"), on_delete=models.CASCADE, related_name='sent_to')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    sent_on = models.DateTimeField(_("Sent Now"), auto_now_add=True)
    
    class Meta:
        unique_together = ["sent_from", "sent_to"]