from django.contrib import admin 
from .models import Actor, Movie, MovieActor, Journal , Director              

# نمایش بهتر Actor در پنل ادمین
class ActorAdmin(admin.ModelAdmin):
    list_display = ('FirstName', 'LastName', 'Gender', 'Birth_date')
    search_fields = ('FirstName', 'LastName')
    list_filter = ('Gender',)

# نمایش بهتر Movie در پنل ادمین
class MovieAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Genre', 'IMDBscore', 'MovieDirector')
    search_fields = ('Title',)
    list_filter = ('Genre', 'MovieDirector')

# نمایش بهتر ارتباط MovieActor
class MovieActorAdmin(admin.ModelAdmin):
    list_display = ('movie', 'actor', 'role')
    search_fields = ('movie__Title', 'actor__FirstName', 'actor__LastName')
    list_filter = ('role',)

# نمایش Journal
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'excerpt')
    list_filter = ('created_at',)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('FirstName', 'LastName', 'Gender', 'Birth_date')  # ستون‌های قابل نمایش
    search_fields = ('FirstName', 'LastName', 'Biography')            # قابلیت جستجو
    list_filter = ('Gender', 'Birth_date')                            # فیلتر بر اساس جنسیت و تاریخ تولد
    ordering = ('LastName',)                                          # مرتب‌سازی پیش‌فرض بر اساس نام 
#@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست نمایش داده می‌شوند
    list_display = ("title", "excerpt", "created_at", "updated_at", "image_preview")

    # قابلیت جستجو روی عنوان و متن
    search_fields = ("title", "excerpt", "content")

    # فیلتر کناری
    list_filter = ("created_at", "updated_at")

    # ترتیب پیش‌فرض
    ordering = ("-created_at",)

    # فیلدهای فقط خواندنی
    readonly_fields = ("created_at", "updated_at", "image_preview")

    # گروه‌بندی فیلدها در فرم جزئیات
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("title", "excerpt", "content")
        }),
        ("تصویر و زمان‌ها", {
            "fields": ("image", "image_preview", "created_at", "updated_at"),
            "classes": ("collapse",)  # بخش جمع‌شونده
        }),
    )

    def image_preview(self, obj):
        """نمایش تصویر کوچک در پنل ادمین"""
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:100px;" />'
        return "—"
    image_preview.allow_tags = True
    image_preview.short_description = "پیش‌نمایش تصویر"
# ثبت در پنل ادمین
admin.site.register(Actor, ActorAdmin) 
admin.site.register(Movie, MovieAdmin) 
admin.site.register(MovieActor, MovieActorAdmin) 
admin.site.register(Journal, JournalAdmin)
admin.site.register(Director, DirectorAdmin)