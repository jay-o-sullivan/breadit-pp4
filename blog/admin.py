from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin  import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')
    
    def post(self, obj):
        return obj.post.comment  # Replace with the actual field name on the Comment model
        post.short_description = 'Post Title'