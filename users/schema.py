import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.db import transaction
from graphql import GraphQLError
from core.models import Country, Company, CompanyDatabase, ActivationCode, ResetPassword
import secrets
from django.conf import settings
from users.models import Apps, CompanyUsers, Permission, Department, Role, Invitation, Member, Model
from erplicense.models import CompanyUsers as CU
from common_utils.switch_database import SwitchDatabase
from graphql_jwt.decorators import login_required
from common_utils.mailer import Mailer
from common_utils.decorators import check_permission, company_database, check_login
from datetime import datetime, timedelta


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class ResetPasswordType(DjangoObjectType):
    class Meta:
        model = ResetPassword


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission


class AppsType(DjangoObjectType):
    class Meta:
        model = Apps


class CompanyUserTypes(DjangoObjectType):
    class Meta:
        model = CompanyUsers


class CUType(DjangoObjectType):
    class Meta:
        model = CU


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department


class RoleType(DjangoObjectType):
    class Meta:
        model = Role


class InvitationType(DjangoObjectType):
    class Meta:
        model = Invitation


class MemberType(DjangoObjectType):
    class Meta:
        model = Member


class CodeType(DjangoObjectType):
    class Meta:
        model = ActivationCode


class CheckDomain(graphene.Mutation):
    domain = graphene.String()

    class Arguments:
        domain = graphene.String(required=True)

    def mutate(self, info, domain):
        domain_instance = Company.objects.filter(domain=domain).first()
        if domain_instance is not None:
            raise GraphQLError("Domain already exists!")

        return CheckDomain(domain=domain)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    company = graphene.Field(CompanyType)

    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        company = graphene.String(required=True)
        country = graphene.Int(required=True)
        domain = graphene.String(required=True)

    @transaction.atomic
    def mutate(self, info, username, password, email, name, phone, company, country, domain):
        """User registration function"""
        if info.context.user.id is not None:
            raise GraphQLError("You're already logged in!")

        email_check = get_user_model().objects.filter(email=email).first()
        if email_check is not None:
            raise GraphQLError("Email is already in use!")

        user = get_user_model()(
            first_name=name,
            username=username,
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()

        get_country = Country.objects.filter(id=country).first()
        company = Company(name=company, phone=phone, user=user, country=get_country, domain=domain)
        company.save()

        code = secrets.token_hex(16)
        activation = ActivationCode(user=user, code=code)
        activation.save()

        db = CompanyDatabase(db_name="company_" + str(company.id), company=company)
        db.save()

        return CreateUser(user=user, company=company)


class ActivateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    company = graphene.Field(CompanyType)

    class Arguments:
        code = graphene.String(required=True)

    @transaction.atomic
    def mutate(self, info, code):
        """Activates users with the activation code provided"""
        activation = ActivationCode.objects.filter(code=code).first()
        if activation is None:
            raise GraphQLError("Wrong activation code provided!")

        user = get_user_model().objects.filter(id=activation.user_id).first()
        if user is None:
            raise GraphQLError("No user found with the activation code!")

        company = Company.objects.filter(user_id=user.id).first()
        if company is None:
            cu = CU.objects.filter(user_id=user.id).first()
            company = Company.objects.filter(id=cu.company_id).first()

        db = CompanyDatabase.objects.filter(company_id=company.id).first()
        if db is None:
            raise GraphQLError("No database found! Please contact the support center!")

        user.is_active = True
        user.save()
        activation.delete()
        return ActivateUser(user=user, company=company)


class ResetPasswordRequest(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    @check_login
    def mutate(self, info, email):
        """Make a password reset request"""
        user = get_user_model().objects.filter(email=email).first()
        if user is None:
            raise GraphQLError("Email doesn't exist!")

        now = datetime.now()
        earlier = now - timedelta(hours=24)
        check_reset = ResetPassword.objects.filter(user=user,
                                                   created_at__range=(earlier, now)).first()
        if check_reset is not None:
            raise GraphQLError("A password reset link already sent to your email!")

        with transaction.atomic():
            reset = ResetPassword(
                user=user,
                code=secrets.token_hex(16)
            )
            reset.save()

            reset_link = settings.RESET_PASSWORD_URL + reset.code
            subject = 'xERP: Reset password.'
            email_body = "<strong> Reset password! </strong> " \
                         "<p>Click the link below to go to the password reset page." \
                         "</p> <a href=" + reset_link + ">click here</a>  <p> Thank you </p>"

            # sending Mail
            mailer = Mailer()
            response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

        return ResetPasswordRequest(message="An email with password reset link was sent!")


class ResetPasswordDone(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        code = graphene.String(required=True)
        password = graphene.String(required=True)

    @check_login
    def mutate(self, info, email, code, password):
        """Resets with the new password"""
        user = get_user_model().objects.filter(email=email).first()
        if user is None:
            raise GraphQLError("Email doesn't exist!")

        now = datetime.now()
        earlier = now - timedelta(hours=24)
        check_reset = ResetPassword.objects.filter(user=user,
                                                   code=code,
                                                   created_at__range=(earlier, now)).first()
        if check_reset is None:
            raise GraphQLError("No reset request found! Resend code again!")

        with transaction.atomic():
            user.set_password(password)
            user.save()
            check_reset.delete()

        return ResetPasswordDone(message="Password was reset! Try login now!")


class SendInvitation(graphene.Mutation):
    invitation = graphene.Field(InvitationType)
    user = graphene.Field(CompanyUserTypes)
    department = graphene.Field(DepartmentType)
    role = graphene.Field(RoleType)
    module = graphene.Field(AppsType)

    class Arguments:
        email = graphene.String(required=True)
        department = graphene.Int(required=True)
        role = graphene.Int(required=True)
        module = graphene.Int(required=True)

    @login_required
    @company_database
    @check_permission("project", "invitation", "Add")
    def mutate(self, info, db, user, email, department, role, module):
        """Send invitation on a specific app for an email"""
        module_instance = Apps.objects.using(db).filter(module_id=module).first()
        if module_instance is None:
            raise GraphQLError("Wrong module/app provided")

        department_instance = Department.objects.using(db).filter(id=department, app=module_instance).first()
        if department_instance is None:
            raise GraphQLError("Wrong department provided!")

        role_instance = Role.objects.using(db).filter(id=role, app=module_instance).first()
        if role_instance is None:
            raise GraphQLError("Wrong role provided!")

        check_invite = Invitation.objects.using(db).filter(email=email,
                                                           department_id=department,
                                                           role_id=role,
                                                           app_id=module)
        if check_invite.exists():
            raise GraphQLError("Invitation is already sent for this user!")

        check_user = CompanyUsers.objects.using(db).filter(email=email).first()
        if check_user is not None:
            member_check = Member.objects.using(db).filter(user_id=check_user.id,
                                                           app_id=module,
                                                           department_id=department,
                                                           role_id=role).first()
            if member_check is not None:
                return GraphQLError("This member is already on board!")

        with transaction.atomic():
            invite_instance = Invitation(
                email=email,
                department_id=department,
                role_id=role,
                app_id=module,
                invited_by=user
            )
            invite_instance.save(using=db)

            invitation_link = info.context.META['HTTP_DOMAIN'] + '.' + settings.ACCEPT_INVITATION_URL + '?email=' + email + '&module=' + str(module) + '&department=' + str(department) + '&role=' + str(role)
            subject = 'xERP: Accept the invitation.'
            email_body = "<strong> Welcome to xERP! </strong> " \
                         "<p>You are invited on a department. Here is the invitation link given below. Please use this link to registration/accept." \
                         "</p> <a href=" + invitation_link + ">click here</a>  <p> Thank you </p>"

            # sending Mail
            mailer = Mailer()
            response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

        return SendInvitation(invitation=invite_instance)


class AcceptExisting(graphene.Mutation):
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        email = graphene.String(required=True)
        module = graphene.Int(required=True)
        department = graphene.Int(required=True)
        role = graphene.Int(required=True)

    @login_required
    @company_database
    def mutate(self, info, db, user, email, module, department, role):
        """Accept invitation as an existing company user"""
        if user.email != email:
            raise GraphQLError("Wrong email provided!")

        check_invite = Invitation.objects.using(db).filter(email=email,
                                                           department_id=department,
                                                           role_id=role,
                                                           app_id=module).first()

        if check_invite is None:
            raise GraphQLError("No invitation sent to you!")

        company = Company.objects.filter(domain=info.context.META['HTTP_DOMAIN']).first()
        cu = CU(
            company=company,
            module_id=module,
            user=info.context.user,
            is_owner=False
        )
        cu.save()

        member = Member(
            user=user,
            app_id=module,
            department_id=department,
            role_id=role
        )
        member.save(using=db)
        check_invite.delete(using=db)

        return AcceptExisting(user=user)


class AcceptInvite(graphene.Mutation):
    user = graphene.Field(CompanyUserTypes)

    class Arguments:
        email = graphene.String(required=True)
        module = graphene.Int(required=True)
        department = graphene.Int(required=True)
        role = graphene.Int(required=True)

    @login_required
    def mutate(self, info, email, module, department, role):
        """Accept invite as existing in system but not in the company user"""
        domain = info.context.META['HTTP_DOMAIN']
        user = info.context.user
        db = SwitchDatabase.company_database(domain)

        if user.email != email:
            raise GraphQLError("Wrong email provided!")

        check_invite = Invitation.objects.using(db).filter(email=email,
                                                           department_id=department,
                                                           role_id=role,
                                                           app_id=module).first()

        if check_invite is None:
            raise GraphQLError("No invitation sent to you!")

        company = Company.objects.filter(domain=domain).first()
        cu = CU(
            company=company,
            module_id=module,
            user=info.context.user,
            is_owner=False
        )
        cu.save()

        company_user = CompanyUsers(
            user_id=user.id,
            name=user.first_name,
            username=user.username,
            email=user.email,
            is_owner=False
        )
        company_user.save(using=db)

        member = Member(
            user=company_user,
            app_id=module,
            department_id=department,
            role_id=role
        )
        member.save(using=db)
        check_invite.delete(using=db)

        return AcceptExisting(user=company_user)


class AcceptNew(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        module = graphene.Int(required=True)
        department = graphene.Int(required=True)
        role = graphene.Int(required=True)

    def mutate(self, info, name, email, username, password, module, department, role):
        """Accept invitation as new user"""
        if info.context.user.id is not None:
            return GraphQLError("Already logged in!")

        domain = info.context.META['HTTP_DOMAIN']
        db = SwitchDatabase.company_database(domain)

        check_user = get_user_model().objects.filter(email=email).first()
        if check_user is not None:
            raise GraphQLError("You are already on board! Please login first!")

        check_invite = Invitation.objects.using(db).filter(email=email,
                                                           app_id=module,
                                                           department_id=department,
                                                           role_id=role).first()
        if check_invite is None:
            raise GraphQLError("No invitation found!")

        company = Company.objects.filter(domain=domain).first()

        with transaction.atomic():
            user = get_user_model()(
                first_name=name,
                username=username,
                email=email,
                is_active=False
            )
            user.set_password(password)
            user.save()

            company_user = CU(
                company=company,
                module_id=module,
                user=user,
                is_owner=False
            )
            company_user.save()

            code = secrets.token_hex(16)
            activation = ActivationCode(user=user, code=code)
            activation.save()

        cu = CompanyUsers(
            user_id=user.id,
            name=user.first_name,
            username=user.username,
            email=user.email,
            is_owner=False
        )
        cu.save(using=db)

        member = Member(
            user=cu,
            app_id=module,
            department_id=department,
            role_id=role
        )
        member.save(using=db)
        check_invite.delete(using=db)

        return AcceptNew(user=user)


class Mutation(graphene.ObjectType):
    check_domain = CheckDomain.Field()
    create_user = CreateUser.Field()
    activate_user = ActivateUser.Field()
    reset_password_request = ResetPasswordRequest.Field()
    reset_password = ResetPasswordDone.Field()
    send_invitation = SendInvitation.Field()
    accept_new = AcceptNew.Field()
    accept_existing = AcceptExisting.Field()
    accept_invite = AcceptInvite.Field()


class ModelType(DjangoObjectType):
    class Meta:
        model = Model


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType)
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    permissions = graphene.List(PermissionType)
    departments = graphene.List(DepartmentType)
    roles = graphene.List(RoleType)
    codes = graphene.List(CodeType)
    headers = graphene.String()
    companies = graphene.List(CompanyType)
    cu = graphene.List(CUType)
    member = graphene.List(MemberType)
    models = graphene.List(ModelType)

    def resolve_countries(self, info):
        return Country.objects.all()

    def resolve_codes(self, info):
        return ActivationCode.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_companies(self, info):
        # domain = info.context.META['HTTP_DOMAIN']
        user = info.context.user
        # db = SwitchDatabase.company_user(domain, user)
        as_cuser = CU.objects.filter(user=user).values_list('company_id', flat=True).distinct()
        companies = Company.objects.filter(id__in=as_cuser)
        if companies.exists() is False:
            companies = Company.objects.filter(user=user)
        return companies

    @login_required
    @company_database
    def resolve_member(self, info, db, user):
        member = Member.objects.using(db).filter(user=user)
        return member

    @login_required
    @company_database
    @check_permission("project", "permission", "List")
    def resolve_permissions(self, info, db, user):
        return Permission.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "department", "List")
    def resolve_departments(self, info, db, user):
        return Department.objects.using(db).all()

    @login_required
    @company_database
    @check_permission("project", "role", "List")
    def resolve_roles(self, info, db, user):
        return Role.objects.using(db).all()
