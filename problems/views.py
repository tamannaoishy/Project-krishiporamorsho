from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .models import *
from datetime import date
from problems.models import Signup,problem


# Create your views here.
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def index(request):
    return render(request, 'index.html')


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pass']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}

    return render(request, 'login.html', d)


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['oishy']
        p = request.POST['noPASSword']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html', d)


def signup1(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['username']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        a = request.POST['area']
        r = request.POST['role']
        u = User.objects.create_user(username=f, password=p, first_name=f)
        Signup.objects.create(user=u, contact=c, area=a, role=r)
        '''
        try:
            user = User.objects.create_user(user_name=e, password=p, first_name=f, last_name=l)
            Signup.objects.create(user=user, contact=c, area=a, role=r)
            error = "no"
        except:
            error = "yes"
        '''
    #d = {'error': error}

    return render(request, 'signup.html',locals())


def admin_home(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    pn = problem.objects.filter(status="pending").count()
    sl = problem.objects.filter(status="solved").count()
    all = problem.objects.all().count()
    d = {'pn': pn,'sl': sl,'all': all}
    return render(request, 'admin_home.html',d)


def Logout(request):
    logout(request)
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user=user)
    d = {'user': user,'data': data}
    return render(request, 'profile.html', d)


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == 'POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "no"
        else:
            error = "yes"
    d = {'error': error}

    return render(request, 'changepassword.html', d)


def upload_problems(request):
    signup_obj = Signup.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return redirect('login')
    elif signup_obj.role != 'Farmer':
        return redirect('login')
    error = ""
    if request.method == 'POST':
        a = request.POST['area']
        f = request.POST['field']
        p = request.FILES['problemfile']
        ft = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()

        user = problem.objects.create(user=u, area=a, field=f, problemfile=p,
                                      filetype=ft, description=d, status='pending')
        error = "no"
        d = {'error': error}
        '''
        try:
            user = problem.objects.create(user=u, uploadindate=date.today(), area=a, field=f, problemfile=p,
                                               filetype=ft, description=d, status='pending')

            error = "no"
        except:
            error = "yes"
        '''
    d = {'error': error}
    return render(request, 'upload_problems.html', d)


def view_myproblems(request):
    signup_obj = Signup.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return redirect('login')
    elif signup_obj.role != 'Farmer':
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    problems = problem.objects.filter(user=user)

    d = {'problems': problems}
    return render(request, 'view_myproblems.html', d)

def solution(request, pk):
    problem_obj = problem.objects.get(id=pk)
    solution_obj = solve.objects.get(problem=problem_obj)
    context = {
        'problem_obj': problem_obj,
        'solution_obj' : solution_obj
    }
    return render(request, 'solution.html', context)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    users = Signup.objects.all()
    d = {'users': users}
    return render(request, 'view_users.html', d)


def all_problems(request):
    signup_obj = Signup.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return redirect('admin_login')
    elif signup_obj.role != 'Agriculturist':
        return redirect('login')
    problems = problem.objects.all()
    
    if request.method == 'POST':
        slv = request.POST['slv']
        releted_problem_id = int(request.POST['problem'])
        problem_obj = problem.objects.get(id=releted_problem_id)

        solve_obj = solve.objects.create(
            problem = problem_obj,
            solution = slv,
            solver =  signup_obj
        )
        solve_obj.save()
        problem_obj.status = "solved"
        problem_obj.save()

    context = {
        'problems' : problems,
    }
    
    return render(request, 'all_problems.html', context)

'''
def accepted_problems(request):
    
    
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    user = User.objects.get(id=request.user.id)
    problems = problem.objects.filter(status='pending')
    
    d = {'problems': problems}
    
    return render(request, 'accepted_problems', d)
    '''
    
def solved_problems(request):
    
    if not request.user.is_authenticated:
        return redirect('admin_login')
   
    user = User.objects.get(id=request.user.id)
    problems = problem.objects.filter(status='solved')

    d = {'problems': problems}
    return render(request, 'solved_problems', d)


def accepted_problems(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = User.objects.get(id=request.user.id)
    problems = problem.objects.filter(status='pending')


    d = {'problems': problems}
    return render(request, 'accepted_problems.html', d)


'''
def assign_status(request,pk):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    problem_obj = problem.objects.get(id=pk)
    error =""
    if request.method == 'POST':
        s = request.POST['status']
        problem_obj.status = s
        problem_obj.save()
        error = "no"
    d = {'problem_obj': problem_obj, 'error': error}
    return render(request, 'assign_status.html',d)'''

def admin_problems(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    problems = problem.objects.all()


    d = {'problems': problems}
    return render(request, 'admin_problems.html', d)
