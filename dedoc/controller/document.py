from sqlalchemy.exc import IntegrityError

from dedoc.app import db
from dedoc.constants import SQL_DUPLICATE_ERROR, SQL_CONSTRAINT_ERROR
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

def change_document_state(document_id, new_state):
    try:
        document = Document.query.filter_by(id=document_id).first()
        if not document:
            return 'No document with such ID.'

        document.state = new_state
        db.session.commit()
        return None
    except IntegrityError as error:
        str_error = str(error)

        if SQL_DUPLICATE_ERROR in str_error:
            return 'Document already exists!'
        if SQL_CONSTRAINT_ERROR in str_error:
            return 'No such document state!'

        print(error)
        return "Unknown error"
