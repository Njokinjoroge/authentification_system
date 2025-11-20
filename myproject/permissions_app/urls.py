from django.urls import path
from .views import RoleListCreateView, AccessRoleRuleListCreateView

urlpatterns = [
    path('roles/', RoleListCreateView.as_view(), name='roles'),
    path('access-rules/', AccessRoleRuleListCreateView.as_view(), name='access-rules'),
]
