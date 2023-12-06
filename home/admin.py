from django.contrib import admin
from . models import *

class GoalList(admin.TabularInline):
    model = Goal
    
class UserGoalAdmin(admin.ModelAdmin):
    inlines = [GoalList]
    
admin.site.register(UserGoal,UserGoalAdmin)

