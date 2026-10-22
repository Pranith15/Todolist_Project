from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task


class TodoAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='Password123!'
        )
        self.user2 = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='Password456!'
        )
        self.task1 = Task.objects.create(
            user=self.user1,
            title='Alice Task 1',
            description='Details for Alice Task 1',
            priority='HIGH',
            completed=False
        )
        self.task2 = Task.objects.create(
            user=self.user2,
            title='Bob Task 1',
            description='Details for Bob Task 1',
            priority='LOW',
            completed=False
        )

    def test_unauthenticated_user_redirected_to_login(self):
        """Unauthenticated user trying to access tasks is redirected to login."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_user_can_login(self):
        """User can log in successfully."""
        response = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))

    def test_user_can_register(self):
        """A new user can register and is redirected to task list."""
        response = self.client.post(reverse('register'), {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password1': 'SecretPass999!',
            'password2': 'SecretPass999!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='charlie').exists())

    def test_user_can_logout(self):
        """Logged in user can log out."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_task_list_isolation(self):
        """User only sees their own tasks."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Task 1')
        self.assertNotContains(response, 'Bob Task 1')

    def test_add_task(self):
        """Logged in user can add a task."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.post(reverse('task_create'), {
            'title': 'New Test Task',
            'description': 'Test description',
            'priority': 'MEDIUM',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(user=self.user1, title='New Test Task').exists())

    def test_edit_task(self):
        """Logged in user can edit their own task."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.post(reverse('task_update', kwargs={'pk': self.task1.id}), {
            'title': 'Updated Alice Task',
            'description': 'Updated description',
            'priority': 'HIGH',
            'completed': True,
        })
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Alice Task')
        self.assertTrue(self.task1.completed)

    def test_cannot_edit_other_user_task(self):
        """User cannot edit another user's task (returns 404)."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.post(reverse('task_update', kwargs={'pk': self.task2.id}), {
            'title': 'Hacked Bob Task',
            'priority': 'HIGH',
        })
        self.assertEqual(response.status_code, 404)
        self.task2.refresh_from_db()
        self.assertEqual(self.task2.title, 'Bob Task 1')

    def test_delete_task(self):
        """Logged in user can delete their own task."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.post(reverse('task_delete', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_cannot_delete_other_user_task(self):
        """User cannot delete another user's task (returns 404)."""
        self.client.login(username='alice', password='Password123!')
        response = self.client.post(reverse('task_delete', kwargs={'pk': self.task2.id}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=self.task2.id).exists())

    def test_toggle_task_completion(self):
        """Logged in user can toggle a task's completed status."""
        self.client.login(username='alice', password='Password123!')
        self.assertFalse(self.task1.completed)

        # Toggle to completed
        response = self.client.get(reverse('task_toggle', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

        # Toggle back to incomplete
        response = self.client.get(reverse('task_toggle', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.completed)

    def test_search_and_filter(self):
        """Task filtering by search keyword and status works."""
        self.client.login(username='alice', password='Password123!')
        Task.objects.create(user=self.user1, title='Buy Groceries', priority='LOW', completed=True)

        # Search for 'Groceries'
        response = self.client.get(reverse('task_list') + '?q=Groceries')
        self.assertContains(response, 'Buy Groceries')
        self.assertNotContains(response, 'Alice Task 1')

        # Filter by completed status
        response = self.client.get(reverse('task_list') + '?status=completed')
        self.assertContains(response, 'Buy Groceries')
        self.assertNotContains(response, 'Alice Task 1')
