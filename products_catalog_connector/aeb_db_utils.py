from products_catalog_connector.models import *

# from products_catalog_connector.aeb_db_utils import AebDbUtils


class AebDbUtils():
    @staticmethod
    def remove_seller(seller_id):
        seller = Seller.objects.get(pk=seller_id)
        pictures_deleted = 0
        pictures_keeped = 0
        products_deleted = 0
        distributions_deleted = 0
        products = Product.objects.filter(
            product_id__in=Distribution.objects.filter(seller=seller).values('product_id'))
        for product in products:
            print(f"PRODUCT: {product.pk}")
            product_distributions = Distribution.objects.filter(
                product=product, seller=seller)
            for product_distribution in product_distributions:
                print(f"distribution deletion: {product_distribution.pk}")
                product_distribution.delete()
                distributions_deleted += 1
            descriptions = Description.objects.filter(product=product)
            for description in descriptions:
                print(f"description deletion: {description.pk}")
                description.delete()
            pictures = product.picture.all()
            for picture in pictures:
                keep_picture = False
                picture_products = picture.product_set.all()
                for picture_product in picture_products:
                    if keep_picture:
                        break
                    picture_product_distributions = Distribution.objects.filter(
                        product=picture_product)
                    for picture_product_distribution in picture_product_distributions:
                        if picture_product_distribution.seller != seller:
                            keep_picture = True
                            break
                if keep_picture:
                    pictures_keeped += 1
                else:
                    print(f"picture deletion: {picture.pk}")
                    picture.delete()
                    pictures_deleted += 1
                print(
                    f"deleted: {pictures_deleted} - keeped: {pictures_keeped}")
            print(f"product deletion: {product.pk}")
            product.delete()
            products_deleted += 1
        print(
            f"Total pictures deleted: {pictures_deleted} - Total pictures keeped: {pictures_keeped}")
        print(f"Distributions deleted: {distributions_deleted}")
        print(f"Products deleted: {products_deleted}")
        print(f"{seller.name} removed!")
        seller.delete()
        return "ok!"

    @staticmethod
    def change_categories():
        salumi_category = Category.objects.filter(name="salumi")[0]
        salumi_products = Product.objects.filter(category=salumi_category)
        salumi_products_count = salumi_products.count()
        gastronomia_category = Category.objects.filter(name="gastronomia")[0]
        salumi_subcategory = Subcategory.objects.filter(
            name="salumi", category=gastronomia_category)[0]

        for index, salumi_product in enumerate(salumi_products, start=1):
            salumi_product.category = gastronomia_category
            salumi_product.subcategory = salumi_subcategory
            salumi_product.save()
            print(
                f"{index} of {salumi_products_count} - {salumi_product.get_description()} changed!")

        igiene_category = Category.objects.filter(name="igiene")[0]
        igiene_products = Product.objects.filter(category=igiene_category)
        igiene_products_count = igiene_products.count()
        igiene_casa_category = Category.objects.filter(name="igiene casa")[0]

        for index, igiene_product in enumerate(igiene_products, start=1):
            igiene_product.category = igiene_casa_category
            igiene_product.subcategory = None
            igiene_product.save()
            print(
                f"{index} of {igiene_products_count} - {igiene_product.get_description()} changed!")

        return "OK!"

    @staticmethod
    def update_products():
        non_food_category = Category.objects.filter(name="non food")[0]
        no_food_category = Category.objects.filter(name="no food")[0]
        home_subcategory = Subcategory.objects.filter(
            name="home", category=no_food_category)[0]
        professional_category = Category.objects.filter(name="professional")[0]
        horeca_category = Category.objects.filter(name="horeca")[0]
        grocery_subcategory = Subcategory.objects.filter(
            name="grocery", category=horeca_category)[0]
        baby_food_category = Category.objects.filter(name="baby food")[0]
        alimentari_category = Category.objects.filter(name="alimentari")[0]
        dispensa_subcategory = Subcategory.objects.filter(
            name="dispensa", category=alimentari_category)[0]

        non_food_products = Product.objects.filter(category=non_food_category)
        non_food_products_count = non_food_products.count()
        professional_products = Product.objects.filter(
            category=professional_category)
        professional_products_count = professional_products.count()
        baby_food_products = Product.objects.filter(
            category=baby_food_category)
        baby_food_products_count = baby_food_products.count()

        print(f"non_food_products count: {non_food_products.count()}")
        print(f"professional_products count: {professional_products.count()}")
        print(f"baby_food_products count: {baby_food_products.count()}")
        print(f"-----------------------------------------")

        for index, non_food_product in enumerate(non_food_products, start=1):
            non_food_product.category = no_food_category
            non_food_product.subcategory = home_subcategory
            non_food_product.save()
            print(
                f"{index} of {non_food_products_count} - {non_food_product.get_description()} changed!")

        for index, professional_product in enumerate(professional_products, start=1):
            professional_product.category = horeca_category
            professional_product.subcategory = grocery_subcategory
            professional_product.save()
            print(
                f"{index} of {professional_products_count} - {professional_product.get_description()} changed!")

        for index, baby_food_product in enumerate(baby_food_products, start=1):
            baby_food_product.category = alimentari_category
            baby_food_product.subcategory = dispensa_subcategory
            baby_food_product.save()
            print(
                f"{index} of {baby_food_products_count} - {baby_food_product.get_description()} changed!")

        non_food_products = Product.objects.filter(category=non_food_category)
        professional_products = Product.objects.filter(
            category=professional_category)
        baby_food_products = Product.objects.filter(
            category=baby_food_category)
        baby_food_products_count = baby_food_products.count()
        print(f"-----------------------------------------")
        print(f"non_food_products count: {non_food_products.count()}")
        print(f"professional_products count: {professional_products.count()}")
        print(f"baby_food_products count: {baby_food_products.count()}")
