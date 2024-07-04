
from django.urls import path


from . import hod_views, staff_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("department/add", hod_views.add_department, name='add_department'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_timeline/", hod_views.add_timeline, name='add_timeline'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("timeline/manage/", hod_views.manage_timeline, name='manage_timeline'),
    path("timeline/edit/<int:timeline_id>",
         hod_views.edit_timeline, name='edit_timeline'),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("client/add/", hod_views.add_client, name='add_client'),
    path("project/add/", hod_views.add_project, name='add_project'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("client/manage/", hod_views.manage_client, name='manage_client'),
    path("department/manage/", hod_views.manage_department, name='manage_department'),
    path("project/manage/", hod_views.manage_project, name='manage_project'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("department/delete/<int:department_id>",
         hod_views.delete_department, name='delete_department'),

    path("project/delete/<int:project_id>",
         hod_views.delete_project, name='delete_project'),

    path("timeline/delete/<int:timeline_id>",
         hod_views.delete_timeline, name='delete_timeline'),

    path("client/delete/<int:client_id>",
         hod_views.delete_client, name='delete_client'),  
    path("client/edit/<int:client_id>",
         hod_views.edit_client, name='edit_client'),
    path("department/edit/<int:department_id>",
         hod_views.edit_department, name='edit_department'),
    path("project/edit/<int:project_id>",
         hod_views.edit_project, name='edit_project'),


    # Employee
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),





   

]
