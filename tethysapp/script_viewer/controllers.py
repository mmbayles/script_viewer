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

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'script_viewer/home.html', context)

def chart_data(request, res_id, src):
    print res_id
    script = 'r'
    # checks if we already have an unzipped xml file
    file_path = utilities.waterml_file_path(res_id)
    # if we don't have the xml file, downloads and unzips it
    if not os.path.exists(file_path):
        waterml = utilities.unzip_waterml(request, res_id,src)




    url_zip ='http://www.hydroshare.org/hsapi/resource/'+res_id
    r = requests.get(url_zip, verify=False)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    file_list = z.namelist()

    for  file in file_list:
        if '.py' in file:
            script = 'python'
        elif '.r' in file:
            script = 'r'
        elif '.m' in file:
            script = 'matlab'
    # returns an error message if the unzip_waterml failed
    if not os.path.exists(file_path):
        data_for_chart = {'status': 'Resource file not found'}
    else:
        # parses the WaterML to a chart data object
        data_for_chart = utilities.Original_Checker(file_path,script)

    print script
    print "JSON Reponse"
    print datetime.now()
    return JsonResponse(data_for_chart)
    # resp = HttpResponse(data_for_chart, content_type="text/plain; charset=utf-8")
    # return resp
