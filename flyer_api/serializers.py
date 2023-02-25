from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, FileUploadParser
from flyer_api.models import UserProductImage, UserProduct, PageExtraIconsTemplate, PageBannerTemplate, PageTitleTemplate, PageLayoutTemplate, Profile, Project, ProjectPage, ProjectProduct, ProjectImage, ProductBlockTemplate,PageFormat,Category
from django.conf import settings


class PageExtraIconsTemplateSerializer(serializers.ModelSerializer):
    template_data = serializers.JSONField(required=False)

    class Meta:
        model = PageExtraIconsTemplate
        fields = ('name', 'template_data', 'image')


class PageBannerTemplateSerializer(serializers.ModelSerializer):
    template_data = serializers.JSONField(required=False)

    class Meta:
        model = PageBannerTemplate
        fields = ('name', 'template_data', 'image')


class PageTitleTemplateSerializer(serializers.ModelSerializer):
    template_data = serializers.JSONField(required=False)

    class Meta:
        model = PageTitleTemplate
        fields = ('name', 'template_data', 'image')


class PageLayoutTemplateSerializer(serializers.ModelSerializer):
    template_data = serializers.JSONField(required=False)

    class Meta:
        model = PageLayoutTemplate
        fields = ('name', 'template_data', 'image')


class ProductBlockTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBlockTemplate
        fields = ('code', 'image')


class ProfileTemplateSerializer(serializers.ModelSerializer):
    product_block_template = ProductBlockTemplateSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('seller_code', 'product_block_template')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileTemplateSerializer(many=False)
    page_layout_template = PageLayoutTemplateSerializer(many=True)
    page_title_template = PageTitleTemplateSerializer(many=True)
    page_banner_template = PageBannerTemplateSerializer(many=True)
    page_extra_icons_template = PageExtraIconsTemplateSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'profile', 'page_layout_template',
                  'page_title_template', 'page_banner_template', 'page_extra_icons_template')


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ('url', 'favorite')


class ProjectProductSerializer(serializers.ModelSerializer):
    additional_data = serializers.JSONField(required=False)
    images = ProjectImageSerializer(many=True)

    class Meta:
        model = ProjectProduct
        fields = ('code', 'other_codes', 'position', 'description_brand', 'description_type', 'description_tastes', 'description_weight', 'price', 'price_without_discount',
                  'discount_percentage', 'pieces_number', 'loyalty', 'focus', 'stopper', 'poster',
                  'note', 'additional_data', 'images')


class ProjectPageSerializer(serializers.ModelSerializer):
    products = ProjectProductSerializer(many=True)

    class Meta:
        model = ProjectPage
        fields = ('name', 'number', 'products')


class ProjectTemplateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_template_file']


class CreateProjectSerializer(serializers.ModelSerializer):
    project_template_file = serializers.FileField(required=False,
                                                  max_length=None, allow_empty_file=False, use_url="project_templates", help_text="Excel project template (File upload with multipart/form-data)")

    class Meta:
        model = Project
        fields = ('name', 'project_template_file', )


class ProjectSerializer(serializers.ModelSerializer):
    frontend_data = serializers.JSONField(
        required=False, help_text="frontend app specific data json object")
    status = serializers.SerializerMethodField(help_text="project status")
    pages = ProjectPageSerializer(many=True, required=False)
    # project_template_file = serializers.FileField(required=False,
    #                                               max_length=None, allow_empty_file=False, use_url="project_templates", help_text="Excel project template (File upload with multipart/form-data)")

    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'frontend_data',
                  'project_template_file', 'project_pdf_file', 'pages', )
        read_only_fields = ('status',)

    def get_status(self, obj):
        return obj.get_status_display()

    def create(self, validated_data):
        # return Project.objects.create(**validated_data)
        # return Project(**validated_data)
        # validated_data['project_template_file']
        # project_template_file = validated_data.pop('project_template_file', None)
        # if password is not None:
        project = Project.objects.create(**validated_data)
        if project.project_template_file:
            project.build_from_template_file()

        # pages_data = validated_data.pop('pages')
        # ProjectPage.objects.create(project=project, **pages_data)

        return project

    # def update(self, validated_data):
    def update(self, instance, validated_data):
        # project = self.get_object()
        project = instance
        pages = validated_data.pop('pages', None)
        if pages is not None:
            project.pages.all().delete()

            for page in pages:
                # project.pages.create(**page)
                products = page.pop('products', None)
                project_page = ProjectPage.objects.create(
                    project=project, **page)
                if products is not None:
                    for product in products:
                        images = product.pop('images', None)
                        project_product = ProjectProduct.objects.create(
                            project_page=project_page, **product)
                        if images is not None:
                            for image in images:
                                ProjectImage.objects.create(
                                    project_product=project_product, **image)

        project.__dict__.update(**validated_data)
        project.save()
        return project


class ProjectSendToAgencySerializer(serializers.ModelSerializer):
    frontend_data = serializers.JSONField(
        required=False, help_text="frontend app specific data json object")
    pages = ProjectPageSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('frontend_data', 'project_pdf_file', 'pages', )


class CatalogImageSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)


class CatalogProductSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    description_brand = serializers.CharField(max_length=200)
    description_type = serializers.CharField(max_length=200)
    description_tastes = serializers.CharField(max_length=200)
    description_weight = serializers.CharField(max_length=200)
    images = serializers.ListField(child=CatalogImageSerializer(
    ), allow_empty=True, min_length=None, max_length=None)


class UserProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductImage
        fields = ('id', 'image_file', )


class UserProductSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=50, required=True)
    description_brand = serializers.CharField(max_length=200, required=True)
    description_type = serializers.CharField(max_length=200, required=True)
    images = UserProductImageSerializer(many=True, required=False)

    class Meta:
        model = UserProduct
        fields = ('code', 'description_brand', 'description_type',
                  'description_tastes', 'description_weight', 'images', )

    def create(self, validated_data):
        # images = self.context['request'].FILES
        images = validated_data.pop('images', None)
        user_product = UserProduct.objects.create(**validated_data)
        if images is not None:
            for image in images:
                UserProductImage.objects.create(user_product=user_product, **image)
        return user_product


class PageFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageFormat
        fields = ('name', 'width','height','type',)
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'image',)
        
class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'page_format','stopper_format','poster_format','category','client',)