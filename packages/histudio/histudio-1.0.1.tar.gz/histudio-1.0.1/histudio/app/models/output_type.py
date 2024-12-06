from histudio.app import db
from histudio.app.models.serializer import SerializerMixin
from histudio.app.models.base import BaseMixin


class OutputType(db.Model, BaseMixin, SerializerMixin):
    """
    Type of an output files (geometry, cache, etc.)
    """

    name = db.Column(db.String(40), unique=True, nullable=False, index=True)
    short_name = db.Column(db.String(20), nullable=False)
