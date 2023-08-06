import pymysql
from cmhlims.connectToLIMS import connect_to_lims

def get_sample_names():
    lims_db = connect_to_lims()

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



if __name__ == '__main__':
    out = get_sample_names()
    print(out)