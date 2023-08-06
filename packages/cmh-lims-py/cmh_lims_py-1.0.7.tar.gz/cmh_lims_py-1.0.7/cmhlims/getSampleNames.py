import pymysql
import connectToLIMS as cl

def get_sample_names():
    config_file = '/Users/mkumar1/Desktop/cmhlims_py/database.yml'
    environment = 'production'  # The desired LIMS environment from the config file
    lims_db = cl.connect_to_lims(config_file, environment)
    #lims_db = connect_to_lims()

    try:
        with lims_db.cursor() as cursor:
            samples_query = "select label from samples;"
            cursor.execute(samples_query)
            sample_names = [row[0] for row in cursor.fetchall()]
    finally:
        lims_db.close()

    return sample_names

def connect_to_lims():
    lims_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database'
    }

    lims_db = pymysql.connect(**lims_config)

    return lims_db

if __name__ == '__main__':
    out = get_sample_names()
    print(out)