from json import JSONEncoder
from datetime import datetime


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, JSONEncoder):
    def default(self, o):
        #   if the object to decode is the same class as what's in the
        #   model property, then
        if isinstance(o, self.model):
            #     * create an empty dictionary that will hold the property names
            #       as keys and the property values as values
            d = {}
            #     * for each name in the properties list
            for property in self.properties:
                #         * get the value of that property from the model instance
                #           given just the property name
                value = getattr(o, property)
                #         * put it into the dictionary with that property name as
                #           the key
                d[property] = value
            #     * return the dictionary
            return d
        #   otherwise,
        else:
            return super().default(o)  # From the documentation
