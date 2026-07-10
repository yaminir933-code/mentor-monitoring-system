# Generated migration to add Cloudinary storage to Project.file

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_academicrecord_assignments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file',
            field=models.FileField(
                blank=True,
                null=True,
                storage=cloudinary_storage.storage.RawMediaCloudinaryStorage,
                upload_to='projects/',
            ),
        ),
    ]
