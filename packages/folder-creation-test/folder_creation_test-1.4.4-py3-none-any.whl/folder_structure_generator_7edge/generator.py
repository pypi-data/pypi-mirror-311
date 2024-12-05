import os
import yaml
from InquirerPy import inquirer
import shutil
import importlib.resources  # For locating resources in the installed package

def create_dynamodb_table_configuration(table_name, partition_key, sort_key):
    """
    Dynamically creates the DynamoDB table configuration with the given keys and LSIs.
    
    :param table_name: Name of the DynamoDB table
    :param partition_key: Partition key for the DynamoDB table
    :param sort_key: Sort key for the DynamoDB table
    :param lsi_keys: List of tuples containing LSI name and sort key
    :return: The DynamoDB table configuration as a dictionary
    """
    # Create the table's primary key schema and attributes
    table_config = {
        table_name: {
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": table_name,
                "AttributeDefinitions": [
                    {"AttributeName": partition_key, "AttributeType": "S"},
                    {"AttributeName": sort_key, "AttributeType": "S"}
                ],
                "KeySchema": [
                    {"AttributeName": partition_key, "KeyType": "HASH"},
                    {"AttributeName": sort_key, "KeyType": "RANGE"}
                ],
                "BillingMode": "PAY_PER_REQUEST",
                "LocalSecondaryIndexes": []
            }
        }
    }

    
    return table_config


def create_folder_structure_with_files():
    """
    Creates a folder structure in the current working directory and copies all files 
    from the source folder into the newly created structure.

    :param source_folder: The path to the folder containing the files to copy.
    """
    try:
        base_package_path = importlib.resources.files('folder_structure_generator_7edge')

        source_folder = f"{base_package_path}/backend_folder"  # Replace with the actual path

        # Define the root directory (current working directory)
        target_folder = os.getcwd()
        
        os.makedirs(f"{target_folder}/services", exist_ok=True)
        os.makedirs(f"{target_folder}/runbooks", exist_ok=True)



        # Copy all files from the source folder into the target folder
        if os.path.exists(source_folder):
            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print("Folders created. Please navigate to the service folder and run the 'create' command to set up a new service.")
        else:
            print(f"Source folder '{source_folder}' does not exist.")
    
    except Exception as e:
        print(f"An error occurred while creating the folder structure: {e}")



# Function to create necessary directories
def create_directories(folders):
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

# Function to create handler files with boilerplate content
def create_handler_files(base_dir, handler_files, language_choice, file_extension):
    for file_name in handler_files:
        file_path = os.path.join(base_dir, "handlers", f"{file_name}.{file_extension}")
        content = ""

        if language_choice == "Python":
            content = """import json
import boto3
from marshmallow import Schema, fields, ValidationError
from lib.helper import headers



# Define Marshmallow schema
class InputSchema(Schema):
    field1 = fields.Str(required=True)  # Example field, replace with your actual field
    field2 = fields.Int(required=True)  # Example field, replace with your actual field
    # Add your own fields here

def handler(event, context):
    try:
        # Log the event
        print('Event:', json.dumps(event))

        # Parse and validate request body
        body = json.loads(event.get('body', '{}'))

        try:
            schema = InputSchema()
            validated_data = schema.load(body)
        except ValidationError as err:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps(
                    {
                        "success_status": False,
                        "message": next(iter(err.messages.values()))[0],
                    }
                ),
            }

        # Business logic goes here
        print('Validated data:', validated_data)

        return {
            'statusCode': 200,
            "headers": headers,

            'body': json.dumps({ "success_status": True, 'message': 'Success'})
        }

    except Exception as error:
        print('Error:', error)
        return {
            'statusCode': 500,
            "headers": headers,

            'body': json.dumps({"success_status": False, 'message': 'There was an error while creating the template'})
        }
"""
        else:
            content = """const AWS = require('aws-sdk')
const Joi = require('joi');
const helpers = require('./lib/helper');  // Import the entire helper.js file



/**
 * AWS Lambda handler function
 * @param {Object} event - Lambda event object
 * @param {Object} context - Lambda context object
 * @returns {Object} Lambda response
 */

 // Define Joi validation schema
const schema = Joi.object({
    field1: Joi.string().required(), // Example field, replace with your actual field
    field2: Joi.number().required(), // Example field, replace with your actual field
    // Add your own fields here
});


module.exports.handler = async (event, context) => {
    try {
        console.log('Event:', JSON.stringify(event))

        // Parse and validate request body
        const body = JSON.parse(event.body);
        const validationResult = schema.validate(body)
        if (validationResult.error) {
            const errorMessage = (validationResult.error.details[0].type === 'object.unknown') ? 'Please fill in all the mandatory fields' : validationResult.error.message
            return {
                statusCode: 400,
                headers: helpers.headers(),
                body: JSON.stringify({ message: errorMessage }),
            }
        }

        return {
            statusCode: 200,
            headers: helpers.headers(),
            body: JSON.stringify({ success_status: true, message: 'Success' })
        }

    } catch (error) {
        console.error('Error:', error)
        return {
            statusCode: 500,
            headers: helpers.headers(),
            body: JSON.stringify({ success_status: false, message: 'There was an error while creating the template' })
        }
    }
}
"""
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Created file: {file_path}")

