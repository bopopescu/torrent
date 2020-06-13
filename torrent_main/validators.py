from django import forms


def validate_torrent(value):
    file_format = value.name.split('.')[-1]
    if file_format != 'torrent':
        raise forms.ValidationError('Invalid torrent format')
    return value
