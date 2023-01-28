from django.urls import path, include
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'addexpense', AddExpenseView, basename='addexpense')
router.register(r'additem', CategoryLookupView, basename='additem')

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('voice-expense', VoiceExpenseView.as_view()),
    path('', include(router.urls))
]

urlpatterns += router.urls