# Function to process template files and replace placeholders
def process_templates(template_files, base_dir, service_name, runtime, dynamodb_config= None):
    for template_name, template_path in template_files.items():
        output_file = template_name.replace('-template', '').replace('swagger', f"{service_name.strip()}-swagger")
        subfolder = "docs" if any(x in template_name for x in ["swagger", "hooks", "dredd"]) else ""
        output_path = os.path.join(base_dir, subfolder, output_file)

        try:
            with open(template_path, 'r') as template_file:
                content = template_file.read()


                # If the file is a YAML configuration, handle it differently
                if "serverless" in template_name and template_name.endswith(".yml"):
                    serverless_config_yml = yaml.safe_load(content)
                     # Update YAML content dynamically
                    serverless_config_yml["service"] = service_name.strip()
                    serverless_config_yml["provider"]["runtime"] = runtime
                    if dynamodb_config:
                        # Add the DynamoDB resource to the serverless config
                        if "resources" not in serverless_config_yml:
                            serverless_config_yml["resources"] = {"Resources": {}}
                        serverless_config_yml["resources"]["Resources"].update(dynamodb_config)
                    
                    # Save updated YAML back to the output path
                    with open(output_path, 'w') as file:
                        yaml.dump(serverless_config_yml, file, default_flow_style=False, sort_keys=False)
                else:
                    # For other files, use string replacement
                    content = content.replace("service_name", service_name.strip())
                    if "serverless" in template_name:
                        content = content.replace("run_time", runtime)
                    
                    with open(output_path, 'w') as file:
                        file.write(content)

            print(f"Created file: {output_path}")
        except FileNotFoundError:
            print(f"Template file not found: {template_path}")

# Function to create the .env file
def create_env_file(base_dir):
    env_file_path = f"{base_dir}/.env"
    with open(env_file_path, 'w') as file:
        file.write("""STAGE=dev
DEBUG=true""")
    print(f"Created file: {env_file_path}")

# Function to check and update serverless-compose.yml
def update_serverless_compose(service_name):
    os.chdir("..")
    current_path = os.getcwd()

    compose_file = f'{current_path}/serverless-compose.yml'
    

    print(f"Updating existing {compose_file}...")
    with open(compose_file, 'r') as file:
        compose_data = yaml.safe_load(file) or {}
    

    # Ensure 'services' is initialized as a dictionary
        if 'services' not in compose_data or compose_data['services'] is None:
            compose_data['services'] = {}

    # Add new service to the services section
    service_path = f"services/{service_name.strip()}"
    compose_data['services'][service_name.strip()] = {
        'path': service_path,
        'config': "serverless.yml"
    }
    
    # Write updated data back to the file
    with open(compose_file, 'w') as file:
        yaml.dump(compose_data, file, default_flow_style=False)
    
    print(f"Service {service_name} added to {compose_file}")

