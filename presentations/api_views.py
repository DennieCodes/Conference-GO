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
        # "status",
        # "conference",
    ]


# API_LIST_PRESENTATION
def api_list_presentations(request, conference_id):
    presentations = [
        {
            "title": p.title,
            "status": p.status.name,
            "href": p.get_api_url(),
        }
        for p in Presentation.objects.filter(conference=conference_id)
    ]
    return JsonResponse({"presentations": presentations})


# API_SHOW_PRESENTATION
def api_show_presentation(request, id):

    presentation = Presentation.objects.get(id=id)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )
