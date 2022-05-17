from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from api.views import ProfileViewSet, HobbyViewSet, JobViewSet, SpecificJobViewSet

router = DefaultRouter()
router.register('profile', ProfileViewSet)
router.register('hobby', HobbyViewSet)
router.register('job', JobViewSet)
router.register('teacher', SpecificJobViewSet, basename='teacher')



urlpatterns = [
    path('', include(router.urls)),
    path('__debug__/', include('debug_toolbar.urls')),
    path('home/', views.home, name='home'),
]
