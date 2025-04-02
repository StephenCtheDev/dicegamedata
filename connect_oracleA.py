import cx_Oracle

# Database connection details
dsn = cx_Oracle.makedsn("45.86.211.19", "1521", sid="orcl")

try:
    connection = cx_Oracle.connect("c##dicegame", "stephen123", dsn)
    cursor = connection.cursor()

    print("Connected to Oracle successfully!")

    # Ensure table exists
    try:
        cursor.execute("""
            DECLARE 
                table_exists EXCEPTION;
                PRAGMA EXCEPTION_INIT(table_exists, -955);
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE dice_rolls (
                    die1 NUMBER,
                    die2 NUMBER,
                    roll_count NUMBER,
                    PRIMARY KEY (die1, die2)
                )';
            EXCEPTION
                WHEN table_exists THEN NULL; -- Ignore "table already exists" error
            END;
        """)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        print(f"Table creation error: {e}")

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
    print(f"Error connecting to Oracle: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

