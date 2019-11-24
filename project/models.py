from django.db import models
from common_utils.base_entity import BaseEntityBasicAbstract
from users.models import CompanyUsers
from django.core.validators import URLValidator


class Project(BaseEntityBasicAbstract):
    """User can create/update/delete project"""
    title = models.CharField(max_length=60)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(CompanyUsers, related_name='project_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='project_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='project_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class ProjectFiles(BaseEntityBasicAbstract):
    """User can create/update/delete project_files"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_path = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='project_file_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='project_file_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='project_file_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class ProjectDetails(BaseEntityBasicAbstract):
    """User can create/update/delete project_details"""
    key = models.CharField(max_length=60)
    value = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='project_detail_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='project_detail_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='project_detail_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Goal(BaseEntityBasicAbstract):
    """User can create/update/delete goal"""
    title = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='goal_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='goal_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='goal_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class GoalFiles(BaseEntityBasicAbstract):
    """User can create/update/delete goal_files"""
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    file_path = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='goal_file_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='goal_file_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='goal_file_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class GoalDetails(BaseEntityBasicAbstract):
    """User can create/update/delete goal_details"""
    key = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='goal_detail_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='goal_detail_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='goal_detail_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Task(BaseEntityBasicAbstract):
    """User can create/update/delete task"""
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Selected for Development', 'Selected for Development'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    )
    PRIORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    )
    title = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    enabled = models.BooleanField(default=True)
    goal = models.ForeignKey(Goal, null=True, blank=True, on_delete=models.CASCADE)
    assignee = models.ForeignKey(CompanyUsers, on_delete=models.CASCADE, related_name='assignee',
                                 null=True, blank=True)
    reporter = models.ForeignKey(CompanyUsers, on_delete=models.CASCADE, related_name='reporter',
                                 null=True, blank=True)
    updated_by = models.ForeignKey(CompanyUsers, related_name='task_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='task_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class TaskFiles(BaseEntityBasicAbstract):
    """User can create/update/delete task_files"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file_path = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='task_file_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='task_file_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='task_file_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class TaskDetails(BaseEntityBasicAbstract):
    """User can create/update/delete task_details"""
    key = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='task_detail_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='task_detail_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='task_detail_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class TaskComments(BaseEntityBasicAbstract):
    """User can create/update/delete task_comments"""
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    add_file = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='task_comment_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='task_comment_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='task_comment_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class Issue(BaseEntityBasicAbstract):
    """User can create/update/delete issue"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='issue_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='issue_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='issue_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class IssueDetails(BaseEntityBasicAbstract):
    """User can create/update/delete issue_details"""
    key = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CompanyUsers, related_name='issue_detail_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='issue_detail_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='issue_detail_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class IssueFiles(BaseEntityBasicAbstract):
    """User can create/update/delete issue_files"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file_path = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='issue_file_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='issue_file_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='issue_file_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)


class IssueComments(BaseEntityBasicAbstract):
    """User can create/update/delete issue_comments"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    comment = models.TextField()
    add_file = models.TextField(validators=[URLValidator()])
    created_by = models.ForeignKey(CompanyUsers, related_name='issue_comment_created_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(CompanyUsers, related_name='issue_comment_updated_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)
    deleted_by = models.ForeignKey(CompanyUsers, related_name='issue_comment_deleted_by',
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)








