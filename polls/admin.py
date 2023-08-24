from django.contrib import admin

from .models import Tag, PostFileContent, Post, Follow, Stream

admin.site.register(Tag)
admin.site.register(PostFileContent)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
