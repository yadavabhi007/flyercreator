import os
from io import BytesIO
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

from flyer_api.models import Project

class Command(BaseCommand):
    help = 'Generate project PDF'

    def add_arguments(self, parser):
        parser.add_argument('arguments', nargs='+', type=str)

    def handle(self, *args, **options):
        project_id = options['arguments'][0]
        absolute_uri = options['arguments'][1]
        pdf_type = options['arguments'][2]
        project = Project.objects.get(pk=project_id)
        images = []
        pdf_page_width = 0
        pdf_page_height = 0
        if pdf_type == "page":
            pages = project.pages.all().order_by("number")
            for page in pages:
                page_image_path = page.image.url
                images.append(page_image_path)
                pdf_page_width = int(project.page_format.width)
                pdf_page_height = int(project.page_format.height)
        elif pdf_type == "stopper":
            stoppers = project.stoppers.all()
            for stopper in stoppers:
                image_path = stopper.image.url
                images.append(image_path)
                pdf_page_width = int(project.stopper_format.width)
                pdf_page_height = int(project.stopper_format.height)
        elif pdf_type == "poster":
            posters = project.posters.all()
            for poster in posters:
                image_path = poster.image.url
                images.append(image_path)
                pdf_page_width = int(project.poster_format.width)
                pdf_page_height = int(project.poster_format.height)
        context = {'project': project, 'images': images, 'width':pdf_page_width, "height": pdf_page_height}
        html = render_to_string("flyer_builder_manager/project/pdf.html", context=context)
        # css = CSS(string='@page{ size: A4; margin:0mm}')
        # page_style = '{size: '+str(int(pdf_page_width))+'mm '+str(int(pdf_page_height))+'mm; margin: 0mm; }'
        right = '{margin-left: 0mm;margin-right:0mm;}'
        left = '{margin-left: 0mm;margin-right:0mm;}}'

        page_style = '{size: '+str(int(pdf_page_width))+'mm '+str(int(pdf_page_height))+'mm; margin: 0mm; }'
        # css = CSS(string=f"@page {page_style}; @top-left {right}  @top-right {left}")
        css = CSS(string=f"@page {page_style};")

        print(css.__dict__)
        font_config = FontConfiguration()
        pdf = HTML(string=html, base_url=absolute_uri).write_pdf(font_config=font_config, stylesheets=[css])
        bytes_io = BytesIO(pdf)
        if pdf_type == "stopper":
            project.project_stopper_pdf_file.save(f"{project.name}_stopper.pdf", content=bytes_io)
        elif pdf_type == "poster":
            project.project_poster_pdf_file.save(f"{project.name}_poster.pdf", content=bytes_io)
        else:
            project.project_pdf_file.save(f"{project.name}.pdf", content=bytes_io)
        project.pdf_last_generation = timezone.now()
        project.pdf_generation_in_progress = False
        project.save()
