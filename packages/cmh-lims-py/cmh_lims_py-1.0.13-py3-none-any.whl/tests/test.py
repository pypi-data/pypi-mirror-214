import yaml
import pymysql

lims_config_yaml = '/Users/mkumar1/Desktop/cmhlims_py/database.yml'

with open(lims_config_yaml, 'r') as f:
  config = yaml.safe_load(f)['production']
  print(config)

print(list(config.keys()))

# Connect to LIMS
con = pymysql.connect(host        = config['host'],
                      user        = config['username'],
                      password    = config['password'],
                      db          = config['database'],
                      ssl_ca      = config['sslca']
                      #,cursorclass = pymysql.cursors.DictCursor
                      )

cur = con.cursor()
sql = 'SELECT * FROM samples LIMIT 10'
cur.execute(sql)
results = cur.fetchall()
con.close()

for result in results:
  print(result)