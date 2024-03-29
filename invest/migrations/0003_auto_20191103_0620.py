# Generated by Django 2.2.6 on 2019-11-03 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0002_expenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='goals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recurring', models.IntegerField()),
                ('recurring_start', models.PositiveSmallIntegerField()),
                ('recurring_end', models.PositiveSmallIntegerField()),
                ('recurring_inf', models.PositiveSmallIntegerField()),
                ('less_freq', models.IntegerField()),
                ('less_freq_start', models.PositiveSmallIntegerField()),
                ('less_freq_end', models.PositiveSmallIntegerField()),
                ('less_freq_freq', models.PositiveSmallIntegerField()),
                ('less_freq_inf', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Income_Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i1_income', models.IntegerField()),
                ('i1_start', models.PositiveSmallIntegerField()),
                ('i1_end', models.PositiveSmallIntegerField()),
                ('i1_inf', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LFG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lg1_cost', models.IntegerField()),
                ('lg1_start', models.PositiveSmallIntegerField()),
                ('lg1_freq', models.PositiveSmallIntegerField()),
                ('lg1_end', models.PositiveSmallIntegerField()),
                ('lg1_inf', models.PositiveSmallIntegerField()),
                ('lg2_cost', models.IntegerField()),
                ('lg2_start', models.PositiveSmallIntegerField()),
                ('lg2_freq', models.PositiveSmallIntegerField()),
                ('lg2_end', models.PositiveSmallIntegerField()),
                ('lg2_inf', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OTG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g1_year', models.PositiveSmallIntegerField()),
                ('g1_cost', models.IntegerField()),
                ('g1_inf', models.PositiveSmallIntegerField()),
                ('g2_year', models.PositiveSmallIntegerField()),
                ('g2_cost', models.IntegerField()),
                ('g2_inf', models.PositiveSmallIntegerField()),
                ('g3_year', models.PositiveSmallIntegerField()),
                ('g3_cost', models.IntegerField()),
                ('g3_inf', models.PositiveSmallIntegerField()),
                ('g4_year', models.PositiveSmallIntegerField()),
                ('g4_cost', models.IntegerField()),
                ('g4_inf', models.PositiveSmallIntegerField()),
                ('g5_year', models.PositiveSmallIntegerField()),
                ('g5_cost', models.IntegerField()),
                ('g5_inf', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='eqshare',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='equity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
