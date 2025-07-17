from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('Food', 'Food'),
    ('Rent', 'Rent'),
    ('Utilities', 'Utilities'),
    ('Travel', 'Travel'),
    ('Other', 'Other'),
]

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.amount} on {self.date}"
