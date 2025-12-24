from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonerange',
            name='registry_source',
            field=models.CharField(
                choices=[
                    ('3xx', 'Диапазон 3XX'),
                    ('4xx', 'Диапазон 4XX'),
                    ('8xx', 'Диапазон 8XX'),
                    ('9xx', 'Диапазон 9XX')
                ],
                db_index=True,
                default=None,
                null=True,
                max_length=10,
            ),
        ),
    ]