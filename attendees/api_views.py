from django.http import JsonResponse
from .models import Attendee


# API_LIST_ATTENDEES
def api_list_attendees(request, conference_id):
    # response = []
    # attendees = Attendee.objects.all()
    # for attendee in attendees:
    #     response.append(
    #         {
    #             "name": attendee.name,
    #             "href": attendee.get_api_url(),
    #         }
    #     )
    attendees = [
        {
            "name": p.name,
            "href": p.get_api_url(),
        }
        for p in Attendee.objects.filter(conference=conference_id)
    ]

    return JsonResponse({"attendees": attendees})


# API_SHOW_ATTENDEE
def api_show_attendee(request, id):
    attendee = Attendee.objects.get(id=id)
    return JsonResponse(
        {
            "name": attendee.name,
            "email": attendee.email,
            "company_name": attendee.company_name,
            "created": attendee.created,
            "conference": {
                "name": attendee.conference.name,
                "href": attendee.conference.get_api_url(),
            },
        }
    )
