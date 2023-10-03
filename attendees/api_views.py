import json
from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from django.views.decorators.http import require_http_methods
from .models import Attendee
from events.models import Conference


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
@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.all()

        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)

        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )


# API_SHOW_ATTENDEE
@require_http_methods(["GET", "DELETE", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)

        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Attendee.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"}, status=400
            )

        attendee = Attendee.objects.filter(id=id).update(**content)
        return JsonResponse(
            attendee, encoder=AttendeeDetailEncoder, safe=False
        )
