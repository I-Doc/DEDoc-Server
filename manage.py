import sys

from dedoc.app import app, db

def run():
    app.run(debug=True, host='0.0.0.0')

def not_found():
    print('command not found')

def migrate():
    print('applying migrations...')
    import dedoc.models
    from dedoc.models.document_state import DocumentState
    from dedoc.constants import DOCUMENT_STATES

    for name, description in DOCUMENT_STATES:
        db.session.add(DocumentState(name=name, description=description))

    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except Exception:
        print('command not found... default will be chosen (run)')
        command = 'run'

    commands = {
        'run': run,
        'migrate': migrate,
    }
    commands.get(command, not_found)()
