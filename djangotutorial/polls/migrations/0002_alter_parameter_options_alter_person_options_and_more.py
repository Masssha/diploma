# Generated by Django 5.1.5 on 2025-02-02 11:13

import django.db.models.deletion
import django.utils.timezone
import polls.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameter',
            options={'ordering': ('parameter_name',)},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('email',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='person',
            managers=[
                ('objects', polls.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='company',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='person',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='Birthday'),
        ),
        migrations.AddField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='person',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='person',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='person',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='person',
            name='password',
            field=models.CharField(default='12345', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.CharField(choices=[('owner', 'owner'), ('buyer', 'buyer')], default='buyer', max_length=5, verbose_name='user type'),
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='shop',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('basket', 'basket state'), ('new', 'new'), ('confirmed', 'confirmed'), ('assembled', 'assembled'), ('sent', 'sent'), ('delivered', 'delivered'), ('canceled', 'canceled')], max_length=15),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
