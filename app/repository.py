from typing import List, Dict, Any, Optional
from app.database import get_db_connection


class Repository:
    """Base repository class for database operations"""
    
    @staticmethod
    def fetch_one(query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a query and fetch one result
        
        Args:
            query: SQL query string
            params: Optional tuple of query parameters
            
        Returns:
            Dictionary with column names as keys, or None if no result
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def fetch_all(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a query and fetch all results
        
        Args:
            query: SQL query string
            params: Optional tuple of query parameters
            
        Returns:
            List of dictionaries with column names as keys
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def execute(query: str, params: Optional[tuple] = None, commit: bool = True) -> int:
        """
        Execute a query (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query string
            params: Optional tuple of query parameters
            commit: Whether to commit the transaction (default: True)
            
        Returns:
            Number of affected rows (rowcount)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
            return cursor.rowcount
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()