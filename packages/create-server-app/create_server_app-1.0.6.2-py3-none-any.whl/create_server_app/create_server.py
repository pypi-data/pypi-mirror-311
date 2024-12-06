import os
import subprocess
import pkg_resources
import re

def create_server_project(project_name):
    # Define the directory structure for the project
    dirs = [
        project_name
    ]

    # Create directories
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

    # Create the main app.py file
    app_py_content = """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open(os.path.join(project_name, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # create an AppConfig for the project
    app_config_content = """ 
import os
import datetime


class Timezone:

    def __init__(self):
        super().__init__()
        #gmt + 8
        self.timezone = 8

    def getTimezone(self):
        return datetime.timezone(datetime.timedelta(hours=self.timezone))


class Environment:

    def __init__(self):
        super().__init__()
        self.environment = os.getenv('ENVIRONMENT')
        if self.environment not in [
                'localdev', 'localprod', 'clouddev', 'cloudprod', 'localTest', 'cloudTest'
        ]:
            raise Exception("Invalid environment")

    def getEnvironment(self):
        return self.environment

    def getIsCloudEnvironment(self):
        return self.getEnvironment() in ['clouddev', 'cloudprod']

    def getIsProductionEnvironment(self):
        return self.getEnvironment() in ['cloudprod']

    def getisLocalDevEnvironment(self):
        return self.getEnvironment() in ['localdev']

    def getisLocalEnvironment(self):
        return self.getEnvironment() in ['localdev', 'localprod']

    def getIsDevEnvironment(self):
        return self.getEnvironment() in ['localdev', 'clouddev']
    
    def getIsTestEnvironment(self):
        return self.getEnvironment() in ['localTest', 'cloudTest']


class PubSubConfig():

    def __init__(self):
        super().__init__()
        # Pub/Sub settings
        self.PROJECT_ID = ''

        # setting runLocalPubSub to True or False. If set to true the pubsub will make
        # a request to another local server that the user specified in the function to
        # mock the pubsub. If set to false the pubsub will skip this step.
        # THIS IS USED FOR TESTING PURPOSES
        self.runLocalPubSub = os.getenv('runLocalPubSub')
        if self.runLocalPubSub.lower() not in ['true', 'false']:
            raise Exception("Invalid runLocalPubSub")
        if self.runLocalPubSub.lower() == 'true':
            self.runLocalPubSub = True
        elif self.runLocalPubSub.lower() == 'false':
            self.runLocalPubSub = False

    def getProjectId(self):
        return self.PROJECT_ID


class AppConfig(Environment, PubSubConfig, Timezone):

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    appConfig = AppConfig()

"""
    with open(os.path.join(project_name, 'AppConfig.py'), 'w') as f:
        f.write(app_config_content)

    def parse_requirement(req_line):
        """
        Parse a requirement string to extract the package name and version constraint.
        Handles cases like:
        - Flask
        - pytest>=8.0.0
        - pymongo==4.8.0
        """
        match = re.match(r"([a-zA-Z0-9\-_]+)([><=~!]*.*)?", req_line.strip())
        if match:
            package = match.group(1)
            version = match.group(2) or ""
            return package, version
        return None, None

    # Create a requirements.txt for the project
    requirements_content = """Flask==3.0.3
pytest==8.3.3
pytest-cov==6.0.0
pymongo==4.8.0
"""
    requirements_path = os.path.join(project_name, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write(requirements_content)

    try:
        with open(requirements_path) as req_file:
            requirements = req_file.readlines()

        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        to_install = []

        for req in requirements:
            req = req.strip()
            if not req or req.startswith("#"):
                continue

            pkg_name, version_constraint = parse_requirement(req)
            if not pkg_name:
                print(f"Skipping invalid requirement line: {req}")
                continue

            if pkg_name.lower() in installed_packages:
                installed_version = installed_packages[pkg_name.lower()]
                if version_constraint:
                    if not pkg_resources.Requirement.parse(req).specifier.contains(installed_version, prereleases=True):
                        print(f"'{pkg_name}' does not satisfy '{version_constraint}'. Adding to install list.")
                        to_install.append(req)
                    else:
                        print(f"'{pkg_name} ({installed_version})' satisfies '{version_constraint}'. Skipping.")
                else:
                    print(f"'{pkg_name} ({installed_version})' is installed with no specific constraint. Skipping.")
            else:
                print(f"'{pkg_name}' is not installed. Adding to install list.")
                to_install.append(req)

        if to_install:
            subprocess.check_call([os.sys.executable, "-m", "pip", "install"] + to_install)
            print("Requirements installed/updated successfully!")
        else:
            print("All required packages are already installed.")
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements.")
        print(f"Error: {e}")

    # Create an __init__.py file in the app directory to structure the package
    with open(os.path.join(project_name, '__init__.py'), 'w') as f:
        f.write('# Initialize the app package')


    # Create a sample MongoDB connection file in app/models/mongo.py
    mongo_content = """from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from AppConfig import AppConfig
import time
import os
# from pubSub import PubSub


