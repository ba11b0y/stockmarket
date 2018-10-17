from neo4django.db.models import Property

class FloatProperty(Property):
    def get_default(self):
        return 0.0

    def to_neo(self, value):
        return float(value)