# Generated by Django 3.1.13 on 2021-07-11 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0002_auto_20210711_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(blank=True, help_text='First or given name of person (leave blank for organizations)', max_length=100, null=True)),
                ('family_name', models.CharField(help_text='Last or family name of person, or name of organization as contributor', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('orcid', models.CharField(blank=True, help_text='The ORCID identifier (e.g. 0000-0003-3230-6090)', max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='email',
        ),
        migrations.RemoveField(
            model_name='article',
            name='family_name',
        ),
        migrations.RemoveField(
            model_name='article',
            name='given_name',
        ),
        migrations.AlterField(
            model_name='article',
            name='doi',
            field=models.CharField(help_text='The Digital Object Identifier (e.g. 10.3998/ergo.12405314.0002.002)', max_length=255, verbose_name='DOI'),
        ),
        migrations.AddField(
            model_name='article',
            name='contributor',
            field=models.ManyToManyField(blank=True, help_text='A contributor to the article', null=True, to='lookup.Contributor'),
        ),
    ]
