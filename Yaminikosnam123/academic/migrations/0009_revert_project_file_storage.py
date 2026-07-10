# Revert Project.file storage from RawMediaCloudinaryStorage back to
# MediaCloudinaryStorage so that existing image-type uploads remain accessible.

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0008_alter_project_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file',
            field=models.FileField(
                blank=True,
                null=True,
                storage=cloudinary_storage.storage.MediaCloudinaryStorage,
                upload_to='projects/',
            ),
        ),
    ]
