import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote

class Database_PD():
	def __init__(self, username, host, db_name, password):
		super().__init__()
		self.sqlEngine = create_engine(
			"mysql+pymysql://{}:%s@{}:3306/{}".format(username, host, db_name) % quote(password)
		)

	def select_data(self, query):
		with self.sqlEngine.connect() as connection:
			df = pd.read_sql(text(query), con=connection) 
			return df

	def insert_data(self, table_name, df, dtype):
		with self.sqlEngine.connect() as connection:
			df.to_sql(name=table_name, index=False, con=connection, if_exists="append", dtype=dtype)
	
	def update_data(self, table_name, df, query, dtype=None):
		with self.sqlEngine.connect() as connection:
			df.to_sql(name="temp_{}".format(table_name), index=False, con=connection, if_exists="replace")
			with connection.begin():
				connection.execute(query)
	
	def close_conn(self):
		self.sqlEngine.dispose()
	
		