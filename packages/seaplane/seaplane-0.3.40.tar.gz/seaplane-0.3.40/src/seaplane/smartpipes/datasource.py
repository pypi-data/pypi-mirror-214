from typing import Optional, Any, List, Dict
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import Json

class RequestDataSource:
    def __init__(self, database: str, host: str, username: str, password:str, port: int = 5432) -> None:
        self.conn: connection = psycopg2.connect(
            database=database,
            host=host,
            user=username,
            password=password,
            port=port,
        )

        self.conn.set_session(autocommit=True)
    
    def save_request(self, id: str, batch_count: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute(""" INSERT INTO requests
                        (id, status, batch_count)
                        VALUES
                        (%s, %s, %s)""", [id, "processing", batch_count])
        row_count: int = cursor.rowcount
        cursor.close()
        return row_count

    def save_result(self, request_id: str, order: int, output: Any) -> None:
        cursor = self.conn.cursor()
        cursor.execute(""" INSERT INTO results
                        (request_id, original_order, output)
                        VALUES
                        (%s, %s, %s)""", [request_id, order, Json(output)])
        row_count: int = cursor.rowcount
        cursor.close()
        return row_count

    def get_request_status(self, request_id: str) -> Optional[Any]:         
        cursor = self.conn.cursor()
        cursor.execute("""
          SELECT r.id, r.batch_count,
              (SELECT COUNT(*) FROM results rs WHERE rs.request_id = r.id) AS result_count
          FROM requests r
          WHERE r.id = %s;
        """, [request_id])
        row = cursor.fetchone()        
        result = None
        if row:
          result = {
              'request_id': row[0],
              'batch_count': row[1],
              'result_count': row[2]
          }
        cursor.close()
        return result 

    def get_request_results(self, request_id: str) -> List[Dict[str, Any]]:         
        cursor = self.conn.cursor()
        cursor.execute("""
          SELECT output
          FROM results
          WHERE request_id = %s
          ORDER BY original_order ASC;
        """, [request_id])
        rows = cursor.fetchall()        

        results = []
        for row in rows:
            results.append(row[0])        

        cursor.close()
        return results
        