# Generated by Django 4.2.4 on 2023-08-31 22:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_comment_user_alter_comment_content_alter_news_imgurl_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
