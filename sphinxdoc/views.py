# encoding: utf-8

import datetime
import os.path

from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson as json

from sphinxdoc.models import App


def documentation(request, slug, url):
    app = get_object_or_404(App, slug=slug)
    url = url.strip('/')
    
    path = os.path.join(app.path, url, 'index.fjson')
    if not os.path.exists(path):
        path = os.path.dirname(path) + '.fjson'
        if not os.path.exists(path):
            raise Http404('"%s" does not exist' % path)

    templates = (
        'sphinxdoc/%s.html' % os.path.basename(url),
        'sphinxdoc/documentation.html',
    )
    
    data = {
        'app': app,
        'doc': json.load(open(path, 'rb')),
        'env': json.load(open(
                os.path.join(app.path, 'globalcontext.json'), 'rb')),
        'version': app.name,
        'docurl': url,
        'update_date':  datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(app.path, 'last_build'))),
        'home': app.get_absolute_url(),
        # 'search': urlresolvers.reverse('document-search', kwargs={'lang':lang, 'version':version}),
        'redirect_from': request.GET.get('from', None),
    
    }
    return render_to_response(templates, data,
            context_instance=RequestContext(request))
