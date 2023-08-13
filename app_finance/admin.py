from django.contrib import admin
from .models import Revenue, Expense

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = 'date_revenue', 'description', 'revenue', 'calcular_total_receitas',
    list_display_links = list_display
    search_fields = list_display
    list_filter = 'date_revenue',

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Verifica se é uma nova receita
            obj.user = request.user
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def calcular_total_receitas(self, obj):
        return obj.calcular_total_receitas()

    calcular_total_receitas.short_description = 'Total de Receitas'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = 'due_date', 'pay_day', 'description', 'expense', 'status', 'category', 'calcular_total_despesas',
    list_display_links = list_display
    search_fields = list_display_links
    list_filter = 'due_date',
    
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Verifica se é uma nova despesa
            obj.user = request.user
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
    
    def calcular_total_despesas(self, obj):
        return obj.calcular_total_despesas()

    calcular_total_despesas.short_description = 'Total de Despesas'