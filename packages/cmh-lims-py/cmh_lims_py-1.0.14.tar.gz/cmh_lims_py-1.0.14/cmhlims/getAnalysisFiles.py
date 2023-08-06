import pymysql
import pandas as pd
from cmhlims.connectToLIMS import connect_to_lims


def get_analysis_files(analysis_ids):
    if len(analysis_ids) == 0:
        raise ValueError("getAnalysisFiles() requires at least one analysis_id")

    files_query_template = """select f.file_path as file_path,
        a.id as analysis_id,
        t.label as file_type_label,
        t.abbrev as file_type_abbrev
        from downstream_analysis_files f,
            downstream_analysis_file_types t,
            downstream_analyses a
        where a.id = f.downstream_analysis_id
            and f.downstream_analysis_file_type_id = t.id
            and a.id IN ({analysis_ids_list});"""


    analysis_ids_list = ",".join(str(analysis_id) for analysis_id in analysis_ids)
    print("%%%%%%")
    print(analysis_ids_list)
    print("%%%%%%")
    files_query = files_query_template.format(analysis_ids_list=analysis_ids_list)


    #db_con = cl.connect_to_lims(config_file, environment)
    #print(sv.set_shared_variable())
    #db_con = cl.connect_to_lims(sv.shared_variable, sv.env_variable)
    db_con = connect_to_lims()

    try:
        with db_con.cursor() as cursor:
            cursor.execute(files_query)
            columns = [column[0] for column in cursor.description]
            files_data = cursor.fetchall()
            files_df = pd.DataFrame(files_data, columns=columns)
    finally:
        db_con.close()

    return files_df

if __name__ == '__main__':
    out=get_analysis_files(["2287"])
    print(out)
