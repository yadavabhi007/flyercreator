import collections
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from flyer_api.utils.project_template_parser import ProjectTemplateParser
from products_catalog_connector.models import Block
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=100)
    seller_code = models.IntegerField(null=True)
    excel_parser_name = models.CharField(max_length=100, null=True, blank=True)
    flyer_block_id_ref = models.IntegerField(null=True, blank=True, verbose_name=_("Riferimento flyer block ID"))
    stopper_block_id_ref = models.IntegerField(null=True, blank=True, verbose_name=_("Riferimento stopper block ID"))
    locandina_block_id_ref = models.IntegerField(null=True, blank=True, verbose_name=_("Riferimento locandina block ID"))
    only_catalog = models.BooleanField(default=False, verbose_name=_("Only products catalog access"))

    def get_blocks(self):
        return Block.objects.filter(seller=self.seller_code, type=0)
        # return Block.objects.filter(seller=13, type=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

class BlockInfo(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey( Client, on_delete=models.CASCADE, related_name='block_infos', null=True, blank=True)
    ref_block_id = models.IntegerField(
        null=True, blank=True, verbose_name=_("Riferimento ID block"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Block Info')
        verbose_name_plural = _('Block Infos')


class BlockInfoImage(models.Model):
    block_info = models.ForeignKey(
        BlockInfo, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='block_info_images', max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = _('Block Info Image')
        verbose_name_plural = _('Block Info Images')


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='category_images', max_length=100, null=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categorys')


class PageLayoutTemplate(models.Model):
    name = models.CharField(_("Name"),max_length=100, null=True, blank=True)
    template_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True)
    image = models.ImageField(
        upload_to='page_layout_template_images', max_length=100, null=True, blank=True)
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, null=True, related_name="page_layout_templates")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True,null=True, related_name="page_layout_templates")
    code = models.CharField(_("Code"),max_length=100, null=True, blank=True)
    rows = models.IntegerField(_("Rows"),null=True, blank=True, default=4)
    columns = models.IntegerField(_("Columns"),null=True, blank=True, default=4)
    default = models.BooleanField(default=False)
    # aspect_ratio = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        verbose_name = _('Page Layout Template')
        verbose_name_plural = _('Page Layout Templates')

class PageTitleTemplate(models.Model):
    name = models.CharField(_("Name"),max_length=100, null=True, blank=True)
    template_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True)
    image = models.ImageField(
        upload_to='page_title_template_images', max_length=100, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="page_title_template")

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        verbose_name = _('Page Title Template')
        verbose_name_plural = _('Page Title Templates')

class PageBannerTemplate(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    template_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True)
    image = models.ImageField(
        upload_to='page_banner_template_images', max_length=100, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="page_banner_template")

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        verbose_name = _('Page Banner Template')
        verbose_name_plural = _('Page Banner Templates')

class PageExtraIconsTemplate(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    template_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True)
    image = models.ImageField(
        upload_to='page_banner_template_images', max_length=100, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="page_extra_icons_template")

    def __str__(self):
        return '{name}'.format(name=self.name)
    
    class Meta:
        verbose_name = _('Page ExtraIcons Template')
        verbose_name_plural = _('Page ExtraIcons Templates')

class ProductBlockTemplate(models.Model):
    code = models.IntegerField()
    image = models.ImageField(
        upload_to='product_block_template_images', max_length=100, null=True)

    def __str__(self):
        return 'Template {code}'.format(code=self.code)
    
    class Meta:
        verbose_name = _('Product Block Template')
        verbose_name_plural = _('Product Block Templates')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, related_name='profile')
    # seller_code = models.IntegerField(null=True)
    project_page_zoom = models.IntegerField(null=True, blank=True, default=100)
    # product_block_template = models.ForeignKey(
    #     ProductBlockTemplate, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def zoom_factor(self):
        return float(self.project_page_zoom / 100)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class ProjectProductStyle(models.Model):
    STYLE_CHOICES = (
            ('normal', 'font-weight: normal;'),
            ('bold', 'font-weight: bold;'),
            ('italic','font-style: italic'),
    )
    
    FONT_STYLE_CHOICES = (
            ('Oswald', 'font: Oswald;'),
            ('Poppins', 'font: Poppins;'),
            ('PT Sans','font: PT Sans'),
            ('Robot','font:Robot'),
            ('State','font:State'),
    )
    price_color = models.CharField(max_length=100, null=True, blank=True)
    description_color = models.CharField(max_length=100, null=True, blank=True)
    description_brand_color = models.CharField(max_length=100, null=True, blank=True)
    description_type_color = models.CharField(max_length=100, null=True, blank=True)
    description_tastes_color = models.CharField(max_length=100, null=True, blank=True)
    description_weight_color = models.CharField(max_length=100, null=True, blank=True)
    price_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    description_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    description_brand_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    description_type_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    description_tastes_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    description_weight_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='normal')
    price_integer_font = models.CharField(max_length=20, choices=FONT_STYLE_CHOICES,default="Oswald")
    price_integer_font_size = models.IntegerField(default=42)
    price_float_font = models.CharField(max_length=20, choices=FONT_STYLE_CHOICES,default="Oswald")
    price_float_font_size = models.IntegerField(default=28)
    description1_font = models.CharField(max_length=20, choices=FONT_STYLE_CHOICES,default="Oswald")
    description1_font_size = models.IntegerField(default=12)
    description2_font = models.CharField(max_length=20, choices=FONT_STYLE_CHOICES,default="Oswald")
    description2_font_size = models.IntegerField(default=12)

    class Meta:
        verbose_name = _('Project Product Style')
        verbose_name_plural = _('Project Product Styles')

