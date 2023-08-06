import click
import os
import importlib
from sqlalchemy import create_engine, inspect, text, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def faons():
    """
    Faons CLI tool for project creation.
    """
    pass

@click.command('initializeproject')
@click.argument('project_name')
def initializeproject(project_name):
    """
    Create a new project with the given name.
    """
    # Create the project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)
    click.echo(f"Created project directory: {project_dir}")

    # Create additional directories
    directories = ['conf', 'src', 'src/core', 'src/config', 'src/logger']
    for directory in directories:
        directory_path = os.path.join(project_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        click.echo(f"Created directory: {directory_path}")

    # Create files
    files = {
        'main.py': '''import uvicorn
from utils import include_routers, init
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title="FAONS - Made on Fast API", version="0.0.6")
include_routers(app)


@app.get("/")
def main_route():
    return "Welcome to FAONS"

if __name__ == '__main__':
    init()
    uvicorn.run(app, host="127.0.0.1", port=5001)
        ''',
        'settings.py': '''from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# Change you database connection over here
DATABASE_URL = f'sqlite:///{BASE_DIR}/db.sqlite3'
        ''',
        'utils.py':'''from pathlib import Path
from fastapi import FastAPI, APIRouter
from importlib import import_module


def include_routers(app: FastAPI):
    """
    Discovers router modules in the app
    """
    routers_dir = Path("src/core")
    for router_file in routers_dir.rglob("router.py"):
        module_name = ".".join(router_file.with_suffix("").parts)
        module = import_module(module_name)
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            app.include_router(router)
def init():
    """
    Add functions that need to be run during program initialization
    """
    pass
        ''',
        'README.md':'# Project Documentation',
        'conf/__init__.py':'',
        'conf/env.conf':'',
        'src/__init__.py':'',
        'src/config/__init__.py':'',
        'src/config/config.py':'',
        'src/config/constants.py':'',
        'src/core/__init__.py':'',
        'src/logger/__init__.py':'',
    }
    for file_path, file_content in files.items():
        file_path = os.path.join(project_dir, file_path)
        with open(file_path, 'w') as file:
            file.write(file_content)
        click.echo(f"Created file: {file_path}")

    click.echo("Project initialized successfully.")

@click.command('startapp')
@click.argument('app_name')
@click.option('--project-dir', help='Path to the project directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def startapp(app_name, project_dir):
    """
    Create a new app with the given name.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)

    if not os.path.exists(project_dir):
        click.echo(f"Project directory does not exist: {project_dir}")
        return

    project_core_dir = os.path.join(project_dir, 'src/core')
    if not os.path.exists(project_core_dir):
        click.echo("The 'startapp' command can only be executed within a project directory created by 'initializeproject'.")
        return

    # Create additional directories
    directories = [os.path.join(project_core_dir, app_name)]
    for directory in directories:
        directory_path = os.path.join(project_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        click.echo(f"Created app: {directory_path}")

    # Create files
    files = {
        os.path.join(project_core_dir, app_name, '__init__.py'): '',
        os.path.join(project_core_dir, app_name, 'handler.py'): '# Define the logic for your router in this file',
        os.path.join(project_core_dir, app_name, 'models.py'): '''from pydantic import BaseModel

# Define your models below this line
        ''',
        os.path.join(project_core_dir, app_name, 'router.py'):f'''from fastapi import APIRouter, Response

router = APIRouter()

# Define your endpoints below this line. We have already created one for you

@router.get("/{app_name}")
def {app_name}():
    return "This is your first endpoint from {app_name} app"
        ''',
        os.path.join(project_core_dir, app_name, 'schema.py'):'# Define the tables for your app in this file',
        os.path.join(project_core_dir, app_name, 'utils.py'):'# Define the utilities for your app in this file',
    }
    for file_path, file_content in files.items():
        file_path = os.path.join(project_dir, file_path)
        with open(file_path, 'w') as file:
            file.write(file_content)

    click.echo("App created successfully.")

def import_schemas(project_dir):
    schemas = []
    src_path = os.path.join(project_dir, 'src', 'core')
    
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file == 'schema.py':
                module_path = os.path.relpath(root, src_path).replace(os.sep, '.')
                module_name = os.path.splitext(file)[0]
                full_module_name = f'{module_path}.{module_name}'

                try:
                    spec = importlib.util.spec_from_file_location(full_module_name, os.path.join(root, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    schemas.append(module)
                except Exception as e:
                    print(f"Failed to import module: {full_module_name}")
                    print(f"Error details: {str(e)}")

    return schemas

def schemalist(schemas):
    classes = []
    for schema in schemas:
        for name, obj in schema.__dict__.items():
            if isinstance(obj, type) and issubclass(obj, schema.Base) and obj is not schema.Base:
                classes.append(obj.__tablename__)
    return classes

@click.command('updateschema')
@click.option('--project-dir', help='Path to the project directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def updateschema(project_dir):
    """
    Update the database schema by creating or altering tables.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)

    if not os.path.exists(project_dir):
        click.echo(f"Project directory does not exist: {project_dir}")
        return

    settings_path = os.path.join(project_dir, 'settings.py')

    # Read settings from the module
    settings = {}
    with open(settings_path, 'r') as f:
        exec(f.read(), settings, {'__file__': settings_path})
    settings = {}
    exec_globals = {'__file__': os.path.abspath(settings_path)}
    exec(open(settings_path).read(), exec_globals, settings)

    # Get the db_url from the settings
    db_url = settings['DATABASE_URL']
    engine = create_engine(db_url)

    # Define the create_or_alter_tables function here
    def create_or_alter_tables(engine):
        metadata = MetaData()
        faons_schema_table = Table(
            'faons_schema',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('table_name', String, unique=True)
        )
        Session = sessionmaker(bind=engine)
        session = Session()

        schemas = import_schemas(project_dir)
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Create 'faons_schema' table if it doesn't exist
        if "faons_schema" not in existing_tables:
            metadata.create_all(engine)
            print("Table 'faons_schema' created.")

        # Get the table names from the 'faons_schema' table
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM faons_schema"))
            faons_table_names = [row[0] for row in result]

        # Create or alter tables
        for schema in schemas:
            for name, obj in schema.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, schema.Base) and obj is not schema.Base:
                    if hasattr(obj, '__tablename__'):
                        table_name = obj.__tablename__
                        # if table_name in existing_tables and table_name in faons_table_names:
                        #     print(f"Table '{table_name}' already exists in 'faons_schema' table.")
                        #     continue
                        if table_name in existing_tables:
                            try:
                                # Table already exists, compare table structure
                                with engine.connect() as connection:
                                    metadata.reflect(bind=engine)
                                    existing_table = metadata.tables[table_name]
                                    schema_table = obj.__table__
                                    # Check if table columns match
                                    for column in schema_table.columns:
                                        if column.name not in existing_table.columns:
                                            # Add missing column
                                            connection.execute(
                                                text(f'ALTER TABLE "{table_name}" ADD COLUMN "{column.name}" {column.type}')
                                            )
                                            print(f"Table '{table_name}' altered. Column '{column.name}' added.")

                                for column in existing_table.columns:
                                    if column.name not in schema_table.columns:
                                        # Remove extra column
                                        with engine.connect() as connection:
                                            connection.execute(
                                                text(f'ALTER TABLE "{table_name}" DROP COLUMN "{column.name}"')
                                            )
                                        print(f"Table '{table_name}' altered. Column '{column.name}' dropped.")

                                # Reflect the changes to the metadata
                                metadata.reflect(bind=engine)

                            except Exception as e:
                                print(f"An error occurred while altering table '{table_name}': {str(e)}")
                        else:
                            # Table does not exist, create it
                            obj.metadata.create_all(engine)
                            print(f"Table '{table_name}' created.")

                        # Add the table name to 'faons_schema' table
                        if table_name not in faons_table_names:
                            try:
                                with engine.begin() as connection:
                                    connection.execute(faons_schema_table.insert().values(table_name=table_name))
                                print(f"Table '{table_name}' added to 'faons_schema' table.")
                                # Commit the changes to the database
                                connection.commit()
                            except Exception as e:
                                print(f"An error occurred while adding table '{table_name}' to 'faons_schema' table: {str(e)}")

        # Get the table names from the 'faons_schema' table again
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM faons_schema"))
            faons_table_names = [row[0] for row in result]
            classes = schemalist(schemas)

        # Remove tables that no longer exist in the schema
        for table_name in existing_tables:
            if (
                table_name not in ['faons_models', 'faons_schema']
                and table_name not in classes
                and table_name in existing_tables
            ):
                with engine.connect() as connection:
                    # Check if the table name exists in faons_schema before dropping it
                    result = connection.execute(
                        text("SELECT 1 FROM faons_schema WHERE table_name = :table_name"),
                        {"table_name": table_name},
                    )
                    if result.fetchone() is not None:
                        connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}"'))
                        print(f"Table '{table_name}' removed.")
                        # Delete the corresponding record from the 'faons_schema' table
                        try:
                            with engine.begin() as connection:
                                connection.execute(
                                    text(f"DELETE FROM faons_schema WHERE table_name = :table_name"),
                                    {"table_name": table_name},
                                )
                            print(f"Record for table '{table_name}' deleted from 'faons_schema' table.")
                        except Exception as e:
                            print(
                                f"An error occurred while deleting record for table '{table_name}' from 'faons_schema' table: {str(e)}"
                            )

        session.close()

    # Call the create_or_alter_tables function
    create_or_alter_tables(engine)


