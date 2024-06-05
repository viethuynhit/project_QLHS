
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentMan', '0002_subject_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dateOfBirth',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 10, 0, 0)),
        ),
    ]
