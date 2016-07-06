from lxml import etree
import numpy
import requests
import time
from datetime import timedelta
from dateutil import parser
from django.http import HttpResponse
import urllib2
from .app import ScriptViewer
import csv
import zipfile
import StringIO
import time
import zipfile
import os
import dateutil.parser
from datetime import datetime
import pandas as pd

def get_app_base_uri(request):
    base_url = request.build_absolute_uri()
    if "?" in base_url:
        base_url = base_url.split("?")[0]
    return base_url


def get_workspace():
    return ScriptViewer.get_app_workspace().path
def waterml_file_path(res_id):
    base_path = get_workspace()
    file_path = base_path + "/id/" + res_id
    if not file_path.endswith('.txt'):
        file_path += '.txt'
    return file_path
def unzip_waterml(request, res_id,src):
    # print "unzip!!!!!!!"
    print "unzipping"
    print datetime.now()
    # this is where we'll unzip the waterML file to
    temp_dir = get_workspace()
    # waterml_url = ''

    # get the URL of the remote zipped WaterML resource
    print src
    if not os.path.exists(temp_dir+"/id"):
        os.makedirs(temp_dir+"/id")

    if 'cuahsi'in src :
        # url_zip = 'http://bcc-hiswebclient.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/'+res_id+'/zip'
        url_zip = 'http://qa-webclient-solr.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/'+res_id+'/zip'
    # elif 'hydroshare' in src:
    #     url_zip = 'https://www.hydroshare.org/hsapi/_internal/'+res_id+'/download-refts-bag/'
    elif 'hydroshare_script' in src:
        url_zip =  'https://www.hydroshare.org/django_irods/download/bags/'+res_id+'.zip'
        print url_zip
        # data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
        # for line in data: # files are iterable
        #     print line
    else:
        url_zip = 'http://' + request.META['HTTP_HOST'] + '/apps/data-cart/showfile/'+res_id


    if src != 'hydroshare_generic':
        waterml_url = "test"

        r = requests.get(url_zip, verify=False)

        try:
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            file_list = z.namelist()
            print file_list
            try:
                for file in file_list:
                    if 'hydroshare_script' in src:
                        if '.r' in file:
                            file_data = z.read(file)
                            file_temp_name = temp_dir + '/id/' + res_id + '.txt'
                            file_temp = open(file_temp_name, 'wb')
                            file_temp.write(file_data)
                            file_temp.close()
                            # base_url = request.build_absolute_uri()
                            # if "?" in base_url:
                            #     base_url = base_url.split("?")[0]
                            # waterml_url = base_url + "temp_waterml/cuahsi/id/" + res_id + '.xml'


                    else:
                        file_data = z.read(file)
                        file_temp_name = temp_dir + '/id/' + res_id + '.xml'
                        file_temp = open(file_temp_name, 'wb')
                        file_temp.write(file_data)
                        file_temp.close()
                        # getting the URL of the zip file
                        # base_url = request.build_absolute_uri()
                        # if "?" in base_url:
                        #     base_url = base_url.split("?")[0]
                        # waterml_url = base_url + "temp_waterml/cuahsi/id/" + res_id + '.xml'

            # error handling

            # checks to see if data is an xml
            # except etree.XMLSyntaxError as e:
            #     print "Error:Not XML"
            #     return False

            # checks to see if Url is valid
            except ValueError, e:
                print "Error:invalid Url"
                return False

            # checks to see if xml is formatted correctly
            except TypeError, e:
                print "Error:string indices must be integers not str"
                return False

        # check if the zip file is valid
        except zipfile.BadZipfile as e:
                error_message = "Bad Zip File"
                print "Bad Zip file"
                return False

    # finally we return the waterml_url
    print "File created"
    print datetime.now()
    return waterml_url
def Original_Checker(file_path):
    f = open(file_path, 'r')
    response = f.read()
    # response.encode(encoding='UTF-8',errors='strict')

    return {'script':response}