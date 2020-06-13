from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from torrent_main import models, forms, filters


class HomeView(generic.ListView):
    model = models.Torrent
    template_name = 'torrent_main/home.html'
    queryset = model.published.all()
    # queryset = model.objects.filter(is_pub=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_list = context.get('object_list')

        categories = models.Category.objects.all()
        context['week'] = obj_list.order_by('-downloads')[:12]
        for category in categories:
            context[category.category_name] = self.model.published.filter(
                category__category_name=category.category_name).order_by('-downloads')[:12]
        return context


class TorrentDetailView(generic.DetailView):
    model = models.Torrent
    template_name = 'torrent_main/torrent_detail.html'
    context_object_name = 'torrent'
    comment_form = forms.TorrentCommentForm

    # Если не авторизирован - доступ только к is_pub=True (done)
    # Если авторизирован - доступ ко всем is_pub=True + к своим
    def get_object(self, queryset=None):
        if self.request.user.is_staff:
            return get_object_or_404(self.model, slug=self.kwargs['slug'])
        else:
            return self.model.published.get_by_user(user=self.request.user, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form
        return context

    def post(self, *args, **kwargs):
        form = self.comment_form(self.request.POST)
        if form.is_valid():
            obj = self.get_object()
            author = self.request.user
            form.instance.torrent = obj
            form.instance.author = author
            form.save()
        context = super().get_context_data(**kwargs)
        context['comment_form'] = form
        return self.render_to_response(context=context)


@login_required
def download_torrent(request, slug):
    torrent = models.Torrent.published.get_by_user(user=request.user, slug=slug)
    torrent.downloads += 1
    torrent.save()

    filename = torrent.file
    response = HttpResponse(filename.read())
    response['content-type'] = 'application/x-bittorrent'
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename.name)
    return response


class SearchView(generic.ListView):
    model = models.Torrent
    context_object_name = 'torrents'
    queryset = model.published.filter()
    template_name = 'torrent_main/torrent_list.html'
    filter = filters.TorrentSortingFilter

    def get_queryset(self):
        search_value = self.request.GET.get('search')
        category_value = self.request.GET.get('category')
        if search_value:
            return self.queryset.filter(title__contains=search_value)
        if category_value:
            return self.queryset.filter(category__slug=category_value)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['torrents'] = self.filter(self.request.GET, queryset=self.get_queryset()).qs
        context['search_field'] = self.request.GET.get('search')
        context['category_value'] = self.request.GET.get('category')
        context['sorting'] = self.filter
        return context


def filter(request):
    if request.is_ajax() and request.method == 'GET':
        orderby = request.GET.get('sorting')
        category_value = request.GET.get('category_value')
        search_value = request.GET.get('search_value')
        if category_value:
            data = models.Torrent.published.filter(category__category_name=category_value).order_by(orderby)
        else:
            data = models.Torrent.published.filter(title__icontains=search_value).order_by(orderby)
        context = {'torrents': data}
        html_rendered = render_to_string('torrent_main/torrent_filter_ajax_response.html', context)
        return JsonResponse({'html': html_rendered})


class TorrentCreation(LoginRequiredMixin, generic.CreateView):
    model = models.Torrent
    form_class = forms.TorrentCreationForm
    template_name = 'torrent_main/torrent_creation.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        obj = self.object
        obj.uploaded_by = self.request.user
        obj.save()
        return response

    def get_success_url(self):
        return reverse('uploads')


class UploadsList(LoginRequiredMixin, generic.ListView):
    model = models.Torrent
    template_name = 'torrent_main/uploads_list.html'
    context_object_name = 'torrents'

    def get_queryset(self):
        return self.model.objects.filter(uploaded_by=self.request.user)
