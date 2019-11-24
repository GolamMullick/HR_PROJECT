import graphene
from graphene_django import DjangoObjectType
from .models import Project, ProjectFiles, ProjectDetails, Goal, GoalFiles, GoalDetails, \
    Task, TaskFiles, TaskDetails, TaskComments, Issue, IssueDetails, IssueFiles, IssueComments
from django.db import transaction
from graphql import GraphQLError
from users.schema import CompanyUserTypes
from graphql_jwt.decorators import login_required
from datetime import datetime
from common_utils.decorators import check_permission, company_database


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project


class ProjectFilesType(DjangoObjectType):
    class Meta:
        model = ProjectFiles


class ProjectDetailsType(DjangoObjectType):
    class Meta:
        model = ProjectDetails


class GoalType(DjangoObjectType):
    class Meta:
        model = Goal


class GoalFilesType(DjangoObjectType):
    class Meta:
        model = GoalFiles


class GoalDetailsType(DjangoObjectType):
    class Meta:
        model = GoalDetails


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class TaskFilesType(DjangoObjectType):
    class Meta:
        model = TaskFiles


class TaskDetailsType(DjangoObjectType):
    class Meta:
        model = TaskDetails


class TaskCommentsType(DjangoObjectType):
    class Meta:
        model = TaskComments


class IssueType(DjangoObjectType):
    class Meta:
        model = Issue


class IssueDetailsType(DjangoObjectType):
    class Meta:
        model = IssueDetails


class IssueFilesType(DjangoObjectType):
    class Meta:
        model = IssueFiles


class IssueCommentsType(DjangoObjectType):
    class Meta:
        model = IssueComments


class CreateProject(graphene.Mutation):
    project = graphene.Field(ProjectType)
    details = graphene.List(ProjectDetailsType)
    files = graphene.List(ProjectFilesType)
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "project", "Add")
    def mutate(self, info, db, user,  title, **kwargs):
        description = kwargs.get("description")
        start_date = None
        end_date = None

        if kwargs.get('start_date') is not None:
            start_date = datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d')
        if kwargs.get('end_date') is not None:
            end_date = datetime.strptime(kwargs.get('end_date'), '%Y-%m-%d')

        with transaction.atomic():
            project_instance = Project(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                created_by=user
            )

            project_instance.save(using=db)

        return CreateProject(project=project_instance)


class DeleteProject(graphene.Mutation):
    project_deleted = graphene.Field(ProjectType)

    class Arguments:
        project = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "project", "Remove")
    def mutate(self, info, db, user, project):
        project_instance = Project.objects.using(db).filter(id=project,
                                                            deleted_at=None,
                                                            deleted_by=None).first()

        if project_instance is None:
            raise GraphQLError("Project not found!")

        with transaction.atomic():
            project_instance.deleted_at = datetime.utcnow()
            project_instance.deleted_by = user
            project_instance.save(using=db)

        return DeleteProject(project_deleted=project_instance)


class UpdateProject(graphene.Mutation):
    project_updated = graphene.Field(ProjectType)

    class Arguments:
        project = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "project", "Edit")
    def mutate(self, info, db, user, project, **kwargs):
        project_instance = Project.objects.using(db).filter(id=project,
                                                            deleted_at=None,
                                                            deleted_by=None).first()
        if project_instance is None:
            raise GraphQLError("Project is not found!")

        with transaction.atomic():
            if kwargs.get('title') is not None:
                project_instance.title = kwargs.get('title')
            if kwargs.get('description') is not None:
                project_instance.description = kwargs.get('description')
            if kwargs.get('start_date') is not None:
                project_instance.start_date = kwargs.get(' start_date')
            if kwargs.get('end_date') is not None:
                project_instance.end_date = kwargs.get('end_date')

            project_instance.updated_by = user
            project_instance.updated_at = datetime.utcnow()
            project_instance.save(using=db)

        return UpdateProject(project_updated=project_instance)


class DetailsBulkInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    value = graphene.String(required=True)


