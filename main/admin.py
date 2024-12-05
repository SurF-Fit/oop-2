from django.contrib import admin
import datetime
from .models import AdvUser, Category, InteriorDesign
from .utilities import send_activation_notification

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')

send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'

admin.site.register(Category)

@admin.register(InteriorDesign)
class InteriorDesignAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at', 'description']
    list_filter = ['status', 'created_at']
    search_fields = ['description']

class NoactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                                    date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                    date_joined__date__lt=d)

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NoactivatedFilter,)
    fields = (
        ('username',),
        ('email',),
        ('is_active',),
        ('is_staff',),
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined',)
    actions = (send_activation_notification,)

admin.site.register(AdvUser, AdvUserAdmin)
