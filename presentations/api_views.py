import json
from common.json import ModelEncoder
from django.http import JsonResponse
from .models import Presentation
from events.models import Conference
from django.views.decorators.http import require_http_methods


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]

    def get_extra_data(self, o):
        return {
            "status": o.status.name,
            "conference": o.conference.name,
        }


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]

    def get_extra_data(self, o):
        return {
            "status": o.status.name,
        }


# API_LIST_PRESENTATION
@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = [
            {
                "title": p.title,
                "status": p.status.name,
                "href": p.get_api_url(),
            }
            for p in Presentation.objects.filter(conference=conference_id)
        ]
        return JsonResponse(
            presentations,
            encoder=PresentationListEncoder,
            safe=False,
        )
    else:
        content = json.loads(request.body)

        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


# API_SHOW_PRESENTATION
@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation, encoder=PresentationDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)

        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        Presentation.objects.filter(id=id).update(**content)

        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation, encoder=PresentationDetailEncoder, safe=False
        )
