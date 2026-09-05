from django.db import models
from django.conf import settings

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
     )
    title = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.CharField()
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
