import os
from create_server_app import mongoDb, AppConfig, app, requirements, objects, test_functions

def create_server_project(project_name):
    # Define the directory structure for the project
    dirs = [
        project_name
    ]
    # Create directories
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

    # Create the app.py file
    app.create_app_routes(project_name)

    # create an AppConfig for the project
    AppConfig.create_app_config(project_name)

    # create a requirements file
    requirements.create_requirements_file(project_name)

    # create a mongoDb file
    mongoDb.create_mongoDb(project_name)

    # create an objects file
    objects.create_objects_file(project_name)

    # Create a basic test file in the tests folder
    test_functions.create_test_functions_file(project_name)

    # Create README.md with basic instructions
    readme_content = f"# {project_name}\n\nA simple Flask server template with MongoDB integration."
    with open(os.path.join(project_name, 'README.md'), 'w') as f:
        f.write(readme_content)

    print(f"Project {project_name} created successfully!")

if __name__ == '__main__':
    project_name = input("Enter the project name: ")
    create_server_project(project_name)
