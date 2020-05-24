from django.contrib import admin

from .models import User_info, Cheque, HistoryNote
# Register your models here.
class ChequeAdmin(admin.ModelAdmin):
    #fields = ('activated', 'amount',)
    search_fields = ('id', 'sequrity_code')
    list_display = ('id', 'author', 'amount', 'sequrity_code', 'activated')
    #list_editable = ('author', 'amount', 'sequrity_code', 'activated')
    list_filter = ('activated', )
    ordering = ('id', 'amount', 'author', 'activated', )

admin.site.register(User_info)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(HistoryNote)