class mongoDb:

    def __init__(self):
    
        if AppConfig().getEnvironment() == 'cloudprod':
            uri = os.getenv('MONGO_URI_ACCOUNTING')
            
            if uri is None:
                raise Exception(
                    'MONGO_URI_ACCOUNTING environment variable is not set')

            self.client = MongoClient(uri,
                                      server_api=ServerApi('1'),
                                      tz_aware=True)
            databaseName = ''
        if AppConfig().getEnvironment() == 'clouddev':
            uri = "mongodb+srv://ladia123:Bigreddog12.@cluster0.pgvpdb1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            self.client = MongoClient(uri,
                                      server_api=ServerApi('1'),
                                      tz_aware=True)
            databaseName = ''

        # testEnvironment is used for automated testing while the actual is used for production / development
        if AppConfig().getEnvironment() == 'localdev':
            self.client = MongoClient('localhost', 27017, tz_aware=True)
            databaseName = 'testEmployeeProfile'
        if AppConfig().getEnvironment() == 'localTest':
            self.client = MongoClient('localhost', 27017, tz_aware=True)
            databaseName = 'testEmployeeProfile'
        if AppConfig().getEnvironment() == 'localprod':
            self.client = MongoClient('localhost', 27017, tz_aware=True)
            databaseName = 'testEmployeeProfile'

        self.db = self.client[databaseName]

    def ping(self):
        try:
            start_time = time.time()  # get current time
            self.client.admin.command('ping')
            end_time = time.time()  # get current time after ping

            elapsed_time = end_time - start_time  # calculate elapsed time
            elapsed_time_ms = elapsed_time * 1000  # convert to milliseconds

            print(
                "Pinged your deployment. You successfully connected to MongoDB! Response time: %f ms"
                % elapsed_time_ms)
            return elapsed_time_ms
        except Exception as e:
            print(e)

    def create(self, data, collection_name, session=None):
        # Insert a document into the collection and return the created data.
        print("Creating data in collection: " + collection_name +
              " with data: " + str(data))
        start_time = time.time()  # get current time
        result = self.db[collection_name].insert_one(data, session=session)
        end_time = time.time()  # get current time after ping

        elapsed_time = end_time - start_time  # calculate elapsed time
        elapsed_time_ms = elapsed_time * 1000  # convert to milliseconds

        print(collection_name + " Response time: %f ms" % elapsed_time_ms)
        return self.db[collection_name].find_one({"_id": result.inserted_id},
                                                 session=session)

    def read(self, query, collection_name, projection={}, session=None,findOne=False, count=False):
        # Read documents from the collection.
        start_time = time.time()  # get current time

        if findOne:
            data = self.db[collection_name].find_one(query, projection, session=session)
        else:
            data = list(self.db[collection_name].find(query,
                                                    projection,
                                                    session=session))
        end_time = time.time()  # get current time after ping

        elapsed_time = end_time - start_time  # calculate elapsed time
        elapsed_time_ms = elapsed_time * 1000  # convert to milliseconds

        print(collection_name + ' ' + str(query) +
              " Response time: %f ms" % elapsed_time_ms)
        return data

    def readWithPagination(self,
                           query,
                           collection_name,
                           page,
                           limit,
                           projection={},
                           sort={
                               'keyToSort': None,
                               'sortOrder': None
                           },
                           reverse=False,
                           session=None):

        # add validations for page and limit
        if limit == None or limit < 1:
            if page > 1:
                raise ValueError(
                    "Page must be 1 if limit is None or less than 1")
        # Read documents from the collection with pagination.
        start_time = time.time()  # get current time

        # Get the total number of documents matching the query
        totalDocuments = self.db[collection_name].count_documents(query)

        #set limit to total document if limit == None
        if limit is None:
            limit = totalDocuments  # or any sensible large number

        # Create the MongoDB query
        cursor = self.db[collection_name].find(query,
                                               projection,
                                               session=session)

        if reverse:
            cursor = cursor.sort([('$natural', -1)])

        # Apply sorting if keyToSort is provided
        if sort['keyToSort'] and sort['sortOrder'] != 0:
            cursor = cursor.sort(sort['keyToSort'], sort['sortOrder'])

        # Calculate the number of documents to skip
        skip = (page - 1) * limit
        # Apply skip and limit for pagination AFTER sorting
        cursor = cursor.skip(skip).limit(limit)

        # Retrieve the documents
        data = list(cursor)

        # Calculate total pages
        if totalDocuments == 0:
            totalPages = 0
        else:
            totalPages = (totalDocuments + limit - 1) // limit

        end_time = time.time()  # get current time after query

        elapsed_time = end_time - start_time  # calculate elapsed time
        elapsed_time_ms = elapsed_time * 1000  # convert to milliseconds

        print(collection_name + ' ' + str(query) +
              " Response time: %f ms" % elapsed_time_ms)

        # Return the paginated data along with pagination metadata
        return {
            'data': data,
            'page': page,
            'limit': limit,
            'totalDocuments': totalDocuments,
            'totalPages': totalPages
        }

    def update(self,
               query,
               new_values,
               collection_name,
               checkVersion=False,
               incrementVersion=True,
               session=None):
        # Update documents in the collection.
        print('Updating data in collection: ' + collection_name +
              ' with query: ' + str(query) + ' and new values: ' +
              str(new_values))

        if checkVersion:
            latestData = self.db[collection_name].find_one(
                {
                    '_id': query['_id'],
                    '_version': query['_version']
                },
                session=session)
            if latestData is None:
                raise Exception(
                    'Your data is outdated. Please refresh the page and try again.'
                )
        else:
            latestData = self.db[collection_name].find_one(
                {'_id': query['_id']}, session=session)

        newVersion = latestData['_version'] + 1
        oldVersion = newVersion - 1
        new_values['_version'] = newVersion

        # we update the query with the new version
        if checkVersion == True:
            query['_version'] = oldVersion
        else:
            if '_version' in query:
                query.pop('_version')

        def find_instance(d, o, path=""):
            if isinstance(d, dict):
                for key, value in d.items():
                    current_path = f"{path}.{key}" if path else key  # Construct the current path

                    if isinstance(value, dict):
                        # Recursively check nested dictionaries
                        found, instance_path = find_instance(
                            value, o, current_path)
                        if found:
                            print('object detected', instance_path)
                    elif isinstance(value, list):
                        # Recursively check nested lists
                        for i, item in enumerate(value):
                            found, instance_path = find_instance(
                                item, o, f"{current_path}[{i}]")
                            if found:
                                print('object detected', instance_path)
                    elif isinstance(value, o):
                        # Return True and the path if a value is an instance of the specified class
                        print('object detected', current_path)

            elif isinstance(d, list):
                for i, item in enumerate(d):
                    found, instance_path = find_instance(
                        item, o, f"{path}[{i}]")
                    if found:
                        print('object detected', instance_path)

            # Return False and an empty string if no instance of the class is found
            return False, ""

        # from objects import Unit
        # find_instance(new_values, Unit)

        if incrementVersion == False:
            new_values.pop('_version')

        result = self.db[collection_name].update_many(query, {
            '$set': new_values,
        },
                                                      session=session)

        if incrementVersion == True:
            if result.modified_count == 0:
                raise ValueError("No documents were modified.")

        if checkVersion == True:
            query.pop('_version')

        updatedData = self.read(query, collection_name, session=session)
        return updatedData

    def delete(self, query, collection_name, session=None):
        # Delete documents from the collection.
        print('Deleting data in collection: ' + collection_name +
              ' with query: ' + str(query))

        if query == {} and AppConfig().getIsProductionEnvironment():
            raise Exception(
                'You cannot delete all documents in the collection in production environment'
            )

        deleted_result = self.db[collection_name].delete_many(query,
                                                              session=session)

        if deleted_result.deleted_count > 0:
            return deleted_result.deleted_count
        else:
            return 'No document to delete'

    def getAllCollections(self):
        # Get all collections in the database.
        return self.db.list_collection_names()

    def deleteAllDataInDatabaseForDevEnvironment(self):
        # Delete all documents from the collection. Only works in the dev environment

        if not AppConfig().getIsDevEnvironment():
            raise Exception(
                'This function is only available in the localdev environment')

        allCollections = self.getAllCollections()
        for x in allCollections:
            self.db[x].delete_many({})

    def createTransaction(self, updateFunction, pubSubMessage=None):
        if AppConfig().getIsCloudEnvironment():
            with self.client.start_session() as session:
                with session.start_transaction():
                    try:
                        res = updateFunction(session)
                        # Commit the transaction

                        if pubSubMessage is not None:
                            topic = pubSubMessage['topic']
                            message = pubSubMessage['message']
                            PubSub().publishMessage(topic, message)

                        session.commit_transaction()
                        print("Transaction committed successfully.")
                        return res
                    except Exception as e:
                        print("Transaction aborted due to an error:", e)
                        # Abort the transaction
                        session.abort_transaction()
        else:
            res = updateFunction(None)
            return res

    def getAllCollectionNames(self):
        # Get all collections in the database.
        return self.db.list_collection_names()


if __name__ == '__main__':
    mongoDb().ping()
    pass

"""
    with open(os.path.join(project_name, 'mongoDb.py'), 'w') as f:
        f.write(mongo_content)

    # create an objects file
    objects_content = """# add your objects here

"""
    with open(os.path.join(project_name, 'objects.py'), 'w') as f:
        f.write(objects_content)

    # Create a basic test file in the tests folder
    test_content = """import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    rv = client.get('/')
    assert rv.data == b"Hello, World!"
"""
    with open(os.path.join(project_name, 'test_functions.py'), 'w') as f:
        f.write(test_content)

    # Create README.md with basic instructions
    readme_content = f"# {project_name}\n\nA simple Flask server template with MongoDB integration."
    with open(os.path.join(project_name, 'README.md'), 'w') as f:
        f.write(readme_content)

    print(f"Project {project_name} created successfully!")

if __name__ == '__main__':
    project_name = input("Enter the project name: ")
    create_server_project(project_name)
