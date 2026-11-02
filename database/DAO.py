from database.DB_connect import DBConnect
from model.cliente import Cliente

class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT YEAR(InvoiceDate) AS year
                FROM invoice 
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getNodi(anno1,anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT c.CustomerId AS id, c.FirstName AS nome, c.LastName AS cognome,
                       c.Country AS paese, SUM(il.UnitPrice * il.Quantity) AS spesa
                FROM Customer c, InvoiceLine il, Invoice i, Track t
                WHERE il.InvoiceId = i.InvoiceId AND c.CustomerId = i.CustomerId
                  AND t.TrackId = il.TrackId AND YEAR(i.InvoiceDate) BETWEEN %s AND %s
                GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Country
                """
        cursor.execute(query, (anno1,anno2))
        for row in cursor:
            c = Cliente(row["id"], row["nome"], row["cognome"], row["paese"], float(row["spesa"]))
            results.append(c)
        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getCoppia(anno1,anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT i.CustomerId as id, t.AlbumId AS aId
                FROM InvoiceLine il, Invoice i, Track t
                WHERE il.InvoiceId = i.InvoiceId AND t.TrackId = il.TrackId AND YEAR(i.InvoiceDate) BETWEEN %s AND %s
                GROUP BY i.CustomerId, t.AlbumId
                """
        cursor.execute(query, (anno1,anno2))
        for row in cursor:
            results.append((row["id"],row["aId"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTitoliAlbum():
        conn = DBConnect.get_connection()
        if conn is None:
            return {}
        results = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ab.AlbumId, ab.Title
                FROM Album ab
                """
        cursor.execute(query)
        for row in cursor:
            results[row["AlbumId"]] = row["Title"]
        cursor.close()
        conn.close()
        return results