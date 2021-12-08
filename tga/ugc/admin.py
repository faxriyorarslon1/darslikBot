from django.contrib import admin

from .forms import ProfileForm
from .models import (
                        Profile,
                        Faculty,
                        Area,
                        Laboratories,
                        Subjects,
                        Lectures
                    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name','surname','semestr', 'role')
    form = ProfileForm


class LaboratoriesAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(LaboratoriesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user)

class LecturesAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(LecturesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user)


admin.site.register(Faculty) 
admin.site.register(Area)    
admin.site.register(Laboratories, LaboratoriesAdmin)
admin.site.register(Lectures, LecturesAdmin)
admin.site.register(Subjects)         


