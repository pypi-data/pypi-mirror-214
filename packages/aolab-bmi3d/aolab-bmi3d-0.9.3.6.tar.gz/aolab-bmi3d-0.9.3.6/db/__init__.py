try:
    import pymysql
    pymysql.version_info = (1, 3, 13, "final", 0)
    pymysql.install_as_MySQLdb()
except:
    print("Warning: pymysql is not installed, cannot access remote database")