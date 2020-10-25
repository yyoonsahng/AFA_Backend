from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=128, null=False)
    image = models.ImageField(default='media/default_image.jpeg')
    class Meta:
        db_table = "User"

        # Table이름을 "User"로 정한다 default 이름은 api_user_user가 된다.