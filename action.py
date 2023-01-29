from database import Database

class Action:

    def perform_action(self, i):
        map_actions = {
            1 : self.print_all_building,
            2 : self.print_all_performance,
            3 : self.print_all_audience,
            4 : self.add_building,
            5: self.delete_building,
            6: self.add_performance,
            7 : self.delete_performance,
            8 : self.add_audience,
            9 : self.delete_audience,
            10 : self.assign_performance_on_building,
            11 : self.reserve_performance,
            12 : self.print_performances_assigned_on_building,
            13 : self.print_audiences_reserved_performance,
            14 : self.print_ticket_booking_status_of_a_performance,
            16 : self.reset_database
        }
        map_actions[i]()


    def __init__(self, db : Database) -> None:
        self._db = db

    # SELECT 문의 결과를 주어진 형식에 맞게 변형
    def format_results(type, results):
        line = '--------------------------------------------------------------------------------\n'
        res = line

        if type == 'building':
            headers = ['id', 'name', 'location', 'capacity', 'assigned']
            formats = [8, 32, 16, 16, 8]
        elif type == 'performance':
            headers = ['id', 'name', 'type', 'price', 'booked']
            formats = [8, 32, 16, 16, 8]
        elif type == 'audience':
            headers = ['id', 'name', 'gender', 'age']
            formats = [8, 40, 16, 16]
        elif type == 'status':
            headers = ['seat_number', 'audience_id']
            formats = [40, 40]

        for i in range(len(headers)):
            res += f'{headers[i]:<{formats[i]}}'
        res += '\n'

        res += line

        for row in results:
            temp_result = ''
            for i in range(len(headers)):
                temp_result += f'{row[headers[i]]:<{formats[i]}}'
            res += temp_result
            res += '\n'

        if not results:
            res += '\n'
        
        res += line
        return res
    
    #1 모든 공연장 출력
    def print_all_building(self):
        query  = "SELECT id, name, location, capacity FROM building;"
        buildings = self._db.fetch(query)

        for building in buildings:
            building_id = building['id']
            query = f"SELECT COUNT(*) as count FROM assign WHERE building_id = {building_id}"
            count = self._db.fetch(query)[0]['count']
            building['assigned'] = count
        print(buildings)


    #2 모든 공연 정보 출력
    def print_all_performance(self):
        query  = "SELECT id, name, type, price FROM performance;"
        performances =self._db.fetch(query)
        for performance in performances:
            performance_id = performance['id']
            query = f"SELECT COUNT(*) AS booked FROM reservation WHERE performance_id = {performance_id};"
            booked = self._db.fetch(query)[0]['booked']
            performance['booked'] = booked
        print(performances)

    #3 모든 관객 정보 출력
    def print_all_audience(self):
        query  = "SELECT id, name, gender, age FROM audience;"
        audiences = self._db.fetch(query)
        print(audiences)


    #4 공연장 추가
    def add_building(self):
        try:
            name = input('building name : ')[:200]
            location = input("location of building :")[:200]
            capacity = int(input('Building capacity: '))

            if capacity < 1:
                print("capacity should be bigger than 0")
                return 

            query = f"INSERT INTO building(name, location, capacity) VALUES ('{name}', '{location}', {capacity});"
            self._db.execute(query)
            print("Adding building complete")
        except:
            print("input is not valid")

    #5 공연장 삭제

    def delete_building(self, id):
        building = self._get_building_with_id(id)
        if building is None:
            print(f"Building with {id} does not exist.")
            return 
        query = "DELETE FROM building WHERE id = {id};"
        self._db.execute(query)
        print(f"Deleting building with id : {id} is successfully completed.")

    
    def _get_building_with_id(self, id):
        query = f"SELECT * FROM building WHERE id = {id};"
        data  = self._db.fetch(query)
        if not len(data):
            return None
        return data[0]

    #6 공연 추가
    def add_performance(self):
        try:
            name = input("name : ")[:200]
            type = input("type : ")[:200]
            price = int(input("price : "))
            if price < 0:
                print("price should be equal to or greater than 0")
                return 
            query = f"INSERT INTO performance(name, type, price) VALUES('{name}', '{type}', {price});"
            self._db.execute(query)
            print("Insert performance finished successfully.")
        except:
            print("input is not valid")
    
    #7 공연 삭제
    def delete_performance(self, id):
        performance = self._get_performance_with_id(id)
        if performance is None:
            print(f"There is no performance with id : {id}.")
            return 
        query = f"DELETE FROM performance WHERE id = {id};"
        self._db.execute(query)
        print(f"DEleting performance with id : {id} has successfully completed")

    def _get_performance_with_id(self, id):
        query  = f"SELECT * FROM performance WHERE id = {id};"
        data = self._db.fetch(query)
        if not len(data):
            return None
        return data[0]


    #8 관객 추가
    def add_audience(self):
        try:
            name = input("name : ")[:200]
            gender = input("type : ")[:1]
            age = int(input("age : "))

            if gender not in ('M', 'F'):
                print("Gender should be either M or F.")
                return 


            if age < 1:
                print("Age should be equal to or greater than 1")
                return 
            qeury = f"INSERT INTO audience(name, gender, age) VALUES('{name}', '{gender}', {age});"
        except:
            print("Input is not valid")

    #9 관객 삭제
    def delete_audience(self, id):
        audience = self._get_audience_with_id(id)
        if audience is None:
            print(f"There is no audience with id : {id}.")
            return 
        query = f"DELETE FROM audience WHERE id = {id};"
        self._db.execute(query)
        print(f"Deleting audience with id : {id} has successfully completed")


    def _get_audience_with_id(self, id):
        query  = f"SELECT * FROM audience WHERE id = {id};"
        data = self._db.fetch(query)
        if not len(data):
            return None
        return data[0]
    
    #10 공연배정
    def assign_performance_on_building(self):
        building_id = int(input("building id : "))
        if self._get_audience_with_id(building_id) is None:
            print(f"There is no building with id : {building_id}")
            return 
        performance_id = int(input("performance id : "))
        if self._get_performance_with_id(performance_id) is None:
            print(f"There is no performance with id : {performance_id}")
            return 
        
        building_id_previously_assigned= self._get_building_id_with_performance_id(performance_id)
        if building_id_previously_assigned:
            print(f"The performance is already assigned on building id : {building_id_previously_assigned}")
            return 
        
        query = f"INSERT INTO assign (building_id, performance_id) VALUES({building_id}, {performance_id});"
        self._db.execute(query)
        print("Successfully assign performance.")


    def _get_building_id_with_performance_id(self, performance_id):
        query = f"SELECT building_id FROM assign WHERE performance_id = {performance_id};"
        data = self._db.fetch(query)
        if len(data):
            return None
        return data[0]['building_id']
    
    #11 공연 예매
    def reserve_performance(self):
        performance_id = int(input("performance id : "))
        performance = self._get_performance_with_id(performance_id)
        if  performance is None:
            print(f"There is no performance with {performance_id}.")
            return 
        building_id= self._get_building_id_with_performance_id(performance_id) 
        if building_id is None:
            print(f"Performance hasn't been assigned.")
            return 

        audience_id = int(input("audience_id : "))
        audience = self._get_audience_with_id(audience_id)
        if  audience is None:
            print(f"There is no audience with {audience_id}.")
        seat_list = list(map(int, input().replace(" ", "").split(",")))

        capacity = self._get_capacity_with_building_id(building_id)

        if not self._valid_seat_in_capacity(seat_list, capacity):
            print("Invalid seat number")
            return 
        if not self._check_seat_is_available(seat_list):
            print("Some seats has been already taken.")
        
        query  = f"iNSERT INTO reservation VALUES({performance_id}, {audience_id}, %d);"
        self._db.executemany(query, seat_list)

        total_price = self._calculate_ticket_price(performance, audience) * len(seat_list)
        return round(total_price)

    def _calculate_ticket_price(self, performance, audience):
        price = performance['price']
        age = audience['age']

        if age > 0 and age < 8:
            return 0
        elif age < 13:
            return price * 0.5
        elif age < 19:
            return price * 0.8
        else:
            return price
        

    def _seat_list_to_sql(self, seat_list):
        res = "("
        for seat in seat_list:
            res += seat +","
        res = res[:len(res) - 1]
        res += ")"
        return res
    
    def _check_seat_is_available(self, seat_list):
        seat_list_sql = self._seat_list_to_sql(seat_list)
        query = f"SELECT COUNT(*) as count FROM reservation WHERE seat_number IN {seat_list_sql};"
        count = self._db.execute(query)[0]['count']
        if count > 0:
            return False
        return True


    def _get_capacity_with_building_id(self, building_id):
        query = f"SELECT capacity FROM building WHERE id = {building_id};"
        return self._db.fetch(query)[0]['capacity']
    
    def _valid_seat_in_capacity(self, seat_list, capacity):
        for seat in seat_list:
            if seat < 1 or seat > capacity:
                return False
        return True
    

    #12 공연장에 배정된 공연 몰록 출력
    def print_performances_assigned_on_building(self):
        building_id = int(input("building id : "))
        if self._get_building_with_id(building_id) is None:
            print(f"There is no bulding with {building_id}.")
            return

        query1 = f"SELECT performance_id FROM ASSIGN WHERE building_id = {building_id};"

        performances = self._db.fetch(query2)
        performance_ids = [performance['id'] for performance in performances]

        query2 = f"""
        SELECT T.id, T.name, T.type, T.price, COUNT(*) as count 
        FROM performance AS T LEFT JOIN reservation AS S ON T.id = S.id
        WHERE T.id = (%d);
        """
        result = self._db.fetchmany(query2, performance_ids)
        print(result)


    #13 공연장에 배정된 공연 목록 출력

    def print_audiences_reserved_performance(self):
        performance_id = int(input("performance id : "))
        if self._get_performance_with_id(performance_id) is None:
            print(f"There is no performance with {performance_id}.")
            return 
        
        query = f"""
        SELECT DISTINCT A.id, A.name, A.gender, A.age
        FROM audience AS A JOIN reservation AS R ON A.id = R.audience_id
        WHERE R.performance_id = {performance_id};
        """
        audiences = self._db.fetch(query)
        print(audiences)

    #14 공연의 좌석 별 예매 상황 출력
    def print_ticket_booking_status_of_a_performance(self):
        performance_id = int(input("performance id : "))
        if self._get_performance_with_id(performance_id) is None:
            print(f"There is no performance with {performance_id}.")
            return 

        bulding_id = self._get_building_id_with_performance_id(performance_id)
        if bulding_id is None:
            print("Haven't been assigned to a building.")
            return 


        query2 = f"""
        SELECT R.seat_number, R.audience_id
        FROM Reservation AS R JOIN Audience A ON R.audience_id = A.id
        WHERE R.performance_id = {performance_id};
        """
        seat_info =self._db.execute(query2)
        capacity = self._get_capacity_with_building_id(bulding_id)

        seat_reservation = self._parse_seat_reservation(seat_info, capacity)

        print(seat_reservation)


    def _parse_seat_reservation(seat_info, capacity):
        res = {i : None for i in range(1, capacity + 1)}
        for info in seat_info:
            seat_num = info['seat_number']
            audience_id = info['audience_id']
            res[seat_num] = audience_id
        return res



    #16 데이터베이스 리셋 및 생성
    def reset_database(self):
        self._db.reset()




    
    


            

    


        
