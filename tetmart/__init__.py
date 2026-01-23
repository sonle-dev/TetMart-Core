import pymysql

# Đánh lừa Django rằng đây là phiên bản mysqlclient mới nhất
# (Dòng này cần thiết vì bạn đang dùng Django 5.x/6.x)
pymysql.version_info = (2, 2, 7, "final", 0)

pymysql.install_as_MySQLdb()