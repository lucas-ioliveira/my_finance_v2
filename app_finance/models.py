from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Revenue(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
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
    CATEGORY_CHOICE = (
        ('1', 'Casa'),
        ('2', 'Cartão de crédito'),
        ('3', 'Compras de mercado'),
        ('4', 'Educação'),
        ('5', 'Exercício físico'),
        ('6', 'Gasolina'),
        ('7', 'Investimentos'),
        ('8', 'Lazer'),
        ('9', 'Outros'),
        ('10', 'Presentes'),
    )
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    due_date = models.DateField(verbose_name='Vencimento')
    pay_day = models.DateField(verbose_name='Data de pagamento', blank=True, null=True)
    description = models.CharField(verbose_name='Descrição', max_length=255)
    expense = models.FloatField(verbose_name='Despesa')
    category = models.CharField(verbose_name='Categoria',max_length=30, choices=CATEGORY_CHOICE)
    status = models.CharField(verbose_name='Status', max_length=3, choices=STATUS_CHOICE, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def calcular_total_despesas(self):
        total = Expense.objects.aggregate(models.Sum('expense'))['expense__sum']
        return total if total is not None else 0
    
@receiver(pre_save, sender=Expense)
def update_status(sender, instance, **kwargs):
    if instance.pay_day:
        instance.status = 'PG'
    else:
        instance.status = 'APG'