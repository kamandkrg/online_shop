from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True, default=None)

    def __str__(self):
        return f"{self.parent}/{self.name}"


class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return str(self.category)



