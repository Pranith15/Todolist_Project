"""
Seed demo data for TaskFlow Django To-Do App.
Run with: python seed_demo.py
"""

import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from todos.models import Task


def run_seed():
    print("[*] Seeding demo data...")

    username = "demouser"
    password = "Password123!"
    email = "demo@example.com"

    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password(password)
        user.save()
        print(f"Created demo user: '{username}'")
    else:
        print(f"Demo user '{username}' already exists.")

    today = timezone.now().date()

    sample_tasks = [
        {
            'title': 'Set up Django To-Do List Application',
            'description': 'Configure database, models, forms, templates, and authentication.',
            'priority': 'HIGH',
            'completed': True,
            'due_date': today - timedelta(days=2),
        },
        {
            'title': 'Prepare weekly project presentation',
            'description': 'Summarize sprint achievements, open blockers, and milestones.',
            'priority': 'HIGH',
            'completed': False,
            'due_date': today + timedelta(days=1),
        },
        {
            'title': 'Submit travel expense report',
            'description': 'Attach invoice PDFs and receipts for reimbursement.',
            'priority': 'MEDIUM',
            'completed': False,
            'due_date': today - timedelta(days=1),  # Overdue
        },
        {
            'title': 'Read chapter 4 of Clean Code',
            'description': 'Take notes on formatting and meaningful names.',
            'priority': 'LOW',
            'completed': False,
            'due_date': today + timedelta(days=7),
        },
    ]

    for item in sample_tasks:
        task, was_created = Task.objects.get_or_create(
            user=user,
            title=item['title'],
            defaults=item
        )
        if was_created:
            print(f"  + Added task: {task.title}")
        else:
            print(f"  * Task already exists: {task.title}")

    print("\n[SUCCESS] Seed completed successfully!")
    print(f"Login credentials:\n   Username: {username}\n   Password: {password}\n")


if __name__ == '__main__':
    run_seed()
