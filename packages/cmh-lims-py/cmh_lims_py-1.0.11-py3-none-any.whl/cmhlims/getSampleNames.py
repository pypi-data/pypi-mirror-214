import pymysql
import cmhlims.connectToLIMS as cl

def get_sample_names():
    lims_db = cl.connect_to_lims()

    try:
        with lims_db.cursor() as cursor:
            samples_query = "select label from samples;"
            print("Before executing query")
            cursor.execute(samples_query)
            print("After executing query")
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