class CreateProjectDetails(graphene.Mutation):
    details = graphene.List(ProjectDetailsType)

    class Arguments:
        project = graphene.Int(required=True)
        details = graphene.List(DetailsBulkInput)

    @login_required
    @company_database
    @check_permission("project", "projectdetails", "Add")
    def mutate(self, info, db, user, project, details):
        project_instance = Project.objects.using(db).filter(id=project,
                                                            deleted_at=None,
                                                            deleted_by=None).first()
        if project_instance is None:
            raise GraphQLError("Project is not found!")

        project_details = []

        for d in details:
            detail = ProjectDetails(
                key=d.key,
                value=d.value,
                project=project_instance,
                created_by=user
            )
            detail.save(using=db)
            project_details.append(detail)

        return CreateProjectDetails(details=project_details)


class UpdateProjectDetails(graphene.Mutation):
    details_updated = graphene.Field(ProjectDetailsType)

    class Arguments:
        details = graphene.Int(required=True)
        key = graphene.String()
        value = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "projectdetails", "Edit")
    def mutate(self, info, db, user, details, **kwargs):
        details_instance = ProjectDetails.objects.using(db).filter(id=details,
                                                                   deleted_at=None,
                                                                   deleted_by=None).first()
        if details_instance is None:
            raise GraphQLError("Details  not found!")

        if kwargs.get('key') is not None:
            details_instance.key = kwargs.get('key')
        if kwargs.get('value') is not None:
            details_instance.value = kwargs.get('value')

        details_instance.updated_by = user
        details_instance.updated_at = datetime.utcnow()
        details_instance.save(using=db)

        return UpdateProjectDetails(details_updated=details_instance)


class DeleteProjectDetails(graphene.Mutation):
    details_deleted = graphene.Field(ProjectDetailsType)

    class Arguments:
        details = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "projectdetails", "Remove")
    def mutate(self, info, db, user, details):
        details_instance = ProjectDetails.objects.using(db).filter(id=details,
                                                                   deleted_at=None,
                                                                   deleted_by=None).first()

        if details_instance is None:
            raise GraphQLError("Details  not found!")

        details_instance.deleted_by = user
        details_instance.deleted_at = datetime.utcnow()
        details_instance.save(using=db)

        return DeleteProjectDetails(details_deleted=details_instance)


class CreateGoal(graphene.Mutation):
    goal = graphene.Field(GoalType)
    details = graphene.List(GoalDetailsType)
    files = graphene.List(GoalFilesType)
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        project = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "goal", "Add")
    def mutate(self, info, db, user, title, project, **kwargs):
        project_instance = Project.objects.using(db).filter(id=project,
                                                            deleted_at=None,
                                                            deleted_by=None).first()

        if project_instance is None:
            raise GraphQLError("Project not found!")

        description = kwargs.get("description")
        start_date = None
        end_date = None

        if kwargs.get('start_date') is not None:
            start_date = datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d')
        if kwargs.get('end_date') is not None:
            end_date = datetime.strptime(kwargs.get('end_date'), '%Y-%m-%d')
        with transaction.atomic():
            goal_instance = Goal(
                title=title,
                project=project_instance,
                description=description,
                start_date=start_date,
                end_date=end_date,
                created_by=user
            )
            goal_instance.save(using=db)

        return CreateGoal(goal=goal_instance)


