from typing import Optional, Any
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

    def get_results_from_request(self, request_id: str) -> Any:         
        cursor = self.conn.cursor()
        cursor.execute("""
          SELECT rs.request_id, r.batch_count, COUNT(*) AS result_count
          FROM requests r
          JOIN results rs ON r.id = rs.request_id
          WHERE rs.request_id = %s
          GROUP BY rs.request_id, r.batch_count;
        """, [request_id])
        row = cursor.fetchone()        
        result = {
            'request_id': row[0],
            'batch_count': row[1],
            'result_count': row[2]
        }
        cursor.close()
        return result        
        