from events.api_views import ConferenceListEncoder
from common.json import ModelEncoder
from django.http import JsonResponse
from .models import Attendee


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
        "email",
        "company_name",
        "created",
        "conference",
    ]

    encoders = {
        "conference": ConferenceListEncoder(),
    }


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


# API_LIST_ATTENDEES
def api_list_attendees(request, conference_id):
    attendees = Attendee.objects.all()

    return JsonResponse(
        {"attendees": attendees},
        encoder=AttendeeListEncoder,
    )


# API_SHOW_ATTENDEE
def api_show_attendee(request, id):
    attendee = Attendee.objects.get(id=id)
    return JsonResponse(
        attendee,
        encoder=AttendeeDetailEncoder,
        safe=False,
    )
