# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.utils import OperationalError
import django.utils.timezone
import django.core.validators

# Create auth user if it does not already exist, i.e. if migrating
# from an existing database with emory_ldap users.
# A new installation that never had the emory_ldap user model set as
# the django auth_user_model will already have auth.User.


class CreateModelOptional(migrations.CreateModel):
    # extend the createmodel migration operation to make the
    # database forwards optional (catches and swallows an error because
    # the table already exists), and make the backwards do nothing

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        try:
            super(CreateModelOptional, self).database_forwards(app_label,
                schema_editor, from_state, to_state)
        except OperationalError as err:
            # if creating a new db, this will error because auth_user
            # already exists - but that's fine
            pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # do nothing, since creation is optional and table may have existed before
        pass

    def describe(self):
        # base description is something like "create model name"
        return super(CreateModelOptional, self).describe() + ' if it does not already exist'


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        CreateModelOptional(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
            bases=(models.Model,)
        )
    ]
