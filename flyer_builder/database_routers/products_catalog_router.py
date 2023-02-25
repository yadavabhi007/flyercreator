class ProductsCatalogRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'products_catalog_connector':
            return 'products_catalog_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'products_catalog_connector':
            # raise Exception("This model is read only!")
            return 'products_catalog_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if (db == 'products_catalog_db'):
            return False