def create_service_structure():
    try:
        # get currenct path
        current_path = os.getcwd()
        if not current_path.endswith('services'):
            print("Please navigate to the 'services' folder and try again.")
            return        
        # Get the directory where the generator.py script is located
        base_package_path = importlib.resources.files('folder_structure_generator_7edge')

        # Paths to template files inside the package
        template_files = {
            "dredd-template.yml": base_package_path / "dredd-template.yml",
            "serverless-template.yml": base_package_path / "serverless-template.yml",
            "hooks-template.py": base_package_path / "hooks-template.py",
            "swagger-template.json": base_package_path / "swagger-template.json",
        }

        # Prompt user for the service name
        service_name = inquirer.text(message="Enter the service name:").execute()
        if not service_name.strip():
            print("Error: Service name cannot be empty.")
            return

         # Ask if the user wants to add DynamoDB
        use_dynamodb = inquirer.confirm(message="Do you want to add a DynamoDB table?").execute()
        table_name = None
        partition_key = 'partition_key'  # default partition key
        sort_key = 'sort_key'  # default sort key
        # lsi_count = 0  # Default to no LSI

        if use_dynamodb:
            table_name = inquirer.text(message="Enter the DynamoDB table name:").execute()
            if not table_name.strip():
                print("Error: table name cannot be empty.")
                return
        # # Ask user for partition and sort keys with default values
        # partition_key = "partition_key"  # Define the default value programmatically
        # partition_key_input = inquirer.prompt([{
        #     "type": "input",
        #     "name": "partition_key",
        #     "message": f"Enter the partition key for DynamoDB table (default: {partition_key}):",
        #     "default": partition_key,  # Set the default value
        #     "validate": lambda val: len(val) > 0 or "Partition key cannot be empty",  # Optional validation
        # }])["partition_key"]

        # # If the user doesn't input anything, use the default
        # partition_key = partition_key_input if partition_key_input else partition_key

        # sort_key = inquirer.text(
        #     message=f"Enter the sort key (default: {sort_key}):", 
        #     default=sort_key
        # ).execute()

        # # Ask how many LSIs the user wants to add
        # lsi_count = inquirer.prompt(
        #     [
        #         {
        #             'type': 'number',
        #             'name': 'lsi_count',
        #             'message': 'How many local secondary indexes (LSIs) do you want to add?',
        #             'default': 0
        #         }
        #     ]
        # )['lsi_count']

        # lsi_keys = []
        # for i in range(lsi_count):
        #     # Ask user for LSI details (name and key schema)
        #     lsi_name = inquirer.text(message=f"Enter the name of LSI #{i + 1}:").execute()
        #     lsi_sort_key = inquirer.text(
        #         message=f"Enter the sort key for LSI #{i + 1}:", 
        #         default=f"{lsi_name}_sort_key"
        #     ).execute()
        #     lsi_keys.append((lsi_name, lsi_sort_key))

        # Prompt user for the programming language
        language_choice = inquirer.select(
            message="Select the programming language:",
            choices=["Python", "Node.js"]
        ).execute()

        # Determine file extension and runtime based on language choice
        file_extension = "py" if language_choice == "Python" else "js"
        runtime = 'python3.11' if language_choice == 'Python' else 'nodejs14.x'

        base_path =  f"{current_path}/{service_name.strip()}"

        # Define folder structure
        folders = [
            f"{base_path}/handlers",
            f"{base_path}/docs"
        ]
        
        # Create necessary directories
        create_directories(folders)

        # Handler files
        handler_files = ["add", "list", "view", "update", "delete"]

        # Create handler files with boilerplate content
        create_handler_files(base_path, handler_files, language_choice, file_extension)

        # Dynamically create the DynamoDB table configuration
        if table_name:
            dynamodb_config = create_dynamodb_table_configuration(table_name, partition_key, sort_key)

        # Process template files and replace placeholders
        process_templates(template_files, base_path, service_name, runtime, dynamodb_config=dynamodb_config)

        # Create .env file with environment variables
        create_env_file(base_path)

        # Update serverless-compose.yml
        update_serverless_compose(service_name)

        print("\nService structure generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")




