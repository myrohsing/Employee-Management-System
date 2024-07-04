from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        logger.debug(f"Request path: {request.path}, Module: {modulename}, User: {user.username if user.is_authenticated else 'Anonymous'}")
        
        if user.is_authenticated:
            if user.user_type == '1':  # Admin
                if modulename in ['main_app.staff_views', 'main_app.hod_views'] and request.path != reverse('admin_home'):
                    logger.debug("Admin redirect to admin_home")
                    return redirect(reverse('admin_home'))
            elif user.user_type == '2':  # Staff
                if modulename == 'main_app.hod_views' and request.path != reverse('staff_home'):
                    logger.debug("Staff redirect to staff_home")
                    return redirect(reverse('staff_home'))
            else:  # None of the above
                logger.debug("Invalid user type, redirect to login_page")
                return redirect(reverse('login_page'))
        else:
            allowed_paths = [reverse('login_page'), reverse('user_login')]
            if request.path in allowed_paths or modulename == 'django.contrib.auth.views':
                pass
            else:
                logger.debug("Unauthenticated user, redirect to login_page")
                return redirect(reverse('login_page'))
