from django.contrib import admin
from django.urls import path, include
from journal import views as journal_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
    path('accounts/signup/', journal_views.signup, name='signup'),
    path('', include('journal.urls')),  # Dashboard & entries
]
