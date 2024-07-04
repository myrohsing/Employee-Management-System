import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_clients = Client.objects.all().count()
    projects = Project.objects.all()
    total_project = projects.count()
    total_department = Department.objects.all().count()
 
    attendance_list = []
    project_list = []
    for project in projects:
        
        project_list.append(project.name[:7])
       

  
    department_all = Department.objects.all()
    department_name_list = []
    project_count_list = []
    client_count_list_in_department = []

    for department in department_all:
        projects = Project.objects.filter(department_id=department.id).count()
        clients= Client.objects.filter(department_id=department.id).count()
        department_name_list.append(department.name)
        project_count_list.append(projects)
        client_count_list_in_department.append(clients)
    
    project_all = Project.objects.all()
    project_list = []
    client_count_list_in_project = []
    for project in project_all:
        department = Department.objects.get(id=project.department.id)
        client_count = Client.objects.filter(department_id=department.id).count()
        project_list.append(project.name)
        client_count_list_in_project.append(client_count)


    # For Clients
    client_attendance_present_list=[]
    client_attendance_leave_list=[]
    client_name_list=[]

    clients = Client.objects.all()
    for client in clients:
      
        client_name_list.append(client.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_clients': total_clients,
        'total_staff': total_staff,
        'total_department': total_department,
        'total_project': total_project,
        'project_list': project_list,
        'attendance_list': attendance_list,
        'client_attendance_present_list': client_attendance_present_list,
        'client_attendance_leave_list': client_attendance_leave_list,
        "client_name_list": client_name_list,
        "client_count_list_in_project": client_count_list_in_project,
        "client_count_list_in_department": client_count_list_in_department,
        "department_name_list": department_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Employee'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            department = form.cleaned_data.get('department')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_client(request):
    client_form = ClientForm(request.POST or None, request.FILES or None)
    context = {'form': client_form, 'page_title': 'Add Client'}
    if request.method == 'POST':
        if client_form.is_valid():
            first_name = client_form.cleaned_data.get('first_name')
            last_name = client_form.cleaned_data.get('last_name')
            address = client_form.cleaned_data.get('address')
            email = client_form.cleaned_data.get('email')
            gender = client_form.cleaned_data.get('gender')
            password = client_form.cleaned_data.get('password')
            department= client_form.cleaned_data.get('department')
            timeline = client_form.cleaned_data.get('timeline')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.client.timeline = timeline
                user.client.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_client'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_client_template.html', context)


def add_department(request):
    form = DepartmentForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department()
                department.name = name
                department.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_department'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_department_template.html', context)


def add_project(request):
    form = ProjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Project'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            staff = form.cleaned_data.get('staff')
            try:
                project = Project()
                project.name = name
                project.staff = staff
                project.department = department
                project.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_project'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_project_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Employees'
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_client(request):
    clients = CustomUser.objects.filter(user_type=3)
    context = {
        'clients': clients,
        'page_title': 'Manage Clients'
    }
    return render(request, "hod_template/manage_client.html", context)


def manage_department(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
        'page_title': 'Manage Department'
    }
    return render(request, "hod_template/manage_department.html", context)


def manage_project(request):
    projects = Project.objects.all()
    context = {
        'departments': projects,
        'page_title': 'Manage Projects'
    }
    return render(request, "hod_template/manage_project.html", context)


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Employees'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            salary = form.cleaned_data.get('salary')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password:
                    user.set_password(password)
                if passport:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                user.save()
                
                staff.salary = salary
                staff.phone_number = phone_number
                staff.department = department
                staff.save()

                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fill the form properly")
    return render(request, "hod_template/edit_staff_template.html", context)



def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    form = ClientForm(request.POST or None, instance=client)
    context = {
        'form': form,
        'client_id': client_id,
        'page_title': 'Edit Clients'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            timeline = form.cleaned_data.get('timeline')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=client.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                client.timeline = timeline
                user.gender = gender
                user.address = address
                client.department = department
                user.save()
                client.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_client', args=[client_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_client_template.html", context)


def edit_department(request, department_id):
    instance = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': department_id,
        'page_title': 'Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department.objects.get(id=department_id)
                department.name = name
                department.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_department_template.html', context)


def edit_project(request, project_id):
    instance = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'project_id': project_id,
        'page_title': 'Edit Project'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                project = Project.objects.get(id=project_id)
                project.name = name
                project.staff = staff
                project.department = department
                project.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[project_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'hod_template/edit_project_template.html', context)


def add_timeline(request):
    form = TimelineForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Timeline'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Timeline Created")
                return redirect(reverse('add_timeline'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_timeline_template.html", context)


def manage_timeline(request):
    timelines = Timeline.objects.all()
    context = {'timelines': timelines, 'page_title': 'Manage Timelines'}
    return render(request, "hod_template/manage_timeline.html", context)


def edit_timeline(request, timeline_id):
    instance = get_object_or_404(Timeline, id=timeline_id)
    form = TimelineForm(request.POST or None, instance=instance)
    context = {'form': form, 'timeline_id': timeline_id,
               'page_title': 'Edit Timeline'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Timeline Updated")
                return redirect(reverse('edit_timeline', args=[timeline_id]))
            except Exception as e:
                messages.error(
                    request, "Timeline Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_timeline_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_timeline_template.html", context)

    else:
        return render(request, "hod_template/edit_timeline_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)





@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Employee Feedback Messages'
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Employees'
        }
        return render(request, "hod_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False





def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Employees",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)



@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Employee Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/admin.jpg')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, "Employee deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_client(request, client_id):
    client = get_object_or_404(CustomUser, client__id=client_id)
    client.delete()
    messages.success(request, "Client deleted successfully!")
    return redirect(reverse('manage_client'))


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    try:
        department.delete()
        messages.success(request, "Department deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some client projects are assigned to this department already. Kindly change the affected client department and try again")
    return redirect(reverse('manage_department'))


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect(reverse('manage_project'))


def delete_timeline(request, timeline_id):
    timeline = get_object_or_404(Timeline, id=timeline_id)
    try:
        timeline.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_timeline'))
