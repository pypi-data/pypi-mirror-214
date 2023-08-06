import yaml
import pymysql
import configparser
import os

def connect_to_lims(config=None, environment=None):
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(os.path.join(os.path.dirname(__file__), 'config.ini'))

    config_file = config.get('shared', 'config_file')
    #config_file=os.path.join(os.path.dirname(__file__), config_file)
    print(os.path.dirname(__file__))
    environment = config.get('shared', 'environment')

    '''
    print("------------------")
    print(config_file)
    print(environment)
    print("------------------")
    '''

    if config_file is None or environment is None:
        raise ValueError("Options cmhlims.lims_config_yaml and cmhlims.lims_environment must be set before using cmhlims functions.")

    with open(config_file, 'r') as file:
        lims_config = yaml.safe_load(file)

    if environment not in lims_config:
        raise ValueError("LIMS environment not found in configuration YAML: " + environment)

    lims_config = lims_config[environment]

    db_con = pymysql.connect(
        user=lims_config['username'],
        password=lims_config['password'],
        host=lims_config['host'],
        database=lims_config['database'],
        ssl_ca=lims_config['sslca'],
        autocommit=True
    )

    '''
    cur = db_con.cursor()
    sql = 'SELECT * FROM samples LIMIT 10'
    cur.execute(sql)
    results = cur.fetchall()
    db_con.close()

    for result in results:
        print(result)
    '''

    return db_con

if __name__ == '__main__':

    try:
        db_connection = connect_to_lims()
        print("Connection successful!")
    except Exception as e:
        print("An error occurred:", str(e))