import os
shared_variable = None
env_variable = None

def set_shared_variable(config_file):
    global shared_variable
    shared_variable = config_file

def set_shared_env(env):
    global env_variable
    env_variable = env

def set_config(config_file):
    os.environ["cmhlims.lims_config_yaml"] = config_file

def get_config():
    return os.getenv("cmhlims.lims_config_yaml")

def set_environment(environment):
    os.environ["environment"] = environment

def get_environment():
    return os.environ["environment"]