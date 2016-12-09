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
from django.views.decorators.cache import never_cache
import logging

logger = logging.getLogger(__name__)

use_hs_client_helper = True
try:
    from tethys_services.backends.hs_restclient_helper import get_oauth_hs
except Exception as ex:
    use_hs_client_helper = False
    logger.error("tethys_services.backends.hs_restclient_helper import get_oauth_hs: " + ex.message)
@login_required()
@never_cache
def home(request):
    """
    Controller for the app home page.
    """
    # temp_dir = utilities.get_workspace()
    # print temp_dir
    # temp_dir = temp_dir[:-24]
    # print temp_dir
    utilities.viewer_counter(request)
    context = {}
    return render(request, 'script_viewer/home.html', context)
def chart_data(request, res_id, src):
    data_for_chart = {}
    error = False
    is_owner = False
    print "JSON Reponse"
    print datetime.now()
    print "update"
    # Downloading all files types that work with app from hydroshare
    file_path = utilities.get_workspace() + '/id'
    root_dir = file_path + '/' + res_id
    try:
        shutil.rmtree(root_dir)
    except:
        nothing =None
    try:
        if use_hs_client_helper:
            hs = get_oauth_hs(request)
        else:
            hs = getOAuthHS(request)
        hs.getResource(res_id, destination=file_path, unzip=True)
        data_dir = root_dir + '/' + res_id + '/data/contents/'
        # f = open(data_dir)
        # print f.read()
        for subdir, dirs, files in os.walk(data_dir):
            for file in files:
                # if '.r' in file or '.R' in file or'.py' in file or '.m' in file or '.txt' in file or '.xml' in file:
                    data_file = data_dir + file
                    with open(data_file, 'r') as f:
                        # print f.read()
                        data = f.read()
                        # print data
                        f.close()
                        print data
                        try:
                            data= data.decode('latin-1')
                        except:
                            data = data
                        data_for_chart.update({str(file): data})

        # data_for_chart = {'bjo':'hello'}
        user =  hs.getUserInfo()
        user1 = user['username']
        # resource = hs.getResourceList(user ='editor')
        resource = hs.getResourceList(owner = user1)
        for  res in resource:
            # print res
            id = res["resource_id"]
            # print id
            if(res_id ==res["resource_id"]):
                is_owner = True
    except Exception as inst:
        data_for_chart = 'You are not authorized to access this resource'
        owner = False
        error = True
        print 'start'
        print(type(inst))
        print(inst.args)
        try:
            data_for_chart = str(inst)
        except:
            data_for_chart = "There was an error loading data for resource"+res_id
        print "end"
    return JsonResponse({"data":data_for_chart,"owner":is_owner,"error":error})
        # return JsonResponse({"data":data_for_chart.decode(encoding='UTF-8',errors='strict'),"owner":is_owner,"error":error})
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
    script = request.POST.get('script')
    file_path = utilities.get_workspace() + '/id'
    root_dir = file_path + '/' + res_id
    data_dir = root_dir + '/' + res_id + '/data/contents/' + file_name
    print data_dir

    try:
        if use_hs_client_helper:
            hs = get_oauth_hs(request)
        else:
            hs = getOAuthHS(request)
        if save_type == 'save':
            # os.remove(data_dir)
            with open(data_dir, 'wb') as f:
                f.write(script)

            hs.deleteResourceFile(res_id, file_name)
            # raw_input('PAUSED')
            hs.addResourceFile(res_id, data_dir)
        else:
            with open(data_dir, 'wb') as f:
                f.write(script)

            hs.addResourceFile(res_id, data_dir)
            # raw_input('PAUSED')
        shutil.rmtree(root_dir)
        file = {"File Uploaded": file_name}
    except:
        file = {"File not saved": file_name}
    return JsonResponse(file)

def delete_file(request, res_id, file_name, src):

    try:
        if use_hs_client_helper:
            hs = get_oauth_hs(request)
        else:
	        hs = getOAuthHS(request)
        file_path = utilities.get_workspace() + '/id'
        root_dir = file_path + '/' + res_id
        data_dir = root_dir + '/' + res_id + '/data/contents/' + file_name

        hs.deleteResourceFile(res_id, file_name)
        shutil.rmtree(root_dir)
        file = {"File Deleted": file_name}
    except:
        file = {'File not Deleted':file_name}
    return JsonResponse(file)

def view_counter(request):
    temp_dir = utilities.get_workspace()
    file_path = temp_dir[:-24] + 'view_counter.txt'
    file_temp = open(file_path, 'r')
    content = file_temp.read()
    return JsonResponse({"Number of Viewers":content})

def error_report(request):
    print os.path.realpath('controllers.py')
    temp_dir = utilities.get_workspace()
    temp_dir = temp_dir[:-24]
    file_path = temp_dir + '/error_report.txt'
    if not os.path.exists(temp_dir+"/error_report.txt"):
        file_temp = open(file_path, 'a')
        file_temp.close()
        content = ''
    else:
        file_temp = open(file_path, 'r')
        content = file_temp.read()
    return JsonResponse({"Error Reports":content})