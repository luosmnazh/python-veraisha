from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UnauthenticatedOnlyMixin(UserPassesTestMixin):
    authenticated_next_page = 'cars:index'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.authenticated_next_page)


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = []
    raise_exception = False
    permission_denied_message = "You do not have permission to access this page."

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.group_required).exists()

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('cars:index')
