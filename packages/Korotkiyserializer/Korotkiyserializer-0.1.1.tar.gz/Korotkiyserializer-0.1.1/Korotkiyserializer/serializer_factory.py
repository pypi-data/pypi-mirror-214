from Korotkiyserializer.Korotkiyserializer.xml_serializer import xml_serializer
from Korotkiyserializer.Korotkiyserializer.json_serializer import json_serializer


class factory:

    @staticmethod
    def create_serializer(f_mat: str):
        f_mat = f_mat.lower()

        if f_mat == "json":
            return json_serializer()
        elif f_mat == "xml":
            return xml_serializer()
        else:
            raise ValueError
