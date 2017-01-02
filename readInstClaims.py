def readInstClaims(cursor, query, params=()) :

        print("executing query [%s]",(query))
        params = {}
       	cursor.execute(query, params)

        colnames = [desc[0] for desc in cursor.description]
        print(colnames)
        count = 0
        for row in cursor.fetchall():
                print(row)
                count = count + 1
                for (name, value) in zip(colnames, row):
                        print(name, '\t->', value)
                        print
        print "Total Records %d", count

def initHsql():
        import jaydebeapi
        conn = jaydebeapi.connect('org.hsqldb.jdbcDriver',['jdbc:hsqldb:hsql://localhost/', 'SA', ''],'C:/Users/cho922/.m2/repository/org/hsqldb/hsqldb/2.3.3/hsqldb-2.3.3.jar',)

        cursor = conn.cursor()

def initOracle():
        import cx_Oracle
        #conn = cx_Oracle.connect("system/oracle@50.21.182.140/orcl")
        conn = cx_Oracle.connect('system', 'oracle', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	conn = cx_Oracle.connect(props.get('db.oracle.userId'), props.get('db.oracle.passwd'), props.get('db.oracle.connectString.python'))
        return conn

if __name__ == '__main__': # self test
        import cx_Oracle
        print '%s,%s,%s', 
        conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
        print conn.version
        cursor = conn.cursor()
        query="select * from json_claim jc where jc.json_doc.\"_id\"='2o6FR7v8Wfzr6vk1V-5-1480799300666'"
               select * from json_claim jc where jc.json_doc.\"_id\"='2o6FR7v8Wfzr6vk1V-5-1480799300666'
        #query = "select * from json_claim jc where jc.json_doc.\"_id\"='Ap2XjFNnsFTNlVaI4-5-1481257921969'"
        readInstClaims(cursor, query)
