from abc import ABC, abstractmethod
from decimal import Decimal
from .models import Product, Category

class IProductDataSource(ABC):
    @abstractmethod
    def get_products(self):
        pass

class DatabaseProductDataSource(IProductDataSource):
    def get_products(self):
        """Devuelve los elementos de la DB"""
        return Product.objects.all()

class MockProduct:
    def __init__(self, id, name, description, stock, price, image, category_id, date_added):
        self.id = id
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.image = image
        self.category_id = category_id
        self.pk = id
        self.date_added = date_added

class HardcodedProductDataSource(IProductDataSource):
    def get_products(self):
        """Retorna una lista de mocks con la estructura de Product para simular otra fuente de datos"""
        mock_products = [
            MockProduct(id=1, name='Hardcoded Gizmo', description='A fantastic gizmo.', 
                        stock=100, price=Decimal('19.99'), image='products/default.jpg', 
                        category_id=1, date_added=None),
            MockProduct(id=2, name='Static Widget', description='Top quality widget.', 
                        stock=50, price=Decimal('25.50'), image='products/default.jpg', 
                        category_id=1, date_added=None) 
        ]
        return mock_products