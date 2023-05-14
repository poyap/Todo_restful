from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from todo.models import Project, Task
from todo.api.serializers import ProjectSerializer, TaskSerializer

class ProjectTasksListAPIViewTestCase(APITestCase):
    def setUp(self):
        # users
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role=1)
        self.user1 = CustomUser.objects.create_user(username='testuser1', password='testpassword', role=2)
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword',role=2)
        # projects
        self.project = Project.objects.create(name='Test Project', description='Testing project', manager=self.user, status=1)
        self.project1 = Project.objects.create(name='Test Project1', description='Testing project', manager=self.user1, status=1)
        # tasks
        self.task1 = Task.objects.create(name='Task 1', description='Testing task 1', project=self.project, 
                                        status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task2 = Task.objects.create(name='Task 2', description='Testing task 2', project=self.project,
                                        status=2, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task3 = Task.objects.create(name='Task 3', description='Testing task 3', project=self.project1, status=2, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task2.developers.add(self.user1.id)
        self.task3.developers.add(self.user1.id)
    
    def test_developer_in_project_can_see_project_tasks(self):
        self.client.force_login(self.user1)
        url = reverse('todo:project-tasks', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task1, self.task2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
    
    def test_developer_not_in_project_cannot_see_project_tasks(self):
        self.client.force_login(self.user2)
        url = reverse('todo:project-tasks', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task1, self.task2, self.task3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(response.data, serializer_data)
    
    def test_manager_can_see_project_tasks(self):
        """
        Ensure that manager can see lists of tasks whether if they are not in that project.
        """
        self.client.force_login(self.user)
        url = reverse('todo:project-tasks', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task1, self.task2,], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_project_tasks_list_view_with_unauthenticated_user(self):
        """
        Ensure unauthenticated user cannot list tasks of a project.
        """
        url = reverse('todo:project-tasks', kwargs={'project_id': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UserTasksListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role=1)
        self.manager = CustomUser.objects.create_user(username='manager', password='testpassword', role=1)
        self.user1 = CustomUser.objects.create_user(username='testuser1', password='testpassword', role=2)
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', role=2)
        self.user3 = CustomUser.objects.create_user(username='testuser3', password='testpassword',)
        self.user4 = CustomUser.objects.create_user(username='testuser4', password='testpassword',role=2)

        self.project1 = Project.objects.create(name='Test Project 1', description='Testing project 1', manager=self.user, status=1)
        self.task11 = Task.objects.create(name='Task 11', description='Testing task 11', project=self.project1,
                                        status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task12 = Task.objects.create(name='Task 12', description='Testing task 12', project=self.project1,
                                        status=2, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.project2 = Project.objects.create(name='Test Project 2', description='Testing project 2', manager=self.manager, status=1)
        self.task21 = Task.objects.create(name='Task 21', description='Testing task 21', project=self.project2,
        status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task21.developers.add(self.user1.id)
        self.task21.developers.add(self.user2.id)
        self.task22 = Task.objects.create(name='Task 22', description='Testing task 22', project=self.project2,
        status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z')
        self.task22.developers.add(self.user1.id)

    def test_user_tasks_list_view_with_project_manager_user(self):
        """
        Ensure project managers can see all the users tasks.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('todo:user-tasks', kwargs={'project_id':self.project2.id, 'username': self.user1.username})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task21, self.task22], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_user_tasks_list_view_with_developers_in_the_project(self):
        """
        Ensure developers within that project can see other developers tasks.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse('todo:user-tasks', kwargs={'project_id':self.project2.id, 'username': self.user2.username})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task21], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
    
    def test_user_tasks_list_view_with_developers_not_in_the_project(self):
        """
        Ensure developers not in that project can not see other developers/users tasks.
        """
        self.client.force_authenticate(user=self.user4)
        url = reverse('todo:user-tasks', kwargs={'project_id':self.project2.id, 'username': self.user2.username,})
        response = self.client.get(url)
        serializer_data = TaskSerializer([self.task21], many=True).data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_tasks_list_view_with_unauthenticated_user(self):
        """
        Ensure unauthenticated user cannot list all tasks of a user.
        """
        url = reverse('todo:user-tasks', kwargs={'project_id':self.project1.id, 'username': self.user.username,})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProjectManagerTaskAssignAPIViewTestCase(APITestCase):
    def setUp(self):
        self.project_manager = CustomUser.objects.create_user(username='pm_testuser', password='testpassword', role=1)
        self.project_manager1 = CustomUser.objects.create_user(username='pm1_testuser', password='testpassword', role=1)
        self.developer = CustomUser.objects.create_user(username='dev_testuser', password='testpassword', role=2)
        self.developer1 = CustomUser.objects.create_user(username='dev_testuser1', password='testpassword', role=2)
        self.project = Project.objects.create(name='Test Project', description='Testing project', manager=self.project_manager, status=1)
        self.project1 = Project.objects.create(name='Test Project1', description='Testing project', manager=self.project_manager1, status=1)
        self.task = Task.objects.create(name='Task 1', description='Testing task 1', status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z', project=self.project)
        self.task1 = Task.objects.create(name='Task 2', description='Testing task 2', status=1, start_at='2022-05-10T15:30:00Z', deadline='2023-05-10T15:30:00Z', project=self.project)
        self.task.developers.add(self.developer.id)

    def test_project_manager_task_assign_with_valid_project_manager(self):
        """
        Ensure valid project manager(the creator of the project) can assign task to a developer.
        """

        self.client.force_login(self.project_manager)
        url = reverse('todo:task-assign')
        serializer = {
            "id": 3,
            "name": "Task 122",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "developers": [self.developer1.id],
            "project": self.project.id,
            "start_at": "2023-06-01T08:00:00.000Z",
            "deadline": "2023-07-31T23:59:59.000Z",
            "status": 1
        }
        response = self.client.post(url, data=serializer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_project_manager_task_assign_with_different_project_manager(self):
        """
        Ensure different project manager can not assign task to a project that have not created.
        """
        self.client.login(username=self.project_manager1.username, password=self.project_manager1.password)
        url = reverse('todo:task-assign')
        payload = {
            "id": 333,
            "name": "Task 444",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "developers": [self.developer1.id],
            "project": self.project.id,
            "start_at": "2023-06-01T08:00:00.000Z",
            "deadline": "2023-07-31T23:59:59.000Z",
            "status": 1
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.client.logout()
