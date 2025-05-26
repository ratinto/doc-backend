from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, DocumentViewSet, HelloView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AskQuestionView


router = DefaultRouter()
router.register('documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('', include(router.urls)),
    path('ask-question/', AskQuestionView.as_view(), name='ask-question'),
]