from locust import HttpUser, task, between
import os
class CRMUser(HttpUser):
    wait_time=between(0.2,1.0)
    def on_start(self):
        r=self.client.post('/api/auth/login',json={'login':os.getenv('CRM_USER','user'),'password':os.getenv('CRM_PASSWORD','user123')})
        self.headers={'Authorization':f'Bearer {r.json()["access_token"]}'}
    @task(5)
    def institutions(self): self.client.get('/api/institutions?size=20',headers=self.headers)
    @task(3)
    def dashboard(self): self.client.get('/api/dashboard',headers=self.headers)
    @task(1)
    def report(self): self.client.get('/api/reports/export?format=xlsx',headers=self.headers)
