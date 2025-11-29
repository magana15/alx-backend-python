from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message

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
