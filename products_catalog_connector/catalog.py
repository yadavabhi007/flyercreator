from django.db.models import Q
from products_catalog_connector.models import Seller, Product, Distribution, Description
from django.conf import settings


class CatalogProduct(object):
    def __init__(self, code, description, images, description_brand="", description_type="", description_tastes="", description_weight=""):
        self.code = code
        self.description = description.strip()
        self.description_brand = description_brand.strip()
        self.description_type = description_type.strip()
        self.description_tastes = description_tastes.strip()
        self.description_weight = description_weight.strip()
        self.images = images


class CatalogProductImage(object):
    def __init__(self, low_resolution_path):
        self.url = settings.CATALOG_IMAGES_URL_PREFIX + low_resolution_path


class Catalog:
    def get_product_by_code(code, seller_code):
        seller = Seller.objects.get(pk=seller_code)
        distribution = Distribution.objects.get(code=code, seller=seller)
        product = distribution.product
        catalog_product = CatalogProduct(code=code,
                                         description=product.get_description(),
                                         description_brand=product.get_description_brand(),
                                         description_type=product.get_description_type(),
                                         description_tastes=product.get_description_tastes(),
                                         description_weight=product.get_description_weight(),
                                         images=[])
        pictures = product.picture.all()
        for picture in pictures:
            catalog_product.images.append(CatalogProductImage(
                low_resolution_path=picture.low_resolution_path()))
        return catalog_product

    def get_products_by_description(description, seller_code):
        products = []
        distributions = Distribution.objects.filter(seller=seller_code, product_id__in=Description.objects.filter(Q(description__icontains=description))
                                                    .filter(descriptionFieldNum__in=[0, 1, 2, 3]).values('product_id'))

        for distribution in distributions[0:100]:
            product = distribution.product
            pictures = product.picture.all()
            images = []
            for picture in pictures:
                images.append(CatalogProductImage(
                    low_resolution_path=picture.low_resolution_path()))
            products.append(CatalogProduct(code=distribution.code,
                                           description=product.get_description(),
                                           description_brand=product.get_description_brand(),
                                           description_type=product.get_description_type(),
                                           description_tastes=product.get_description_tastes(),
                                           description_weight=product.get_description_weight(),
                                           images=images))
        return products
