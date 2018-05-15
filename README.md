# DEDoc-Server
DEDoc Python-Flask server repository

Requirements:
1. SQL server
2. Python 3.x

Installation:

1. Install all required python packages with:

    `pip install -r requirements.txt`

2. Create in project root folder file `db.conf` with content:

    ```
    [database]
    username = %db_username%
    password = %db_password%
    db_type = %db_type%
    db_name = %db_name%
    host = %db_hostname%
    ```

    If you are using MySQL with pymysql: `mysql+pymysql`

3. Run `python3 manage.py migrate` to create tables.

4. Run `python3 manage.py seed` to fill db with constants.

5. Run `python3 manage.py run` to run development server.
