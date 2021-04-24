from django.contrib import admin
from api import models
# Register your models here.

@admin.register(models.Resident,
                models.Building,
                models.WashingProgram)
class BasicAdmin(admin.ModelAdmin):
    pass

@admin.register(models.WashingMachine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['short_name','building','name','number','machine_type','enabled','timer','available']

    def reset_machines(self,request, queryset):
        queryset.update(timer=None)
    reset_machines.short_description="Remettre les machines disponibles"
    actions = [reset_machines]