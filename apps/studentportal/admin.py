from django.contrib import admin
from .models import StudentPortalImage, Studentprtal, Notification

# ✅ Inline لعرض الصور الإضافية
class StudentPortalImageInline(admin.TabularInline):
    model = StudentPortalImage
    extra = 1

# ✅ admin معدل لعرض الصور الإضافية مع Studentprtal
@admin.register(Studentprtal)
class StudentprtalAdmin(admin.ModelAdmin):
    list_display = ['title', 'types', 'created_at']
    inlines = [StudentPortalImageInline]

# ✅ admin معدل للصور لوحدها
@admin.register(StudentPortalImage)
class StudentPortalImageAdmin(admin.ModelAdmin):
    list_display = ['portal', 'image']

# ✅ admin معدل للـ Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'receiver', 'send_to_all', 'created_at']
    list_filter = ['send_to_all', 'created_at']
    search_fields = ['title', 'body', 'receiver__first_name', 'receiver__last_name']
