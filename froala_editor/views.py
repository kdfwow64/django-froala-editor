import json
# from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string

import uuid


# Allow for a custom storage backend defined in settings.
def get_storage_class():
    return import_string(getattr(settings, 'FROALA_STORAGE_BACKEND', 'django.core.files.storage.DefaultStorage'))()


storage = get_storage_class()

def unique_filename(name):
    ext = name.split('.')[-1]
    filename = "%s.%s" % (name.replace('.' + ext, '') + '-' + str(uuid.uuid4()), ext)
    return filename


def image_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/pjpeg',
            'image/x-png',
            'image/png',
            'image/gif'
        ]
        if not the_file.content_type in allowed_types:
            return HttpResponse(json.dumps({'error': _('You can only upload images.')}),
                                content_type="application/json")
        # Other data on the request.FILES dictionary:
        # filesize = len(file['content'])
        # filetype = file['content-type']

        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'uploads/froala_editor/')
        upload_to = upload_to + 'images/'

        path = storage.save(os.path.join(upload_to, unique_filename(the_file.name)), the_file)
        # link = request.build_absolute_uri(storage.url(path))

        link = 'https://' + getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'sengkuyung-dev') + '.s3-' + getattr(settings, 'AWS_S3_REGION_NAME',
                                                                                                              'ap-southeast-1') + '.amazonaws.com' + path
        # cloudfront_domain = getattr(settings, 'CLOUDFRONT_DOMAIN', '')
        # if cloudfront_domain == '':
        #     link = 'https://' + getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'sengkuyung-dev') + '.s3-' + getattr(settings, 'AWS_S3_REGION_NAME',
        #                                                                                                           'ap-southeast-1') + '.amazonaws.com' + path
        # else:
        #     link = 'https://' + cloudfront_domain + path

        # return JsonResponse({'link': link})
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")


def file_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'uploads/froala_editor/')
        upload_to = upload_to + 'files/'

        path = storage.save(os.path.join(upload_to, unique_filename(the_file.name)), the_file)
        # link = storage.url(path)
        link = 'https://' + getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'sengkuyung-dev') + '.s3-' + getattr(settings, 'AWS_S3_REGION_NAME',
                                                                                                              'ap-southeast-1') + '.amazonaws.com' + path
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")
