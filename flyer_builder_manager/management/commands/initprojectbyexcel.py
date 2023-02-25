import requests
from io import BytesIO
from django.core import files
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from openpyxl import Workbook, load_workbook

from flyer_api.models import Project
from products_catalog_connector.models import Seller, Distribution
from flyer_builder_manager.utils.excel_parsers import parser as excel_parser

class Command(BaseCommand):
    help = 'Generate project PDF'

    def add_arguments(self, parser):
        parser.add_argument('arguments', nargs='+', type=str)

    def handle(self, *args, **options):
        project_id = options['arguments'][0]
        project = Project.objects.get(pk=project_id)

        file_path = project.project_template_file.path
        seller = Seller.objects.get(pk=project.client.seller_code)
        parser_name = project.client.excel_parser_name

        excel_parser.parse(parser_name=parser_name, project=project, seller=seller, excel_file_path=file_path)

        project.initialization_in_progress = False
        project.save()