from django.contrib import admin

from .models import Employee , Employer


# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]

# admin.site.register(Question, QuestionAdmin)

# class EmployeeAdmin(admin.ModelAdmin):
#     # fields = ('__all__',) 

# admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Employee)
admin.site.register(Employer)