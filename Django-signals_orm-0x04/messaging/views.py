from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message

#deleting
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages


class MessageEditView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["content"]
    template_name = "messaging/message_edit.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(sender=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object._edited_by = self.request.user

        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("messaging:message_detail", kwargs={"pk": self.object.pk})

@login_required
def delete_user_view(request):
    """
    Confirm and delete the logged-in user and related messaging data.

    GET -> show confirmation page
    POST -> delete user and redirect to home (or goodbye page)
    """
    if request.method == "POST":
        user = request.user
        # Log user out of the session before deletion:
        logout(request)

        # Perform deletion inside a transaction
        with transaction.atomic():
            user.delete()  # triggers pre_delete -> cleanup_messaging_data_before_user_delete

        messages.success(request, "Your account and its related messaging data were deleted.")
        # Redirect somewhere safe (home or goodbye page)
        return redirect("home")  # change to your site's home URL name

    return render(request, "messaging/confirm_delete.html", {"user": request.user})
