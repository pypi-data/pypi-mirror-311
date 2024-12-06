import pymysql


class DynamicDatabase:
    def __init__(self, host, user, password, database):
        """Initialize the database connection."""
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self.metadata = None  # To store column metadata for table structure
        self.table_created = False  # Flag to track if table has already been created

    def create_table_with_metadata(self, table_name, metadata):
        """
        Create a table based on metadata if it doesn't exist.
        metadata: A dictionary where the key is the column name and the value is a tuple
                  (data type, length, options).
        Options can include 'primary_key', 'auto_increment', etc.
        """
        column_definitions = []
        primary_key = None  # Track primary key
        for name, (data_type, length, *options) in metadata.items():
            # Default column definition
            column_definition = f"{name} {data_type}"

            # Apply length if present
            if length:
                column_definition += f"({length})"

            # Add options like PRIMARY KEY, AUTO_INCREMENT
            if 'primary_key' in options:
                column_definition += " PRIMARY KEY"
                primary_key = name  # Track the primary key column

            if 'auto_increment' in options:
                column_definition += " AUTO_INCREMENT"

            column_definitions.append(column_definition)

        if not primary_key:
            raise ValueError("Table must have a column defined as 'primary_key'.")

        # Join column definitions
        column_definitions_str = ', '.join(column_definitions)

        # Create the table
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions_str});"
        print(f"CREATE TABLE Query: {create_query}")  # Debugging line to check query
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert(self, table_name, data):
        """
        Insert data into the table.
        If metadata is included, create the table and store metadata.
        """
        if self.metadata is None:  # If metadata is not set, create the table
            metadata = {}
            for key, value in data.items():
                # Unpack the column tuple (name, data_type, length, options...)
                column_name, data_type, length, *options = key
                metadata[column_name] = (data_type, length, *options)

            # Create the table with metadata if it doesn't exist
            self.create_table_with_metadata(table_name, metadata)

            # Store the metadata for future reference
            self.metadata = metadata
            self.table_created = True  # Mark the table as created

        # Extract column names and data values (excluding auto-increment columns)
        columns = []
        values = []
        for key, value in data.items():
            column_name, data_type, length, *options = key
            # Skip columns marked as auto-increment (or primary_key)
            if 'auto_increment' in options or 'primary_key' in options:
                continue
            columns.append(column_name)
            values.append(value)

        if not columns:
            raise ValueError("No valid columns provided for insertion.")

        # Ensure the data is inserted properly for each row
        rows = zip(*values)  # Dynamically pair columns with their respective values

        for row in rows:
            processed_data = {columns[i]: value for i, value in enumerate(row)}

            # Debugging the insert statement and data
            placeholders = ', '.join(['%s' for _ in processed_data])  # '%s, %s'
            print(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});")  # Debugging line
            print(f"Values: {tuple(processed_data.values())}")  # Debugging line

            # Execute the insert query
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});"
            self.cursor.execute(insert_query, tuple(processed_data.values()))

        self.conn.commit()

    def read(self, table_name, conditions=None):
        """
        Read data from the table with optional conditions.
        If no conditions are provided, fetch all rows.
        """
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += " WHERE " + " AND ".join([f"{key} = %s" for key in conditions.keys()])

        self.cursor.execute(query, tuple(conditions.values()) if conditions else ())
        result = self.cursor.fetchall()
        return result

    def update(self, table_name, data=None, conditions=None, custom_query=None):
        """
        Update data in the table based on a condition.
        data: dictionary where key is the column to update, value is the new value.
        conditions: dictionary where key is the column to filter, value is the condition.
        custom_query: A string containing a custom SQL query for the update.
        """
        if custom_query:
            # Execute custom query if provided
            print(f"Executing custom query: {custom_query}")  # Debugging line
            self.cursor.execute(custom_query)
        elif data and conditions:
            # Otherwise, build query dynamically based on data and conditions
            set_clause = ", ".join([f"{column} = %s" for column in data.keys()])
            where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])

            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
            print(f"Executing query: {update_query}")  # Debugging line
            self.cursor.execute(update_query, tuple(data.values()) + tuple(conditions.values()))
        else:
            raise ValueError("Either 'custom_query' or both 'data' and 'conditions' must be provided.")

        self.conn.commit()

    def delete(self, table_name, conditions):
        """
        Delete rows from the table based on a condition.
        conditions: dictionary where key is the column to filter, value is the condition.
        """
        where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
        delete_query = f"DELETE FROM {table_name} WHERE {where_clause};"
        self.cursor.execute(delete_query, tuple(conditions.values()))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()


