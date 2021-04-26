# Generated by Django 3.1.5 on 2021-04-22 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('status', models.BooleanField()),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='catagory_created_by', to=settings.AUTH_USER_MODEL)),
                ('modify_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='catogory_modify_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_admin.category')),
            ],
        ),
    ]