from django.contrib import admin
from sidebar.models import SidebarEntry, SidebarCategory

class SidebarCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','side')    



class SidebarAdmin(admin.ModelAdmin):
    list_display = ('category','title','dt')
    search_fields = ('title',)
    list_filter = ('category','display')


admin.site.register(SidebarEntry, SidebarAdmin)
admin.site.register(SidebarCategory, SidebarCategoryAdmin)
    
