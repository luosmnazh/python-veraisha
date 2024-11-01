from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} - {self.get_status_display()}'


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message from {self.user.username} on {self.created_at}'
