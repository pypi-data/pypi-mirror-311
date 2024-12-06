from sqlalchemy_utils import UUIDType

from histudio.app import db
from histudio.app.models.serializer import SerializerMixin
from histudio.app.models.base import BaseMixin

from sqlalchemy.dialects.postgresql import JSONB


class ApiEvent(db.Model, BaseMixin, SerializerMixin):
    """
    Represent notable events occuring on database (asset creation,
    task assignation, etc.).
    """

    name = db.Column(db.String(80), nullable=False, index=True)
    user_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("person.id"), index=True
    )
    project_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("project.id"), index=True
    )
    data = db.Column(JSONB)
