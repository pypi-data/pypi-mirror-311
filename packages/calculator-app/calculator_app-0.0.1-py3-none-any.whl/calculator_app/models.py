from django.db import models

# Create your models here.


class Calculator(models.Model):
    expression = models.CharField(verbose_name="Expression", max_length=128)
    result = models.IntegerField(verbose_name="Result")

    def __str__(self):
        return self.expression