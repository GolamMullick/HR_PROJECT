from functools import wraps
from django.db import connections
from decouple import config
from graphql import GraphQLError
from core.models import Company, CompanyDatabase
from users.models import CompanyUsers, Apps, Member, Model, Permission, MemberPermission, \
    DepartmentRoleModelPermission, DepartmentModelPermission


def check_permission(module="", model="", permission=""):
    """Provide model & permission for checking the user permission"""
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            user = kwargs['user']
            db = kwargs['db']
            app = Apps.objects.using(db).filter(slug=module).first()
            if app is None:
                raise GraphQLError("No such app found!")

            member = Member.objects.using(db).filter(user=user, app=app)
            if member.exists() is False:
                raise GraphQLError("You're not a member on this company module!")

            model_instance = Model.objects.using(db).filter(name=model,
                                                            app=app).first()
            if model_instance is None:
                raise GraphQLError("No such model found!")

            perm_instance = Permission.objects.using(db).filter(name=permission).first()
            if perm_instance is None:
                raise GraphQLError("No such permission found!")

            check = {}
            for m in member:
                mp = MemberPermission.objects.using(db).filter(member=m,
                                                               model=model_instance,
                                                               permission=perm_instance).first()
                if mp is None:
                    print("Not in mp")
                    drmp = DepartmentRoleModelPermission.objects.using(db).filter(
                        department_id=m.department_id,
                        role_id=m.role_id,
                        model=model_instance,
                        permission=perm_instance
                    ).first()
                    if drmp is None:
                        print("Not in drmp")
                        dmp = DepartmentModelPermission.objects.using(db).filter(
                            department_id=m.department_id,
                            model=model_instance,
                            permission=perm_instance
                        ).first()
                        if dmp is None:
                            print("Not in dmp")
                            check[m.id] = False

                check[m.id] = True

            if True not in check:
                raise GraphQLError("You don't have permission!")

            return func(*args, **kwargs)

        return wrap

    return decorator


def company_database(func):
    """Checks company domain & user then switches the database"""
    @wraps(func)
    def wrap(*args, **kwargs):
        domain = args[1].context.META['HTTP_DOMAIN']
        user = args[1].context.user

        if domain is None:
            raise GraphQLError("Please provide company domain!")

        company = Company.objects.filter(domain=domain).first()
        if company is None:
            raise GraphQLError("Provided company domain doesn't exist!")

        if user is None:
            raise GraphQLError("No user data provided!")

        db = CompanyDatabase.objects.filter(company=company).first()
        if db is None:
            raise GraphQLError("No database found!")

        new_database = {}
        new_database['ENGINE'] = config('DATABASE_ENGINE', cast=str)
        new_database['NAME'] = db.db_name
        new_database['USER'] = config('DATABASE_USER', cast=str)
        new_database['PASSWORD'] = config('DATABASE_PASSWORD', cast=str)
        new_database['HOST'] = config('DATABASE_HOST', cast=str)
        new_database['PORT'] = config('DATABASE_PORT', cast=int)
        connections.databases[db.db_name] = new_database

        try:
            check_user = CompanyUsers.objects.using(db.db_name).filter(user_id=user.id).first()
        except Exception:
            raise GraphQLError("No purchased modules found!")

        if check_user is None:
            raise GraphQLError("User not found!")

        kwargs['db'] = db.db_name
        kwargs['user'] = check_user

        return func(*args, **kwargs)

    return wrap


def check_login(func):
    """checks if a user is logged in"""
    @wraps(func)
    def wrap(*args, **kwargs):
        user = args[1].context.user
        if user.id is not None:
            raise GraphQLError("Please logout to perform this action!")

        return func(*args, **kwargs)

    return wrap

