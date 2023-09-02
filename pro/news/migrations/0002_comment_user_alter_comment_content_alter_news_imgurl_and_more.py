# Generated by Django 4.2.4 on 2023-08-31 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="news",
            name="imgurl",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="news",
            name="keywords",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
