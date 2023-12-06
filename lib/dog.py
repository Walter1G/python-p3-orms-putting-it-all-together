import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name,breed):
        self.name=name
        self.breed=breed
        self.id=None
        
    @classmethod
    def create_table(cls):
        CURSOR.execute("CREATE TABLE IF NOT EXISTS dogs (name TEXT,breed TEXT)")
        
    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
    
    def save(self):
        sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    
    @classmethod
    def create(cls,name,breed):
        dog=Dog(name,breed)
        dog.save()
        return dog
        
    def new_from_db():
        dog = Dog(row[1], row[2])
        dog.id = row[0]
        return dog
    
    def get_all():
        sql = "SELECT * FROM dogs"
        result = CURSOR.execute(sql).fetchall()
        dogs = [Dog.new_from_db(row) for row in result]
        return dogs
    
    def update(self):
        sql = "UPDATE dogs SET name=?, breed=? WHERE id=?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
        
    def find_or_create_by(name, breed):
        existing_dog = Dog.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return Dog.create(name, breed)
    
    def find_by_id(id):
        sql = "SELECT * FROM dogs WHERE id=?"
        result = CURSOR.execute(sql, (id,)).fetchone()
        if result:
            return Dog.new_from_db(result)
        else:
            return None