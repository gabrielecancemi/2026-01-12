from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_nodi(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.constructorId , c.constructorRef , c.name , c.nationality, MIN(d.dob) as oldest_driver_dob
                   from races r , results re , constructors c, drivers d 
                    where YEAR(r.`date`) >= %s and YEAR(r.`date`) <= %s
                    and r.raceId = re.raceId and c.constructorId = re.constructorId 
                    and d.driverId = re.driverId 
                    and re.`position` is not null
                    group by c.constructorId"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_archi(idC, anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.constructorid as c1, t2.constructorid as c2, count(distinct(t1.driverid)) as w from 
                    (
                    select c.constructorId, re.driverId, r.raceId from races r , results re , constructors c
                    where YEAR(r.`date`) >= %s and YEAR(r.`date`) <= %s
                    and r.raceId = re.raceId and c.constructorId = re.constructorId 
                    and re.`position` is not null
                    ) as t1,
                    (
                    select c.constructorId, re.driverId, r.raceId from races r , results re , constructors c
                    where YEAR(r.`date`) >= %s and YEAR(r.`date`) <= %s
                    and r.raceId = re.raceId and c.constructorId = re.constructorId 
                    and re.`position` is not null
                    ) as t2
                    where t1.raceid <> t2.raceid 
                    and t1.constructorid < t2.constructorid 
                    and t1.driverid = t2.driverid 
                    group by t1.constructorid , t2.constructorid"""

        cursor.execute(query, (anno1, anno2, anno1, anno2))

        for row in cursor:
            results.append((idC[row["c1"]], idC[row["c2"]], row["w"]))

        cursor.close()
        conn.close()
        return results



