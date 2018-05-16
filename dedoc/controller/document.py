from sqlalchemy.exc import IntegrityError

from dedoc.app import db
from dedoc.constants import SQL_DUPLICATE_ERROR
from dedoc.models.document import Document


def create_document(document):
    try:
        new_document = Document(
            name=document['name'],
            owner=document['owner'],
            template=document['template'],
            state=document['state'],
            data=document['data'],
        )

        db.session.add(new_document)
        db.session.commit()

        return new_document, None
    except IntegrityError as error:
        str_error = str(error)

        if SQL_DUPLICATE_ERROR in str_error:
            return None, 'Document already exists!'

        return None, str(error)
