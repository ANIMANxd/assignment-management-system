# backend/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AssignmentTransaction, Org, Course, Semester, Subject, TechSkill, Assignment, Student
from django.shortcuts import get_object_or_404

# === Helper Functions for Serialization ===

def serialize_org(org):
    return {
        "id": str(org.id),
        "name": org.name
    }

def serialize_course(course):
    return {
        "id": str(course.id),
        "course_name": course.course_name,
        "course_code": course.course_code,
        "org": str(course.org.id) # Returning ID for foreign key
    }

def serialize_semester(semester):
    return {
        "id": str(semester.id),
        "semester_name": semester.semester_name,
        "sem_code": semester.sem_code
    }

def serialize_subject(subject):
    return {
        "id": str(subject.id),
        "subject_name": subject.subject_name,
        "subject_code": subject.subject_code
    }

def serialize_tech_skill(skill):
    return {
        "id": str(skill.id),
        "skill_name": skill.skill_name,
        "skill_code": skill.skill_code
    }

def serialize_student(student):
    return {
        "id": str(student.id),
        "student_usn_no": student.student_usn_no,
        "email": student.email,
        "gender": student.gender,
        "course": serialize_course(student.course) # Nested serialization for read
    }

def serialize_assignment(assignment):
    return {
        "id": str(assignment.id),
        "assignment_name": assignment.assignment_name,
        "assignment_description": assignment.assignment_description,
        "start_date": assignment.start_date,
        "submission_end_date": assignment.submission_end_date,
        "total_marks": assignment.total_marks,
        "assignment_code": assignment.assignment_code,
        "course": serialize_course(assignment.course),
        "semester": serialize_semester(assignment.semester),
        "subject": serialize_subject(assignment.subject),
        "tech_skills": [serialize_tech_skill(skill) for skill in assignment.tech_skills.all()]
    }

def serialize_assignment_transaction(txn):
    return {
        "id": str(txn.id),
        "obtained_marks": txn.obtained_marks,
        "candidate_submit_date": txn.candidate_submit_date,
        "remarks": txn.remarks,
        "student": serialize_student(txn.student),
        "assignment": serialize_assignment(txn.assignment)
    }

# === Views ===

class OrgListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orgs = Org.objects.all()
        data = [serialize_org(org) for org in orgs]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            org = Org.objects.create(name=data.get('name'))
            return Response(serialize_org(org), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CourseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        data = [serialize_course(course) for course in courses]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            org = get_object_or_404(Org, id=data.get('org'))
            course = Course.objects.create(
                course_name=data.get('course_name'),
                course_code=data.get('course_code'),
                org=org
            )
            return Response(serialize_course(course), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SemesterListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        semesters = Semester.objects.all()
        data = [serialize_semester(sem) for sem in semesters]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            semester = Semester.objects.create(
                semester_name=data.get('semester_name'),
                sem_code=data.get('sem_code')
            )
            return Response(serialize_semester(semester), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subjects = Subject.objects.all()
        data = [serialize_subject(sub) for sub in subjects]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            subject = Subject.objects.create(
                subject_name=data.get('subject_name'),
                subject_code=data.get('subject_code')
            )
            return Response(serialize_subject(subject), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TechSkillListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = TechSkill.objects.all()
        data = [serialize_tech_skill(skill) for skill in skills]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            skill = TechSkill.objects.create(
                skill_name=data.get('skill_name'),
                skill_code=data.get('skill_code')
            )
            return Response(serialize_tech_skill(skill), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        data = [serialize_student(student) for student in students]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            course = get_object_or_404(Course, id=data.get('course_id'))
            student = Student.objects.create(
                student_usn_no=data.get('student_usn_no'),
                email=data.get('email'),
                gender=data.get('gender'),
                course=course
            )
            return Response(serialize_student(student), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AssignmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assignments = Assignment.objects.all()
        data = [serialize_assignment(assign) for assign in assignments]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            course = get_object_or_404(Course, id=data.get('course_id'))
            semester = get_object_or_404(Semester, id=data.get('semester_id'))
            subject = get_object_or_404(Subject, id=data.get('subject_id'))
            
            assignment = Assignment.objects.create(
                assignment_name=data.get('assignment_name'),
                assignment_description=data.get('assignment_description'),
                start_date=data.get('start_date'),
                submission_end_date=data.get('submission_end_date'),
                total_marks=data.get('total_marks'),
                assignment_code=data.get('assignment_code'),
                course=course,
                semester=semester,
                subject=subject
            )
            
            # Handle ManyToMany field
            tech_skill_ids = data.get('tech_skill_ids', [])
            if tech_skill_ids:
                tech_skills = TechSkill.objects.filter(id__in=tech_skill_ids)
                assignment.tech_skills.set(tech_skills)

            return Response(serialize_assignment(assignment), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AssignmentTransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        txns = AssignmentTransaction.objects.all()
        data = [serialize_assignment_transaction(txn) for txn in txns]
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            student = get_object_or_404(Student, id=data.get('student_id'))
            assignment = get_object_or_404(Assignment, id=data.get('assignment_id'))
            
            txn = AssignmentTransaction.objects.create(
                obtained_marks=data.get('obtained_marks'),
                remarks=data.get('remarks'),
                student=student,
                assignment=assignment
            )
            return Response(serialize_assignment_transaction(txn), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)