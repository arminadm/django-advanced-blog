from django.contrib import admin
from blog.models import Post, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "title",
        "image",
        "status",
        "category",
        "created_date",
        "updated_date",
        "published_date",
    ]
    list_filter = ["status", "category"]
    search_fields = ["author", "title", "category"]
    ordering = ["-created_date"]


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_date", "updated_date"]
    search_fields = ["name"]
    ordering = ["-created_date"]


admin.site.register(Category, CategoryAdmin)
