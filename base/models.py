from django.db import models
from django.contrib.auth.models import User

class AddExpenseModel(models.Model):
    CATEGORIES = (
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('bills', 'Bills'),
        ('clothes', 'Clothes'),
        ('groceries', 'Groceries'),
        ('extra', 'Extra')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=100, choices=CATEGORIES, default='extra')
    price = models.IntegerField()
    expense_added = models.DateField()
    
class CategoryLookup(models.Model):
    CATEGORIES = (
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('bills', 'Bills'),
        ('clothes', 'Clothes'),
        ('groceries', 'Groceries'),
        ('extra', 'Extra')
    )
    category = models.CharField(max_length=100, choices=CATEGORIES, default='extra')
    name = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name
    