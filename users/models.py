from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("O email deve ser fornecido")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'ADMIN'
    COLABORADOR = 'COLAB'
    PERFIL_CHOICES = [
        (ADMIN, 'Administrador'),
        (COLABORADOR, 'Colaborador'),
    ]

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    perfil = models.CharField(max_length=6, choices=PERFIL_CHOICES, default=COLABORADOR)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_temporary_password = models.BooleanField(default=True)  

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
