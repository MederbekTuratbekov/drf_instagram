from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import UserProfile, Follow, Post, PostLike, Comment, CommentLike, Story, Save, SaveItem


admin.site.register(Follow)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Story)
admin.site.register(Save)
admin.site.register(SaveItem)


class TranslateAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile, TranslateAdmin)
admin.site.register(Post, TranslateAdmin)
admin.site.register(Comment, TranslateAdmin)
