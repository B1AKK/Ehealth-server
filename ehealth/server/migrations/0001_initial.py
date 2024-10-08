# Generated by Django 5.0.3 on 2024-03-20 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.user')),
                ('specialization', models.CharField(max_length=64)),
            ],
            bases=('server.user',),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.user')),
                ('status', models.CharField(max_length=64)),
                ('med_info', models.CharField(max_length=255)),
            ],
            bases=('server.user',),
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.user')),
            ],
            bases=('server.user',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('rb', 'Radiobutton'), ('chb', 'Checkbox'), ('txt', 'Text')], max_length=16)),
                ('options', models.JSONField()),
                ('form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='server.form')),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='doctor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forms', to='server.doctor'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='patients',
            field=models.ManyToManyField(to='server.employee'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='server.question')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='server.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='manager_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff', to='server.manager'),
        ),
    ]
