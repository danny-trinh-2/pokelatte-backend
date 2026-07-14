from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import routers
from pokemon import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'pokemon/level', views.PokemonAPILevel, 'pokemon-level')
router.register(r'pokemon/evolve', views.PokemonAPIEvolve, 'pokemon-evolve')
router.register(r'pokemon', views.PokemonAPIView, 'pokemon')
router.register(r'user', views.CurrentUserView, 'user')


def health_check(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.HomeView, name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
