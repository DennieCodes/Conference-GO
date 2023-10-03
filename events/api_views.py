from common.json import ModelEncoder
from django.http import JsonResponse
from .models import Conference, Location


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
    ]


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
    ]


# API_LIST_CONFERENCES
def api_list_conferences(request):
    # response = []
    conferences = Conference.objects.all()
    # for conference in conferences:
    #     response.append(
    #         {
    #             "name": conference.name,
    #             "href": conference.get_api_url(),
    #         }
    #     )
    # return JsonResponse({"conferences": response})
    return JsonResponse(
        {"conferences": conferences},
        encoder=ConferenceListEncoder,
    )


# API_SHOW_CONFERENCE
def api_show_conference(request, id):
    conference = Conference.objects.get(id=id)

    return JsonResponse(
        conference,
        encoder=ConferenceDetailEncoder,
        safe=False,
    )


# API_LIST_LOCATIONS
def api_list_locations(request):
    response = []
    locations = Location.objects.all()
    for location in locations:
        response.append(
            {
                "name": location.name,
                "href": location.get_api_url(),
            }
        )
    return JsonResponse({"locations": response})


# API SHOW LOCATION
def api_show_location(request, id):
    location = Location.objects.get(id=id)
    return JsonResponse(
        {
            "name": location.name,
            "city": location.city,
            "room_count": location.room_count,
            "created": location.created,
            "updated": location.updated,
            "state": {
                "name": location.state.name,
            },
        }
    )
