from common.json import ModelEncoder
from django.http import JsonResponse
from .models import Presentation


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
def api_list_presentations(request, conference_id):
    presentations = Presentation.objects.get(conference=conference_id)

    return JsonResponse(
        presentations,
        encoder=PresentationListEncoder,
        safe=False,
    )


# API_SHOW_PRESENTATION
def api_show_presentation(request, id):

    presentation = Presentation.objects.get(id=id)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )
