from .models import AdvUser, InteriorDesign
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView
from .form import RegisterUserForm , FormDesign
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def index(request):
    designs = InteriorDesign.objects.all()[:4]
    num_status = InteriorDesign.objects.filter(status='status_2').count()
    return render(request, 'main/index.html', {'designs': designs, 'num_status': num_status})

def create_design(request):
    if request.method == 'POST':
        form = FormDesign(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.user = request.user
            design.save()
            return redirect('main:profile')
    else:
        form = FormDesign()

    return render(request, 'pages/create_disign.html', {'form': form})

def delete_design(request, design_id):
    design = get_object_or_404(InteriorDesign, id=design_id)

    if design.user == request.user:
        if design.status == 'Новая':
            design.delete()
            messages.success(request, 'Заявка успешно удалена.')
        else :
            messages.error(request, 'Вы не можете удалить заявку с этим статусом.')
    else:
        messages.error(request, 'Вы не можете удалить эту заявку.')

    return redirect('main:profile')

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'pages/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class BBLoginView(LoginView):
    template_name = 'pages/login.html'

class RegisterDoneView(TemplateView):
    template_name = 'pages/register_done.html'
    success_url = reverse_lazy('main:profile')

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'pages/logout.html'

def profile(request):
    status_filter = request.GET.get('status', 'Новая')
    designs = InteriorDesign.objects.filter(user=request.user, status=status_filter)
    return render(request, 'pages/profile.html', {'designs': designs})

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')