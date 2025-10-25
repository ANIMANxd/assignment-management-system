from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Org, Course, Semester, Subject, TechSkill,
    Assignment, Student, AssignmentTransaction
)

# We need to tell the admin to use our custom User model.
# We inherit from the base UserAdmin to get all of its default features.
class CustomUserAdmin(UserAdmin):
    # You can add custom fields to the list_display or fieldsets if you add them to your User model
    pass

@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    """Admin configuration for the Organization model."""
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for the Course model."""
    list_display = ('course_name', 'course_code', 'org')
    search_fields = ('course_name', 'course_code')
    list_filter = ('org',) # Adds a filter sidebar by organization

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    """Admin configuration for the Semester model."""
    list_display = ('semester_name', 'sem_code')
    search_fields = ('semester_name', 'sem_code')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin configuration for the Subject model."""
    list_display = ('subject_name', 'subject_code')
    search_fields = ('subject_name', 'subject_code')

@admin.register(TechSkill)
class TechSkillAdmin(admin.ModelAdmin):
    """Admin configuration for the TechSkill model."""
    list_display = ('skill_name', 'skill_code')
    search_fields = ('skill_name', 'skill_code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for the Student model."""
    list_display = ('student_usn_no', 'email', 'course')
    search_fields = ('student_usn_no', 'email')
    list_filter = ('course',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for the Assignment model."""
    list_display = ('assignment_name', 'assignment_code', 'course', 'semester', 'subject', 'total_marks', 'submission_end_date')
    search_fields = ('assignment_name', 'assignment_code')
    list_filter = ('course', 'semester', 'subject')
    
    # Provides a much better UI for Many-to-Many fields like tech_skills
    filter_horizontal = ('tech_skills',)

@admin.register(AssignmentTransaction)
class AssignmentTransactionAdmin(admin.ModelAdmin):
    """Admin configuration for the AssignmentTransaction model."""
    list_display = ('student', 'assignment', 'obtained_marks', 'candidate_submit_date')
    # Use double-underscore to search on related model fields
    search_fields = ('student__student_usn_no', 'assignment__assignment_name') 
    list_filter = ('assignment__course', 'assignment')
    
    # Make auto-populated fields read-only in the admin
    readonly_fields = ('candidate_submit_date',)


# Register the custom User model with its admin configuration
admin.site.register(User, CustomUserAdmin)