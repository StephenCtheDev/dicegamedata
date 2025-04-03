import cx_Oracle

# Database connection details (Update with your AWS RDS endpoint)
dsn = cx_Oracle.makedsn("dicegamedb.cs18k2emgxne.us-east-1.rds.amazonaws.com", 1521, service_name="DATABASE")  # Use service_name for RDS

try:
    connection = cx_Oracle.connect("admin", "GiveMeAllTheGoods789", dsn)
    cursor = connection.cursor()

    print("Connected to AWS Oracle RDS successfully!")

    def update_roll_count(die1, die2):
        """Inserts or updates dice roll counts."""
        try:
            cursor.execute("""
                MERGE INTO dice_rolls d
                USING (SELECT :die1 AS die1, :die2 AS die2 FROM dual) src
                ON (d.die1 = src.die1 AND d.die2 = src.die2)
                WHEN MATCHED THEN
                    UPDATE SET roll_count = d.roll_count + 1
                WHEN NOT MATCHED THEN
                    INSERT (die1, die2, roll_count) VALUES (src.die1, src.die2, 1)
            """, {"die1": die1, "die2": die2})
            connection.commit()
        except cx_Oracle.DatabaseError as e:
            print(f"Database error (update_roll_count): {e}")

    def get_roll_counts():
        """Fetches all dice roll counts for display on the second HTML page."""
        try:
            cursor.execute("SELECT die1, die2, roll_count FROM dice_rolls ORDER BY die1, die2")
            return cursor.fetchall()
        except cx_Oracle.DatabaseError as e:
            print(f"Database error (get_roll_counts): {e}")
            return []

except cx_Oracle.DatabaseError as e:
    print(f"Error connecting to Oracle RDS: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()


