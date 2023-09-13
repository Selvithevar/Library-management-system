# library/models.py

from django.db import models

class Book(models.Model):
    book_id = models.IntegerField(null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    stock = models.PositiveIntegerField(null=True)
    isbn = models.CharField(max_length=10,null=True)
    publisher = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title},{self.author}'

class Member(models.Model):
    name = models.CharField(max_length=100)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f'{self.name},{self.outstanding_debt}'

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(null=True)
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=50,null=True)


    def __str__(self):
        return f'{self.book},{self.member}'
