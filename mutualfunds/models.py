from django.db import models
# Create your models here.
class users(models.Model):
    name = models.TextField()
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=254 )
    contact = models.BigIntegerField()
    marital = models.TextField()
    retire = models.PositiveSmallIntegerField()

class income(models.Model):
    sal_and_bonus = models.IntegerField()
    sal_ends = models.PositiveSmallIntegerField()
    exp_sal_growth_in_per = models.PositiveSmallIntegerField()
    rent = models.IntegerField()
    rent_ends = models.PositiveSmallIntegerField()
    exp_growth = models.PositiveSmallIntegerField()
    business=models.IntegerField()
    business_ends=models.PositiveSmallIntegerField()
    business_growth=models.PositiveSmallIntegerField()
    other = models.IntegerField()
    other_ends=models.PositiveSmallIntegerField()
    other_growth = models.PositiveSmallIntegerField()
