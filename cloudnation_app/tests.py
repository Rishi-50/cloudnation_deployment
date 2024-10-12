from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import GithubDetails, AppDetails, AppPlans, DatabaseDetails, DbPlans, EnvVariables

CustomUser = get_user_model()

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@example.com", full_name="Test User", password="password123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

class GithubDetailsTestCase(BaseTestCase):

    def test_create_github_details(self):
        url = "/githubdetails/"
        data = {
            "organization": "TestOrg",
            "repo": "TestRepo",
            "branch": "main"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GithubDetails.objects.count(), 1)

    def test_github_details_list(self):
        GithubDetails.objects.create(user=self.user, organization="TestOrg", repo="TestRepo", branch="main")
        url = "/githubdetails/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class AppDetailsTestCase(BaseTestCase):

    def test_create_app_details(self):
        url = "/appdetails/"
        data = {
            "name": "TestApp",
            "region": "India - Mumbai",
            "framework": "React"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AppDetails.objects.count(), 1)

    def test_app_details_list(self):
        AppDetails.objects.create(user=self.user, name="TestApp", region="India - Mumbai", framework="React")
        url = "/appdetails/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class AppPlansTestCase(BaseTestCase):

    def test_create_app_plan(self):
        url = "/appplans/"
        data = {
            "plan_type": "Starter, 10 GB, 512 MB, 2, $0.0278, $20"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AppPlans.objects.count(), 1)

    def test_app_plans_list(self):
        AppPlans.objects.create(user=self.user, plan_type="Starter, 10 GB, 512 MB, 2, $0.0278, $20")
        url = "/appplans/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class DatabaseDetailsTestCase(BaseTestCase):

    def test_create_database_details(self):
        url = "/databasedetails/"
        data = {
            "db_type": "Postgresql"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(DatabaseDetails.objects.count(), 1)

    def test_database_details_list(self):
        DatabaseDetails.objects.create(user=self.user, db_type="Postgresql")
        url = "/databasedetails/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class DbPlansTestCase(BaseTestCase):

    def test_create_db_plan(self):
        url = "/dbplans/"
        data = {
            "plan_type": "Starter, 10 GB, 512 MB, 2, $0.0278, $20"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(DbPlans.objects.count(), 1)

    def test_db_plans_list(self):
        DbPlans.objects.create(user=self.user, plan_type="Starter, 10 GB, 512 MB, 2, $0.0278, $20")
        url = "/dbplans/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    


