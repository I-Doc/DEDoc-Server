from sqlalchemy.exc import IntegrityError

from dedoc.app import db
from dedoc.models.document import Document


SQL_DUPLICATE_ERROR = '1062'


def create_document(document):
    try:
        new_document = Document(
            name=document['name'],
            owner=document['owner'],
            template=document['template'],
            state=document['state'],
            data=document['data'],
            cdate=document['cdate'],
            mdate=document['mdate'],
        )

        db.session.add(new_document)
        db.session.commit()

        return new_document, None
    except IntegrityError as error:
        str_error = str(error)

        if SQL_DUPLICATE_ERROR in str_error:
            return None, 'Document already exists!'

        return None, str(error)
