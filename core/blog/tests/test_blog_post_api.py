from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from datetime import datetime
from accounts.models import User

@pytest.fixture
def apiClient():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email = 'test@pytest.com',
        password = 'complexpassword123@',
    )
    return user

@pytest.mark.django_db
class TestPostApi():
    client = APIClient()
    def test_getMethod_postList_response_200_status_code(self, apiClient):
        url = reverse('blog:api-v1:post-list')
        response = apiClient.get(url)
        assert response.status_code == 200
    
    def test_postMethod_unAuthorized_createPost_response_401_status_code(self, apiClient):
        url = reverse('blog:api-v1:post-list')
        data = { 
            "title" : 'this post created by test case',
            "content" : 'this is a content about that post which created by test case',
            "status" : True,
            "published_date" : datetime.now()
        }
        response = apiClient.post(url, data=data)
        assert response.status_code == 401
    
    def test_postMethod_Authorized_createPost_validData_response_201_status_code(self, common_user, apiClient):
        url = reverse('blog:api-v1:post-list')
        user = common_user
        # for user login you can use both force_login or force_authenticate
        # apiClient.force_login(user)
        apiClient.force_authenticate(user)
        data = {
            "title" : 'this post created by test case',
            "content" : 'this is a content about that post which created by test case',
            "status" : True,
            "published_date" : datetime.now()   
        }
        response = apiClient.post(url, data=data)
        assert response.status_code == 201
    
    def test_postMethod_Authorized_createPost_invalidData_response_400_status_code(self, apiClient, common_user):
        url = reverse('blog:api-v1:post-list')
        user = common_user
        apiClient.force_login(user)
        data = {}
        response = apiClient.post(url, data=data)
        assert response.status_code == 400
