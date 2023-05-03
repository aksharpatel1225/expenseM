from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import RegisterForm
from expense.models import Expense,Payee
from django.views.generic.edit import CreateView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from user.models import *


#register Function
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', context={'form': form})

#login Function
def login_view(request):
    print(request.method)
    print(request.user.is_authenticated)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('/user/dashboard')
        else:
            return render(request, 'user/login.html', {'form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form})
#logout
def logout_request(request):
    logout(request)
    return redirect("login")

  #profile page
def profile(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(payee__user=request.user).all()
        try:
            user_income = sum(list(expenses.filter(transactionType="income").values_list('amount', flat=True)))
        except: 
            user_income = 0
            
        try:
            user_expenses = sum(list(expenses.filter( transactionType="expense").values_list('amount', flat=True)))
        except:
            user_expenses = 0
            
        try:
            safe_amount = user_income - (user_income * 10 / 100)
        except: 
            safe_amount = 0
        #print("*"*80)
        #print("user_income", user_income)
        #print("user_expenses", user_expenses)
        return render(request, 'user/profile.html', {"expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": safe_amount - user_expenses})
    else:
        
    #  return redirect('login')
        return render(request, 'user/profile.html',{})
# class profile(CreateView):
#     fields = '__all__'
#     model = Expense
#     template_name = 'profile.html'
#     success_url = '/profile'
     
    #dashboard calling  After login 
def dashboard(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(payee__user=request.user).all()
        # Expense =Expense.objects.all()
        try:
            user_income = sum(list(expenses.filter(transactionType="income").values_list('amount', flat=True)))
        except: 
            user_income = 0
            
        try:
            user_expenses = sum(list(expenses.filter( transactionType="expense").values_list('amount', flat=True)))
        except:
            user_expenses = 0
            
        try:
            safe_amount = user_income - (user_income * 10 / 100)
            safe_amount = int(safe_amount)
        except: 
            safe_amount = 0
        #print("*"*80)
        #print("user_income", user_income)
        #print("user_expenses", user_expenses)
        return render(request, 'user/dashboard.html', {"expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": safe_amount - user_expenses})
    else:
        return redirect('dashboard')

    #Expense Addition

# class add_expense(CreateView):
#     fields = ['amount','expDateTime','category','subCategory','paymentMethod','status','description','transactionType',]
#     model = Expense
#     template_name = 'add.html'
#     success_url = '/success'
#     def form_valid(self,form):
#         payee, created = Payee.objects.get_or_create(user=self.request.user, defaults={'name': self.request.user.username})

#         form.instance.payee = payee
#         form.instance.save()
#         subject = ' Alert Expense/Income Added'
#         message = 'Expense/Income Has Been Added in Expenser Manager.'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = self.request.User_user.email
#         send_mail(subject,message,email_from,recipient_list)
#         return super().form_invalid(form)
  
#     #added Expense Page And Email
from django.contrib.auth.mixins import LoginRequiredMixin

class add_expense(LoginRequiredMixin, CreateView):
    fields = ['amount', 'expDateTime', 'category', 'subCategory', 'paymentMethod', 'status', 'description', 'transactionType']
    model = Expense
    template_name = 'user/add.html'
    success_url = '/user/success/'

    def form_valid(self, form):
        # create a Payee object for the logged-in user if it doesn't exist
        payee, created = Payee.objects.get_or_create(user=self.request.user, defaults={'name': self.request.user.username})

        # set the payee field of the Expense object to the Payee instance
        form.instance.payee = payee
        form.instance.save()

        # subject = 'Alert Expense/Income Added'
        # message = 'We are pleased to inform you that your recent income/expense has been added successfully to your Expense Manager App. Your updated records are now available for you to access and review at any time.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [self.request.user.email]
        # send_mail(subject, message, email_from, recipient_list)
        
        return super().form_valid(form)

#sucess page and mail to user
def success(request):
    subject = ' Alert Expense/Income Added'
    message = 'We are pleased to inform you that your recent income/expense has been added successfully to your Expense Manager App. Your records are now available for you to access and review at any time.With our Expense Manager App, you can easily keep track of your income and expenses, set budgets, and monitor your spending habits. By doing so, you can better manage your finances, avoid overspending, and achieve your financial goals.'
    email_from = settings.EMAIL_HOST_USER
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['aksharpatel1225@gmail.com',]
    
    send_mail(subject,message,email_from,recipient_list)
    return render(request,'user/success.html',{})

     #Calender 
def calender_request(request):
    return render(request,'user/calendar.html',{})

     #safe to spend With Database
def safe(request): 
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(payee__user=request.user).all()
        try:
            user_income = sum(list(expenses.filter(transactionType="income").values_list('amount', flat=True)))
        except: 
            user_income = 0
            
        try:
            user_expenses = sum(list(expenses.filter( transactionType="expense").values_list('amount', flat=True)))
        except:
            user_expenses = 0
            
        try:
            safe_amount = user_income - (user_income * 10 / 100)
            safe_amount = int(safe_amount)
        except: 
            safe_amount = 0
        #print("*"*80)
        #print("user_income", user_income)
        #print("user_expenses", user_expenses)
        return render(request, 'user/safe.html', {"expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": safe_amount - user_expenses})
        # return render(request,'user/safe.html',{ })

      #chart With Database
def analyse(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(payee__user=request.user).all()
        try:
            user_income = sum(list(expenses.filter(transactionType="income").values_list('amount', flat=True)))
        except: 
            user_income = 0
            
        try:
            user_expenses = sum(list(expenses.filter( transactionType="expense").values_list('amount', flat=True)))
        except:
            user_expenses = 0
            
        try:
            safe_amount = user_income - (user_income * 10 / 100)
            safe_amount = int(safe_amount)
        except: 
            safe_amount = 0
        
        chart_data = [user_income, safe_amount - user_expenses, user_expenses]
        return render(request,'user/analyse.html', {"chart_data": chart_data ,  "expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": safe_amount - user_expenses})
    return render(request,'user/analyse.html', {"chart_data": [0, 0, 0],})


# def merchant(request):
#     return render(request,'merchant.html',{})
    # return render(request, 'profile.html', {}
 
    #about us page
def about(request):
    return render(request,'user/about.html',{})

     #expense category list
def category(request):
    return render(request,'user/category.html',{})

     #transaction History From Database
def template(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(payee__user=request.user).all()
        return render(request,'user/template.html',{"expenses": expenses})
    return render(request,'user/template.html',)

      #expense mamanger logo page
def exp(request):
    return render(request,'exp.html',{})



# def sendMail(request):
#     subject = ' Alert Expense\Income Added'
#     message = 'Expense Has Been Added in Expenser Manager Typical budget categories might include housing, utilities, groceries, and transportation.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['dhyeyshukla11@gmail.com','dhyeyshukla17@gmail.com',]
#     res =  send_mail(subject,message,email_from,recipient_list)
#     print(res)
#     return HttpResponse('mail sent')
    
     #forget password page calling
def forget(request):
    return render(request,'forget.html',{})


# def search(request):
#     query = request.GET['query']
#     # alllist = Property_info.objects.all()
#     alllist = Expense.objects.filter(description__icontains=query)
#     params = {'user/template/': alllist}
#     return render(request, "user/search.html" , params)