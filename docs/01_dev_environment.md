# Dev Environment

This is a somewhat straightforward python Flask app, backed by a Postgres database. 

### With the Dev Container

The repository has a dev container configured which you can use if you wish. This greatly simplifies the development environment setup process as it installs a relevant version of python, the app's dependencies, postgres server and database, some CLI tools and even some extensions into your an isolated workspace.

1. Install a dev container capable IDE (we're using vscode by default), Git and Docker/podman/your container orchestration tool of choice.
2. Ensure you have the Dev Containers extension installed.
3. Clone and open the repository. Vscode will nudge you to open it in a dev container.
4. Click "Run" in the debug pane. 

Both the dev container and postgres can be deleted and rebuilt as needed without losing your DB. On recreate, they will automatically re-attach themselves to the `hackspace-mgmt_devcontainer_postgres-data` volume. This contains the data itself, so it's the important one to keep safe.

### Without the Dev Container

<details>
    <summary>Expand</summary>

#### Requiments:
- Python 3.9+
- PostgreSQL 14+
- Some ability to run Postgres queries directly - pgAdmin is a good GUI option, while `psql` is a good CLI. Both are bundled with Postgres.
- Git

In a terminal, navigate to the `hackspace-mgmt` folder and create a virtual environment with `python3 -m venv .venv`. This environment can then be activated with `source .venv/bin/activate` or `.venv/Scripts/activate.ps1` depending on which OS/terminal you are using.

Update pip with `python -m pip install --upgrade pip`.

Install the requirements with `pip install -r requirements.txt`.

You should now be able to run the server with `flask --app hackspace_mgmt:create_app --debug run` or by launching via the vscode debug pane.

Navigate to `http://127.0.0.1:5000/admin/` and you should be able to see a bare admin page!

</details>

### Database Setup

The database schema is managed by the `Flask-Migrate` package, which will automatically create the database and update the schema for you on app startup. 

However, `./sample_dataset.sql` contains a pg_dump which can be useful for development environments as it contains a realistic set of data to test with. 

1. Create a fresh database using `psql -h localhost -U postgres -c "CREATE DATABASE hackspace"`.
2. Apply the dump using `psql -h localhost -U postgres hackspace < sample_dataset.sql`.
