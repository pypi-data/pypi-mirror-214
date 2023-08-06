import pymysql
import pandas as pd
import cmhlims.connectToLIMS as cl

def get_analyses(sample_names, reference_genome):
    print(reference_genome)
    if len(reference_genome) != 1:
        raise ValueError("getAnalyses() supports only a single reference genome")
  
    if len(sample_names) == 0:
        raise ValueError("getAnalyses() requires at least one sample name")

    analysis_query_template = """select s.label as sample_name,
        a.id as analysis_id,
        a.label as analysis_name,
        a.base_dir as analysis_dir,
        a.analysis_date as analysis_date,
        q.label as sequence_type,
        t.label as analysis_type,
        r.label as reference_genome
        from samples s,
            downstream_analyses a,
            downstream_analysis_types t,
            sequence_types q,
            reference_genomes r
        where s.id = a.sample_id
            and a.sequence_type_id = q.id
            and a.reference_genome_id = r.id
            and a.downstream_analysis_type_id = t.id
            and r.label = '{ref_genome}'
            and s.label IN ({sample_list});"""

    sample_list = "'" + "','".join(sample_names) + "'"
    print("*****")
    print(sample_list)
    print(reference_genome[0])
    print(analysis_query_template)
    print("*****")

    analysis_query = analysis_query_template.format(ref_genome=reference_genome[0], sample_list=sample_list)
    
    #config_file = '/Users/mkumar1/Desktop/cmhlims_py/database.yml'
    #environment = 'production'  # The desired LIMS environment from the config file
    #lims_db = cl.connect_to_lims(config_file, environment)
    lims_db = cl.connect_to_lims()

    try:
        with lims_db.cursor() as cursor:
            cursor.execute(analysis_query)
            print("^^^^^")
            print(analysis_query)
            print("^^^^^")
            columns = [column[0] for column in cursor.description]
            analyses_data = cursor.fetchall()
            analyses_df = pd.DataFrame(analyses_data, columns=columns)
    finally:
        lims_db.close()

    return analyses_df

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
    out=get_analyses(["cmh000514"], ["GRCh38"])

    print(out)