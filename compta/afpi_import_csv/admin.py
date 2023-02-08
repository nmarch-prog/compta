from django.contrib import admin
from .models import TypeFichier, CorrespondanceColonnes, FormatCsv

# Register your models here.

admin.site.register(TypeFichier)
admin.site.register(CorrespondanceColonnes)
admin.site.register(FormatCsv)
