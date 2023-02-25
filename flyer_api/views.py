import coreapi
import coreschema
import django_filters.rest_framework

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from rest_framework import viewsets, mixins, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import action, parser_classes
from rest_framework import parsers, status

from flyer_api.models import Project,Category,PageLayoutTemplate,PageFormat
from flyer_api.serializers import (UserProductSerializer, CreateProjectSerializer, ProjectSendToAgencySerializer, CatalogProductSerializer,
                                   ProjectSerializer, UserSerializer, ProjectTemplateFileSerializer, ProjectPageSerializer,PageFormatSerializer,CategorySerializer,PageLayoutTemplateSerializer)

from products_catalog_connector.catalog import Catalog, Product


class UserViewSet(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    API endpoint that allow current user to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that manages projects.
    A user can view and edit their own projects.

    list:
    List all user projects

    retrieve:
    Retrieve project instance

    create:
    Create a new project instance.

    update:
    Update project instance.

    partial_update:
    Partial update (only some fields) project instance

    project_template_file:
    Upload Excel Project template file

    send_to_agency:
    Send project to agency for print
    """

    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.projects.all()

    # def list(self, request):
    #     pass

    @swagger_auto_schema(request_body=CreateProjectSerializer, responses={201: ProjectSerializer}, parser_classes=(parsers.MultiPartParser,))
    def create(self, request):
        return super().create(request)

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # @swagger_auto_schema(methods=['post'], request_body=no_body)
    @swagger_auto_schema(methods=['post'], request_body=ProjectSendToAgencySerializer)
    @action(detail=True, methods=['post'])
    def send_to_agency(self, request, pk=None):
        pass


class CurrentUserView(APIView):
    """
    API endpoint for current user info

    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer_context = {
            'request': request,
        }
        serializer = UserSerializer(request.user, context=serializer_context)
        return Response(serializer.data)

    def get_serializer(self):
        return UserSerializer()


@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[openapi.Parameter('code', openapi.IN_QUERY, description="Product code to search", type=openapi.TYPE_STRING), openapi.Parameter(
        'description', openapi.IN_QUERY, description="Product description to search", type=openapi.TYPE_STRING)],
    operation_description="API endpoint that allow to search product in catalog by code or by description"
))
class CatalogProductListView(generics.ListAPIView):
    serializer_class = CatalogProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        data_result = []
        code = self.request.query_params.get('code', None)
        description = self.request.query_params.get('description', None)
        if code is not None:
            catalog_product = Catalog.get_product_by_code(
                code=code, seller_code=self.request.user.profile.seller_code)
            if catalog_product is not None:
                data_result.append(catalog_product)
        elif description is not None:
            data_result = Catalog.get_products_by_description(
                description=description, seller_code=self.request.user.profile.seller_code)

        return data_result

class UserProductCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProductListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProductSerializer
    
    def get_queryset(self):
        return self.request.user.products.all()
    
class PageFormatListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PageFormatSerializer
    
    def get_queryset(self):
        return PageFormat.objects.filter(type="flyer")
    
class StopperListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PageFormatSerializer
    
    def get_queryset(self):
        return PageFormat.objects.filter(type="stopper")
    
class PosterListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PageFormatSerializer
    
    def get_queryset(self):
        return  PageFormat.objects.filter(type="poster")

    
class CategoryListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.all()
    
class PageLayoutTemplateListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PageLayoutTemplateSerializer
    
    def get_queryset(self):
        return PageLayoutTemplate.objects.all()
    
class CreateProject(APIView):
    	def post(self, request):
            project = request.data
            number_of_pages=int(project['number_of_pages'][0])
            print(request.data)
            template=PageLayoutTemplate.objects.filter(default=True)[0]
            serializer = CreateProjectSerializer(data=project)
            if serializer.is_valid(raise_exception=True):
                project_saved = serializer.save()
                for i in range(1, number_of_pages+1):
                    page=project_saved.pages.create(number=i,template=template)
                    page.create_cells()
                    page.create_super_cells()
                return Response({"success": "Project '{}' created successfully".format(project_saved.name)})
