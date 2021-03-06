from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User
from .forms import AlumniSignupForm, RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


class SignupView(CreateView):
    model = User
    form_class = AlumniSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'alumni'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('alumni-profile')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = RegistrationForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('alumni-profile')

    else:
        u_form = RegistrationForm(instance=request.user)

    context = {
        'form': u_form
    }
    return render(request, 'registration.html', context)
