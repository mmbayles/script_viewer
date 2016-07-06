from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import utilities
import os
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
    # checks if we already have an unzipped xml file
    file_path = utilities.waterml_file_path(res_id)
    # if we don't have the xml file, downloads and unzips it
    if not os.path.exists(file_path):
        utilities.unzip_waterml(request, res_id,src)

    # returns an error message if the unzip_waterml failed
    if not os.path.exists(file_path):
        data_for_chart = {'status': 'Resource file not found'}
    else:
        # parses the WaterML to a chart data object
        data_for_chart = utilities.Original_Checker(file_path)


    print "JSON Reponse"
    print datetime.now()
    return JsonResponse(data_for_chart)

    # resp = HttpResponse(data_for_chart, content_type="text/plain; charset=utf-8")
    # return resp
