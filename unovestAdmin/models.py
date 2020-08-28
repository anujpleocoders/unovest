from django.db import models

# Create your models here.

# models for scheme
class schema_data(models.Model):
    amc = models.TextField(max_length=299)
    code = models.IntegerField()
    scheme_name = models.TextField(max_length=299)
    scheme_type = models.TextField(max_length=299)
    scheme_category = models.TextField(max_length=299)
    scheme_nav_name = models.TextField(max_length=299)
    scheme_minimum_amount = models.TextField(max_length=299)
    launch_date = models.TextField(max_length=299)
    closure_date = models.TextField(max_length=299)
    isis_div_payout = models.CharField(max_length=299, null=True)
    isis_div_reinvestment = models.CharField(max_length=299, null=True)

    def __str__(self):
        return str(self.amc)

class nav_history(models.Model):
    code = models.IntegerField()
    scheme_name = models.TextField(max_length=299)
    isis_div_payout = models.CharField(max_length=299, null=True)
    isis_div_reinvestment = models.CharField(max_length=299, null=True)
    net_asset_value = models.TextField(max_length=299)
    repurchase_price = models.TextField(max_length=299)
    sale_price = models.TextField(max_length=299)
    date_open_ended = models.TextField(max_length=299)
  

    def __str__(self):
        return str(self.scheme_name)
# end models for scheme

# # models for settings

# models for category in settings
class category(models.Model):
    name = models.TextField(max_length=299)
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

# models for sub category in settings
class sub_category(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    name = models.TextField(max_length=299)
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)


# models for tax in settings
class tax(models.Model):
    tax = models.TextField(max_length=299)
    percent = models.IntegerField()
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.tax)


# models for Time Horizon in settings
class timeHorizons(models.Model):
    name = models.TextField(max_length=300)
    period_year = models.TextField(max_length=299)
    description = models.TextField(max_length=299)
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)


# models for risk profile in settings
class riskProfiles(models.Model):
    name = models.TextField(max_length=300)
    description = models.TextField(max_length=299)
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)


# models for risk profile in settings
class assetTypes(models.Model):
    name = models.TextField(max_length=300)
    description = models.TextField(max_length=299)
    is_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)


# # end models for settings