class ProjectPageStyle(models.Model):
    BORDER_CHOICES = (
        ('dotted', 'border-style: dotted;'),
        ('dashed', 'border-style: dashed;'),
        ('solid', 'border-style: solid;'),
        ('double', 'border-style: double;')
    )
    border_color = models.CharField(max_length=100, null=True, blank=True)
    border_width = models.IntegerField(default=1)
    border_style = models.CharField(max_length=20, choices=BORDER_CHOICES, default='solid')
    header_per = models.IntegerField(default=10)
    footer_per = models.IntegerField(default=9)
    body_per = models.IntegerField(default=81)
    #Todo below fileds not user need to remmove in future
    header_image = models.ImageField(null=True, blank=True)
    footer_image = models.ImageField(null=True, blank=True)


    class Meta:
        verbose_name = _('Project Page Style')
        verbose_name_plural = _('Project Page Styles')

class PageFormat(models.Model):
    FORMAT_CHOICES = [
        ("flyer", 'flyer'),
        ("stopper", 'stopper'),
        ("poster", 'poster'),
    ]
    name = models.CharField(max_length=30)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    type = models.CharField(choices=FORMAT_CHOICES, default="flyer", max_length=50)


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('Page Format')
        verbose_name_plural = _('Page Formats')

def pdf_path(instance, filename):
    return 'project/{0}/pdf/{1}'.format(instance.pk, filename)

