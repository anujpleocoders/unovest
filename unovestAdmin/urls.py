from django.contrib import admin
from django.urls import path, include
from unovestAdmin import views as unovestAdminViews

urlpatterns = [
    # path('',unovestAdminViews.login, name="login"),
    path('',unovestAdminViews.loginUser),
    path('login-submit',unovestAdminViews.loginSubmit, name='login-submit'),
    path('logout',unovestAdminViews.logoutUser, name='logout'),
    path('dashboard/',unovestAdminViews.index, name="dashboard"),
    path('scheme-data/', unovestAdminViews.schemeData, name="scheme-data"), 
    path('scheme-data-analysis/', unovestAdminViews.schemeDataAnalysis, name="scheme-data-analysis"), 
    path('fetch-schema-data/', unovestAdminViews.fetchSchemeData, name="fetch-schema-data"),
    path('nav-history/', unovestAdminViews.navHistory, name="nav-history"),
    path('fetch-nav-history/', unovestAdminViews.fetchNavHistory, name="fetch-nav-history"),


# customer managment
    path('customer/', unovestAdminViews.customer, name="customer"),
    path('customer-detail/<int:id>', unovestAdminViews.customerDetail, name="customer-detail"),
    path('customer-status', unovestAdminViews.customerStatus, name="customer-status"),
# End customer managment


# Master scheme
    path('master-scheme/', unovestAdminViews.masterScheme, name="master-scheme"),
# End Master scheme

  
#Settings menu urls

    path('settings/', unovestAdminViews.settings, name="settings"),
    path('account-security', unovestAdminViews.accountSecurity, name="account-security"),
    path('settings/api-settings', unovestAdminViews.apiSettingsSchemData, name="api-settings"),
    path('settings/login-attempt', unovestAdminViews.loginAttempt, name="login-attempt"),

#category url in settings
    path('settings/category', unovestAdminViews.categories, name="category"),
    path('settings/category-status', unovestAdminViews.categoryStatus, name="category-status"),
    path('settings/category-edit', unovestAdminViews.categoryEdit, name="category-edit"),
# end of category url in settings


# sub category url in settings
    path('settings/sub-category', unovestAdminViews.subCategories, name="sub-category"),
    path('settings/sub-category-status', unovestAdminViews.subCategoryStatus, name="sub-category-status"),
    path('settings/sub-category-edit', unovestAdminViews.subCategoryEdit, name="sub-category-edit"),
# end sub category url in settings


# sub tax url in settings
    path('settings/tax-category', unovestAdminViews.taxCategory, name="tax-category"),
    path('settings/tax-status', unovestAdminViews.taxStatus, name="tax-status"),
    path('settings/tax-edit', unovestAdminViews.taxEdit, name="tax-edit"),
# end sub tax url in settings


# sub horizon url in settings
    path('settings/time-horizon', unovestAdminViews.timeHorizon, name="time-horizon"),
    path('settings/time-horizon-status', unovestAdminViews.timeHorizonsStatus, name="time-horizon-status"),
    path('settings/time-horizon-edit', unovestAdminViews.timeHorizonsEdit, name="time-horizon-edit"),
# end sub horizon url in settings


# sub risk-profile url in settings
    path('settings/risk-profile', unovestAdminViews.riskProfile, name="risk-profile"),
    path('settings/risk-profile-status', unovestAdminViews.riskProfilesStatus, name="risk-profile-status"),
    path('settings/risk-profile-edit', unovestAdminViews.riskProfilesEdit, name="risk-profile-edit"),
# end sub risk-profile url in settings


# sub asset-type url in settings
    path('settings/asset-type', unovestAdminViews.assetType, name="asset-type"),
    path('settings/asset-type-status', unovestAdminViews.assetTypesStatus, name="asset-type-status"),
    path('settings/asset-type-edit', unovestAdminViews.assetTypesEdit, name="asset-type-edit"),
# end sub asset-type url in settings

#End Settings menu urls

# CHANGE PASSWORD
    path('account-security/change-password', unovestAdminViews.changePassword, name="change-password"),
# END CHANGE PASSWORD

# Allauth login
    # path('', include('allauth.urls')),
# End allauth login

]
