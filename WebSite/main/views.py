from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse 
import random, os, time

from forms import cropLabelForm, cropFieldForm
from models import cropLabel, cropField

def index(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "index.html", context)


def mission(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "mission.html", context)


def app(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "app.html", context)


def cropLabelView(request):
    if request.method == 'POST':
        form = cropLabelForm( request.POST or None )
        
        if form.is_valid():
            label = cropLabel(
                srcFile = request.POST['srcFile'],
                x = request.POST['x'],
                y = request.POST['y'],
                width = request.POST['width'],
                height = request.POST['height'],
                duration = request.POST['duration']
            )
            
            label.duration = round( time.time() - float(label.duration) )
            label.save()

            return HttpResponseRedirect(reverse('cropLabelView'))
    
    path = r"/home/wwwUser/humain/static/images/iDigBio"
    filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])

    srcFile = "/static/images/iDigBio/" + filename 
    
    form = cropLabelForm(
            initial={'srcFile': srcFile, 'x': 0, 'y': 0, 'width': 0, 'height': 0, 'duration': round( time.time() )}
        )

    return render(request, "cropLabel.html", {'form': form, 'filename': srcFile})


def cropFieldsView(request):
    if request.method == 'POST':
        form = cropFieldForm( request.POST or None )
        #print "Errors: ", form.errors , "\n"
        if form.is_valid():            
            f_srcFile = request.POST['srcFile']
            
            f_width = request.POST['width_country']
            f_height = request.POST['height_country']
            if (f_width != '0') and (f_height != '0'):
                field1 = cropField(
                    srcFile = f_srcFile,
                    field = 1,
                    x = request.POST['x_country'],
                    y = request.POST['y_country'],
                    width = f_width,
                    height = f_height,
                    duration = request.POST['duration_country']
                )
                field1.save()
                 
            f_width = request.POST['width_date']
            f_height = request.POST['height_date']
            if (request.POST['width_date'] != '0') and (f_height != '0'):
                field2 = cropField(
                    srcFile = f_srcFile,
                    field = 2,
                    x = request.POST['x_date'],
                    y = request.POST['y_date'],
                    width = request.POST['width_date'],
                    height = f_height,
                    duration = request.POST['duration_date']
                )
                field2.save()  
             
            f_width = request.POST['width_latitude']
            f_height = request.POST['height_latitude']
            if (f_width != '0') and (f_height != '0'):
                field3 = cropField(
                    srcFile = f_srcFile,
                    field = 3,
                    x = request.POST['x_latitude'],
                    y = request.POST['y_latitude'],
                    width = f_width,
                    height = f_height,
                    duration = request.POST['duration_latitude']
                )
                field3.save()  
             
            f_width = request.POST['width_longitude']
            f_height = request.POST['height_longitude']
            if (f_width != '0') and (f_height != '0'):
                field4 = cropField(
                    srcFile = f_srcFile,
                    field = 4,
                    x = request.POST['x_longitude'],
                    y = request.POST['y_longitude'],
                    width = f_width,
                    height = f_height,
                    duration = request.POST['duration_longitude']
                )
                field4.save()  
             
            f_width = request.POST['width_name']
            f_height = request.POST['height_name']
            if (f_width != '0') and (f_height != '0'):
                field5 = cropField(
                    srcFile = f_srcFile,
                    field = 5,
                    x = request.POST['x_name'],
                    y = request.POST['y_name'],
                    width = f_width,
                    height = f_height,
                    duration = request.POST['duration_name']
                )
                field5.save()  

            return HttpResponseRedirect(reverse('cropFieldsView'))
    
    path = r"/home/wwwUser/humain/static/images/iDigBio"
    filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])

    srcFile = "/static/images/iDigBio/" + filename 
    
    form = cropFieldForm(
        initial={'srcFile': srcFile}
    )

    return render(request, "cropFields.html", {'form': form, 'filename': srcFile})


def catalog(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "catalog.html", context)


def contact(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "contact.html", context)


def help1(request):
    userid = -1
    username = "Guest"

    context = {
        'userid': userid,
        'username': username
    }
    
    return render(request, "help.html", context)
