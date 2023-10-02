from django.http import JsonResponse

from .models import Presentation


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
        {
            "presenter_name": presentation.presenter_name,
            "company_name": presentation.company_name,
            "presenter_email": presentation.presenter_email,
            "title": presentation.title,
            "synopsis": presentation.synopsis,
            "created": presentation.created,
            "status": {"status": presentation.status.name},
            "conference": {
                "name": presentation.conference.name,
                "href": presentation.conference.get_api_url(),
            },
        }
    )
