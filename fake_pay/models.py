import uuid
from django.db import models


class Country(models.Model):
    """Страна"""
    uuid_country = models.UUIDField(db_column='uuid_country', db_comment='uuid_country', default=uuid.uuid4, primary_key=True, editable=False)
    country = models.CharField(db_column='country', db_comment='country', max_length=250, db_index=True, unique=True)

    class Meta:
        db_table = 'country'
        ordering = 'country',


class Bank(models.Model):
    """Банк"""
    uuid_bank = models.UUIDField(db_column='uuid_bank', db_comment='uuid_bank', default=uuid.uuid4, primary_key=True, editable=False)
    bank = models.CharField(db_column='bank', db_comment='bank', max_length=250, db_index=True, unique=True)
    code_bank = models.IntegerField(db_column='code_bank', db_comment='code_bank', db_index=True, unique=True)
    balance = models.DecimalField(db_column='balance', db_comment='balance', max_digits=100, decimal_places=2, default=0)
    uuid_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='bank_uuid_country', db_comment='uuid_country', db_column='uuid_country', null=True, blank=True)

    class Meta:
        db_table = 'bank'
        ordering = 'bank', 'code_bank'


class Currency(models.Model):
    """Валюта"""
    uuid_currency = models.UUIDField(db_column='uuid_currency', db_comment='uuid_currency', default=uuid.uuid4, primary_key=True, editable=False)
    currency = models.CharField(db_column='currency', db_comment='currency', max_length=250, db_index=True, unique=True)
    code_currency = models.IntegerField(db_column='code_currency', db_comment='code_currency', db_index=True, unique=True)

    class Meta:
        db_table = 'currency'
        ordering = 'currency', 'code_currency'


class Transaction(models.Model):
    """Переводы"""
    uuid_transaction = models.UUIDField(db_column='uuid_transaction', db_comment='uuid_transaction', default=uuid.uuid4, primary_key=True, editable=False)
    date_pay = models.DateField(db_column='date_pay', db_comment='date_pay')
    user_from = models.CharField(db_column='user_from', db_comment='user_from', max_length=250, db_index=True)
    user_to = models.CharField(db_column='user_to', db_comment='user_to', max_length=250, db_index=True)
    bank_from = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='bank_from', db_comment='bank_from', related_name='transaction_bank_from')
    bank_to = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='bank_to', db_comment='bank_to', related_name='transaction_bank_to')
    pay = models.DecimalField(db_comment='pay', db_column='pay', max_digits=10, decimal_places=2, default=0)
    percent_pay = models.DecimalField(db_comment='percent_pay', db_column='percent_pay', max_digits=10, decimal_places=2, default=0)
    uuid_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='transaction_uuid_currency', db_column='uuid_currency', db_comment='uuid_currency')

    class Meta:
        db_table = 'transaction'
        ordering = 'date_pay', 'user_from', 'user_to'
