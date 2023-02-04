from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from books import views as BooksView
from reviews import views as ReviewView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'books', BooksView.Books)
router.register(r'reviews', ReviewView.Reviews)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/accounts/', include('accounts.urls')),
    path('api-auth', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)