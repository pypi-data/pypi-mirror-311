import os

def create_objects_file(project_name):
    objects_content = """# add your objects here

"""
    with open(os.path.join(project_name, 'objects.py'), 'w') as f:
        f.write(objects_content)