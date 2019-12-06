from django.db import models
from django.utils.translation import get_language

class Role (models.Model):
    id   = models.BigAutoField(primary_key = True)
    name = models.TextField(null = True)
    desc = models.TextField(null = True)

    class Meta:
        db_table = "roles"
        managed = True
        

class Permission (models.Model):
    id   = models.BigAutoField(primary_key = True)
    name = models.TextField(null = True)
    name_en = models.TextField(null = True)
    name_ar = models.TextField(null = True)
    desc = models.TextField(null = True)
    

    
    class Meta:
        db_table = "permissions"
        managed = True
        

        
class Admin (models.Model):

    id       = models.BigAutoField(primary_key = True)
    username = models.TextField(null = True)
    fullname = models.TextField(null = True)
    password = models.TextField(null = True)
    email    = models.TextField(null = True)
    role     = models.ForeignKey(Role, on_delete=models.CASCADE, null = True)
    avatar     = models.TextField(default="avatar.png", null = True)
    register_date = models.DateTimeField(auto_now_add = True, null= True)
    permission = models.ManyToManyField(Permission, blank = True, related_name="permissions")
    

    class Meta:
        db_table = "users"
        managed = True
        

  

        
class Category(models.Model):
    id = models.BigAutoField(primary_key = True)
    desc_image = models.TextField(null = True)
     
    class Meta:
        db_table = "categories"

    
    @classmethod
    def related_products(self, id):

        related_products_id_list = Product.objects.prefetch_related("category").filter(category__id=int(id)).values_list("id", flat=True) 
        result =  {
            "results": Product_translation.objects.prefetch_related("product").filter(product__id__in=related_products_id_list, language=get_language()), 
            "images": Product_images.objects.prefetch_related("product").filter(product__id__in=related_products_id_list)
        }
        return result
   


class Category_translation(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.TextField()
    desc = models.TextField()
    Category = models.ForeignKey(Category, on_delete = models.CASCADE)
    language = models.CharField(max_length = 255, default = "en")

    class Meta:
        db_table = "category_translation"



class Product(models.Model):
    id = models.BigAutoField(primary_key = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    buy_price = models.TextField(null = True)
    sell_price = models.TextField(null = True);
    available_quantity = models.TextField(null = True)

        
    class Meta:
        db_table = "products"



class Product_translation(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.TextField()
    desc = models.TextField()
    language = models.CharField(max_length = 255, default = "en")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        db_table = "product_translation"

        
        
class Product_images(models.Model):
    id= models.BigAutoField(primary_key = True)
    image  = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    
    class Meta:
        db_table = "products_images"




class Client(models.Model):
    name = models.TextField()
    phone = models.TextField()
    address = models.TextField()

    class Meta:
        db_table = "clients"


class Order(models.Model):
    id = models.BigAutoField(primary_key = True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through="Order_product")
    delivered = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True,null= True)
    
    class Meta:
        db_table = "orders"
        managed=True
        
class Order_product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    quantity = models.CharField(max_length=253)
    
    class Meta:
        db_table="order_product"
