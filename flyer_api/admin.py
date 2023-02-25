import json
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from flyer_api.models import *
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django_reverse_admin import ReverseModelAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class PageLayoutTemplateInline(NestedStackedInline):
    model = PageLayoutTemplate
    can_delete = False
    extra = 0

class ProjectProductStyleInline(admin.StackedInline):
    model=ProjectProductStyle


class ProjectPageStyleInline(admin.StackedInline):
    model=ProjectPageStyle



class ProjectProductStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_color', "description_color", "description_brand_color",'description_type_color','description_type_color','description_weight_color','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectproductstyle/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectproductstyle/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(ProjectProductStyle,ProjectProductStyleAdmin)


class ProjectPageStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'border_color', "border_width", "border_style",'header_per','footer_per','body_per','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagestyle/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagestyle/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(ProjectPageStyle,ProjectPageStyleAdmin)



class PageTitleTemplateInline(admin.StackedInline):
    model = PageTitleTemplate
    can_delete = False
    extra = 0


class PageBannerTemplateInline(admin.StackedInline):
    model = PageBannerTemplate
    can_delete = False
    extra = 0


class PageExtraIconsTemplateInline(admin.StackedInline):
    model = PageExtraIconsTemplate
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if (obj is None) or (not obj.is_staff):
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        return ()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class BlockInfoImageInline(NestedStackedInline):
    model = BlockInfoImage
    extra = 0
    fk_name = 'block_info'


class BlockInfoInline(NestedStackedInline):
    model = BlockInfo
    extra = 0
    fk_name = 'client'
    inlines = [BlockInfoImageInline]


class ClientAdmin(NestedModelAdmin):
    inlines = (PageLayoutTemplateInline, BlockInfoInline)
    list_display = ('id', 'name','seller_code','excel_parser_name','flyer_block_id_ref','only_catalog','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/client/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/client/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


class ProjectPageAdmin(ReverseModelAdmin):
    inline_reverse = ['product_page_style', "product_style"]
    inline_type = 'stacked' 
    list_display = ('id', 'project','template','number','category','name','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpage/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpage/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))



admin.site.register(Client, ClientAdmin)

class PageLayoutTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "client", "code","rows","columns","default","Action")
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/pagelayouttemplate/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/pagelayouttemplate/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(PageLayoutTemplate,PageLayoutTemplateAdmin)

class ProjectStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', "border_color", "border_style","Action")
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectstyle/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectstyle/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(ProjectStyle,ProjectStyleAdmin)

class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "client","Action")
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/bannerimage/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/bannerimage/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(BannerImage,BannerImageAdmin)

admin.site.register(ProjectPage,ProjectPageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'preview_image_tag','Action')
    readonly_fields = ["image_tag"]
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/category/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/category/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

    def image_tag(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        )
        )

    image_tag.short_description = "Current Image"

    def preview_image_tag(self, obj):
        return mark_safe('<img src="{url}" width="auto" height="50" />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        )
        )

    preview_image_tag.short_description = "Image"


admin.site.register(Category, CategoryAdmin)


class ProjectPageInline(admin.TabularInline):
    model = ProjectPage
    fields = ('number', 'category', 'name', 'products_list_link')
    readonly_fields = ["products_list_link"]
    extra = 0

    def products_list_link(self, obj):
        if not (obj.id is None):
            return mark_safe(u'<a href="../../../%s/?project_page__id__exact=%d">Products List</a>' % (
                'projectproduct', obj.id))
        else:
            return "-"

    products_list_link.short_description = "Products"

class ProjectAdmin(ReverseModelAdmin):
    inline_reverse = ['product_style', 'product_page_style']
    inline_type = 'stacked' 
    inlines = (ProjectPageInline,)
    exclude = ('frontend_data',)
    list_display = ('id', 'name', 'client', 'status','Action')
    list_filter = ('client', 'status')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/project/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/project/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

    readonly_fields = ["frontend_data_formatted"]

    def frontend_data_formatted(self, obj):
        data = json.dumps(obj.frontend_data, indent=2)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(data, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br/>"
        return mark_safe(style + response)

    frontend_data_formatted.short_description = "Frontend Data"



admin.site.register(Project, ProjectAdmin)

class PageFormatAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'type', "height", "width","Action")
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/pageformat/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/pageformat/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(PageFormat, PageFormatAdmin)


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 0


class ProjectProductAdmin(ReverseModelAdmin):
    inline_reverse = ['product_style']
    inline_type = 'stacked' 
    list_display = ('id', 'project', 'cell', 'ref_id','code','other_codes','position','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectproduct/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectproduct/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
    inlines = (ProjectImageInline,)

    # def has_module_permission(self, request):
    #     return False


class UserProductImageInline(admin.StackedInline):
    model = UserProductImage
    extra = 0


class UserProductAdmin(admin.ModelAdmin):
    inlines = (UserProductImageInline,)
    list_display = ('id', 'user', 'code', 'description_brand','description_type','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/userproduct/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/userproduct/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

class PageTemplateInline(admin.StackedInline):
    model=PageTemplate
    max_num=3
    extra=3

class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'page_format','Action')
    inlines = (PageTemplateInline,)
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/templatetheme/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/templatetheme/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            ))
        return None

class SpecialImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'type','category','Action')

    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/specialimage/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/specialimage/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            ))
        return None
    
admin.site.register(UserProduct, UserProductAdmin)

admin.site.register(ProjectProduct,ProjectProductAdmin)

class ProductBlockTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'code','image_tag','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/productblocktemplate/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/productblocktemplate/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{url}" width="auto" height="50" />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            ))
        return None

admin.site.register(ProductBlockTemplate,ProductBlockTemplateAdmin)

class ProjectPageCellAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'x_top_left_coord', 'y_top_left_coord','width','height','position','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagecell/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagecell/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(ProjectPageCell,ProjectPageCellAdmin)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','project_page_zoom','client','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/profile/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/profile/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(Profile,ProfileAdmin)

admin.site.register(SpecialImage,SpecialImageAdmin)

class ProjectPageSpecialCellAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'type', 'width','height','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagespecialcell/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectpagespecialcell/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(ProjectPageSpecialCell,ProjectPageSpecialCellAdmin)

class ProjectStopperAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'number', 'stopper_style','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectstopper/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectstopper/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(ProjectStopper,ProjectStopperAdmin)


class ProjectPosterAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'number', 'poster_style','product','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectposter/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/projectposter/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(ProjectPoster,ProjectPosterAdmin)


class TemplateThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'page_format','is_active','Action')
    list_display_links = None
    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/templatetheme/{}/change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/flyer_api/templatetheme/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(TemplateTheme,PageTemplateAdmin)