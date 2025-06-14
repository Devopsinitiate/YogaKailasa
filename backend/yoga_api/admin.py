from django.contrib import admin
from .models import Pose, BreathingExercise, Course, UserProfile

class PoseAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty')
    search_fields = ('name', 'description')
    list_filter = ('difficulty',)

class BreathingExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes')
    search_fields = ('name', 'description')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title', 'description')
    list_filter = ('price',)
    filter_horizontal = ('poses', 'breathing_exercises') # Or filter_vertical

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'enrolled_courses_count')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('enrolled_courses_list_display',) # To display enrolled courses

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def enrolled_courses_count(self, obj):
        return obj.enrolled_courses.count()
    enrolled_courses_count.short_description = 'Enrolled Courses Count'

    def enrolled_courses_list_display(self, obj):
        return ", ".join([course.title for course in obj.enrolled_courses.all()])
    enrolled_courses_list_display.short_description = 'Enrolled Courses'

    # If you want to make enrolled_courses editable in UserProfileAdmin (not recommended if handled by payments)
    # filter_horizontal = ('enrolled_courses',)


admin.site.register(Pose, PoseAdmin)
admin.site.register(BreathingExercise, BreathingExerciseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
