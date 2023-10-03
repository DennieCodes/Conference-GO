from json import JSONEncoder
from django.db.models import QuerySet
from datetime import datetime


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    def default(self, o):
        #   if the object to decode is the same class as what's in the
        #   model property, then
        if isinstance(o, self.model):
            d = {}
            # if o has the attribute get_api_url
            #    then add its return value to the dictionary
            #    with the key "href"
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            for property in self.properties:
                value = getattr(o, property)
                d[property] = value

            return d
        else:
            return super().default(o)  # From the documentation
