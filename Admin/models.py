from django.db import models
        
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
    sell_price = models.TextField();
    
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