def create_table(model, engine):
    
    # Define the table name based on the model class name
    table_name = model.__name__
    metadata = MetaData()
    # Check if table already exists
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        # Create columns based on the fields in the model
        columns = [
            Column(field_name, String) for field_name, field in model.__annotations__.items()
        ]

        # Define the table
        table = Table(table_name, metadata, *columns)

        # Create the table in the database
        table.create(bind=engine)
        print(f"Table '{table_name}' created.")
    else:
        # Table already exists, check for columns to add or modify
        existing_columns = inspector.get_columns(table_name)
        schema_columns = [
            Column(field_name, String) for field_name, field in model.__annotations__.items()
        ]

        # Check if any new columns need to be added
        for column in schema_columns:
            if column.name not in [c['name'] for c in existing_columns]:
                column_name = column.name
                column_type = column.type
                with engine.connect() as connection:
                    connection.execute(
                        text(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type}')
                    )
                print(f"Table '{table_name}' altered. Column '{column_name}' added.")

        # Check if any columns need to be modified or dropped
        for column in existing_columns:
            if column['name'] not in [c.name for c in schema_columns]:
                column_name = column['name']
                with engine.connect() as connection:
                    connection.execute(
                        text(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"')
                    )
                print(f"Table '{table_name}' altered. Column '{column_name}' dropped.")


def import_models(directory):
    models = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'models.py':
                path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.basename(path))[0]
                module_spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                models.append(module)
    return models



