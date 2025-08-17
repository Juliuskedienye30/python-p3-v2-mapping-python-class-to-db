# Import the database connection (CONN) and cursor (CURSOR) from __init__.py
# These let us communicate with the SQLite database
from __init__ import CURSOR, CONN


class Department:
    # The constructor initializes a Department object with name, location, and optional id
    def __init__(self, name, location, id=None):
        self.id = id              # Database-generated primary key (auto-incremented integer)
        self.name = name          # Name of the department
        self.location = location  # Location of the department

    # Magic method for printing a Department object in a readable format
    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    # ---------- DATABASE METHODS ----------

    @classmethod
    def create_table(cls):
        """
        Create a table named 'departments' if it doesn’t exist already.
        The table will have: id (primary key), name, and location.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,   -- Auto-incrementing primary key
            name TEXT,                -- Name of department (string)
            location TEXT)            -- Location of department (string)
        """
        CURSOR.execute(sql)   # Execute the SQL query to create the table
        CONN.commit()         # Save changes to the database

    @classmethod
    def drop_table(cls):
        """
        Drop the 'departments' table if it exists.
        This deletes all data and structure.
        """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)   # Execute SQL command
        CONN.commit()         # Save changes

    def save(self):
        """
        Save the current Department object into the database.
        Insert its name and location, then update its id to match the row id.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        # Use parameter substitution (?) to safely insert values
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()         # Save changes to the database

        # Get the auto-generated id of the newly inserted row
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        """
        A shortcut method:
        1. Create a new Department object.
        2. Save it into the database.
        3. Return the object.
        """
        department = cls(name, location)  # Create object
        department.save()                 # Save it in DB
        return department                 # Return the saved object

    def update(self):
        """
        Update the database row that corresponds to this Department object.
        It will update the name and location where the id matches.
        """
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        # Execute SQL update with the object's current attributes
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()  # Save changes

    def delete(self):
        """
        Delete the row in the database that corresponds to this Department object.
        This removes the department entirely.
        """
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))  # Pass id as a tuple (important!)
        CONN.commit()  # Save changes
