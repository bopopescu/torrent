from django import forms

from torrent_main import models, validators


class TorrentCreationForm(forms.ModelForm):

    file = forms.FileField(validators=[validators.validate_torrent])

    class Meta:
        model = models.Torrent
        fields = ('category', 'ttype', 'language', 'image', 'file', 'title', 'description')


class TorrentCommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ('text', )