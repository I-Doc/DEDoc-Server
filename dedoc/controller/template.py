from sqlalchemy.exc import IntegrityError

from dedoc.app import db
from dedoc.constants import SQL_DUPLICATE_ERROR
from dedoc.models.template import Template


def create_template(template):
    try:
        new_template = Template(
            name=template['name'],
            data=template['data'],
        )

        db.session.add(new_template)
        db.session.commit()

        return new_template, None
    except IntegrityError as error:
        str_error = str(error)

        if SQL_DUPLICATE_ERROR in str_error:
            return None, 'Template already exists!'

        return None, str(error)
