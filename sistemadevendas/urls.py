from django.contrib.auth import views as auth_views
from django.urls import include, path
from sistemadevendas import views
from users.views import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', views.home, name='home'),
    path('fornecedores/', include('vendedores.urls')),
    path('estoque/', include('estoque.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('users/', include('users.urls'))
]
