# Generated by Django 2.2.6 on 2019-11-02 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mutualfunds', '0004_delete_expenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular', models.IntegerField()),
                ('regular_ends', models.PositiveSmallIntegerField()),
                ('exp_inf_reg', models.PositiveSmallIntegerField()),
                ('uti', models.IntegerField()),
                ('uti_ends', models.PositiveSmallIntegerField()),
                ('exp_inf_uti', models.PositiveSmallIntegerField()),
                ('grocery', models.IntegerField()),
                ('grocery_ends', models.PositiveSmallIntegerField()),
                ('exp_inf_groc', models.PositiveSmallIntegerField()),
                ('mon_leisure', models.IntegerField()),
                ('leisure_ends', models.PositiveSmallIntegerField()),
                ('exp_les_inf', models.PositiveSmallIntegerField()),
                ('me', models.IntegerField()),
                ('me_ends', models.PositiveSmallIntegerField()),
                ('me_inf', models.PositiveSmallIntegerField()),
                ('ds', models.IntegerField()),
                ('ds_ends', models.PositiveSmallIntegerField()),
                ('exp_ds_inf', models.PositiveSmallIntegerField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutualfunds.users')),
            ],
        ),
    ]