#import pymysql
#pymysql.install_as_MySQLdb()
import pymysql
# Đánh lừa Django rằng đây là phiên bản mới nhất
pymysql.version_info = (2, 2, 7, "final", 0) 
pymysql.install_as_MySQLdb()