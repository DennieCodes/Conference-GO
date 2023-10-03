from common.json import ModelEncoder
from django.http import JsonResponse
from .models import Conference, Location


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
    ]

    def get_extra_data(self, o):
        return {"state": o.state.abbreviation}


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]


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
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }


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

    locations = Location.objects.all()

    return JsonResponse(
        {"locations": locations},
        encoder=LocationListEncoder,
    )


# API SHOW LOCATION
def api_show_location(request, id):
    location = Location.objects.get(id=id)
    return JsonResponse(
        location,
        encoder=LocationDetailEncoder,
        safe=False,
    )
