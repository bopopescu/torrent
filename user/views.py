from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from torrent_main import models as torrent_models


class UploadsList(LoginRequiredMixin, generic.ListView):
    model = torrent_models.Torrent
    template_name = 'torrent_main/uploads_list.html'
    context_object_name = 'torrents'

    def get_queryset(self):
        return self.model.objects.filter(uploaded_by=self.request.user)


