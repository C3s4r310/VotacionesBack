from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class VotanteManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio')
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password or dni)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(dni, password, **extra_fields)


class Votante(AbstractBaseUser, PermissionsMixin):
    # Padrón — cargado por el admin
    dni          = models.CharField(max_length=8, unique=True)
    nombres      = models.CharField(max_length=100)
    apellidos    = models.CharField(max_length=100)
    fecha_nac    = models.DateField()
    distrito     = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    correo       = models.EmailField(unique=True)
    foto_dni     = models.ImageField(upload_to='padron/', null=True, blank=True)

    # Se llena cuando el votante llega
    foto_rostro  = models.ImageField(upload_to='rostros/', null=True, blank=True)

    # Estado del votante
    validado     = models.BooleanField(default=False)
    ya_voto      = models.BooleanField(default=False)
    activo       = models.BooleanField(default=True)

    # Django internos
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    #Cuando hay intentos fallidos
    intentos_fallidos = models.IntegerField(default=0)

    USERNAME_FIELD  = 'dni'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'fecha_nac', 'correo']

    objects = VotanteManager()

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - DNI: {self.dni}'

    class Meta:
        verbose_name        = 'Votante'
        verbose_name_plural = 'Votantes'