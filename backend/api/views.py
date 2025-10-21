# backend/api/views.py

from rest_framework import generics
from .models import AssignmentTransaction, Org, Course, Semester, Subject, TechSkill, Assignment, Student
from .serializers import (
    OrgSerializer, CourseSerializer, SemesterSerializer, 
    SubjectSerializer, TechSkillSerializer, AssignmentSerializer, StudentSerializer, AssignmentTransactionSerializer
)
from rest_framework.permissions import IsAuthenticated 



class OrgListCreateView(generics.ListCreateAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class SemesterListCreateView(generics.ListCreateAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class TechSkillListCreateView(generics.ListCreateAPIView):
    queryset = TechSkill.objects.all()
    serializer_class = TechSkillSerializer
    permission_classes = [IsAuthenticated]

class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class AssignmentTransactionListCreateView(generics.ListCreateAPIView):
    queryset = AssignmentTransaction.objects.all()
    serializer_class = AssignmentTransactionSerializer
    permission_classes = [IsAuthenticated]