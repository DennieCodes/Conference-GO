from django.http import JsonResponse
from .models import Conference, Location


# API_LIST_CONFERENCES
def api_list_conferences(request):
    response = []
    conferences = Conference.objects.all()
    for conference in conferences:
        response.append(
            {
                "name": conference.name,
                "href": conference.get_api_url(),
            }
        )
    return JsonResponse({"conferences": response})


# API_SHOW_CONFERENCE
def api_show_conference(request, id):
    conference = Conference.objects.get(id=id)

    return JsonResponse(
        {
            "name": conference.name,
            "starts": conference.starts,
            "ends": conference.ends,
            "description": conference.description,
            "created": conference.created,
            "updated": conference.updated,
            "max_presentations": conference.max_presentations,
            "max_attendees": conference.max_attendees,
            "location": {
                "name": conference.location.name,
                "href": conference.location.get_api_url(),
            },
        }
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
