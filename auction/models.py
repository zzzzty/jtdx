from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20,unique=True)
    photo = models.ImageField(upload_to='product/%Y/%m/%d/',blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_sell = models.BooleanField(default=False)
    #start_price = 
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'
        ordering = ('create_time','is_sell',)

class SellProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True)
    belong = models.CharField(max_length=20)
    price = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "prodcut:%s belong:%s"%(self.product.name,self.belong)
    class Meta:
        unique_together = ['product','belong','price']
        verbose_name = '产品价格'
        verbose_name_plural = '产品价格'
        ordering = ('price','create_time',)



