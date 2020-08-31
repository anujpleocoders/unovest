from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json, requests, csv, codecs
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from unovestAdmin.models import ( 
                                schema_data, 
                                category, 
                                sub_category,
                                tax,
                                timeHorizons,
                                riskProfiles,
                                assetTypes,
                                nav_history,
                            )
from admin_honeypot.models import LoginAttempt
from django.urls import reverse
from .forms import ChangePasword
from django.contrib import messages

 

# Create your views here.
def loginUser(request):
    nextUrl = request.GET.get('next')
    return render(request, 'unovestAdmin/login.html', {'nextUrl':nextUrl})
    

# Checking login by username and password
def loginSubmit(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # next url for user to redirect directly after login
        nextUrl = request.POST.get('nextUrl')

        if username and password:
            user = authenticate(username = username, password = password)     
            if user:
                if user.is_staff:
                    login(request, user)

                    if nextUrl == 'None':
                        return redirect(index)
                    else:
                        return redirect(nextUrl)
                else:
                    return render(request, 'unovestAdmin/login.html' ,{'error':"Invalid Login Username or Password"})
            else:
                return render(request, 'unovestAdmin/login.html' ,{'error':"Invalid Login Username or Password"})


@login_required(login_url='/secret/') #redirect when user is not logged in
def logoutUser(request):
    logout(request)
    return redirect(loginUser)


@login_required(login_url='/secret/') #redirect when user is not logged in
def index(request):
    return render(request, 'unovestAdmin/index.html')


# Customer managemment
@login_required(login_url='/secret/') #redirect when user is not logged in
def customer(request):
    print('User=>', User.objects)
    user_lists = User.objects.all()
    context = {
        'user_lists': user_lists
    }
    return render(request, 'unovestAdmin/customer.html', context)


@login_required(login_url='/secret/') #redirect when user is not logged in
def customerDetail(request, id):
    if request.user.is_authenticated:
        if request.user.is_staff:
            userDetails = User.objects.filter(id = id).first()
            context = {
                'users': userDetails
            }
            return render(request, 'unovestAdmin/customer_detail.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def customerStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                user_id = request.POST.get('id',"")
                if status == '1':
                    User.objects.filter(id = user_id).update(
                        is_active = False
                    )
                else:
                    User.objects.filter(id = user_id).update(
                        is_active = True
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')

# End customer managemnet


@login_required(login_url='/secret/') #redirect when user is not logged in
def schemeData(request):
    datas = schema_data.objects.order_by('code').all()
    # get rows value 
    # Show 5 contacts per page.
    
    if request.GET.get('val'):
        rows = request.GET.get('val')
    else:
         rows = 10

    paginator = Paginator(datas, rows) 

    page_number = request.GET.get('page')
    if page_number:
        page_number = page_number
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)


    context = {
        'datas':page_obj,
        'rows':rows,
        'page_number':page_number
    }

    return render(request, 'unovestAdmin/scheme_data.html', context)

def schemeDataAnalysis(request):
    navHistories = nav_history.objects.order_by('code').filter(isis_div_payout = 'INF209K01165').all()
    return render(request, 'unovestAdmin/schem_data_analysis.html',{'navHistories':navHistories})


@login_required(login_url='/secret/') #redirect when user is not logged in
def fetchSchemeData(request):
    url = 'http://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0'
    csvfile = requests.get(url, allow_redirects=True)

    files_data = csvfile.content.decode('utf-8')
    lines = files_data.split("\n")
    i = 0
    print(lines)
    for line in lines:
        dataLists = line.split(",")     

        if line:
            if i > 0:
                # fetching value of ISIN 
                try:
                    isin = dataLists[9].split("INF")
                    if len(isin) > 2:
                        isis_div_payout = 'INF'+isin[1]
                        isis_div_reinvestment = 'INF'+isin[2]
                    elif len(isin)>1:
                        isis_div_payout = 'INF'+isin[1]
                        isis_div_reinvestment = None
                except IndexError:
                    isis_div_payout = None
                    isis_div_reinvestment = None
                


                # Checking for data already exist or not
                exist = schema_data.objects.filter(code = dataLists[1]).first()
                if exist:
                    schema_data.objects.filter(code = dataLists[1]).update(
                        amc = dataLists[0],
                        code = dataLists[1],
                        scheme_name = dataLists[2],
                        scheme_type = dataLists[3],
                        scheme_category = dataLists[4],
                        scheme_nav_name = dataLists[5],
                        scheme_minimum_amount = dataLists[6],
                        launch_date = dataLists[7],
                        closure_date = dataLists[8],
                        isis_div_payout = isis_div_payout,
                        isis_div_reinvestment = isis_div_reinvestment,
                    )
                else:
                    schema_data.objects.create(
                        amc = dataLists[0],
                        code = dataLists[1],
                        scheme_name = dataLists[2],
                        scheme_type = dataLists[3],
                        scheme_category = dataLists[4],
                        scheme_nav_name = dataLists[5],
                        scheme_minimum_amount = dataLists[6],
                        launch_date = dataLists[7],
                        closure_date = dataLists[8],
                        isis_div_payout = isis_div_payout,
                        isis_div_reinvestment = isis_div_reinvestment,
                    )
            i += 1    

    return redirect(schemeData)


@login_required(login_url='/secret/') #redirect when user is not logged in
def navHistory(request):
    # get rows value    
    if request.GET.get('val'):
        rows = request.GET.get('val')
    else:
        rows = 10
    datasCount = nav_history.objects.count()
    datas = nav_history.objects.order_by('code').all()
    paginator = Paginator(datas, rows)

    page_number = request.GET.get('page')
    if page_number:
        page_number = page_number
    else:
        page_number = 1

    try:
        page_obj= paginator.page(page_number)
        page_obj.object_list
    except:
        page_obj = False
        
    print('page_obj=>', page_obj)
    context = {
        'datas':page_obj,
        'datasCount':datasCount,
        'rows':rows,
        'page_number':page_number
    }
    return render(request, 'unovestAdmin/nav_history.html', context)


@login_required(login_url='/secret/') #redirect when user is not logged in
def fetchNavHistory(request):
    
    for year in range(2000, 2020):
        for mf in range(0, 101):
            url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf='+str(mf)+'&tp=1&frmdt=01-jan-2001&todt=31-Dec-2002'
            csvfile = requests.get(url, allow_redirects=True)
            files_data = csvfile.content.decode('utf-8')
            lines = files_data.split("\n")
            d = 0
            for line in lines:
                dataLists = line.split(",")
                for dataList in dataLists:
                    if d > 5:
                        data = dataList.split(";")
                        print('data=>', data)
                        if len(data) > 5:
                            if '<div id="prepage" style="position:absolute' not in data:
                                # Saving data
                                nav_history.objects.create(
                                    code = data[0],
                                    scheme_name = data[1],
                                    isis_div_payout = data[2],
                                    isis_div_reinvestment = data[3],
                                    net_asset_value = data[4],
                                    repurchase_price = data[5],
                                    sale_price = data[6],
                                    date_open_ended = data[7],
                                )
                    d += 1    

    return redirect(navHistory)


# MAster scheme 
@login_required(login_url='/secret/') #redirect when user is not logged in
def masterScheme(request):
    return render(request, 'unovestAdmin/master_scheme.html')

# Settings
@login_required(login_url='/secret/') #redirect when user is not logged in
def accountSecurity(request):
    return render(request, 'unovestAdmin/account_security.html')




@login_required(login_url='/secret/') #redirect when user is not logged in
def settings(request):
    return render(request, 'unovestAdmin/settings.html')


@login_required(login_url='/secret/') #redirect when user is not logged in
def apiSettings(request):
    return render(request, 'unovestAdmin/api_settings.html')


@login_required(login_url='/secret/') #redirect when user is not logged in
def apiSettingsSchemData(request):
    return render(request, 'unovestAdmin/api_settings_schem_data.html')

# categories

@login_required(login_url='/secret/') #redirect when user is not logged in
def categories(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('current_page')
        print(request.POST.get('category'))
        if current_page == 'add':
            category.objects.create(
                name = request.POST.get('category')
            )
            return HttpResponseRedirect('category')

        # update category
        if current_page == 'edit':            
            category_id = request.POST.get('category_id')
            category.objects.filter(id = category_id).update(
                name = request.POST.get('category')
            )
            return HttpResponseRedirect('category')
        
    categories = category.objects.order_by('-id').all()
    context = {
        'categories' : categories
    }   
    return render(request, 'unovestAdmin/category.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def categoryStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                category_id = request.POST.get('id',"")
                print('status',status)
                if status == '1':
                    category.objects.filter(id = category_id).update(
                        is_status = 0
                    )
                else:
                    category.objects.filter(id = category_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')

@login_required(login_url='/secret/') #redirect when user is not logged in
def categoryEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                category_id = request.POST.get('id',"")
                details= category.objects.filter(id = category_id).first()
                categoryDetails = {
                    'id' : details.id,
                    'name': details.name,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"categoryDetails": categoryDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')

# end of categories 

# sub categories
@login_required(login_url='/secret/') #redirect when user is not logged in
def subCategories(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('sub_current_page')
        if current_page == 'add':
            sub_category.objects.create(
                category_id = request.POST.get('category'),
                name = request.POST.get('sub_category')
            )
            return HttpResponseRedirect('sub-category')

        # update category
        if current_page == 'edit':            
            sub_category_id = request.POST.get('sub_category_id')
            sub_category.objects.filter(id = sub_category_id).update(
                category_id = request.POST.get('category'),
                name = request.POST.get('sub_category')
            )
            return HttpResponseRedirect('sub-category')
        
    sub_categories = sub_category.objects.order_by('-id').all()
    categories = category.objects.order_by('-id').all()
    context = {
        'sub_categories' : sub_categories,
        'categories' : categories
    }   
    return render(request, 'unovestAdmin/sub_category.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def subCategoryStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                category_id = request.POST.get('id',"")
                if status == '1':
                    sub_category.objects.filter(id = category_id).update(
                        is_status = 0
                    )
                else:
                    sub_category.objects.filter(id = category_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')

@login_required(login_url='/secret/') #redirect when user is not logged in
def subCategoryEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                sub_category_id = request.POST.get('id',"")
                details= sub_category.objects.filter(id = sub_category_id).first()
                categoryDetails = {
                    'id' : details.id,
                    'category_id': details.category_id,
                    'name': details.name,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"categoryDetails": categoryDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')
    
# end of subcategories

# tax
@login_required(login_url='/secret/') #redirect when user is not logged in
def taxCategory(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('tax_page')
        if current_page == 'add':
            tax.objects.update(
                is_status = '0'
            )
            tax.objects.create(
                tax = request.POST.get('tax_name'),
                percent = request.POST.get('tax_percent')
            )
           

            return HttpResponseRedirect('tax-category')

        # update category
        if current_page == 'edit':            
            tax_id = request.POST.get('tax_id')
            tax.objects.filter(id = tax_id).update(
                tax = request.POST.get('tax_name'),
                percent = request.POST.get('tax_percent')
            )
            return HttpResponseRedirect('tax')
        
    taxes = tax.objects.order_by('-id').all()
    context = {
        'taxes' : taxes
    }   
    return render(request, 'unovestAdmin/tax.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def taxStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                tax_id = request.POST.get('id',"")
                if status == '1':
                    tax.objects.filter(id = tax_id).update(
                        is_status = 0
                    )
                else:
                    tax.objects.update(
                        is_status = 0
                    )
                    tax.objects.filter(id = tax_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')


@login_required(login_url='/secret/') #redirect when user is not logged in
def taxEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                tax_id = request.POST.get('id',"")
                details= tax.objects.filter(id = tax_id).first()
                taxDetails = {
                    'id' : details.id,
                    'percent': details.percent,
                    'tax': details.tax,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"taxDetails": taxDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')
# end of tax


# timeHorizon in settings
@login_required(login_url='/secret/') #redirect when user is not logged in
def timeHorizon(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('time_horizon_page')
        if current_page == 'add':
            timeHorizons.objects.create(
                name = request.POST.get('name'),
                period_year = request.POST.get('period_year'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('time-horizon')

        # update category
        if current_page == 'edit':            
            horizon_id = request.POST.get('horizon_id')
            timeHorizons.objects.filter(id = horizon_id).update(
                name = request.POST.get('name'),
                period_year = request.POST.get('period_year'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('time-horizon')
        
    timeHorizonsDetails = timeHorizons.objects.order_by('-id').all()
    context = {
        'timeHorizons' : timeHorizonsDetails
    }   
    return render(request, 'unovestAdmin/horizon.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def timeHorizonsStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                timeHorizons_id = request.POST.get('id',"")
                if status == '1':
                    timeHorizons.objects.filter(id = timeHorizons_id).update(
                        is_status = 0
                    )
                else:
                    timeHorizons.objects.update(
                        is_status = 0
                    )
                    timeHorizons.objects.filter(id = timeHorizons_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')


@login_required(login_url='/secret/') #redirect when user is not logged in
def timeHorizonsEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                time_horizon_id = request.POST.get('id',"")
                details= timeHorizons.objects.filter(id = time_horizon_id).first()
                timeHorizonsDetails = {
                    'id' : details.id,
                    'name': details.name,
                    'period_year': details.period_year,
                    'description': details.description,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"timeHorizonsDetails": timeHorizonsDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')
# end of timeHorizon in settings


# riskProfile in settings
@login_required(login_url='/secret/') #redirect when user is not logged in
def riskProfile(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('risk_profile_page')
        if current_page == 'add':
            riskProfiles.objects.create(
                name = request.POST.get('risk_profile_name'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('risk-profile')

        # update category
        if current_page == 'edit':            
            risk_profile_id = request.POST.get('risk_profile_id')
            riskProfiles.objects.filter(id = risk_profile_id).update(
                name = request.POST.get('risk_profile_name'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('risk-profile')
        
    riskProfilesDetails = riskProfiles.objects.order_by('-id').all()
    context = {
        'riskProfiles' : riskProfilesDetails
    }   
    return render(request, 'unovestAdmin/risk_profile.html', context)

@login_required(login_url='/secret/') #redirect when user is not logged in
def riskProfilesStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                riskProfiles_id = request.POST.get('id',"")
                if status == '1':
                    riskProfiles.objects.filter(id = riskProfiles_id).update(
                        is_status = 0
                    )
                else:
                    riskProfiles.objects.update(
                        is_status = 0
                    )
                    riskProfiles.objects.filter(id = riskProfiles_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')


@login_required(login_url='/secret/') #redirect when user is not logged in
def riskProfilesEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                time_horizon_id = request.POST.get('id',"")
                details= riskProfiles.objects.filter(id = time_horizon_id).first()
                riskProfilesDetails = {
                    'id' : details.id,
                    'name': details.name,
                    'description': details.description,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"riskProfilesDetails": riskProfilesDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')
# end of riskProfile in settings


# riskProfile in settings
@login_required(login_url='/secret/') #redirect when user is not logged in
def assetType(request):
    if request.method == "POST":
        # add new category
        current_page = request.POST.get('asset_types_page')
        if current_page == 'add':
            assetTypes.objects.create(
                name = request.POST.get('asset_types_name'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('asset-type')

        # update category
        if current_page == 'edit':            
            assest_type_id = request.POST.get('asset_types_id')
            assetTypes.objects.filter(id = assest_type_id).update(
                name = request.POST.get('asset_types_name'),
                description = request.POST.get('description'),
            )
            return HttpResponseRedirect('asset-type')
        
    assetTypesDetails = assetTypes.objects.order_by('-id').all()
    context = {
        'assetTypes' : assetTypesDetails
    }   
    return render(request, 'unovestAdmin/assest_type.html', context)


@login_required(login_url='/secret/') #redirect when user is not logged in
def assetTypesStatus(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                status = request.POST.get('status',"")
                assetTypes_id = request.POST.get('id',"")
                if status == '1':
                    assetTypes.objects.filter(id = assetTypes_id).update(
                        is_status = 0
                    )
                else:
                    assetTypes.objects.update(
                        is_status = 0
                    )
                    assetTypes.objects.filter(id = assetTypes_id).update(
                        is_status = 1
                    )
                return HttpResponse('succes')
            return HttpResponse('error')
        return HttpResponse('error')


@login_required(login_url='/secret/') #redirect when user is not logged in
def assetTypesEdit(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                asset_type_id = request.POST.get('id',"")
                details= assetTypes.objects.filter(id = asset_type_id).first()
                assetTypesDetails = {
                    'id' : details.id,
                    'name': details.name,
                    'description': details.description,
                    'is_status': details.is_status,
                    'created_at': details.created_at
                }
                return JsonResponse({"assetTypesDetails": assetTypesDetails}, status=200)
            return HttpResponse('error')
        return HttpResponse('error')
# end of riskProfile in settings


# end settings


# ACCOUNT AND SECURITY

# Change password
@login_required(login_url='/secret/') #redirect when user is not logged in
def changePassword(request):
    if request.user.is_staff:
        if request.method == 'POST':
            ChangePaswordForm = ChangePasword(request.POST or None)
            print('request.user=>', request.user.username)
            if ChangePaswordForm.is_valid():
                new_pasword = ChangePaswordForm.cleaned_data.get('new_pasword')
                confirm_pasword = ChangePaswordForm.cleaned_data.get('confirm_pasword')
                if new_pasword != confirm_pasword:
                    messages.warning(request, 'Password does not match')
                    return redirect('change-password')
                else:
                    u = User.objects.get(username__exact = request.user.username)
                    u.set_password(new_pasword)
                    u.save()
                
                del request.user.username
                return redirect(loginUser)
            else:
                messages.warning(request, 'Enter correct password')
                return redirect('change-password')
        else:
            ChangePaswordForm = ChangePasword()
    else:
        logout(request) 
        return redirect('secret')   
    
    return render(request,'unovestAdmin/change_password.html', {'ChangePaswordForm':ChangePaswordForm})
# End change password


# login attempt
@login_required(login_url='/secret/') #redirect when user is not logged in
def loginAttempt(request):
    LoginAttempts = LoginAttempt.objects.order_by('-timestamp').all()

    return render(request, 'unovestAdmin/login_attempt.html', {'LoginAttempts':LoginAttempts})
# end login attempt

# END ACCOUNT AND SECURITY