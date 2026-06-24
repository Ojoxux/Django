from django.db import models


class Employee(models.Model):
    name = models.CharField("氏名", max_length=100)
    dept = models.CharField("部署名", max_length=100)
    role = models.CharField("役職", max_length=100)
    email = models.EmailField("メールアドレス")
    joined_date = models.DateField("入社日")

    class Meta:
        verbose_name = "社員"
        verbose_name_plural = "社員"

    def __str__(self):
        return self.name
