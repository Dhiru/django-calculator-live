from django.contrib import admin
from .models import Calculator, Log


admin.site.register(
    Calculator,
    list_display=["id", "title", "slug"],
    list_display_links=["id", "title"],
    ordering=["title"],
    prepopulated_fields={"slug": ("title",)},
)


admin.site.register(
    Log,
    list_display=["id", "calculator", "created", "body_intro"],
    ordering=["-id"],
)
