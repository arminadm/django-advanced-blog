from locust import HttpUser, task

class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post("/accounts/api-v1/jwt/create", data={
            "email": "armin@armin.com",
            "password": "123"
        }).json()
        self.client.headers = {'Authorization': f"Bearer {response.get('access', None)}"}

    @task
    def get_posts_list(self):
        self.client.get("/blog/api-v1/post/")
    
    @task
    def get_categories_list(self):
        self.client.get("/blog/api-v1/category/")