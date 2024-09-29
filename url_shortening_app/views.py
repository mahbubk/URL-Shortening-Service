from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, ShortenedURL
from .forms import UserRegistrationForm, UserLoginForm, ShortenURLForm

# Create your views here.

def log_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# def register(request):
#     if request.method == 'POST':
#         form =  UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data['password'])
#             user.save()
#             return redirect('login')
#         else:
#             form = UserRegistrationForm()
#         return render(request, 'register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             try:
#                 user = User.objects.get(username=username)
#                 if check_password(password, user.password):
#                     request.session['user_id'] = user.id
#                     return redirect('index')
#                 else:
#                     form.add_error(None, 'Invalid username or password')
#             except User.DoesNotExist:
#                 form.add_error(None, 'Invalid username or password')
#         else:
#             form = UserLoginForm()
#         return render(request, 'login.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    return redirect('index')
                else:
                    form.add_error(None, 'Invalid Password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid username')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})



def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('index')


def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None


@log_required
def user_links(request):
    user = get_current_user(request)
    if not user:
        return redirect('index')
    links = ShortenedURL.objects.filter(user=user)
    return render(request, 'user_links.html', {'links': links})


# def get_current_user(request):
#     user_id = request.session.get('user_id')
#     if user_id:
#         try:
#             return User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return None
#     return None
#
# @log_required
# def user_links(request):
#     user = get_current_user(request)
#     if not user:
#         return redirect('index')
#     links = ShortenedURL.objects.filter(user=user)
#     return render(request, 'user_links.html', {'links': links})


def redirect_url(request, short_code):
    try:
        url = ShortenedURL.objects.get(short_code=short_code)
        if url.is_expired():
            return render(request, 'expired.html')
        url.clicks += 1
        url.save()
        return redirect(url.original_url)
    except ShortenedURL.DoesNotExist:
        return render(request, '404.html')



@log_required
def index(request):
    user = get_current_user(request)
    if request.method == 'POST':
        form = ShortenURLForm(request.POST)
        if form.is_valid():
            shortened_url = form.save(commit=False)
            if form.cleaned_data['custom_short_code']:
                shortened_url.short_code = form.cleaned_data['custom_short_code']

            else:
                shortened_url.short_code = shortened_url.generate_short_code()
                shortened_url.custom_short_code = None

            if user:
                shortened_url.user = user
            shortened_url.save()
            return render(request, 'shortend_url.html', {'short_url': shortened_url, 'request': request})

        else :
            print(form.errors)
    else:
        form = ShortenURLForm()
        return render(request, 'index.html', {'form': form, 'user': user})