class Project(models.Model):
    STATUS_CHOICES = [
        (0, 'Draft'),
        (1, 'Completed - Sent to agency'),
        (2, 'Completed - Worked by the agency'),
        (3, 'Completed - In print'),
        (4, 'Archived'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    # group = models.ForeignKey(
    #     Group, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    name = models.CharField(max_length=100, null=False,
                            blank=False, help_text="project name")
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=0, help_text="project status")
    project_template_file = models.FileField(
        upload_to='project_templates', max_length=100, null=True, blank=True)
    project_pdf_file = models.FileField(
        upload_to=pdf_path, max_length=100, null=True, blank=True)
    project_stopper_pdf_file = models.FileField(
        upload_to=pdf_path, max_length=100, null=True, blank=True)
    project_poster_pdf_file = models.FileField(
        upload_to=pdf_path, max_length=100, null=True, blank=True)
    pdf_generation_in_progress = models.BooleanField(default=False)
    initialization_in_progress = models.BooleanField(default=False)
    pdf_last_generation = models.DateTimeField(null=True, blank=True)
    frontend_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True, help_text="json object for frontend app specific data")
    excel_import_log = models.TextField(
        null=True, blank=True, verbose_name="Excel Import Log")
    excel_import_failed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    page_aspect_ratio = models.FloatField(null=True, blank=True)
    product_style = models.OneToOneField(ProjectProductStyle, on_delete=models.CASCADE, null=True)
    product_page_style = models.ForeignKey(ProjectPageStyle,  related_name='page_style', on_delete=models.CASCADE, null=True)
    stopper_style = models.ForeignKey(ProjectPageStyle, related_name='stopper_style', on_delete=models.CASCADE, null=True)
    poster_style = models.ForeignKey(ProjectPageStyle, related_name='poster_style', on_delete=models.CASCADE, null=True)
    page_format = models.ForeignKey(
        PageFormat, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    stopper_format = models.ForeignKey(
        PageFormat, on_delete=models.CASCADE, related_name='project_stopper', null=True, blank=True)
    poster_format = models.ForeignKey(
        PageFormat, on_delete=models.CASCADE, related_name='project_poster', null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return 'Project: ' + self.name

    def update_last_modification_time(self):
        self.updated_at = timezone.now()
        self.save()

    def build_from_template_file(self):
        if not self.project_template_file:
            return False
        ProjectTemplateParser.parse(self)

    def status_label(self):
        if self.status == 0:
            return "In corso"
        if self.status == 1:
            return "Inviato ad agenzia"
        if self.status == 2:
            return "In lavorazione dall'agenzia"
        if self.status == 3:
            return "In stampa"
        if self.status == 4:
            return "Archiviato"
        
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

def page_image_path(instance, filename):
    return 'project/{0}/images/page/{1}'.format(instance.project.pk, filename)


class ProjectPage(models.Model):
    PAGE_RENDER_LENGTH = 600
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='pages')
    template = models.ForeignKey(
        PageLayoutTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, null=True, blank=True)

    product_page_style = models.OneToOneField(ProjectPageStyle, on_delete=models.CASCADE, null=True)
    product_style = models.OneToOneField(ProjectProductStyle, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=page_image_path, null=True, blank=True)

    # send_agency_in_progress = models.BooleanField(default=False)
    # link a title template

    def __str__(self):
        # return 'Page {number} - {project_name} - {user_name}'.format(number=self.number, project_name=self.project.name, user_name=self.project.user.username)
        return f"Page {self.number}"

    def create_cells(self):
        cell_width = (800/self.template.columns)
        page_pixel = 800 / self.project.page_format.width
        body_per = self.product_page_style.body_per if self.product_page_style else 81
        body_height = int((body_per * self.project.page_format.height * page_pixel) / 100)
        cell_height = (body_height/self.template.rows)
        for x in range(self.template.columns):
            for y in range(self.template.rows):
                self.cells.create(x_top_left_coord=x,
                                  y_top_left_coord=y, width=cell_width, height=cell_height)
        self.set_cells_position()

    def create_super_cells(self):
            self.special_cell.create(type='header', width=1, height=1)
            self.special_cell.create(type='footer', width=1, height=1)


    def set_cells_position(self):
        cells = self.cells.order_by("y_top_left_coord", "x_top_left_coord")
        for pos, cell in enumerate(cells, start=1):
            cell.position = pos
            cell.save()

    def get_page_render_width(self):
        return self.template.columns * ProjectPageCell.CELL_RENDER_LENGTH
        # if self.project.page_aspect_ratio > 1:
        #     return ProjectPage.PAGE_RENDER_LENGTH * self.project.page_aspect_ratio
        # else:
        #     return ProjectPage.PAGE_RENDER_LENGTH * ( 1 / self.project.page_aspect_ratio )

    def get_page_render_height(self):
        return self.template.rows * ProjectPageCell.CELL_RENDER_LENGTH
        # if self.project.page_aspect_ratio > 1:
        #     return ProjectPage.PAGE_RENDER_LENGTH
        # else:
        #     return ProjectPage.PAGE_RENDER_LENGTH * ( 1 / self.project.page_aspect_ratio ) / self.project.page_aspect_ratio

    def has_next(self):
        if self.project.pages.count() > self.number:
            return True
        return False

    def has_previous(self):
        if self.number == 1:
            return False
        return True

    def border_color(self):
        color=""
        if self.product_page_style:
            color = self.product_page_style.border_color
        if not color and self.project.product_page_style:
            color = self.project.product_page_style.border_color
        if not color:
            color = "#000000"

        return color

    def border_width(self):
        width=""
        if self.product_page_style:
            width = self.product_page_style.border_width
        if not width and self.project.product_page_style:
            width = self.project.product_page_style.border_width
        if not width:
            width = 1

        return width

    def border_style(self):
        style=""
        if self.product_page_style:
            style =  self.product_page_style.border_style
        if not style and self.project.product_page_style:
            style = self.project.product_page_style.border_style
        if not style:
            style = "solid"
        return style

    def header_height(self):
        page_pixel = 800/self.project.page_format.width
        header_per = self.product_page_style.header_per if self.product_page_style else 10
        return int((header_per * self.project.page_format.height*page_pixel) /100)

    def header_per(self):
        return self.product_page_style.header_per if self.product_page_style else 10

    def footer_height(self):
        page_pixel = 800 / self.project.page_format.width
        footer_per = self.product_page_style.footer_per if self.product_page_style else 9
        return int((footer_per * self.project.page_format.height*page_pixel)/100)

    def footer_per(self):
        return self.product_page_style.footer_per if self.product_page_style else 9

    def body_height(self):
        page_pixel = 800 / self.project.page_format.width
        body_per = self.product_page_style.body_per if self.product_page_style else 81
        return int((body_per * self.project.page_format.height*page_pixel)/100)

    def body_per(self):
        return self.product_page_style.body_per if self.product_page_style else 81

    # def header_image(self):
    #     if self.product_page_style:
    #         if self.product_page_style.header_image:
    #             return self.product_page_style.header_image.url
    #     if self.project.product_page_style:
    #         if self.project.product_page_style.header_image:
    #             return self.project.product_page_style.header_image.url
    #     return ""
    #
    # def footer_image(self):
    #     if self.product_page_style:
    #         if self.product_page_style.footer_image:
    #             return self.product_page_style.footer_image.url
    #     if self.project.product_page_style:
    #         if self.project.product_page_style.footer_image:
    #             return self.project.product_page_style.footer_image.url
    #     return ""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'project'], name='unique_number')
        ]
        verbose_name = _('Project Page')
        verbose_name_plural = _('Project Pages')


