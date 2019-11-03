from django.db import models
# Create your models here.
class users(models.Model):
    name = models.TextField()
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=254)
    contact = models.BigIntegerField()
    marital = models.TextField()
    retire = models.PositiveSmallIntegerField()

class income(models.Model):
    email = models.ForeignKey(users, on_delete=models.CASCADE)
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

class expenses(models.Model):
    regular = models.IntegerField()
    regular_ends = models.PositiveSmallIntegerField()
    exp_inf_reg = models.PositiveSmallIntegerField()
    uti = models.IntegerField()
    uti_ends = models.PositiveSmallIntegerField()
    exp_inf_uti = models.PositiveSmallIntegerField()
    grocery=models.IntegerField()
    grocery_ends=models.PositiveSmallIntegerField()
    exp_inf_groc=models.PositiveSmallIntegerField()
    mon_leisure = models.IntegerField()
    leisure_ends=models.PositiveSmallIntegerField()
    exp_les_inf = models.PositiveSmallIntegerField()
    me = models.IntegerField()
    me_ends=models.PositiveSmallIntegerField()
    me_inf = models.PositiveSmallIntegerField()
    ds = models.IntegerField()
    ds_ends=models.PositiveSmallIntegerField()
    exp_ds_inf = models.PositiveSmallIntegerField()
<<<<<<< HEAD:mutualfunds/models.py
    emi1 = models.IntegerField()
    emi1_end = model.PositiveSmallIntegerField()
    emi2 = models.IntegerField()
    emi2_end = models.PositiveSmallIntegerField()

class portfolio(models.Model):
    equity = models.IntegerField()
    mutual = models.IntegerField()

class goals(models.Model):
    recurring = models.IntegerField()
    recurring_start = models.PositiveSmallIntegerField()
    recurring_end = models.PositiveSmallIntegerField()
    recurring_inf = models.PositiveSmallIntegerField()
    less_freq = models.IntegerField()
    less_freq_start = models.PositiveSmallIntegerField()
    less_freq_end = models.PositiveSmallIntegerField()
    less_freq_freq = models.PositiveSmallIntegerField()
    less_freq_inf = models.PositiveSmallIntegerField()
=======
    emi1=models.IntegerField()
    emi1_end=models.PositiveSmallIntegerField()
    emi2=models.IntegerField()
    emi2_end=models.PositiveSmallIntegerField()

class portfolio(models.Model):
    eqshare = models.IntegerField()
    mutual = models.IntegerField()
>>>>>>> 71a58f660f3e29c4db2d292d6980b7865272bafb:invest/models.py