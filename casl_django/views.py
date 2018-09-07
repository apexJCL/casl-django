from django.http import JsonResponse
from django.views import View
from .casl import permissions
from .casl.converter import Converter


# Create your views here.
class UserPermissionsView(View):
    http_method_names = ['get', 'options']
    filter_fields = [('subject', 'iexact'), ('action', 'icontains')]

    def _get_filters(self, request):
        filters = {}

        for key, value in self.filter_fields:
            if request.GET.get(key, None):
                filters["{field}__{filter}".format(
                    field=key,
                    filter=value
                )] = request.GET.get(key)

        return filters

    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                status=401,
                data={
                    'message': 'No user detected in the current session'
                }
            )
        result = permissions.Permissions.user_permissions(user=request.user)

        return JsonResponse(
            status=200,
            data=result,
            safe=False
        )

    def post(self, request):
        return self._not_allowed(request)

    def patch(self, request):
        return self._not_allowed(request)

    def delete(self, request):
        return self._not_allowed(request)

    def put(self, request):
        return self._not_allowed(request)

    def _not_allowed(self, request):
        return self.http_method_not_allowed(request)
