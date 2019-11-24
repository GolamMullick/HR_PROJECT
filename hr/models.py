from django.db import models
from common_utils.base_entity import BaseEntityBasicAbstract
from users.models import CompanyUsers
from django.core.validators import URLValidator


class Job(BaseEntityBasicAbstract):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Post', 'Post'),
        ('Closed', 'Closed')
    )

    SCOPE_CHOICES = (
        ('Internal_org', 'Internal_org'),
        ('Public', 'Public'),
        ('Recruiters', 'Recruiters')
    )

    REPORTING_CHOICES = (
        ('Remote', 'Remote'),
        ('Telecommuting', 'Telecommuting')

    )

    job_id = models.IntegerField()
    job_title = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    internal_id = models.IntegerField()
    job_publish_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    job_publish_scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='Internal_org')
    location_country = models.CharField(max_length=50)
    reporting_location = models.CharField(max_length=50, choices=REPORTING_CHOICES, default='on_site')
    job_type = models.CharField(max_length=50)
    job_category = models.CharField(max_length=50)
    job_position = models.TextField()
    education_requirement = models.CharField(max_length=50)
    experience_requirements = models.IntegerField()
    salary_amount = models.IntegerField()
    #tags
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(CompanyUsers, related_name='job_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='job_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='job_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Question(BaseEntityBasicAbstract):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question=models.TextField()
    created_by = models.ForeignKey(CompanyUsers, related_name='question_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='question_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='question_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class QuestionOptions(BaseEntityBasicAbstract):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.TextField(null=True, blank=True)
    is_answer = models.BooleanField(default=False)
    created_by = models.ForeignKey(CompanyUsers, related_name='question_options_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='question_options_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='question_options_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Applicant(BaseEntityBasicAbstract):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    resume_upload = models.FileField()
    cover_letter = models.TextField()
    experience = models.CharField(max_length=200)
    eduction = models.CharField(max_length=200)
    job= models.ForeignKey(Job, on_delete=models.CASCADE)
    questionnaire = models.CharField(max_length=50)
    created_by = models.ForeignKey(CompanyUsers, related_name='applicant_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='applicant_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='applicant_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Application(BaseEntityBasicAbstract):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant=models.ForeignKey(Applicant, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='application_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='application_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='application_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Answer(BaseEntityBasicAbstract):
    applicant=models.ForeignKey(Applicant, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.ForeignKey(QuestionOptions, on_delete=models.CASCADE)
    answer = models.TextField()
    created_by = models.ForeignKey(CompanyUsers, related_name='answer_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='answer_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='answer_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Employee(BaseEntityBasicAbstract):
    EMPLOYMENT_CHOICES = (
        ('Contingent', 'Contingent'),
        ('Consultant', 'Consultant')
    )
    CLASSIFICATION_CHOICES = (
        ('Full_time', 'Full_time'),
        ('Part_time', 'Part_time'),
        ('Intern', 'Intern')
    )
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    preferred_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50)
    birth_date = models.IntegerField()
    ssn = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50,choices=EMPLOYMENT_CHOICES, default='Contingent')
    classification = models.CharField(max_length=50, choices=CLASSIFICATION_CHOICES, default='Contingent')
    created_by = models.ForeignKey(CompanyUsers, related_name='employee_id_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='employee_id_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='employee_id_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Contact(BaseEntityBasicAbstract):
    home_phone = models.IntegerField()
    cell_phone = models.IntegerField()
    work_phone = models.IntegerField()
    work_email_address= models.CharField(max_length=50)
    personal_email_address = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='contact_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='contact_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='contact_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class EmergencyContact(BaseEntityBasicAbstract):
    primary_contact= models.IntegerField()
    primary_contact_relation = models.CharField(max_length=50)
    secondary_contact = models.IntegerField()
    secondary_contact_relation = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='emergency_contact_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='emergency_contact_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='emergency_contact_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Address(BaseEntityBasicAbstract):
    present_address = models.CharField(max_length=50)
    permanent_address = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='address_contact_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='address_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='address_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Education(BaseEntityBasicAbstract):
    school_name = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    GPA = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='education_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='education_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='education_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Certification(BaseEntityBasicAbstract):
    vendor_name= models.CharField(max_length=50)
    certification= models.CharField(max_length=50)
    valid_through= models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='certification_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='certification_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='certification_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Languages(BaseEntityBasicAbstract):
    primary_language = models.CharField(max_length=50)
    secondary_language = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='language_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='language_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='language_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class VisaDetails(BaseEntityBasicAbstract):
    visa_date = models.DateField()
    visa_number = models.IntegerField()
    visa_category = models.CharField(max_length=50)
    issuing_country = models.CharField(max_length=50)
    Expiration = models.DateField()
