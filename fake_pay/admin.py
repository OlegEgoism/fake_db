from django.contrib import admin
from fake_pay.models import Country, Bank, Currency, Transaction


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
