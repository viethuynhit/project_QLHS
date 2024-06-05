
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import studentMan.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('role', models.CharField(choices=[('1', 'Admin'), ('2', 'Teacher'), ('3', 'Student')], default='1', max_length=1)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('dateOfBirth', models.DateTimeField(default=datetime.datetime(2022, 6, 8, 0, 0))),
                ('sex', models.CharField(choices=[('1', 'Nam'), ('0', 'Nữ')], default='1', max_length=1)),
                ('phone', models.CharField(default='', max_length=20)),
                ('email', models.EmailField(default='', max_length=254)),
                ('address', models.TextField(default='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', studentMan.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=200, unique=True)),
                ('max_age', models.IntegerField()),
                ('min_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassOfSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classId', models.CharField(max_length=200)),
                ('max_number', models.IntegerField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentMan.age')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubjectID', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('approved_mark', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classOfSchool', models.ManyToManyField(blank=True, to='studentMan.classofschool')),
                ('subject', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='studentMan.subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classOfSchool', models.ManyToManyField(blank=True, to='studentMan.ClassOfSchool')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_mark', models.CharField(choices=[('1', '1'), ('2', '2')], max_length=200)),
                ('markFifteen', models.FloatField(blank=True, null=True)),
                ('markOne', models.FloatField(blank=True, null=True)),
                ('markFinal', models.FloatField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentMan.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentMan.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