class UpdateGoal(graphene.Mutation):
    goal_updated = graphene.Field(GoalType)

    class Arguments:
        goal = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "goal", "Edit")
    def mutate(self, info, db, user, goal, **kwargs):
        goal_instance = Goal.objects.using(db).filter(id=goal,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if goal_instance is None:
            raise GraphQLError("Goal is not found!")

        with transaction.atomic():
            if kwargs.get('title') is not None:
                goal_instance.title = kwargs.get('title')
            if kwargs.get('description') is not None:
                goal_instance.description = kwargs.get('description')
            if kwargs.get('start_date') is not None:
                goal_instance.start_date = kwargs.get(' start_date')
            if kwargs.get('end_date') is not None:
                goal_instance.end_date = kwargs.get('end_date')

            goal_instance.updated_by = user
            goal_instance.updated_at = datetime.utcnow()
            goal_instance.save(using=db)

        return UpdateGoal(goal_updated=goal_instance)


class DeleteGoal(graphene.Mutation):
    goal_deleted = graphene.Field(GoalType)

    class Arguments:
        goal = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "goal", "Remove")
    def mutate(self, info, db, user, goal):
        goal_instance = Goal.objects.using(db).filter(id=goal,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if goal_instance is None:
            raise GraphQLError("Goal not found!")

        with transaction.atomic():
            goal_instance.deleted_at = datetime.utcnow()
            goal_instance.deleted_by = user
            goal_instance.save(using=db)

        return DeleteGoal(goal_deleted=goal_instance)


class CreateGoalDetails(graphene.Mutation):
    details = graphene.List(GoalDetailsType)

    class Arguments:
        goal = graphene.Int(required=True)
        details = graphene.List(DetailsBulkInput)

    @login_required
    @company_database
    @check_permission("project", "goaldetails", "Add")
    def mutate(self, info, db, user, goal, details):
        goal_instance = Goal.objects.using(db).filter(id=goal,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if goal_instance is None:
            raise GraphQLError("Goal not found!")

        goal_details = []

        for d in details:
            detail = GoalDetails(
                key=d.key,
                value=d.value,
                goal=goal_instance,
                created_by=user
            )
            detail.save(using=db)
            goal_details.append(detail)

        return CreateGoalDetails(details=goal_details)


class UpdateGoalDetails(graphene.Mutation):
    details_updated = graphene.Field(GoalDetailsType)

    class Arguments:
        details = graphene.Int(required=True)
        key = graphene.String()
        value = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "projectdetails", "Edit")
    def mutate(self, info, db, user, details, **kwargs):
        details_instance = GoalDetails.objects.using(db).filter(id=details,
                                                                deleted_at=None,
                                                                deleted_by=None).first()
        if details_instance is None:
            raise GraphQLError("Details  not found!")

        if kwargs.get('key') is not None:
            details_instance.key = kwargs.get('key')
        if kwargs.get('value') is not None:
            details_instance.value = kwargs.get('value')

        details_instance.updated_by = user
        details_instance.updated_at = datetime.utcnow()
        details_instance.save(using=db)

        return UpdateGoalDetails(details_updated=details_instance)


class DeleteGoalDetails(graphene.Mutation):
    details_deleted = graphene.Field(GoalDetailsType)

    class Arguments:
        details = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "goaldetails", "Remove")
    def mutate(self, info, db, user, details):
        details_instance = GoalDetails.objects.using(db).filter(id=details,
                                                                deleted_at=None,
                                                                deleted_by=None).first()

        if details_instance is None:
            raise GraphQLError("Details  not found!")

        details_instance.deleted_by = user
        details_instance.deleted_at = datetime.utcnow()
        details_instance.save(using=db)

        return DeleteGoalDetails(details_deleted=details_instance)


class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)
    details = graphene.List(TaskDetailsType)
    files = graphene.List(TaskFilesType)
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        goal = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "task", "Add")
    def mutate(self, info, db, user, title, goal, **kwargs):
        goal_instance = Goal.objects.using(db).filter(id=goal,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if goal_instance is None:
            raise GraphQLError("Goal is not found!")

        description = kwargs.get("description")
        start_date = None
        end_date = None

        if kwargs.get('start_date') is not None:
            start_date = datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d')
        if kwargs.get('end_date') is not None:
            end_date = datetime.strptime(kwargs.get('end_date'), '%Y-%m-%d')

        with transaction.atomic():
            task_instance = Task(
                title=title,
                goal=goal_instance,
                description=description,
                start_date=start_date,
                end_date=end_date,
                reporter=user
            )
            task_instance.save(using=db)

        return CreateTask(task=task_instance)


class UpdateTask(graphene.Mutation):
    task_updated = graphene.Field(TaskType)

    class Arguments:
        task = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "task", "Edit")
    def mutate(self, info, db, user, task, **kwargs):
        task_instance = Task.objects.using(db).filter(id=task,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if task_instance is None:
            raise GraphQLError("Task is not found!")

        with transaction.atomic():
            if kwargs.get('title') is not None:
                task_instance.title = kwargs.get('title')
            if kwargs.get('description') is not None:
                task_instance.description = kwargs.get('description')
            if kwargs.get('start_date') is not None:
                task_instance.start_date = kwargs.get(' start_date')
            if kwargs.get('end_date') is not None:
                task_instance.end_date = kwargs.get('end_date')

            task_instance.updated_by = user
            task_instance.updated_at = datetime.utcnow()
            task_instance.save(using=db)

        return UpdateTask(task_updated=task_instance)


class DeleteTask(graphene.Mutation):
    task_deleted = graphene.Field(TaskType)

    class Arguments:
        task = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "task", "Remove")
    def mutate(self, info, user, db,  task):
        task_instance = Task.objects.using(db).filter(id=task,
                                                      deleted_at=None,
                                                      deleted_by=None).first()

        if task_instance is None:
            raise GraphQLError("Task not found!")

        with transaction.atomic():
            task_instance.deleted_at = datetime.utcnow()
            task_instance.deleted_by = user
            task_instance.save(using=db)

        return DeleteTask(task_deleted=task_instance)


