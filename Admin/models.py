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
        

  
