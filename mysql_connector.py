from mysql import connector
# from dotenv import load_dotenv
# from os import getenv

# load_dotenv()

# db_connector = connector.connect(
# 	user="root", password=getenv("SASTRA_pwd"), host="localhost"
# )

db_connector = connector.connect(user="root", password="password", host="localhost")
if not db_connector.is_connected():
	raise Exception("Database connection failed")

cursor = db_connector.cursor()

cursor.execute("""CREATE DATABASE IF NOT EXISTS `SASTRA`""")
cursor.execute("""USE `SASTRA`""")

def close():
	db_connector.commit()
	cursor.close()
	db_connector.close()
	exit()

if __name__ == "__main__":
	close()
