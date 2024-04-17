# Dev Environment

This is a somewhat straightforward python Flask app, backed by a Postgres database. 

The repository has a dev container configured which you can use if you like.

Requiments:
- Python 3.9+
- PostgreSQL 14+ - installed as part of the devcontainer if you are using it.
- Some ability to run Postgres queries directly - pgAdmin is a good GUI option, while `psql` is a good CLI - both are bundled with Postgres
- Git
- Docker/podman/your container orchestration tool of choice (if using dev containers).

Most of us use VsCode as a lightweight IDE.

### Database Setup

1. Connect to the database using `psql postgres` or using pgAdmin.
2. Create a database called `hackspace`. In psql, you can run the query `CREATE DATABASE hackspace;` (don't forget the semi-colon!).
3. Under the `hackspace-mgmt/migration` folder is a bunch of SQL scripts. Run these, in order, against the new hackspace database. In pgAdmin, you would right click on the database and open the `Query` tool. Then copy-paste in the contents of each file and run them one-by-one.

If you had to change the username, then you'll want to create a postgres user. You can do this by right-clicking the server and then _Create->Login/Group role_. Name the role `postgres`, then on the _Priveleges_ tab, enable _Can Login_ and _Superuser_ (this isn't recommended for production, but fine for development).

### Webserver Setup

In a terminal, navigate to the `hackspace-mgmt` folder and create a virtual environment with `python3 -m venv .venv`. This environment can then be activated with `source .venv/bin/activate` or `.venv/Scripts/activate.ps1` depending on which OS/terminal you are using.

Update pip with `python -m pip install --upgrade pip`.

Install the requirements with `pip install -r requirements.txt`.

You should now be able to run the server with `flask --app hackspace_mgmt:create_app --debug run`.

Navigate to `http://127.0.0.1:5000/admin/` and you should be able to see a bare admin page!