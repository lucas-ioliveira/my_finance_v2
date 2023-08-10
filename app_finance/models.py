from django.db import models


class Revenue(models.Model):
    date_revenue = models.DateField(verbose_name='Data da entrada')
    description = models.CharField(verbose_name='Descrição', max_length=255)
    revenue = models.FloatField(verbose_name='Receita')

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
    
    def calcular_total_receitas(self):
        total = Revenue.objects.aggregate(models.Sum('revenue'))['revenue__sum']
        return total if total is not None else 0


class Expense(models.Model):
    STATUS_CHOICE = (
        ('PG', 'Pago'),
        ('APG', 'À pagar'),
    )
    due_date = models.DateField(verbose_name='Vencimento')
    pay_day = models.DateField(verbose_name='Data de pagamento', blank=True, null=True)

    description = models.CharField(verbose_name='Descrição', max_length=255)
    expense = models.FloatField(verbose_name='Despesa')
    status = models.CharField(verbose_name='Status', max_length=3, choices=STATUS_CHOICE)
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def calcular_total_despesas(self):
        total = Expense.objects.aggregate(models.Sum('expense'))['expense__sum']
        return total if total is not None else 0