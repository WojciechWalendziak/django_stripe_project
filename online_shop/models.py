from django.db import models
from django.core import validators


class Book(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=70, verbose_name='Product Name')
    description = models.TextField(max_length=800, verbose_name='Description')
    quantity = models.IntegerField(verbose_name='Quantity')
    price = models.FloatField(
        verbose_name='Price',
        validators=[
            validators.MinValueValidator(5),
            validators.MaxValueValidator(1000)
        ]
    )


class OrderDetail(models.Model):

    id = models.BigAutoField(primary_key=True)

    customer_email = models.EmailField(verbose_name='Customer Email')
    book = models.ForeignKey(to=Book, verbose_name='Book', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)

    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)