class CreateTaskDetails(graphene.Mutation):
    details = graphene.List(TaskDetailsType)

    class Arguments:
        task = graphene.Int(required=True)
        details = graphene.List(DetailsBulkInput)

    @login_required
    @company_database
    @check_permission("project", "taskdetails", "Add")
    def mutate(self, info, db, user, task, details):
        task_instance = Task.objects.using(db).filter(id=task,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if task_instance is None:
            raise GraphQLError("Task not found!")

        task_details = []

        for d in details:
            detail = TaskDetails(
                key=d.key,
                value=d.value,
                task=task_instance,
                created_by=user
            )
            detail.save(using=db)
            task_details.append(detail)

        return CreateTaskDetails(details=task_details)


class UpdateTaskDetails(graphene.Mutation):
    details_updated = graphene.Field(TaskDetailsType)

    class Arguments:
        details = graphene.Int(required=True)
        key = graphene.String()
        value = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "taskdetails", "Edit")
    def mutate(self, info, db, user, details, **kwargs):
        details_instance = TaskDetails.objects.using(db).filter(id=details,
                                                                deleted_at=None,
                                                                deleted_by=None).first()
        if details_instance is None:
            raise GraphQLError("Details  not found!")

        if kwargs.get('key') is not None:
            details_instance.key = kwargs.get('key')
        if kwargs.get('value') is not None:
            details_instance.value = kwargs.get('value')

        details_instance.updated_by = user
        details_instance.updated_at = datetime.utcnow()
        details_instance.save(using=db)

        return UpdateTaskDetails(details_updated=details_instance)


class DeleteTaskDetails(graphene.Mutation):
    details_deleted = graphene.Field(TaskDetailsType)

    class Arguments:
        details = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "taskdetails", "Remove")
    def mutate(self, info, db, user, details):
        details_instance = GoalDetails.objects.using(db).filter(id=details,
                                                                deleted_at=None,
                                                                deleted_by=None).first()

        if details_instance is None:
            raise GraphQLError("Details  not found!")

        details_instance.deleted_by = user
        details_instance.deleted_at = datetime.utcnow()
        details_instance.save(using=db)

        return DeleteTaskDetails(details_deleted=details_instance)


