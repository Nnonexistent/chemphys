from django.contrib import admin

from journal import models as app_models


class OrganizationAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass


class StaffMemberAdmin(admin.ModelAdmin):
    pass


class PositionInOrganizationInline(admin.TabularInline):
    extra = 0
    model = app_models.PositionInOrganization


class AuthorAdmin(admin.ModelAdmin):
    inlines = [PositionInOrganizationInline]


class ArticleSourceInline(admin.TabularInline):
    model = app_models.ArticleSource
    extra = 0


class ArticleResolutionInline(admin.TabularInline):
    model = app_models.ArticleResolution
    extra = 0


class OrderedAuthorsInline(admin.TabularInline):
    model = app_models.OrderedAuthors
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = (OrderedAuthorsInline, ArticleSourceInline, ArticleResolutionInline)


class ReviewFileInline(admin.TabularInline):
    model = app_models.ReviewFile
    extra = 0


class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewFileInline]


class VolumeAdmin(admin.ModelAdmin):
    pass


admin.site.register(app_models.Organization, OrganizationAdmin)
admin.site.register(app_models.Section, SectionAdmin)
admin.site.register(app_models.StaffMember, StaffMemberAdmin)
admin.site.register(app_models.Author, AuthorAdmin)
admin.site.register(app_models.Article, ArticleAdmin)
admin.site.register(app_models.Review, ReviewAdmin)
admin.site.register(app_models.Volume, VolumeAdmin)
