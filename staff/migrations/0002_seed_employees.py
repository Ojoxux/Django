from datetime import date

from django.db import migrations


def seed_employees(apps, schema_editor):
    Employee = apps.get_model("staff", "Employee")

    employees = [
        {
            "name": "山田 太郎",
            "dept": "営業部",
            "role": "マネージャー",
            "email": "yamada@example.com",
            "joined_date": date(2018, 4, 1),
        },
        {
            "name": "佐藤 華子",
            "dept": "開発部",
            "role": "エンジニア",
            "email": "sato@example.com",
            "joined_date": date(2020, 10, 1),
        },
        {
            "name": "伊藤 健太",
            "dept": "開発部",
            "role": "一般",
            "email": "ito@example.com",
            "joined_date": date(2022, 4, 1),
        },
        {
            "name": "鈴木 一郎",
            "dept": "人事部",
            "role": "一般",
            "email": "suzuki@example.com",
            "joined_date": date(2019, 7, 15),
        },
        {
            "name": "高橋 美咲",
            "dept": "営業部",
            "role": "一般",
            "email": "takahashi@example.com",
            "joined_date": date(2024, 4, 1),
        },
    ]

    for data in employees:
        Employee.objects.get_or_create(email=data["email"], defaults=data)


def unseed_employees(apps, schema_editor):
    Employee = apps.get_model("staff", "Employee")
    emails = [
        "yamada@example.com",
        "sato@example.com",
        "ito@example.com",
        "suzuki@example.com",
        "takahashi@example.com",
    ]
    Employee.objects.filter(email__in=emails).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_employees, unseed_employees),
    ]
