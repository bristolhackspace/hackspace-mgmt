# Dev Environment

This is a somewhat straightforward python Flask app, backed by a Postgres database. 

### With the Dev Container

The repository has a dev container configured which you can use if you wish. This greatly simplifies the development environment setup process as it installs a relevant version of python, the app's dependencies, postgres server and database, some CLI tools and even some extensions into your an isolated workspace.

1. Install a dev container capable IDE (we're using vscode by default), Git and Docker/podman/your container orchestration tool of choice.
2. Ensure you have the Dev Containers extension installed.
3. Clone and open the repository. Vscode will nudge you to open it in a dev container.
4. Click "Run" in the debug pane. 

Note: Both the dev container and postgres can be deleted and rebuilt as needed without losing your DB. They will automatically re-attach themselves to the `hackspace-mgmt_devcontainer_postgres-data` volume which is the important one not to lose as it contains the database itself. 

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

The database is nominally configured by running each of the SQL scripts inside the `migration` folder sequentially. Anytime a new one is added, this will need to be applied before the app is started.

If you're using a dev container, the `migrate.sh` script will be run prior to any debug session which does this automagically! 

Tooling-wise, you may wish to use `psql` - a CLI for interacting with the datbase directly. The dev container comes with it installed, but because it is running in a container, you need to use `psql -h localhost -U postgres (-d hackspace) etc` to connect.

Separately, you may find it helpful to install `pgAdmin`. This is a free GUI tool for exploring Postgres, similar to SSMS. 
