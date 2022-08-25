from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Staff(models.Model):
    ROLE = (
        ("ofitsiant", "ofitsiant"),
        ("boshqaruvchi", "boshqaruvchi"),
        ("kassir", "kassir"),
        ("deliverer", "deliverer"),
    )
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE, null=True, blank=True)
    car_brand = models.CharField(max_length=50, null=True, blank=True)
    car_color = models.CharField(max_length=50, null=True, blank=True)
    car_number = models.CharField(max_length=50, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class TgUser(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    tg_id = models.BigIntegerField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} | {self.phone_number}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Offer(models.Model):
    user = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    offer_text = models.TextField(null=True, blank=True)
    admin_description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.offer_text} | {self.rate}"


class Variant(models.Model):
    name = models.CharField(max_length=150)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    question = models.CharField(max_length=250)
    variant = models.ManyToManyField(Variant, blank=True)
    image = models.ImageField(upload_to="polls/", null=True, blank=True)
    category_product = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question} | {self.category}"


class PollResult(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE, null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.poll.question} | {self.tg_user.full_name}"


class Photos(models.Model):
    registration = models.ImageField(upload_to='bot_photos/', null=True, blank=True)
    start = models.ImageField(upload_to='bot_photos/', null=True, blank=True)
    product = models.ImageField(upload_to='bot_photos/', null=True, blank=True)
