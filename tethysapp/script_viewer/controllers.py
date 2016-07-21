from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import utilities
import os
import zipfile
import StringIO
import requests
from datetime import datetime
from django.conf import settings
from xml.sax._exceptions import SAXParseException
from hs_restclient import HydroShare, HydroShareAuthOAuth2, HydroShareNotAuthorized, HydroShareNotFound
from suds.transport import TransportError
from suds.client import Client
from django.conf import settings
import shutil


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}
    return render(request, 'script_viewer/home.html', context)
def chart_data(request, res_id, src):
    data_for_chart = {}
    print "JSON Reponse"
    print datetime.now()
    # Downloading all files types that work with app from hydroshare
    hs = getOAuthHS(request)
    file_path = utilities.get_workspace() + '/id'
    hs.getResource(res_id, destination=file_path, unzip=True)

    root_dir = file_path + '/' + res_id
    data_dir = root_dir + '/' + res_id + '/data/contents/'
    # f = open(data_dir)
    # print f.read()
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            if '.r' in file or'.py' in file or '.m' in file or '.txt' in file or '.xml' in file:
                data_file = data_dir + file
                with open(data_file, 'r') as f:
                    # print f.read()
                    data = f.read()
                    f.close()
                    data_for_chart.update({str(file): data})

    # data_for_chart = {'bjo':'hello'}
    return JsonResponse(data_for_chart)
    # resp = HttpResponse(data_for_chart, content_type="text/plain; charset=utf-8")
    # return resp


def getOAuthHS(request):
    hs_instance_name = "www"
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", None)
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", None)
    # this line will throw out from django.core.exceptions.ObjectDoesNotExist if current user is not signed in via HydroShare OAuth
    token = request.user.social_auth.get(provider='hydroshare').extra_data['token_dict']
    hs_hostname = "{0}.hydroshare.org".format(hs_instance_name)
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    hs = HydroShare(auth=auth, hostname=hs_hostname)

    return hs


def save_file(request, res_id, file_name, src, save_type):
    script = request.POST['script']

    file_path = utilities.get_workspace() + '/id'
    root_dir = file_path + '/' + res_id
    data_dir = root_dir + '/' + res_id + '/data/contents/' + file_name


    if save_type == 'save':
        # os.remove(data_dir)
        with open(data_dir, 'wb') as f:
            f.write(script)
        hs = getOAuthHS(request)
        hs.deleteResourceFile(res_id, file_name)

        # raw_input('PAUSED')
        hs.addResourceFile(res_id, data_dir)
    else:
        with open(data_dir, 'wb') as f:
            f.write(script)
        hs = getOAuthHS(request)
        hs.addResourceFile(res_id, data_dir)

        # raw_input('PAUSED')
    shutil.rmtree(root_dir)
    file = {"File Uploaded": file_name}
    return JsonResponse(file)


def delete_file(request, res_id, file_name, src):
    file_path = utilities.get_workspace() + '/id'
    root_dir = file_path + '/' + res_id
    data_dir = root_dir + '/' + res_id + '/data/contents/' + file_name
    hs = getOAuthHS(request)
    hs.deleteResourceFile(res_id, file_name)
    shutil.rmtree(root_dir)
    file = {"File Deleted": file_name}
    return JsonResponse(file)