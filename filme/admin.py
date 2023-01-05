from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Filme, Episodio, Usuario


# Só existe que no admin queremos que apareça o campo personalizado
campos = list(UserAdmin.fieldsets)
campos.append(('Histórico', {'fields': ('filmes_vistos',)}))
UserAdmin.fieldsets = tuple(campos)


admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin) # Tanto o usuario que a gente vai crair quanto o useradmin padrao, vai ser
# gerenciado pela classe Usuario