@click.command('updatemodels')
@click.option('--project-dir', help='Path to the project directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def updatemodels(project_dir):
    """
    Update the database schema by creating or altering tables.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)

    if not os.path.exists(project_dir):
        click.echo(f"Project directory does not exist: {project_dir}")
        return

    settings_path = os.path.join(project_dir, 'settings.py')

    # Read settings from the module
    settings = {}
    with open(settings_path, 'r') as f:
        exec(f.read(), settings, {'__file__': settings_path})
    settings = {}
    exec_globals = {'__file__': os.path.abspath(settings_path)}
    exec(open(settings_path).read(), exec_globals, settings)

    # Get the db_url from the settings
    db_url = settings['DATABASE_URL']
    engine = create_engine(db_url)

    # Define the create_or_alter_tables function here
    def create_or_alter_tables(engine, project_dir):
        Session = sessionmaker(bind=engine)
        session = Session()

        models = import_models(project_dir)

        # Get the existing table names
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Define the 'faons_models' table
        metadata = MetaData()
        faons_models_table = Table(
            'faons_models',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('table_name', String, unique=True)
        )

        # Create 'faons_models' table if it doesn't exist
        if "faons_models" not in existing_tables:
            metadata.create_all(engine)
            print("Table 'faons_models' created.")

        # Get the table names from the 'faons_models' table
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM faons_models"))
            faons_table_names = [row[0] for row in result]

        model_classes = []
        # Create or alter tables based on the models
        for model_module in models:
            for name, obj in model_module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel:
                    model_classes.append(obj.__name__)

        # Add the table name to 'faons_models' table
        for table_name in model_classes:
            if table_name not in faons_table_names and table_name != 'faons_models' and table_name != 'faons_schema':
                try:
                    with engine.begin() as connection:
                        connection.execute(faons_models_table.insert().values(table_name=table_name))
                    print(f"Table '{table_name}' added to 'faons_models' table.")
                    # Commit the changes to the database
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred while adding table '{table_name}' to 'faons_models' table: {str(e)}")

        # Get the table names from the 'faons_models' table
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM faons_models"))
            faons_table_names = [row[0] for row in result]


        # Create or alter tables based on the models
        for model_module in models:
            for name, obj in model_module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel:
                    create_table(obj,engine)
                    table_name = obj.__name__
                    if table_name in existing_tables:
                        existing_tables.remove(table_name)

        # Drop tables for classes that were removed from the models.py file
        for table_name in existing_tables:
            if table_name not in ['faons_models', 'faons_schema'] and table_name in faons_table_names:
                with engine.connect() as connection:
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}"'))
                print(f"Table '{table_name}' dropped.")
                with engine.begin() as connection:
                    delete_statement = text('DELETE FROM faons_models WHERE table_name = :table_name')
                    connection.execute(delete_statement.bindparams(table_name=table_name))
                print(f"'{table_name}' removed from models.")
                

        session.close()

    # Call the create_or_alter_tables function
    create_or_alter_tables(engine,project_dir)

    
faons.add_command(initializeproject)
faons.add_command(startapp)
faons.add_command(updateschema)
faons.add_command(updatemodels)

if __name__ == '__main__':
    faons()