class CreateTaskComments(graphene.Mutation):
    comments = graphene.Field(TaskCommentsType)

    class Arguments:
        task = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @login_required
    @company_database
    @check_permission("project", "taskcomments", "Add")
    def mutate(self, info, db, user, task, comment):
        task_instance = Task.objects.using(db).filter(id=task,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if task_instance is None:
            raise GraphQLError("Task not found!")

        with transaction.atomic():
            comment_instance = TaskComments(
                task=task_instance,
                comment=comment,
                created_by=user
            )
            comment_instance.save(using=db)

        return CreateTaskComments(comments=comment_instance)


class UpdateTaskComments(graphene.Mutation):
    comment_updated = graphene.Field(TaskCommentsType)

    class Arguments:
        comment = graphene.Int(required=True)
        text = graphene.String(required=True)

    @login_required
    @company_database
    @check_permission("project", "taskcomments", "Edit")
    def mutate(self, info, db, user, comment, **kwargs):
        comment_instance = TaskComments.objects.using(db).filter(id=comment,
                                                                 deleted_at=None,
                                                                 deleted_by=None).first()
        if comment_instance is None:
            raise GraphQLError("Task comment not found!")

        with transaction.atomic():
            if kwargs.get('text') is not None:
                comment_instance.text = kwargs.get('text')

            comment_instance.updated_by = user
            comment_instance.updated_at = datetime.utcnow()
            comment_instance.save(using=db)

        return UpdateTaskComments(comment_updated=comment_instance)


class DeleteTaskComments(graphene.Mutation):
    comment_deleted = graphene.Field(TaskCommentsType)

    class Arguments:
        comment = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "taskcomments", "Remove")
    def mutate(self, info, db, user, comment):
        comment_instance = TaskComments.objects.using(db).filter(id=comment,
                                                                 deleted_at=None,
                                                                 deleted_by=None).first()
        if comment_instance is None:
            raise GraphQLError("Task comment not found!")

        with transaction.atomic():
            comment_instance.deleted_by = user
            comment_instance.deleted_at = datetime.utcnow()
            comment_instance.save(using=db)

        return DeleteTaskComments(comment_deleted=comment_instance)


class CreateIssue(graphene.Mutation):
    issue = graphene.Field(IssueType)
    details = graphene.List(IssueDetailsType)
    files = graphene.List(IssueFilesType)
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        task = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        target_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "issue", "Add")
    def mutate(self, info, db, user, title, task, **kwargs):
        task_instance = Task.objects.using(db).filter(id=task,
                                                      deleted_at=None,
                                                      deleted_by=None).first()
        if task_instance is None:
            raise GraphQLError("Task not found!")

        description = kwargs.get("description")

        target_date = None

        if kwargs.get('target_date') is not None:
            target_date = datetime.strptime(kwargs.get('target_date'), '%Y-%m-%d')

        with transaction.atomic():
            issue_instance = Issue(
                title=title,
                task=task_instance,
                description=description,
                target_date=target_date,
                created_by=user
            )
            issue_instance.save(using=db)

        return CreateIssue(issue=issue_instance)


class UpdateIssue(graphene.Mutation):
    issue_updated = graphene.Field(IssueType)

    class Arguments:
        issue = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        target_date = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "issue", "Edit")
    def mutate(self, info, db, user, issue, **kwargs):
        issue_instance = Issue.objects.using(db).filter(id=issue,
                                                        deleted_at=None,
                                                        deleted_by=None).first()
        if issue_instance is None:
            raise GraphQLError("Issue not found!")

        with transaction.atomic():
            if kwargs.get('title') is not None:
                issue_instance.title = kwargs.get('title')
            if kwargs.get('description') is not None:
                issue_instance.description = kwargs.get('description')
            if kwargs.get('target_date') is not None:
                issue_instance.target_date = kwargs.get(' target_date')

            issue_instance.updated_by = user
            issue_instance.updated_at = datetime.utcnow()
            issue_instance.save(using=db)

        return UpdateIssue(issue_updated=issue_instance)


class DeleteIssue(graphene.Mutation):
    issue_deleted = graphene.Field(IssueType)

    class Arguments:
        issue = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "issue", "Remove")
    def mutate(self, info, db, user, issue):
        issue_instance = Issue.objects.using(db).filter(id=issue,
                                                        deleted_at=None,
                                                        deleted_by=None).first()

        if issue_instance is None:
            raise GraphQLError("Issue not found!")

        with transaction.atomic():
            issue_instance.deleted_at = datetime.utcnow()
            issue_instance.deleted_by = user
            issue_instance.save(using=db)

        return DeleteIssue(issue_deleted=issue_instance)


