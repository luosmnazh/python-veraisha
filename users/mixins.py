from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UnauthenticatedOnlyMixin(UserPassesTestMixin):
    authenticated_next_page = 'car:home'
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.authenticated_next_page)
