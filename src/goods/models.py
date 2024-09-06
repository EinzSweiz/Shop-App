from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Name")
    slug = models.SlugField(
        max_length=250, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"name: {self.name} slug: {self.slug}"


class Products(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=250, null=True, blank=True, verbose_name="URL")
    image = models.ImageField(upload_to="goods_images", blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, default=0.00, decimal_places=2)
    discount = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00, verbose_name="Discount in %"
    )
    qunatity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('-discount', )

    def __str__(self) -> str:
        return self.name
    
    def product_id(self):
        return f'{self.id:05}'
    
    def total_price(self):
        return round(self.price - (self.price*self.discount/100), 2)
    
