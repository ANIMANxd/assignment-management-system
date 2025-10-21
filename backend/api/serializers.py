# backend/api/serializers.py
from rest_framework import serializers
from .models import AssignmentTransaction, Org, Course, Semester, Subject, TechSkill, Assignment, Student

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__' # A shortcut to include all fields from the model

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSkill
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    # For GET requests, show the full course details
    course = CourseSerializer(read_only=True)
    # For POST requests, accept just the course's ID
    course_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Student
        # List all the model fields, plus our custom write_only field
        fields = [
            'id', 'student_usn_no', 'email', 'gender',
            'course',  # This will be used for reading
            'course_id'  # This will be used for writing
        ]
class AssignmentSerializer(serializers.ModelSerializer):
    # We define nested serializers for read-only representation
    course = CourseSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    tech_skills = TechSkillSerializer(many=True, read_only=True)

    # We define write-only fields to accept UUIDs during creation/update
    course_id = serializers.UUIDField(write_only=True)
    semester_id = serializers.UUIDField(write_only=True)
    subject_id = serializers.UUIDField(write_only=True)
    tech_skill_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, allow_empty=False
    )

    class Meta:
        model = Assignment
        # We list all fields, including our custom ones
        fields = [
            'id', 'assignment_name', 'assignment_description', 'start_date',
            'submission_end_date', 'total_marks', 'assignment_code',
            'course', 'semester', 'subject', 'tech_skills',  # Read-only nested objects
            'course_id', 'semester_id', 'subject_id', 'tech_skill_ids' # Write-only ID fields
        ]

    def create(self, validated_data):
        # We pop the ID fields from the validated data
        tech_skill_ids = validated_data.pop('tech_skill_ids')
        
        # We create the assignment object without the many-to-many field
        assignment = Assignment.objects.create(**validated_data)
        
        # We set the many-to-many relationship
        assignment.tech_skills.set(tech_skill_ids)
        
        return assignment
    

class AssignmentTransactionSerializer(serializers.ModelSerializer):
    # Nested serializers for rich, read-only output
    student = StudentSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    # Write-only fields for accepting IDs on input
    student_id = serializers.UUIDField(write_only=True)
    assignment_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = AssignmentTransaction
        fields = [
            'id', 'obtained_marks', 'candidate_submit_date', 'remarks',
            'student', 'assignment', # For reading
            'student_id', 'assignment_id' # For writing
        ]
        # candidate_submit_date is set automatically by the model (auto_now_add=True)
        # so we don't need to provide it when creating. Let's make it read-only.
        read_only_fields = ['candidate_submit_date']