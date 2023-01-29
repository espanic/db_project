import pymysql


class Database:
    __instance = None

    @classmethod
    def _get_instance(cls):
        return cls.__instance
    
    
    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls._get_instance()
        return cls.__instance
    

    def __init__(self,db ="", host = 'localhost', user = 'root', password = ""):
        print("Connect DB...", end = ' ')
        self.__db = pymysql.connect(host=host, db=db,user=user,password=password, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.__initialize_database()
        print('Done!')

    def __del__(self):
        print("Close database connection..")
        self.__db.close()


    def __initialize_database(self):
        table_names = ['building', 'performance', 'audience', 'assign', 'reservation']
        with self.__db.cursor() as cursor:
            queries = [
                """ CREATE TABLE IF NOT EXISTS building(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    location VARCHAR(200) NOT NULL,
                    capacity INT NOT NULL DEFAULT 0
                );
                """,
                """ CREATE TABLE IF NOT EXISTS performance(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    type VARCHAR(200) NOT NULL,
                    price INT NOT NULL
                );
                """,
                """ CREATE TABLE IF NOT EXISTS audience(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    gender CHAR(1) NOT NULL,
                    age INT NOT NULL
                );
                """,
                """ CREATE TABLE IF NOT EXISTS assign(
                    performance_id INT PRIMARY KEY,
                    building_id INT NOT NULL,
                    CONSTRAINT `fk_assign_performance_id`
                        FOREIGN KEY (performance_id) REFERENCES performance(id) ON DELETE CASCADE,
                    CONSTRAINT `fk_assign_building_id`
                    FOREIGN KEY (building_id) REFERENCES building(id) ON DELETE CASCADE 
                );
                """,
                """ CREATE TABLE IF NOT EXISTS reservation(
                    performance_id INT NOT NULL,
                    audience_id INT NOT NULL,
                    seat_number INT NOT NULL,
                    PRIMARY KEY (performance_id, audience_id),
                    CONSTRAINT `fk_reservation_performance_id`
                        FOREIGN KEY (performance_id) REFERENCES performance(id) ON DELETE CASCADE,
                    CONSTRAINT `fk_reservation_audience_id`
                        FOREIGN KEY (audience_id) REFERENCES audience(id) ON DELETE CASCADE
                )
                """
            ]
            for i, query in enumerate(queries):
                cursor.execute(query)
                print("{} table ok".format(table_names[i]))

    def reset(self):
        print("reseting database...")
        with self.__db.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS building, performance, audience, assign, reservation")
            self.__initialize_database()
            self.__db.commit()
        print("Done!")


    def fetch(self, query):
        with self.__db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        
    def fetchmany(self,query, data):
        with self.__db.cursor() as cursor:
            cursor.executemany(query, data)
            result = cursor.fetchall()
            return result 
        

    def executemany(self, query, data):
        with self.__db.cursor() as cursor:
            cursor.executemany(query, data)
            self.__db.commit()
        
        
    def execute(self, query):
        with self.__db.cursor() as cursor:
            cursor.execute(query)
            self.__db.commit()
        
                            
                            
    


    


    