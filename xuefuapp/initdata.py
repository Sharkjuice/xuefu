#encoding:utf-8
import csv
import pandas as pd
from sqlalchemy import create_engine 
import pdb  
#读取csv文件
csv_file = pd.read_csv('./jingfang.csv',encoding="gbk")
  
#添加newline可以避免一行之后的空格,这样需要在python3环境下运行
#out = open('../../data/capital/2010-Q4','a',newline='')
#csv_write = csv.writer(out,dialect='excel')
pg_user = "tester"
pg_passward = "Test1234"
pg_db = "zhongyifangji_db"
pg_host = "127.0.0.1" 
engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_passward}@/{pg_db}')
try: 
    csv_file = pd.read_csv('./jingfang.csv',encoding="gbk",index_col=0)
    csv_file.set_index('xiangci')
    csv_file.to_sql("fangjiapp_fangji", con=engine,if_exists='append',index_label="xiangci") 
except Exception as e:  
    print(e)

print("write over")