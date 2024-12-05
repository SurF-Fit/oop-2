from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from pkg_resources import require

from .utilities import send_activation_notification
from .validadors import validate_image
from django.urls import reverse


user_registrated = Signal(['instance'])

def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)

class AdvUser(AbstractUser):
    login = models.CharField(max_length=40, verbose_name='Логин')
    is_activated = models.BooleanField(default=True, db_index=True,
                                        verbose_name='Прошел активацию?')


    def delete(self, *args, **kwargs):
        self.bb_set.all().delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category-detail', args=[str(self.id)])

    class Meta:
        pass

class InteriorDesign(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='interior_designs')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    comment = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('status_1', 'Новая'),
        ('status_2', 'Принята в работу'),
        ('status_3', 'Выполнено'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='status_1',
    )
    image = models.ImageField(upload_to='design/', default='design/default.jpg', validators=[validate_image])

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    class Meta:
        pass

class Bb(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True)