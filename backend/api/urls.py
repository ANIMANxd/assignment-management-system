# backend/api/urls.py
from django.urls import path
from .views import AssignmentTransactionListCreateView, OrgListCreateView, CourseListCreateView, SemesterListCreateView, SubjectListCreateView, TechSkillListCreateView, AssignmentListCreateView, StudentListCreateView

urlpatterns = [
    path('orgs/', OrgListCreateView.as_view(), name='org-list-create'),
    
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('semesters/', SemesterListCreateView.as_view(), name='semester-list-create'),
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('tech-skills/', TechSkillListCreateView.as_view(), name='tech-skill-list-create'),
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('assignment-transactions/', AssignmentTransactionListCreateView.as_view(), name='assignment-transaction-list-create'),
]