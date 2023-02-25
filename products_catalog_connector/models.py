import os
from django.db import models
from django.conf import settings


class Flag(models.Model):
    """Flag of a Category"""

    name = models.CharField(
        max_length=200, verbose_name="Nome del flag", db_index=True)
    lastUseTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "flag"


class Seller(models.Model):
    """ A seller"""

    name = models.CharField(max_length=200, db_index=True, verbose_name="Nome")
    vat_number = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="P. IVA")
    email = models.CharField(max_length=100, null=True,
                             blank=True, verbose_name="E-mail")

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "projects_seller"


class Category(models.Model):
    """Category of a Product"""

    name = models.CharField(max_length=200, verbose_name="Nome della categoria", db_index=True)
    flag = models.ManyToManyField(Flag)
    lastUseTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "projects_category"


class Subcategory(models.Model):
    """Subcategory of a Product"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    name = models.CharField(max_length=200, db_index=True,
                            verbose_name="Sottocategoria")

    def get_category_name(self):
        return self.category.name
    get_category_name.short_description = "Categoria"

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "subcategory"  # production
        # db_table = "subcategory" #test


class Picture(models.Model):
    """Single picture of a Product"""

    path = models.CharField(max_length=200, db_index=True)
    lastUseTime = models.DateTimeField(auto_now=True, db_index=True)
    favorite = models.BooleanField(default=True)

    def __str__(self):
        return str(self.path)

    def low_resolution_path(self):
        ''' return the low resolution static image path in the form "static_path/Letter/image.jpg" '''
        img_name = os.path.basename(self.path)
        name, ext = os.path.splitext(img_name)
        # img_to_show = settings.STATIC_LOW_RES_PIC_PATH + \
        #     img_name[0].lower() + "/" + str(name) + settings.JPG_EXT
        img_to_show = img_name[0].lower() + "/" + str(name) + settings.JPG_EXT
        return str(img_to_show)

    def high_resolution_path(self):
        ''' return the high resolution image path in the form "High_res_path/Letter/image.ext" '''
        img_name = self.path.replace(settings.STATIC_PIC_PATH, '')
        img_to_show = settings.HIGH_RES_PICTURES_PATH + img_name
        return str(img_to_show)

    def get_full_name(self):
        '''return the image name and the extension'''
        return os.path.basename(self.path)

    def get_simple_path(self):
        ''' return the path in the form "Letter/Image.ext" '''
        return self.path.replace(settings.STATIC_PIC_PATH, '')
    
    def image_url(self):
        try:
            return settings.CATALOG_IMAGES_URL_PREFIX + self.low_resolution_path()
        except:
            return None

    class Meta:
        managed = False
        db_table = "projects_picture"


class Product(models.Model):
    """A Product"""

    product_id = models.AutoField(primary_key=True, db_index=True)
    creationTime = models.DateTimeField(auto_now_add=True, db_index=True)
    lastModify = models.DateTimeField(auto_now=True, db_index=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, db_index=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, verbose_name="Sotto-categoria", null=True, blank=True, default='')
    producer = models.CharField(
        max_length=50, null=True, blank=True, db_index=True)
    grammageType = models.PositiveIntegerField(null=True, blank=True,)
    grammageValue = models.PositiveIntegerField(null=True, blank=True,)
    picture = models.ManyToManyField(Picture, db_table='projects_product_picture')
    branded_product = models.BooleanField(default=False)  # for PAM product
    welfare = models.BooleanField(
        default=False, verbose_name="benessere")  # benessere PRODUCTION
    baby = models.BooleanField(
        default=False, verbose_name="baby")  # baby PRODUCTION
    packaged = models.BooleanField(
        default=False, verbose_name="confezionato")  # confezionato PRODUCTION
    bulk = models.BooleanField(
        default=False, verbose_name="sfuso")  # sfuso PRODUCTION

    def __str__(self):
        return 'prodotto ' + str(self.product_id)

    def is_for_approval(self):
        return False

    def most_recent_description(self):
        '''
        Return the most recent description
        '''
        descriptions = Description.objects.filter(
            product=self).order_by('-lastUseTime')
        if len(descriptions) > 0:
            return descriptions[0].description
        else:
            return ''

    def get_html_description(self):
        '''
        Return product description in html format
        '''
        descriptions = Description.objects.filter(
            product=self).order_by('descriptionFieldNum')[:4]
        text = ""
        for des in descriptions:
            if des.description != '':
                if des.descriptionFieldNum == 0:
                    text = text + "<b>Campo 1: </b>"
                elif des.descriptionFieldNum == 1:
                    text = text + "<b>Campo 2: </b>"
                elif des.descriptionFieldNum == 2:
                    text = text + "<b>Campo 3: </b>"
                else:
                    text = text + "<b>Campo 4: </b>"
                text = text + des.description + "<br/>"
            else:
                text = text + "<br/>"
        return text

    # def get_description(self):
    #     '''
    #     Return product description
    #     '''
    #     descriptions = Description.objects.filter(
    #         product=self).order_by('descriptionFieldNum')[:4]
    #     text = ""
    #     for des in descriptions:
    #         if des.description != '':
    #             text = text + des.description + "\r"
    #         else:
    #             text = text + " \r"
    #     return text

    def get_description(self):
        '''
        Return product description in text format
        '''
        descriptions = Description.objects.filter(
            product=self).order_by('descriptionFieldNum')[:4]
        text = ""
        for des in descriptions:
            if des.description != '':
                text = text + des.description + " "
            else:
                text = text + " "
        return text
    get_description.short_description = "Descrizione"

    def get_description_brand(self):
        try:
            description = Description.objects.get(
                product=self, descriptionFieldNum=0)
            return description.description
        except Description.DoesNotExist:
            return ""

    def get_description_type(self):
        try:
            description = Description.objects.get(
                product=self, descriptionFieldNum=1)
            return description.description
        except Description.DoesNotExist:
            return ""

    def get_description_tastes(self):
        try:
            description = Description.objects.get(
                product=self, descriptionFieldNum=2)
            return description.description
        except Description.DoesNotExist:
            return ""

    def get_description_weight(self):
        try:
            description = Description.objects.get(
                product=self, descriptionFieldNum=3)
            return description.description
        except Description.DoesNotExist:
            return ""

    def get_category_name(self):
        return self.category.name
    get_category_name.short_description = "Categoria"

    def get_subcategory_name(self):
        return self.subcategory.name
    get_subcategory_name.short_description = "Sottocategoria"

    def pictures(self):
        return "\n".join([p.path for p in self.picture.all()])

    def get_code(self):
        return Distribution.objects.filter(product=self)[0].code

    def image_url(self):
        try:
            return settings.CATALOG_IMAGES_URL_PREFIX + self.picture.filter(favorite=True)[0].low_resolution_path()
        except:
            return None

    def images(self):
        return self.picture.all()

    class Meta:
        managed = False
        db_table = "projects_product"


class Description(models.Model):
    """Description of a Product """
    product = models.ForeignKey(
        Product, db_index=True, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500, db_index=True)
    lastUseTime = models.DateTimeField(auto_now=True, db_index=True)
    descriptionFieldNum = models.PositiveSmallIntegerField(db_index=True)

    def __str__(self):
        return self.description

    class Meta:
        managed = False
        db_table = "projects_description"


class Distribution(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    seller = models.ForeignKey(
        Seller, db_index=True, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50, db_index=True)
    #product_ean = models.OneToOneField(Product_EAN, blank=True, null=True, on_delete=None, verbose_name="Prodotto EAN")

    def __str__(self):
        return self.code

    def get_seller_name(self):
        return self.seller.name
    get_seller_name.short_description = "Cliente"

    class Meta:
        managed = False
        db_table = "projects_distribution"


class Block(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    code = models.CharField(max_length=50, null=True,
                            blank=True, db_index=True)
    name = models.CharField(max_length=100, null=True,
                            blank=True, db_index=True)
    type = models.PositiveSmallIntegerField(db_index=True)
    seller = models.ForeignKey(
        Seller, db_index=True, on_delete=models.DO_NOTHING)
    imgname = models.CharField(max_length=100, null=True, blank=True)
    available = models.BooleanField(default=True, db_index=True)
    last_edit_date = models.DateTimeField(auto_now=True, db_index=True)

    def preview_path(self):
        imgToShow = settings.CATALOG_IMAGES_URL + \
            settings.STATIC_PREVIEW_BLOCK_PATH + \
            str(self.id) + settings.JPG_EXT
        return str(imgToShow)

    # def template_path(self):
    #     template = STATIC_TEMPLATE_BLOCK_PATH + str(self.id) + INDD_EXT
    #     return str(template)

    def __str__(self):
        return str(self.name) + " - codice: " + str(self.code)

    class Meta:
        managed = False
        db_table = "projects_block"


class Layout(models.Model):
    name = models.CharField(max_length=200)
    max_prods_per_page = models.PositiveSmallIntegerField()
    layout_type = models.PositiveSmallIntegerField()  # models.ForeignKey(LayoutType)
    folderPath = models.CharField(max_length=500)
    imgPath = models.CharField(max_length=500)
    stopperFolderPath = models.CharField(max_length=500)
    locandinaFolderPath = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "projects_layout"

class Project(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    is_open = models.BooleanField(default=True, db_index=True)
    creationTime = models.DateTimeField(auto_now_add=True, db_index=True)
    #lastModify = models.DateTimeField(auto_now = True, auto_now_add=True, db_index=True)
    lastModify = models.DateTimeField(auto_now=True, db_index=True)
    sell_in = models.DateField(blank=True, null=True, db_index=True)
    sell_out = models.DateField(blank=True, null=True, db_index=True)
    seller = models.ForeignKey(Seller, db_index=True, on_delete=models.SET_NULL, null=True)
    layout = models.ManyToManyField(Layout, db_table='projects_project_layout')
    default_flyer_block = models.ForeignKey(Block, db_index=True, related_name="flyer_block", on_delete=models.SET_NULL, null=True)
    default_locandina_block = models.ForeignKey(Block, db_index=True, related_name="locandina_block", on_delete=models.SET_NULL, null=True)
    default_stopper_block = models.ForeignKey(Block, db_index=True, related_name="stopper_block", on_delete=models.SET_NULL, null=True)
    project_type = models.PositiveSmallIntegerField()  # models.ForeignKey(LayoutType)
    deleted = models.BooleanField(default=False, db_index=True)
    deleted_date = models.DateField(blank=True, null=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "projects_project"

class FileType(models.Model):
    name = models.CharField(max_length = 30) 
    

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = "dam_filetype"

class FileUploaded(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    id_FileType = models.ForeignKey(FileType, on_delete=models.CASCADE)
    info = models.TextField(null=True, blank=True)
    file = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.info     
    
    def get_mockup_high_resolution_static_path(self):
        image = "https://aebflyer.r1-it.storage.cloud.it/files/"+ str(self.id_project.pk) + "/" + str(self.pk) + "/" + self.file
        return str(image)   
    
    def get_folder_path(self):
        path = FILE_PATH + str(self.id_project.seller.pk) + "/" + str(self.pk) + "/"
        return str(path) 

    class Meta:
        managed = False
        db_table = "dam_fileuploaded"

class PictureItem(models.Model):
    picturePath = models.CharField(max_length=500, db_index=True)
    orderNum = models.PositiveSmallIntegerField(db_index=True)
    # attribute_style = models.ManyToManyField(
    #     AttributeStyle, null=True, db_table='projects_pictureitem_attribute_style')

    def __str__(self):
        return self.picturePath

    def low_resolution_path(self):
        img_name = os.path.basename(self.picturePath)
        name, ext = os.path.splitext(img_name)
        imgToShow = settings.STATIC_LOW_RES_PIC_PATH + \
            img_name[0].lower() + "/" + name + '.jpg'
        return imgToShow

    class Meta:
        managed = False
        db_table = "projects_pictureitem"


class Item(models.Model):
    project = models.ForeignKey(Project, db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, db_index=True, on_delete=models.SET_NULL, null=True)
    changed_from_original = models.BooleanField(default=False)

    category = models.CharField(
        max_length=100, null=True, blank=True, default='')
    field1 = models.CharField(
        max_length=500, null=True, blank=True, default='')
    field2 = models.CharField(
        max_length=500, null=True, blank=True, default='')
    field3 = models.CharField(
        max_length=500, null=True, blank=True, default='')
    field4 = models.CharField(
        max_length=500, null=True, blank=True, default='')

    grammageValue = models.PositiveIntegerField(
        db_index=True, null=True, blank=True)
    price_without_IVA = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    price_with_IVA = models.DecimalField(
        max_digits=10, decimal_places=4, default=0.00)
    price_for_Kg = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)

    pam = models.BooleanField(default=False)
    art_work = models.BooleanField(default=False)
    data = models.CharField(max_length=100, blank=True)
    punti = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=500, blank=True)
    note2 = models.CharField(max_length=100, blank=True)
    note3 = models.CharField(max_length=100, blank=True)

    fidelity_product = models.BooleanField(default=False)
    underpriced_product = models.BooleanField(default=False)
    one_and_one_gratis = models.BooleanField(default=False)
    three_for_two = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    available_pieces = models.PositiveIntegerField(blank=True, null=True)
    max_purchasable_pieces = models.PositiveSmallIntegerField(
        blank=True, null=True)

    # attribute_item = models.ManyToManyField(
    #     AttributeItem, blank=True, null=True, db_table='dam_item_attribute_item')
    # fetch picture_item for interactive flyer
    picture_item = models.ManyToManyField(PictureItem, blank=True, db_table='dam_item_picture_item')
    pictures_available = models.ManyToManyField(PictureItem, blank=True, related_name="available_pictures_item")
    pageNum = models.PositiveSmallIntegerField(db_index=True)
    positionNum = models.PositiveSmallIntegerField(db_index=True)
    onFlyer = models.BooleanField(default=True)
    onStopper = models.BooleanField(default=False)
    onLocandina = models.BooleanField(default=False)
    isFocus = models.BooleanField(default=False)

    flyer_block = models.ForeignKey(
        Block, db_index=True, related_name="my_flyer_block", on_delete=models.SET_NULL, null=True)
    locandina_block = models.ForeignKey(
        Block, db_index=True, related_name="my_locandina_block", on_delete=models.SET_NULL, null=True)
    stopper_block = models.ForeignKey(
        Block, db_index=True, related_name="my_stopper_block", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.project) + ': ' + str(self.product)

    def get_html_description(self):
        '''
        Return product item description in html format
        '''
        text = ""
        text = text + "<b>Campo 1: </b>" + self.field1 + "<br/>"
        text = text + "<b>Campo 2: </b>" + self.field2 + "<br/>"
        text = text + "<b>Campo 3: </b>" + self.field3 + "<br/>"
        text = text + "<b>Campo 4: </b>" + self.field4 + "<br/>"
        return text

    def get_description(self):
        '''
        Return product item description in text format
        '''
        text = ""
        text = text + self.field1 + " " + self.field2 + \
            " " + self.field3 + " " + self.field4
        return text
    get_description.short_description = "Descrizione"

    def get_project_name(self):
        return self.project.name
    get_project_name.short_description = "Progetto"

    class Meta:
        managed = False
        db_table = "item"


class ProjPage(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, db_index=True, on_delete=models.SET_NULL, null=True)
    pageNum = models.PositiveSmallIntegerField(db_index=True)

    def __str__(self):
        return self.project.name + ': ' + self.name + ', Pagina ' + str(self.pageNum)

    class Meta:
        managed = False
        db_table = "projects_projpage"

