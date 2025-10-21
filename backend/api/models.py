# backend/api/models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# We will handle the Professor/User table later by extending Django's User model.

# === Master Tables ===

class User(AbstractUser):
    # We can add professor-specific fields here in the future
    # For example:
    # employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # department = models.CharField(max_length=100, null=True, blank=True)
    pass # For now, we'll just use the default fields


class Org(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=100, unique=True)
    course_code = models.CharField(max_length=20, unique=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester_name = models.CharField(max_length=50, unique=True)
    sem_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.semester_name

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=100, unique=True)
    subject_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.subject_name

class TechSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill_name = models.CharField(max_length=50, unique=True)
    skill_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.skill_name

# === Transactional Tables ===

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_usn_no = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10) # e.g., 'Male', 'Female', 'Other'
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student_usn_no} - {self.email}"

class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment_name = models.CharField(max_length=200)
    assignment_description = models.TextField(max_length=500)
    start_date = models.DateTimeField()
    submission_end_date = models.DateTimeField()
    total_marks = models.IntegerField()
    assignment_code = models.CharField(max_length=20, unique=True)
    
    # Foreign Keys / Relationships
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    tech_skills = models.ManyToManyField(TechSkill) # An assignment can have multiple skills

    def __str__(self):
        return self.assignment_name

class AssignmentTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obtained_marks = models.IntegerField()
    candidate_submit_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField()

    # Foreign Keys / Relationships
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.student_usn_no} submission for {self.assignment.assignment_name}"
    
