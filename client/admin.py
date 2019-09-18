from django.contrib import admin
from .models import Client, Activity, Plan, Payment


class ClientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Client, ClientAdmin)


class ActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Activity, ActivityAdmin)


class PlanAdmin(admin.ModelAdmin):
    pass


admin.site.register(Plan, PlanAdmin)


class PaymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Payment, PaymentAdmin)