class CreateIssueDetails(graphene.Mutation):
    details = graphene.List(IssueDetailsType)

    class Arguments:
        issue = graphene.Int(required=True)
        details = graphene.List(DetailsBulkInput)

    @login_required
    @company_database
    @check_permission("project", "issuedetails", "Add")
    def mutate(self, info, db, user, issue, details):
        issue_instance = Issue.objects.using(db).filter(id=issue,
                                                        deleted_at=None,
                                                        deleted_by=None).first()
        if issue_instance is None:
            raise GraphQLError("Issue not found!")

        issue_details = []

        for d in details:
            detail = IssueDetails(
                key=d.key,
                value=d.value,
                issue=issue_instance,
                created_by=user
            )
            detail.save(using=db)
            issue_details.append(detail)

        return CreateIssueDetails(details=issue_details)


class UpdateIssueDetails(graphene.Mutation):
    details_updated = graphene.Field(IssueDetailsType)

    class Arguments:
        details = graphene.Int(required=True)
        key = graphene.String()
        value = graphene.String()

    @login_required
    @company_database
    @check_permission("project", "issuedetails", "Edit")
    def mutate(self, info, db, user, details, **kwargs):
        details_instance = IssueDetails.objects.using(db).filter(id=details,
                                                                 deleted_at=None,
                                                                 deleted_by=None).first()
        if details_instance is None:
            raise GraphQLError("Details  not found!")

        if kwargs.get('key') is not None:
            details_instance.key = kwargs.get('key')
        if kwargs.get('value') is not None:
            details_instance.value = kwargs.get('value')

        details_instance.updated_by = user
        details_instance.updated_at = datetime.utcnow()
        details_instance.save(using=db)

        return UpdateIssueDetails(details_updated=details_instance)


class DeleteIssueDetails(graphene.Mutation):
    details_deleted = graphene.Field(IssueDetailsType)

    class Arguments:
        details = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "issuedetails", "Remove")
    def mutate(self, info, db, user, details):
        details_instance = IssueDetails.objects.using(db).filter(id=details,
                                                                 deleted_at=None,
                                                                 deleted_by=None).first()

        if details_instance is None:
            raise GraphQLError("Details  not found!")

        details_instance.deleted_by = user
        details_instance.deleted_at = datetime.utcnow()
        details_instance.save(using=db)

        return DeleteIssueDetails(details_deleted=details_instance)


class CreateIssueComments(graphene.Mutation):
    comments = graphene.Field(IssueCommentsType)

    class Arguments:
        issue = graphene.Int(required=True)
        comment = graphene.String(required=True)

    @login_required
    @company_database
    @check_permission("project", "issuecomments", "Add")
    def mutate(self, info, db, user, issue, comment):
        issue_instance = Issue.objects.using(db).filter(id=issue,
                                                        deleted_at=None,
                                                        deleted_by=None).first()
        if issue_instance is None:
            raise GraphQLError("Issue not found!")

        with transaction.atomic():
            comment_instance = IssueComments(
                issue=issue_instance,
                comment=comment,
                created_by=user
            )
            comment_instance.save(using=db)

        return CreateIssueComments(comments=comment_instance)


class UpdateIssueComments(graphene.Mutation):
    comment_updated = graphene.Field(IssueCommentsType)

    class Arguments:
        comment = graphene.Int(required=True)
        text = graphene.String(required=True)

    @login_required
    @company_database
    @check_permission("project", "issuecomments", "Edit")
    def mutate(self, info, db, user, comment, **kwargs):
        comment_instance = IssueComments.objects.using(db).filter(id=comment,
                                                                  deleted_at=None,
                                                                  deleted_by=None).first()
        if comment_instance is None:
            raise GraphQLError("Issue comment not found!")

        with transaction.atomic():
            if kwargs.get('text') is not None:
                comment_instance.text = kwargs.get('text')

            comment_instance.updated_by = user
            comment_instance.updated_at = datetime.utcnow()
            comment_instance.save(using=db)

        return UpdateIssueComments(comment_updated=comment_instance)


