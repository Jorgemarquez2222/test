import logging
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from app_public.app.tools import get_json_from_jsonresponse
from app_public.views.api import ApiDoctorInfo

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
	The public view where users can see doctor's details
	and take appointments
"""


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class ViewDoctorView(TemplateView):
    template_name = "doctor/doctor_view.html"

    def get(self, request, *args, **kwargs):
        try:
            apiresp = ApiDoctorInfo.as_view()(request)
            if apiresp.status_code != 200:
                return apiresp
            json = get_json_from_jsonresponse(apiresp)
            return render(request, self.template_name, {'doctor': json})
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest()