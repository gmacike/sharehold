from django.contrib.auth.decorators import user_passes_test
from django import template

register = template.Library()

@register.simple_tag
def has_any_permission (permissions, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has any of permissions
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        test_passed = False
        for permission in permissions:
            # if isinstance(permission, str):
            #     perms = (permission, )
            # else:
            #     perms = permission
            # First check if the user has the permission (even anon users)
            if user.has_perm(permission):
                test_passed = True
                break

        # In case the 403 handler should be called raise the exception
        if not test_passed and raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return test_passed

    return user_passes_test(check_perms, login_url=login_url)
