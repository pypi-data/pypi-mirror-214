import yaml
import pymysql

def connect_to_lims(config=None, environment=None):
    if config is None or environment is None:
        raise ValueError("Options cmhlims.lims_config_yaml and cmhlims.lims_environment must be set before using cmhlims functions.")

    with open(config, 'r') as file:
        lims_config = yaml.safe_load(file)

    if environment not in lims_config:
        raise ValueError("LIMS environment not found in configuration YAML: " + environment)

    lims_config = lims_config[environment]
    print(lims_config)
    db_con = pymysql.connect(
        user=lims_config['username'],
        password=lims_config['password'],
        host=lims_config['host'],
        database=lims_config['database'],
        #ssl={'ca': lims_config['sslca']},
        ssl_ca=lims_config['sslca']
        ,autocommit=True
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
    config_file = '/Users/mkumar1/Desktop/cmhlims_py/database.yml'
    environment = 'production'  # The desired LIMS environment from the config file

    try:
        db_connection = connect_to_lims(config_file, environment)
        print("Connection successful!")
    except Exception as e:
        print("An error occurred:", str(e))