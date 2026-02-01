from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pretalx_pages", "0001_create_page_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="link_in_nav",
            field=models.BooleanField(
                default=False, verbose_name="Show as navigation tab"
            ),
        ),
    ]