class ProjectPageCell(models.Model):
    CELL_RENDER_LENGTH = 250
    MAX_CELL_WIDTH = 800
    MAX_CELL_HEIGHT = 2

    page = models.ForeignKey(
        ProjectPage, on_delete=models.CASCADE, related_name='cells')
    x_top_left_coord = models.IntegerField(null=True, blank=True, default=0)
    y_top_left_coord = models.IntegerField(null=True, blank=True, default=0)
    width = models.IntegerField(null=True, blank=True, default=0)
    height = models.IntegerField(null=True, blank=True, default=0)
    position = models.IntegerField(null=True, blank=True)

    def render_width(self):
        return self.width * self.CELL_RENDER_LENGTH

    def render_height(self):
        return self.height * self.CELL_RENDER_LENGTH

    def render_left(self):
        return float((self.x_top_left_coord * 100) / self.page.template.columns)

    def render_top(self):
        return float((self.y_top_left_coord * 100) / self.page.template.rows)

    def page_height(self):
        height = self.page.body_height()
        rows = self.page.template.rows
        self.MAX_CELL_HEIGHT = int((height//rows)*2)

    def has_product(self):
        return self.page.project.products.filter(cell=self).count() > 0

    def product(self):
        return self.page.project.products.filter(cell=self)[0]

    def get_template(self):
        return self.page.template

    def is_on_left_border(self):
        return (self.x_top_left_coord == 0)

    def is_on_right_border(self):
        return ((self.x_top_left_coord + self.width) == self.page.template.columns)

    def is_on_bottom_border(self):
        return ((self.y_top_left_coord + self.height) == self.page.template.rows)

    def is_on_top_border(self):
        return (self.y_top_left_coord == 0)

    def can_merge_left(self):
        if self.is_on_left_border():
            return False
        if self.width < self.MAX_CELL_WIDTH:
            width_available = self.MAX_CELL_WIDTH - self.width
            return self.page.cells.filter(x_top_left_coord=(self.x_top_left_coord - 1),
                                          y_top_left_coord=self.y_top_left_coord,
                                          height=self.height,
                                          width__lte=width_available).exists()
            # if width_available == 1:
            #
            # if width_available == 2:
            #     case_1 = self.page.cells.filter(x_top_left_coord=(self.x_top_left_coord - 1),
            #                                     y_top_left_coord=self.y_top_left_coord,
            #                                     height=self.height,
            #                                     width__lte=width_available).exists()
            #     case_2 = self.page.cells.filter(x_top_left_coord=(self.x_top_left_coord - 2),
            #                                     y_top_left_coord=self.y_top_left_coord,
            #                                     height=self.height,
            #                                     width=2).exists()
            #     return (case_1 or case_2)
        else:
            return False

    def can_merge_right(self):
        if self.is_on_right_border():
            return False
        if self.width < self.MAX_CELL_WIDTH:
            width_available = self.MAX_CELL_WIDTH - self.width
            return self.page.cells.filter(x_top_left_coord=(self.x_top_left_coord + 1),
                                          y_top_left_coord=self.y_top_left_coord,
                                          height=self.height,
                                          width__lte=width_available).exists()
        else:
            return False

    def can_merge_top(self):
        if self.is_on_top_border():
            return False
        self.page_height()
        if self.height < self.MAX_CELL_HEIGHT:
            height_available = self.MAX_CELL_HEIGHT - self.height
            return self.page.cells.filter(x_top_left_coord=self.x_top_left_coord,
                                          y_top_left_coord=(
                                              self.y_top_left_coord - 1),
                                          width=self.width,
                                          height__lte=height_available).exists()
        else:
            return False

    def can_merge_bottom(self):
        if self.is_on_bottom_border():
            return False
        self.page_height()
        if self.height < self.MAX_CELL_HEIGHT:
            height_available = self.MAX_CELL_HEIGHT - self.height
            return self.page.cells.filter(x_top_left_coord=self.x_top_left_coord,
                                          y_top_left_coord=(
                                              self.y_top_left_coord + 1),
                                          width=self.width,
                                          height__lte=height_available).exists()
        else:
            return False

    def can_split_vert_2(self):
        one_cell_width = self.MAX_CELL_WIDTH//self.page.template.columns
        return (self.width == one_cell_width*2)

    def can_split_vert_3(self):
        one_cell_width = self.MAX_CELL_WIDTH // self.page.template.columns
        return (self.width == one_cell_width*3)

    def can_split_horiz_2(self):
        self.page_height()
        return (self.height//2 == self.MAX_CELL_HEIGHT//2)
    class Meta:
        verbose_name = _('Project Page Cell')
        verbose_name_plural = _('Project Page Cells')

class BannerImage(models.Model):
    name = models.CharField(max_length=100)
    client= models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='banner', max_length=100)

    class Meta:
        verbose_name = _('Banner Image')
        verbose_name_plural = _('Banner Images')

IMAGE_TYPE_CHOICES = (
    ("header", "header"),
    ("footer", "footer"),
    ("full_page", "fullpage"),
    ("half_page", "half_page"),
    ("stopper_header", "stopper_header"),
    ("stopper_footer", "stopper_footer"),
    ("poster_header", "poster_header"),
    ("poster_footer", "poster_footer")
)

class SpecialImage(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='client_image', max_length=100)
    type = models.CharField(max_length=50, choices=IMAGE_TYPE_CHOICES, default='header')
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return '{0}-{1}'.format(self.type, self.category)
    
    class Meta:
        verbose_name = _('Special Image')
        verbose_name_plural = _('Special Images')

class ProjectPageSpecialCell(models.Model):
    page = models.ForeignKey(
        ProjectPage, on_delete=models.CASCADE, related_name="special_cell")
    type = models.CharField(max_length=50, choices=IMAGE_TYPE_CHOICES, default='header')
    image = models.ForeignKey(SpecialImage,on_delete=models.CASCADE, null=True)
    width = models.IntegerField(null=True, blank=True, default=0)
    height = models.IntegerField(null=True, blank=True, default=0)
    
    class Meta:
        verbose_name = _('Project Page Special Cell')
        verbose_name_plural = _('Project Page Special Cells')
    

class ProjectProduct(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='products')
    cell = models.ForeignKey(
        ProjectPageCell, on_delete=models.SET_NULL, null=True, blank=True)
    ref_id = models.IntegerField(
        null=True, blank=True, verbose_name="Riferimento ID prodotto")
    code = models.CharField(max_length=50, null=True,
                            blank=False, verbose_name="Codice")
    other_codes = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Altri codici")
    position = models.IntegerField(
        default=0, verbose_name="Posizione")
    description = models.CharField(
        max_length=200, null=True, blank=False, verbose_name="Descrizione")
    description_brand = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 1 del prodotto")
    description_type = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 2 del prodotto")
    description_tastes = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 3 del prodotto")
    description_weight = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 4 del prodotto")

    ref_block_id = models.IntegerField(
        null=True, blank=True, verbose_name="Riferimento ID block")

    # inserire codici ean multipli
    price = models.FloatField(null=True, blank=False,
                              verbose_name="Prezzo", default=0)
    price_without_discount = models.FloatField(
        null=True, blank=True, verbose_name="Prezzo senza sconto")
    tag_code = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Codice cartellino")
    discount_percentage = models.FloatField(
        null=True, blank=True, verbose_name="Percentuale sconto")
    pieces_number = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Numero di pezzi")
    max_purchasable_pieces = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    loyalty = models.BooleanField(default=False, verbose_name="Fedeltà")
    focus = models.BooleanField(default=False, verbose_name="Focus")
    stopper = models.BooleanField(default=False, verbose_name="Stopper")
    poster = models.BooleanField(default=False, verbose_name="Locandina")
    note = models.TextField(null=True, blank=True, verbose_name="Note")
    additional_data = JSONField(
        load_kwargs={'object_pairs_hook': collections.OrderedDict}, default={}, blank=True)
    product_style = models.OneToOneField(ProjectProductStyle, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{code} - {description}'.format(code=self.code, description=self.description)

    def image_url(self):
        try:
            return self.images.all()[0].url
        except:
            return ""

    def flyer_block_name(self):
        if self.ref_block_id is not None:
            return Block.objects.get(pk=self.ref_block_id).code
        return "Nessuno"

    def block_icons(self):
        icons = []
        if self.ref_block_id is not None:
            blocks = self.project.client.block_infos.filter(
                ref_block_id=self.ref_block_id)
            for block in blocks:
                for block_image in block.images.all():
                    icons.append(block_image.image.url)
        return icons

    def price_int(self):
        return int(self.price)

    def price_fraction(self):
        return int(round(self.price - int(self.price),2)*100)

    def price_color(self):
        color=""
        if self.product_style:
            color =  self.product_style.price_color
        if not color and self.cell.page.product_style:
            color = self.cell.page.product_style.price_color
        if not color and self.cell.page.project.product_style:
            color = self.cell.page.project.product_style.price_color
        if not color:
            color = "#000000"

        return color

    def description_brand_color(self):
        color = ""
        if self.product_style:
            color =  self.product_style.description_brand_color
        if not color and self.cell.page.product_style:
            color = self.cell.page.product_style.description_brand_color
        if not color and self.cell.page.project.product_style:
            color = self.cell.page.project.product_style.description_brand_color
        if not color:
            color = "#000000"
        return color

    def description_type_color(self):
        color = ""
        if self.product_style:
            color =  self.product_style.description_type_color
        if not color and self.cell.page.product_style:
            color = self.cell.page.product_style.description_type_color
        if not color and self.cell.page.project.product_style:
            color = self.cell.page.project.product_style.description_type_color
        if not color:
            color = "#000000"
        return color

    def description_tastes_color(self):
        color = ""
        if self.product_style:
            color =  self.product_style.description_tastes_color
        if not color and self.cell.page.product_style:
            color = self.cell.page.product_style.description_tastes_color
        if not color and self.cell.page.project.product_style:
            color = self.cell.page.project.product_style.description_tastes_color
        if not color:
            color = "#000000"
        return color

    def description_weight_color(self):
        color = ""
        if self.product_style:
            color = self.product_style.description_weight_color
        if not color and self.cell.page.product_style:
            color = self.cell.page.product_style.description_weight_color
        if not color and self.cell.page.project.product_style:
            color = self.cell.page.project.product_style.description_weight_color
        if not color:
            color = "#000000"
        return color

    def price_style(self):
        style=""
        if self.product_style:
            style =  self.product_style.price_style
        if not style and self.cell.page.product_style:
            style = self.cell.page.product_style.price_style
        if not style and self.cell.page.project.product_style:
            style = self.cell.page.project.product_style.price_style
        if not style:
            style = "normal"

        return style

    def description_brand_style(self):
        style = ""
        if self.product_style:
            style =  self.product_style.description_brand_style
        if not style and self.cell.page.product_style:
            style = self.cell.page.product_style.description_brand_style
        if not style and self.cell.page.project.product_style:
            style = self.cell.page.project.product_style.description_brand_style
        if not style:
            style = "normal"
        return style

    def description_type_style(self):
        style = ""
        if self.product_style:
            style =  self.product_style.description_type_style
        if not style and self.cell.page.product_style:
            style = self.cell.page.product_style.description_type_style
        if not style and self.cell.page.project.product_style:
            style = self.cell.page.project.product_style.description_type_style
        if not style:
            style = "normal"
        return style

    def description_tastes_style(self):
        style = ""
        if self.product_style:
            style =  self.product_style.description_tastes_style
        if not style and self.cell.page.product_style:
            style = self.cell.page.product_style.description_tastes_style
        if not style and self.cell.page.project.product_style:
            style = self.cell.page.project.product_style.description_tastes_style
        if not style:
            style = "normal"
        return style

    def description_weight_style(self):
        style = ""
        if self.product_style:
            style = self.product_style.description_weight_style
        if not style and self.cell.page.product_style:
            style = self.cell.page.product_style.description_weight_style
        if not style and self.cell.page.project.product_style:
            style = self.cell.page.project.product_style.description_weight_style
        if not style:
            style = "normal"
        return style
    
    def price_integer_font(self):
        font=""
        if self.product_style:
            font =  self.product_style.price_integer_font
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.price_integer_font
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.price_integer_font
        if not font:
            font = "Oswald"
            
        return font

    def price_float_font(self):
        font = ""
        if self.product_style:
            font = self.product_style.price_float_font
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.price_float_font
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.price_float_font
        if not font:
            font = "Oswald"

        return font
    
    def description1_font(self):
        font=""
        if self.product_style:
            font =  self.product_style.description1_font
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.description1_font
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.description1_font
        if not font:
            font = "Oswald"
            
        return font
    
    def description2_font(self):
        font=""
        if self.product_style:
            font =  self.product_style.description2_font
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.description2_font
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.description2_font
        if not font:
            font = "Oswald"
            
        return font

    def price_integer_font_size(self):
        font = ""
        if self.product_style:
            font = self.product_style.price_integer_font_size
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.price_integer_font_size
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.price_integer_font_size
        if not font:
            font = 42

        return font

    def price_float_font_size(self):
        font = ""
        if self.product_style:
            font = self.product_style.price_float_font_size
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.price_float_font_size
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.price_float_font_size
        if not font:
            font = 28

        return font

    def description1_font_size(self):
        font = ""
        if self.product_style:
            font = self.product_style.description1_font_size
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.description1_font_size
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.description1_font_size
        if not font:
            font = 12

        return font

    def description2_font_size(self):
        font = ""
        if self.product_style:
            font = self.product_style.description2_font_size
        if not font and self.cell.page.product_style:
            font = self.cell.page.product_style.description2_font_size
        if not font and self.cell.page.project.product_style:
            font = self.cell.page.project.product_style.description2_font_size
        if not font:
            font = 12

        return font
    
    class Meta:
        verbose_name = _('Project Product')
        verbose_name_plural = _('Project Products')   

class ProjectImage(models.Model):
    APPROVAL_CHOICES = [
        (0, 'None'),
        (1, 'Subject to approval'),
        (2, 'Approved'),
        (3, 'Rejected'),
    ]

    code = models.IntegerField(null=True, blank=True)
    project_product = models.ForeignKey(
        ProjectProduct, on_delete=models.CASCADE, related_name='images')
    to_be_approved = models.BooleanField(null=True, blank=True)
    favorite = models.BooleanField(default=False)
    url = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        upload_to='product_images', max_length=100, null=True, blank=True)
    approval_status = models.IntegerField(choices=APPROVAL_CHOICES, default=0)

    def __str__(self):
        return '{url}'.format(url=self.url)

    class Meta:
        verbose_name = _('Project Image')
        verbose_name_plural = _('Project Images')  

class UserProduct(models.Model):
    STATUS_CHOICES = [
        (0, 'In approval'),
        (1, 'Approved'),
        (2, 'Rejected')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    code = models.CharField(max_length=50, null=True,
                            blank=False, verbose_name="Codice")
    description_brand = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 1 del prodotto")
    description_type = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 2 del prodotto")
    description_tastes = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 3 del prodotto")
    description_weight = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Descrizione 4 del prodotto")
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=0, help_text="approval status")

    def get_description(self):
        return " ".join(filter(None, [self.description_brand, self.description_type, self.description_tastes, self.description_weight]))

    def __str__(self):
        return self.get_description()

    class Meta:
        verbose_name = _('User Product')
        verbose_name_plural = _('User Products')

class UserProductImage(models.Model):
    user_product = models.ForeignKey(
        UserProduct, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(
        upload_to='user_product_images', max_length=100)

    def __str__(self):
        return self.image_file.url

    class Meta:
        verbose_name = _('User Product Image')
        verbose_name_plural = _('User Product Images')

class ProjectStyle(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    border_color=models.CharField(max_length=100)
    border_style=models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Project Style')
        verbose_name_plural = _('Project Styles')

def stopper_image_path(instance, filename):
    return 'project/{0}/images/stopper/{1}'.format(instance.project.pk, filename)

class ProjectStopper(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='stoppers')
    number = models.IntegerField(validators=[MinValueValidator(0)])
    stopper_style = models.OneToOneField(ProjectPageStyle, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=stopper_image_path, null=True, blank=True)
    product = models.ForeignKey(ProjectProduct, on_delete=models.CASCADE)
    header_image = models.ForeignKey(SpecialImage, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='stopper_header')
    footer_image = models.ForeignKey(SpecialImage, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='stopper_footer')
    image_top=models.CharField(max_length=20,null=True, blank=True)
    image_left=models.CharField(max_length=20,null=True, blank=True)
    info_top=models.CharField(max_length=20,null=True, blank=True)
    info_left=models.CharField(max_length=20,null=True, blank=True)
    def __str__(self):
        return f"stopper {self.number}"

    def header_height(self):
        page_pixel = 800 / self.project.stopper_format.width
        if not self.project.stopper_style:
            style = ProjectPageStyle.objects.create()
            self.project.stopper_style = style
            self.project.save()
        header_per = self.project.stopper_style.header_per if self.project.stopper_style else 10
        return int((header_per * self.project.stopper_format.height * page_pixel) / 100)

    def header_per(self):
        return self.project.stopper_style.header_per if self.project.stopper_style else 10

    def footer_height(self):
        page_pixel = 800 / self.project.stopper_format.width
        if not self.project.stopper_style:
            style = ProjectPageStyle.objects.create()
            self.project.stopper_style = style
            self.project.save()
        footer_per = self.project.stopper_style.footer_per if self.project.stopper_style else 9
        return int((footer_per * self.project.stopper_format.height * page_pixel) / 100)

    def footer_per(self):
        return self.project.stopper_style.footer_per if self.project.stopper_style else 9

    def body_height(self):
        page_pixel = 800 / self.project.stopper_format.width
        if not self.project.stopper_style:
            style = ProjectPageStyle.objects.create()
            self.project.stopper_style = style
            self.project.save()
        body_per = self.project.stopper_style.body_per if self.project.stopper_style else 81
        return int((body_per * self.project.stopper_format.height * page_pixel) / 100)

    def body_per(self):
        return self.project.stopper_style.body_per if self.project.stopper_style else 81

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['number', 'project'], name='unique_stopper_number')
    #     ]

    class Meta:
        verbose_name = _('Project Stopper')
        verbose_name_plural = _('Project Stoppers')

def poster_image_path(instance, filename):
    return 'project/{0}/images/poster/{1}'.format(instance.project.pk, filename)


class ProjectPoster(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='posters')
    number = models.IntegerField(validators=[MinValueValidator(0)])
    poster_style = models.OneToOneField(ProjectPageStyle, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=poster_image_path, null=True, blank=True)
    product = models.ForeignKey(ProjectProduct, on_delete=models.CASCADE)
    header_image = models.ForeignKey(SpecialImage, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='poster_header')
    footer_image = models.ForeignKey(SpecialImage, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='poster_footer')
    image_top=models.CharField(max_length=20,null=True, blank=True)
    image_left=models.CharField(max_length=20,null=True, blank=True)
    info_top=models.CharField(max_length=20,null=True, blank=True)
    info_left=models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return f"stopper {self.number}"

    def header_height(self):
        page_pixel = 800 / self.project.poster_format.width
        if not self.project.poster_style:
            style = ProjectPageStyle.objects.create()
            self.project.poster_style = style
            self.project.save()
        header_per = self.project.poster_style.header_per if self.project.poster_style.header_per else 10
        return int((header_per * self.project.poster_format.height * page_pixel) / 100)

    def header_per(self):
        return self.project.poster_style.header_per if self.project.poster_style else 10

    def footer_height(self):
        page_pixel = 800 / self.project.poster_format.width
        if not self.project.poster_style:
            style = ProjectPageStyle.objects.create()
            self.project.stopper_style = style
            self.project.save()
        footer_per = self.project.poster_style.footer_per if self.project.poster_style else 9
        return int((footer_per * self.project.poster_format.height * page_pixel) / 100)

    def footer_per(self):
        return self.project.poster_style.footer_per if self.project.poster_style else 9

    def body_height(self):
        page_pixel = 800 / self.project.poster_format.width
        if not self.project.poster_style:
            style = ProjectPageStyle.objects.create()
            self.project.stopper_style = style
            self.project.save()
        body_per = self.project.poster_style.body_per if self.project.poster_style else 81
        return int((body_per * self.project.poster_format.height * page_pixel) / 100)

    def body_per(self):
        return self.project.poster_style.body_per if self.project.poster_style else 81

    class Meta:
        verbose_name = _('Project Poster')
        verbose_name_plural = _('Project Posters')

PAGE_TYPE_CHOICES = [
        ('first_page', 'first_page'),
        ('inner_page', 'inner_page'),
        ('last_page', 'last_page')
    ]

class PageTemplate(models.Model):
    page_type=models.CharField(max_length=100,choices=PAGE_TYPE_CHOICES)
    header_per = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    footer_per = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    full_image = models.BooleanField(default=False)
    half_image = models.BooleanField(default=False)
    template_theme=models.ForeignKey(
        'TemplateTheme', on_delete=models.CASCADE, null=True, blank=True, related_name='templates')
    header_image = models.ForeignKey(SpecialImage,on_delete=models.DO_NOTHING,related_name="template_header",null=True,blank=True,)
    footer_image = models.ForeignKey(SpecialImage, on_delete=models.DO_NOTHING,related_name="template_footer",null=True,blank=True,)
    
    class Meta:
        verbose_name = _('Page Template')
        verbose_name_plural = _('Page Templates')

class TemplateTheme(models.Model):
    name=models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    is_active=models.BooleanField(default=True)
    page_format = models.ForeignKey(
        PageFormat, on_delete=models.CASCADE, null=True, blank=True)
    # row = models.IntegerField(null=True, blank=True, default=4)
    # columns = models.IntegerField(null=True, blank=True, default=4)

    class Meta:
        verbose_name = _('Template Theme')
        verbose_name_plural = _('Template Themes')

