# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import pymysql
from scrapy import signals
from mysql.connector import errorcode
from scrapy.exceptions import DropItem

class OndiskPipeline:

    def __init__(self, host, user, password, database, table, stats):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.ids_seen = set()
#        self.connectdb()

        self.stats = stats
        self.stats.set_value("scrape_cnt", 0)

        self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8')
        self.cursor = self.conn.cursor()

        print ("init_==========")
        print (self.conn)
        print (self.cursor)
        print ("init_==========")
#        print("set size1:" + str(len(self.ids_seen)))
        #try:
##                host='127.0.0.1', user='pocachip', password='media2015!', db='rightwatch', charset='utf8')
        #except mysql.connector.Error as err:
            #if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                #print("Something is wrong with your user name or password")
            #elif err.errno == errorcode.ER_BAD_DB_ERROR:
                #print("Database does not exist")
            #else:
                #print(err)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            table=crawler.settings.get('MYSQL_TABLE'),
            stats=crawler.stats
        )

    def connectdb(self):
        if self.conn is None:
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8')
                return self.conn
    #                host='127.0.0.1', user='pocachip', password='media2015!', db='rightwatch', charset='utf8')
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
                return None
        else:
            return self.conn

    def open_spider(self, spider):
        print("open_spider start")
        # Check if table exists
        spider.myPipeline = self
        #if self.conn is None:
            #self.connectdb()
        self.cursor.execute(f"select idx from {self.table}")
        row = self.cursor.fetchone()
        while row:
            self.ids_seen.add(row[0])
#           spider.ids_seen.add(row[0])
            row = self.cursor.fetchone()
        print("set size1:" + str(len(self.ids_seen)))

    def get_ids(self):
        return self.ids_seen

    def close_spider(self, spider):
        self.cursor.colse()
        self.conn.close()

    def process_item(self, item, spider):
        self.stats.inc_value("scrape_cnt")
        #print ("process_time==========")
        #print (item)
        #print (self.stats.get_value("scrape_cnt"))

        #if (self.stats.get_value("scrape_cnt") > 5):
        #    spider.crawler.engine.close_spider(self, reason='reach max scraped count')
#        if item['author_id'] in self.author_ids_seen:
#            raise DropItem("Duplicate item found: %s" % item)
#        else:
#            self.ids_seen.add(item['author_id'])
#            return item
#vals = [["TEST1", 1], ["TEST2", 2]]

#with connection.cursor() as cursor:
    #cursor.executemany("insert into test(prop, val) values (%s, %s)", vals )
    #connection.commit()
        try:
#            print("Process =====>")
            self.cursor.execute("""INSERT INTO post (website, cat1_code, cat2_code, 
                        cat1_title, cat2_title, idx, txt, Lvl19, price, 
                        seller, partner, attach_file_size, last_update) VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (str(item['website']), str(item['cat1_code']), str(item['cat2_code']), 
                        str(item['category_title']), str(item['sub_category_title']), str(item['idx']), 
                        str(item['txt']), str(item['Lvl19']), str(item['point']), str(item['seller']), 
                        str(item['partner']), str(item['attach_file_size']), str(item['time'])))

                #with self.conn.cursor() as cursor:
                    #print("Process 3")
                    #sql = f'''INSERT INTO {self.table} (website, cat1_code, cat2_code, 
                                #category_title, sub_category_title, idx, txt, Lvl19, price, 
                                #seller, partner, attach_file_size, last_update) VALUES 
                                #(%i, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''' % (
                                #int(item['website']), item['cat1_code'], item['cat2_code'], 
                                #item['category_title'], item['sub_category_title'], item['idx'], 
                                #item['txt'], item['Lvl19'], item['point'], item['seller'], 
                                #item['partner'], item['attach_file_size'], item['time'])
                    #print(sql)
                    #cursor.execute(sql)
            self.conn.commit()
                        #cursor.execute(f'''INSERT INTO {self.table} (website, cat1_code, cat2_code, category_title, sub_category_title, idx, txt, Lvl19, price, seller, partner, attach_file_size, last_update) VALUES (%i, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (item['website'], item['cat1_code'], item['cat2_code'], item['category_title'],
                        #item['sub_category_title'], item['idx'], item['txt'], item['Lvl19'], item['point'],
                        #item['seller'], item['partner'], item['attach_file_size'], item['time']))
                        #self.conn.commit()
            return item
        except mysql.connector.Error as e:
            print("Process error")
            raise DropItem(f'Error inserting item: {e}')
