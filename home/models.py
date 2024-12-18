from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Company table
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Connect with the User model
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/companies/', blank=True, null=True)
    def __str__(self):
        return self.company_name


# Student table
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Connect with the User model
    student_name = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    github = models.URLField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/students/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Contest Model
class Contest(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)  # A short description of the contest
    start_date = models.DateField(blank=True, null=True)  # Optional start date
    end_date = models.DateField(blank=True, null=True)  # Optional end date
    prize = models.CharField(max_length=100, blank=True, null=True)  # Prize details
    location = models.CharField(max_length=200, blank=True, null=True)  # Online or In-person
    tags = models.CharField(max_length=300, blank=True, null=True)  # Tags like AI, ML, DS, etc.
    participants = models.IntegerField(default=0)  # Number of participants
    likes = models.IntegerField(default=0)  # Field to store the number of likes

# News Model
class News(models.Model):
    headline = models.CharField(max_length=1000)
    summary = models.TextField()  # Using TextField for longer summaries
    link = models.URLField()
    published_date = models.DateField(blank=True, null=True)  # Optional published date
    source = models.CharField(max_length=255, blank=True, null=True)  # Source of the news article
    tags = models.CharField(max_length=300, blank=True, null=True)  # Tags for classification like AI, ML, etc.
    likes = models.IntegerField(default=0)  # Field to store the number of likes

    def __str__(self):
        return self.headline


# Contact Model
class Contact(models.Model):
    q_name = models.CharField(max_length=100)
    q_email = models.EmailField()
    q_subject = models.CharField(max_length=1000)
    q_message = models.TextField()


# Jobs table
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Job')
    description = models.TextField()
    field = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    pay_range = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    skills = models.TextField()
    APPLICATION_STATUS_CHOICES = [
            ('applied', 'Applied'),
            ('reviewed', 'Reviewed'),
            ('shortlisted', 'Shortlisted'),
            ('interviewed', 'Interviewed'),
            ('selected', 'Selected'),
        ]
    student_applied = models.JSONField(default=dict)

    def update_application_status(self, student_id, status):
            if str(student_id) in self.student_applied:
                self.student_applied[str(student_id)]['status'] = status
                self.save()
                
    def __str__(self):
        return f"{self.company} - {self.category}"


# Internship table (Similar to Job)
class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Internship')
    description = models.TextField()
    field = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stipend = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    skills = models.TextField()
    student_applied = models.JSONField()  # To store hashmap of students applied

    def __str__(self):
        return f"{self.company} - {self.category}"

class Question(models.Model):
    # Question ID (Primary Key)
    questionId = models.AutoField(primary_key=True)
    
    # Subject for the question (e.g., "Deep Learning", "Data Imputation")
    subject = models.CharField(max_length=100)
    
    # The question text
    question = models.TextField()
    
    # The options for the multiple-choice question
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    
    # The correct answer, stored as the letter corresponding to the correct option
    correct_answer = models.CharField(max_length=1)
    
    # The correct answer option text
    correct_answer_option = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Question {self.questionId}: {self.question}"

    
class SubjectTestData(models.Model):
    testId = models.AutoField(primary_key=True)  # Auto-generated unique test ID
    subject = models.CharField(max_length=100)  # The subject for the test
    score = models.IntegerField(default=0)  # The score of the test
    questions = models.JSONField()  # Store questions, answers, and results as a JSON
    testDate = models.DateField(default=now)

    def __str__(self):
        return f"Test {self.testId} - {self.subject}"
    
class StudentTestData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the student
    test = models.ForeignKey(SubjectTestData, on_delete=models.CASCADE)  # Link to the test
    test_count = models.IntegerField(default=0)  # Number of tests the student has taken
    last_test_score = models.IntegerField(default=0)  # The most recent score of the student
    mathematics_score = models.IntegerField(default=0)
    machine_learning_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - Test {self.test.testId}"