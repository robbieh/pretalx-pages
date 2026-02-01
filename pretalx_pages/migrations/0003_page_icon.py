from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pretalx_pages", "0002_page_link_in_nav"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="icon",
            field=models.CharField(
                blank=True,
                default="fa-file-text-o",
                help_text='Font Awesome icon class (e.g., "fa-heart", "fa-star"). Browse icons at fontawesome.com/v4/icons/',
                max_length=50,
                verbose_name="Tab icon",
            ),
        ),
    ]
