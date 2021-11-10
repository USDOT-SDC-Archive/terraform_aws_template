import logging
import shlex
import subprocess
import sys
import zipfile
import boto3
from botocore.exceptions import ClientError
import os
import yaml
from pprint import pprint

region_name = 'us-east-1'


def get_env():
    client = boto3.client('ssm', region_name=region_name)
    response = client.get_parameter(Name='environment')
    return response['Parameter']['Value']


def get_terraform_bucket():
    return get_env() + '.sdc.dot.gov.platform.terraform'


def get_lambdas():
    lambdas_paths = []
    lambdas_ = {}
    for path, sub_dirs, files in os.walk(os.getcwd()):
        for x in files:
            if x == "lambdas.yaml":
                lambdas_paths.append(os.path.join(os.path.relpath(path, start=os.curdir), x))
                lambdas_path = os.path.join(os.path.relpath(path, start=os.curdir), x)
                with open(lambdas_path, "r") as stream:
                    try:
                        lambdas_.update(yaml.safe_load(stream))
                    except yaml.YAMLError as exc:
                        print(exc)
                        sys.exit()
    for l_name_, l_values_ in lambdas_.items():
        path_ = os.path.normpath(l_values_['path'])
        l_values_['path'] = path_
        module_ = path_.split(os.sep)[1:-2]
        if not module_:
            module_ = ''
        else:
            module_ = '/'.join(module_) + '/'
        l_values_['module'] = module_

    return lambdas_


def zip_dir(zip_path, zip_handle):
    for root, dirs_, files in os.walk(zip_path):
        for file in files:
            zip_handle.write(os.path.join(root, file),
                             os.path.relpath(os.path.join(root, file),
                                             os.path.join(zip_path, '..')))


def upload_file(file_name, bucket, key=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param key: S3 key. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if key is None:
        key = file_name
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").replace("\n", '').replace("\r", ''))
    rc = process.poll()
    return rc


def get_dirs():
    # some directories
    if os.name == 'nt':
        bin_dir = 'Scripts'
        lib_dir = 'Lib'
    else:
        bin_dir = 'bin'
        lib_dir = 'lib/python3.8'
    repo_dir = os.path.split(os.getcwd())[-1]
    return {'bin': bin_dir, 'lib': lib_dir, 'repo': repo_dir}


# must run Python 3.8.x
if not (sys.version_info.major == 3 and sys.version_info.minor == 8):
    raise EnvironmentError("Python must be version 3.8.x")

# get the environment
env = get_env()

# load the deployment vars
lambdas = get_lambdas()

# get the bucket where we will put the zip files
terraform_bucket = get_terraform_bucket()

# get the bin/scripts dirs
dirs = get_dirs()

# ask user to verify
print('================================================================================')
print(f"Do you want to build the Lambda deployment packages for {env}?")
print("Only 'yes' will be accepted to approve.")
input_str = input(f"Process Lambdas for {env}: ").lower()
if input_str != "yes":
    print("Aborted")
    sys.exit()

# ask if we should build/rebuild the venvs
print('================================================================================')
rebuild = True
print(f"Do you want to build/rebuild the virtual environments?")
print("Only 'yes' will be accepted to build/rebuild, all other will skip.")
input_str = input(f"Build or rebuild the virtual environments: ").lower()
if input_str != "yes":
    rebuild = False
    print("Skipped")
print('================================================================================')
print('')

print('Processing...')

if rebuild:
    for l_name, l_values in lambdas.items():
        print('================================================================================')
        # create virtual environment
        print(l_values['path'] + ': Creating virtual environment...')
        subprocess.check_call([sys.executable, "-m", "venv", "--copies", "--clear", os.path.join(l_values['path'], "venv")])
        print(l_values['path'] + ': Creating virtual environment...Done')
        path_to_executable = os.path.join(os.getcwd(), l_values['path'], "venv", dirs['bin'], "python")
        path_to_requirements = os.path.join(os.getcwd(), l_values['path'], "requirements.txt")
        # upgrade pip
        print('--------------------------------------------------------------------------------')
        print(l_values['path'] + ': Upgrading pip...')
        subprocess.check_call([path_to_executable, "-m", "pip", "install", "--upgrade", "pip"])
        print(l_values['path'] + ': Upgrading pip...Done')
        # upgrade setuptools
        print('--------------------------------------------------------------------------------')
        print(l_values['path'] + ': Upgrading setuptools...')
        subprocess.check_call([path_to_executable, "-m", "pip", "install", "--upgrade", "setuptools"])
        print(l_values['path'] + ': Upgrading setuptools...Done')
        # install requirements.txt
        print('--------------------------------------------------------------------------------')
        print(l_values['path'] + ': Installing requirements...')
        subprocess.check_call([path_to_executable, "-m", "pip", "install", "-r", path_to_requirements, "--upgrade"])
        print(l_values['path'] + ': Installing requirements...Done')
        print('================================================================================')
        print('')
else:
    print('================================================================================')
    for l_name, l_values in lambdas.items():
        # don't create virtual environment
        print(l_values['path'] + ': Using the existing virtual environment...')
    print('================================================================================')
    print('')

# zip up the scripts and site packages
for l_name, l_values in lambdas.items():
    print('================================================================================')
    print(l_values['path'])
    print('--------------------------------------------------------------------------------')
    print('Creating zip file...')
    path_to_site_packages = os.path.join(l_values['path'], "venv", dirs['lib'], "site-packages")
    zip_file = os.path.join(l_values['path'], l_name + '.zip')
    with zipfile.ZipFile(zip_file, 'w') as lambda_zip:
        if 'scripts' in l_values.keys():
            for script in l_values['scripts']:
                path_to_script = os.path.join(l_values['path'], script)
                print('Zipping script: ' + script)
                lambda_zip.write(path_to_script, arcname=script)
        if 'site-packages' in l_values.keys():
            for site_package in l_values['site-packages']:
                path_to_site_package = os.path.join(path_to_site_packages, site_package)
                print('Zipping site-package: ' + site_package)
                zip_dir(path_to_site_package, lambda_zip)
    lambda_zip.close()
    print('Creating zip file...Done')

    # upload the zip file
    print('Uploading ')
    print('   from: ' + zip_file)
    print('     to: s3://' + terraform_bucket + '/' + dirs['repo'] + '/lambdas/' + l_values['module'] + l_name + '.zip')
    if upload_file(
            file_name=zip_file,
            bucket=terraform_bucket,
            key=dirs['repo'] + '/lambdas/' + l_values['module'] + l_name + '.zip'):
        print('Uploading...Done')
    else:
        print('Error uploading ' + l_name + '.zip')
    print('================================================================================')
    print('')

print('Processing...Done')
