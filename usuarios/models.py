from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class VotanteManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio')
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(dni, password, **extra_fields)


class Votante(AbstractBaseUser, PermissionsMixin):
    # Datos personales (del DNI)
    dni           = models.CharField(max_length=8, unique=True)
    nombres       = models.CharField(max_length=100)
    apellidos     = models.CharField(max_length=100)
    fecha_nac     = models.DateField()
    distrito      = models.CharField(max_length=100)
    departamento  = models.CharField(max_length=100)
    codigo_val2   = models.CharField(max_length=20)  # código de validación 2 del DNI

    # Imágenes
    foto_dni      = models.ImageField(upload_to='dni/', null=True, blank=True)
    foto_rostro   = models.ImageField(upload_to='rostros/', null=True, blank=True)

    # Estado
    validado      = models.BooleanField(default=False)  # pasó validación facial
    ya_voto       = models.BooleanField(default=False)
    activo        = models.BooleanField(default=True)   # admin puede desactivar

    # Django internos
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'fecha_nac']

    objects = VotanteManager()

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - DNI: {self.dni}'

    class Meta:
        verbose_name = 'Votante'
        verbose_name_plural = 'Votantes'