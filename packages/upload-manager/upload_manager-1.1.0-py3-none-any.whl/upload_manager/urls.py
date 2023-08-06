from django.urls import path
from .views import update_upload_status

urlpatterns = [
    path('<int:upload_id>/upload/', update_upload_status, name='status-upload'),
]