class DeleteIssueComments(graphene.Mutation):
    comment_deleted = graphene.Field(IssueCommentsType)

    class Arguments:
        comment = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "taskcomments", "Remove")
    def mutate(self, info, db, user, comment):
        comment_instance = IssueComments.objects.using(db).filter(id=comment,
                                                                  deleted_at=None,
                                                                  deleted_by=None).first()
        if comment_instance is None:
            raise GraphQLError("comment not found!")

        with transaction.atomic():
            comment_instance.deleted_by = user
            comment_instance.deleted_at = datetime.utcnow()
            comment_instance.save(using=db)

        return DeleteIssueComments(comment_deleted=comment_instance)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_project_details = CreateProjectDetails.Field()
    update_project_details = UpdateProjectDetails.Field()
    delete_project_details = DeleteProjectDetails.Field()
    create_goal = CreateGoal.Field()
    update_goal = UpdateGoal.Field()
    delete_goal = DeleteGoal.Field()
    create_goal_details = CreateGoalDetails.Field()
    update_goal_details = UpdateGoalDetails.Field()
    delete_goal_details = DeleteGoalDetails.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    create_task_details = CreateTaskDetails.Field()
    update_task_details = UpdateTaskDetails.Field()
    delete_task_details = DeleteTaskDetails.Field()
    create_task_comments = CreateTaskComments.Field()
    update_task_comments = UpdateTaskComments.Field()
    delete_task_comments = DeleteTaskComments.Field()
    create_issue = CreateIssue.Field()
    update_issue = UpdateIssue.Field()
    delete_issue = DeleteIssue.Field()
    create_issue_details = CreateIssueDetails.Field()
    update_issue_details = UpdateIssueDetails.Field()
    delete_issue_details = DeleteIssueDetails.Field()
    create_issue_comments = CreateIssueComments.Field()
    update_issue_comments = UpdateIssueComments.Field()
    delete_issue_comments = DeleteIssueComments.Field()


class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)
    project = graphene.Field(ProjectType, project=graphene.Int())
    project_files = graphene.List(ProjectFilesType)
    project_details = graphene.List(ProjectDetailsType)
    goals = graphene.List(GoalType)
    goal = graphene.Field(GoalType, goal=graphene.Int())
    goal_files = graphene.List(GoalFilesType)
    goal_details = graphene.List(GoalDetailsType)
    tasks = graphene.List(TaskType)
    task = graphene.Field(TaskType, task=graphene.Int())
    task_files = graphene.List(TaskFilesType)
    task_details = graphene.List(TaskDetailsType)
    issues = graphene.List(IssueType)
    issue = graphene.Field(IssueType, issue=graphene.Int())
    issue_files = graphene.List(IssueFilesType)
    issue_details = graphene.List(IssueDetailsType)

    @login_required
    @company_database
    @check_permission("project", "project", "List")
    def resolve_projects(self, info, user, db):
        return Project.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "project", "View")
    def resolve_project(self, info, db,user, project):
        return Project.objects.using(db).get(pk=project)

    @login_required
    @company_database
    @check_permission("project", "projectdetails", "List")
    def resolve_project_details(self, info, user, db):
        return ProjectDetails.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "goal", "List")
    def resolve_goals(self, info, user, db):
        return Goal.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "goal", "View")
    def resolve_goal(self, info, user, db, goal):
        return Goal.objects.using(db).get(pk=goal)

    @login_required
    @company_database
    @check_permission("project", "goaldetails", "List")
    def resolve_goal_details(self, info, user, db):
        return GoalDetails.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "task", "List")
    def resolve_tasks(self, info, user, db):
        return Task.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "task", "View")
    def resolve_task(self, info, user, db, task):
        return Task.objects.using(db).get(pk=task)

    @login_required
    @company_database
    @check_permission("project", "taskdetails", "List")
    def resolve_task_details(self, info, user, db):
        return TaskDetails.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "issue", "List")
    def resolve_issues(self, info, user, db):
        return Issue.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "task", "View")
    def resolve_issue(self, info, user, db, issue):
        return Issue.objects.using(db).get(pk=issue)

    @login_required
    @company_database
    @check_permission("project", "issuedetails", "List")
    def resolve_issue_details(self, info, user,  db):
        return IssueDetails.objects.using(db).all()

