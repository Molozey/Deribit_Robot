import pymysql
from My_SQL_config import host, user, password, db_name
from datetime import datetime


def base_placement(type_operation, activity, current_price, volume):
    current_data_time = datetime.now()
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
#        print('Connection success...')

        try:
            with connection.cursor() as cursor:
                insert_request = "INSERT INTO `trades` (TIME_ORDER, TYPE_OPERATION, ACTIVITY, PRICE_OF_ACTION, VOLUME) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(insert_request, (str(current_data_time), str(type_operation), str(activity), float(current_price), float(volume)))
                connection.commit()
#                print('UPDATE SUCCESS...')
        finally:
            connection.close()
    except Exception as ex:
        print('UPDATE FAILED...')
        print(ex)