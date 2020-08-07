import functools
import MySQL_python.linkedList

#133
#as i don't know what i will specifically be doing with our DB yet, here is some code form a previous project that i could edit to use for our purposes.
#use optional

class House(MySQL_python.linkedList.LinkedListItem):
    tableName = "house"
    """
    creates an object for the house
    :param passes in the class for the linked list object. 
    """

    def __init__(self, name):
        """
        merge sort of data
        :param name: list of data to be sorted
        :return: sorted list from low to high
        """
        self.name = name
        super().__init__()


    def id(self):
        """
        creates an id based off a sting that s unique , by putting the sting though a hashing algorithm
        :param : sting to create a hash for
        :return: an id for teh string
        """
        return hash(self)

    @classmethod
    def ddl(cls, connection):
        """
        creates house table in the connection specified with teh name that the class specified
        :param connection: the connection to the database
        """
        connection.cursor().execute(f"CREATE TABLE IF NOT EXISTS {cls.tableName} (ID INTEGER ,name varchar(255) )",)

    def insertIfNotThere(self, connection):
        """
        inserts missing house and return new id or returns existing house id if house already in database
        :param connection: sting to create a hash for
        :return: return new id or returns existing house id if house already in database
        """

        cursor = connection.cursor()
        print(self.tableName,self.name)
        cursor.execute(f"select ID from {self.tableName} where name='{self.name}'")
        existingId = cursor.fetchall()
        if existingId:
            return existingId[0][0]
        connection.cursor().execute(f"INSERT INTO {self.tableName} VALUES ({self.id()}, '{self.name}')")
        return self.id()


class Price(MySQL_python.linkedList.LinkedListItem):
    tableName = "price"

    def __init__(self, houseName, bookingDate, price):
        self.houseName = houseName
        self.price = price
        self.bookingDate = bookingDate
        super().__init__()


    @classmethod
    def ddl(cls, connection):  # create price table
        connection.cursor().execute(f"CREATE TABLE IF NOT EXISTS {cls.tableName} (houseID INTEGER , bookingDate DATE , price FLOAT )", )

    def insert(self, connection):
        houseId = House(self.houseName).insertIfNotThere(connection)
        cursor = connection.cursor()
        cursor.execute(f"select houseID from {self.tableName} where houseId='{houseId}' and bookingDate = '{self.bookingDate}'")
        existingPriceId = cursor.fetchall()
        if existingPriceId:
            print(f"Already have price for {self.houseName} {self.bookingDate}")
        else:
            connection.cursor().execute(f"INSERT INTO {self.tableName} VALUES ({houseId}, '{self.bookingDate}', {self.price})")
            print(f"Inserted price for {self.houseName} {self.bookingDate}")

    @classmethod
    def extract(cls, houseName, connection):  # return all prices and pricingDates for a cottage
        cursor = connection.cursor()
        cursor.execute(f"select p.price, p.bookingDate FROM house h, price p where h.id = p.houseID and h.name = '{houseName}' ", )
        response = cursor.fetchall()
        print(response)
        return response







