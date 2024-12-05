from django.db.transaction import commit

from .models import AdvUser, InteriorDesign, Category
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, DetailView, ListView
from .form import RegisterUserForm , FormDesign, CommentForm, ImageForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .utilities import signer

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

def user_activate(request, sign):
    username = signer.unsign(sign)
    user = get_object_or_404(AdvUser, username=username)
    template = 'pages/activation_done.html'
    user.is_activated = True
    user.is_active = True
    user.save()
    return render(request, template)

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
    user = request.user
    if user.is_staff:
        status_filter = request.GET.get('status', 'Новая')
        designs = InteriorDesign.objects.filter(status=status_filter)
        return render(request, 'admin/admin_profile.html', {'designs': designs})
    else:
        status_filter = request.GET.get('status', 'Новая')
        designs = InteriorDesign.objects.filter(user=request.user, status=status_filter)
        return render(request, 'pages/profile.html', {'designs': designs})

def change_status(request, designs_id):
    design = get_object_or_404(InteriorDesign, id=designs_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        valid_statuses = ['status_2', 'status_3']
        if new_status in valid_statuses:
            if new_status == 'status_2':
                form = CommentForm(request.POST)
                if form.is_valid():
                    design.comment = form.cleaned_data.get('comment', '')
            elif new_status == 'status_3':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    new_image = form.cleaned_data.get('image', None)
                    if new_image:
                        design.image = new_image
            design.status = new_status
            design.save()
            messages.success(request, 'Статус заявки изменен')
    return redirect('main:profile')

class CategoryListView(ListView):
    model = Category
    template_name = 'admin/category_list.html'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'admin/category_datail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designs'] = InteriorDesign.objects.filter(category=self.object)
        return context

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    design = get_object_or_404(InteriorDesign.objects.filter(category=category))
    category.delete()
    design.delete()
    messages.success(request, 'Категория и все связанные с ней проекты успешно удалены.')
    return redirect('main:category')

class DesignListView(ListView):
    model = InteriorDesign
    template_name = 'admin/design_list.html'

class DesignDetailView(DetailView):
    model = InteriorDesign
    template_name = 'admin/design_datail.html'

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')