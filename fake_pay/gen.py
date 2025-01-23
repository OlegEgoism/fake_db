import random
import uuid
from faker import Faker
from decimal import Decimal
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_db.settings')
django.setup()

from fake_pay.models import Country, Bank, Currency, Transaction

fake = Faker('ru_RU')
countries_size = 190
banks_size = 100
currencies_size = 100
transactions_size, batch_size = 500000, 10000


def clear_database():
    """Очитка БД"""
    Transaction.objects.all().delete()
    Bank.objects.all().delete()
    Currency.objects.all().delete()
    Country.objects.all().delete()
    print("База данных очищена!")


def create_countries(countries_size):
    """Создание стран"""
    existing_countries = set(Country.objects.values_list('country', flat=True))
    countries = []
    while len(countries) < countries_size:
        country_name = fake.country()
        if country_name not in existing_countries:
            existing_countries.add(country_name)
            countries.append(Country(uuid_country=uuid.uuid4(), country=country_name))
    Country.objects.bulk_create(countries)
    print(f'Создано стран: {countries_size} шт.')


def create_banks(banks_size):
    """Создание банков"""
    countries = list(Country.objects.all())
    existing_codes = set(Bank.objects.values_list('code_bank', flat=True))  # Существующие коды банков
    banks = []
    while len(banks) < banks_size:
        bank_name = fake.company()
        code_bank = random.randint(1, banks_size)
        while code_bank in existing_codes or Bank.objects.filter(bank=bank_name).exists():
            code_bank = random.randint(1, banks_size)
            bank_name = fake.company()
        existing_codes.add(code_bank)
        banks.append(Bank(
            uuid_bank=uuid.uuid4(),
            bank=bank_name,
            code_bank=code_bank,
            balance=Decimal(random.uniform(1000, 10000000)),
            uuid_country=random.choice(countries)
        ))
    Bank.objects.bulk_create(banks)
    print(f'Создано банков: {banks_size} шт.')


def create_currencies(currencies_size):
    """Создание валют"""
    existing_currencies = set(Currency.objects.values_list('currency', flat=True))
    currencies = []
    while len(currencies) < currencies_size:
        currency_name = fake.currency_name()
        code_currency = random.randint(100, 999)
        if currency_name not in existing_currencies and code_currency not in [c.code_currency for c in currencies]:
            existing_currencies.add(currency_name)
            currencies.append(Currency(uuid_currency=uuid.uuid4(), currency=currency_name, code_currency=code_currency))
    Currency.objects.bulk_create(currencies)
    print(f'Создано валют: {currencies_size} шт.')


def create_transactions(transactions_size, batch_size=10000):
    """Создание переводов"""
    Transaction.objects.all().delete()
    banks = list(Bank.objects.all())
    currencies = list(Currency.objects.all())
    for i in range(0, transactions_size, batch_size):
        transactions = []
        for _ in range(batch_size):
            bank_from, bank_to = random.sample(banks, 2)
            transactions.append(Transaction(
                uuid_transaction=uuid.uuid4(),
                date_pay=fake.date_between(start_date='-10y', end_date='today'),
                user_from=fake.name(),
                user_to=fake.name(),
                bank_from=bank_from,
                bank_to=bank_to,
                uuid_currency=random.choice(currencies),
                pay=Decimal(random.uniform(10, 50000)),
                percent_pay=Decimal(random.uniform(0.1, 5))
            ))
        Transaction.objects.bulk_create(transactions)
        print(f'Записано транзакций: {i + batch_size}/{transactions_size}')
    print(f'Всего создано транзакций: {transactions_size} шт.')


if __name__ == '__main__':
    clear_database()
    create_countries(countries_size)
    create_banks(banks_size)
    create_currencies(currencies_size)
    create_transactions(transactions_size)
    print("База данных успешно заполнена фейковыми данными.")
