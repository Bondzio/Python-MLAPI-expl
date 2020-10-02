# This utility script uploads a given set of files as a dataset using Kaggle API
# Initialize with init_on_kaggle(username, api_key) on Kaggle.
# On a local system, this can be used with the same info stored in ~/.kaggle/kaggle.json file, from which the Kaggle CLI tools look for it.
# call create() to create the dataset if it does not exist.
# call update() to update the dataset if it exists.
# currently create/update needs to be done manually as I have not found support to check if dataset exists.
#
# example use:
#
# from kaggle_secrets import UserSecretsClient
#
# user_secrets = UserSecretsClient()
# api_secret = user_secrets.get_secret("kaggle api key")
#
# kaggle_uploader.resources = []
# kaggle_uploader.init_on_kaggle("donkeys", api_secret)
# kaggle_uploader.base_path = "./upload_dir"
# kaggle_uploader.title = "COVID NLP Preprocessed"
# kaggle_uploader.dataset_id = "covid-nlp-preprocess"
# kaggle_uploader.user_id = "donkeys"
# kaggle_uploader.add_resource("output.zip", "zipped preprocessing data")
# kaggle_uploader.update("new version")
#
# Description of above lines:
# resources = []: Initializes the list of dataset resources as empty list.
#    This is necessary, for example, if you run the same cell multiple times as otherwise
#    multiple calls to add_resource() would keep adding to the list multiple times, even if not the intent.
# base_path = "...": Kaggle CLI expects a single directory that contains all files for your dataset and nothing else.
#    This path should define that directory. Can be relative or absolute, the script converts it to absolute.
#    Script will also generate a Kaggle metadata JSON file in this directory as needed by Kaggle CLI.
# title:          Your dataset title.
# dataset_id:     A unique id (under your account) for this dataset. Kaggle API calls this the "slug".
# user_id:        Your Kaggle account id. The final dataset ID becomes user_id/dataset_id as generated by this script.
# add_resource(): Defines what files in base_dir are part of the dataset. Filename and its description.
# update():       Update an existing dataset. Will fail if the dataset does not exist on Kaggle.
# create():       Create a new dataset. Will fail if one with the same metadata already exists.

#some useful links on the topic:
#https://www.kaggle.com/paultimothymooney/exploring-the-kaggle-api
#https://www.kaggle.com/docs/api
#https://github.com/Kaggle/kaggle-api#create-a-new-dataset
#https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata

import json
import subprocess
import os
from shutil import copyfile
import string
from typing import List, Tuple

# version history:
# 0.3.0 change to use API credentials passed in as string. expect user to store them in Kaggle secrets API
# 0.2.0 used copying the API credentials from given filepath to ~/.kaggle/kaggle.json. Assuming path is to private dataset with credentials file.

__version__ = "0.3.0"

base_path:str = None
user_id:str = None
dataset_id:str = None #called "the slug" in kaggle API
title:str = None
licenses:List[dict] = [{"name": "CC0-1.0"}] #default value
subtitle:str = None
description:str = None
resources:List[Tuple] = []

def reset():
    global resources
    resources = []

def init_on_kaggle(username, api_key):
    global resources
    resources = []
    KAGGLE_CONFIG_DIR = os.path.join(os.path.expandvars('$HOME'), '.kaggle')
    os.makedirs(KAGGLE_CONFIG_DIR, exist_ok = True)
    api_dict = {"username":username, "key":api_key}
    with open(f"{KAGGLE_CONFIG_DIR}/kaggle.json", "w", encoding='utf-8') as f:
        json.dump(api_dict, f)
    cmd = f"chmod 600 {KAGGLE_CONFIG_DIR}/kaggle.json"
    output = subprocess.check_output(cmd.split(" "))
    output = output.decode(encoding='UTF-8')
    print(output)

def exec_command(cmd):
    try:
        output = subprocess.check_output(cmd.split(" "))
    except subprocess.CalledProcessError as e:
        print(f"error code: {e.returncode}")
        raise Exception(e.output.decode(encoding = 'UTF-8'))
    output = output.decode(encoding = 'UTF-8')
    print(output)

def add_resource(path, description):
    global base_path
    assert base_path is not None, f"base_path must be set before adding resourcse. current: {base_path}"
    base_path = os.path.abspath(base_path)
    print(base_path)
    resources.append({"path": f"{base_path}/{path}", "description": description})

def validate_metadata() -> (bool, str):
    valid = True
    error_msg = ""
    if base_path is None:
        error_msg += "kaggle_uploader: base_path is not set, cannot proceed.\n"
        valid = False
    if user_id is None:
        error_msg += "kaggle_uploader: user_id is not set, cannot proceed.\n"
        valid = False
    #kaggle calls the dataset_id "slug"
    valid_slug_chars = string.ascii_letters+"-0123456789"
    if dataset_id is None:
        error_msg += "kaggle_uploader: dataset_id is not set, cannot proceed.\n"
        valid = False
    #https://stackoverflow.com/questions/26703664/check-if-a-string-contains-only-given-characters
    elif any(c not in valid_slug_chars for c in dataset_id):
        error_msg += "kaggle_uploader: dataset_id contains invalid chars. only a-zA-Z and - allowed. Cannot proceed.\n"
        valid = False
    if title is None:
        error_msg += "kaggle_uploader: title is not set, cannot proceed.\n"
        valid = False
    if len(resources) == 0:
        #could also check properties of the resource definitions but leave something for the user..
        error_msg += "kaggle_uploader: no resource to upload defined, cannot proceed.\n"
        valid = False
    if len(error_msg) > 0:
        print(error_msg)

    return valid,error_msg

def create_metadata() -> dict:
    valid, error_msg = validate_metadata()
    if not valid:
        raise Exception(f"Invalid metadata: {error_msg}")

    metadata = {
        "title": title,
        "id": f"{user_id}/{dataset_id}",
        "licenses": licenses,
        "resources": resources
    }
    if subtitle is not None:
        metadata["subtitle"] = subtitle
    if description is not None:
        metadata["description"] = description
    return metadata

def write_metadata(metadata):
    with open(f'{base_path}/dataset-metadata.json', 'w') as f:
        json.dump(metadata, f)

# Create dataset-specific JSON metadata file and run uploader for new dataset
def create() -> dict:
    metadata = create_metadata()
    if metadata is None:
        print("invalid metadata, exiting")
        raise Exception("invalid metadata")

    write_metadata(metadata)
    cmd = f"kaggle datasets create -p {base_path}"
    exec_command(cmd)
    return metadata

# Create dataset-specific JSON metadata file and run uploader for existing dataset
def update(update_msg:str = None) -> dict:
    if update_msg is None:
        update_msg = "new version"
    metadata = create_metadata()
    if metadata is None:
        print("invalid metadata, exiting")
        raise Exception("invalid metadata")

    write_metadata(metadata)
    cmd = f'kaggle datasets version -p {base_path} -m'
    cmd_strings = cmd.split(" ")
    cmd_strings.append(f'"{update_msg}"')
    print(f"running cmd:{cmd_strings}")
    output = subprocess.check_output(cmd_strings)
    output = output.decode(encoding='UTF-8')
    print(output)
    return metadata

