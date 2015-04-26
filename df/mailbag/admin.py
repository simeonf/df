from django.contrib import admin
from mailbag.models import MailBag, MailBagEntry


class MailBagEntryInlineAdmin(admin.StackedInline):
    model = MailBagEntry
    fk_name = "mail_bag"
    list_filter = ('display',)    

class MailBagEntryAdmin(admin.ModelAdmin):
    list_display = ('title','mail_bag', 'display','search')
    search_fields = ('title',)
    list_filter = ('display','search')
    

class MailBagAdmin(admin.ModelAdmin):
    list_display = ('title','dt','display')
    search_fields = ('title',)
    inlines = [MailBagEntryInlineAdmin]
    prepopulated_fields = {"slug" : ('title',)}

admin.site.register(MailBag, MailBagAdmin)
admin.site.register(MailBagEntry, MailBagEntryAdmin)
    
