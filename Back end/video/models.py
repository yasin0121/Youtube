from django.db import models
from PIL import Image
from uuid import uuid4
from django.utils.html import format_html
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

#  category
# __________________________________________________________________________________

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    


# # video
# # __________________________________________________________________________________

def validate_video_file(value):

    valid_mime_types = ['video/mp4', 'video/mpeg', 'video/avi', 'video/webm']
    valid_extensions = ['.mp4', '.mpeg', '.avi', '.webm']
    
    file_mime_type = value.file.content_type
    file_extension = value.name.split('.')[-1].lower()

    if file_mime_type not in valid_mime_types or f".{file_extension}" not in valid_extensions:
        raise ValidationError("Invalid file type. Please upload a valid video file.")

class VIDEO(models.Model):
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.PROTECT, related_name="videos"
    )
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(
    upload_to="media/thumbnails",
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    video_file = models.FileField(upload_to='media/videos')
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    description = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    count_like = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def thumbnail_preview(self):
        
        if self.thumbnail:
            return format_html(
                f"<img src='{self.thumbnail.url}' alt='{self.title}' width='100' height='60' >"
            )
        return "null"
    thumbnail_preview.short_description = "thumbnail_preview"


    def increment_like(self):
        self.count_like += 1
        self.save()

    def decrement_like(self):
        if self.count_like > 0:
            self.count_like -= 1
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # تغییر اندازه تصویر بندانگشتی
        if self.thumbnail:
            img = Image.open(self.thumbnail.path)

            # تنظیم سایز تصویر
            max_size = (720, 404)  # سایز استاندارد (عرض، ارتفاع)
            img.thumbnail(max_size)

            # ذخیره تصویر تغییر اندازه داده‌شده
            img.save(self.thumbnail.path)

# comment
# __________________________________________________________________________________
class Comment(models.Model):
    video = models.ForeignKey(
        VIDEO, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    count_like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add a `related_name` to avoid clashes with reverse accessor
    replay = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name="replies",  # Use a different related_name for the reverse relation
        on_delete=models.SET_NULL,
        verbose_name="پاسخ",
    )

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"comment for : {self.video.title}"

    def increment_like(self):
        self.count_like += 1
        self.save()

    def decrement_like(self):
        if self.count_like > 0:
            self.count_like -= 1
            self.save()

    
class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(VIDEO, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} by {self.user.username}'
