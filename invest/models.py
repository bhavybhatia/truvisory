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
    emi1 = models.IntegerField()
    emi1_end = models.PositiveSmallIntegerField()
    emi2 = models.IntegerField()
    emi2_end = models.PositiveSmallIntegerField()

class portfolio(models.Model):
    equity = models.IntegerField()
    mutual = models.IntegerField()


class OTG(models.Model):
    g1_year = models.PositiveSmallIntegerField()
    g1_cost = models.IntegerField()
    g1_inf = models.PositiveSmallIntegerField()
    g2_year = models.PositiveSmallIntegerField()
    g2_cost = models.IntegerField()
    g2_inf = models.PositiveSmallIntegerField()
    g3_year = models.PositiveSmallIntegerField()
    g3_cost = models.IntegerField()
    g3_inf = models.PositiveSmallIntegerField()
    g4_year = models.PositiveSmallIntegerField()
    g4_cost = models.IntegerField()
    g4_inf = models.PositiveSmallIntegerField()
    g5_year = models.PositiveSmallIntegerField()
    g5_cost = models.IntegerField()
    g5_inf = models.PositiveSmallIntegerField()

class LFG(models.Model):
    lg1_cost = models.IntegerField()
    lg1_start = models.PositiveSmallIntegerField()
    lg1_freq = models.PositiveSmallIntegerField()
    lg1_end = models.PositiveSmallIntegerField()
    lg1_inf = models.PositiveSmallIntegerField()
    lg2_cost = models.IntegerField()
    lg2_start = models.PositiveSmallIntegerField()
    lg2_freq = models.PositiveSmallIntegerField()
    lg2_end = models.PositiveSmallIntegerField()
    lg2_inf = models.PositiveSmallIntegerField()

class Income_Goal(models.Model):
    i1_income = models.IntegerField()
    i1_start = models.PositiveSmallIntegerField()
    i1_end = models.PositiveSmallIntegerField()
    i1_inf = models.PositiveSmallIntegerField()
