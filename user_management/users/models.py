from django.db import models
import random
import string

def random_table_name():
    return 'tbl_' + ''.join(random.choices(string.digits, k=10))

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    table_name = models.CharField(max_length=255, unique=True)  # Increase max_length to 255
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.table_name:
            self.table_name = 'tbl_' + ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)

