== How to run python

== Pre-requisites
Since we are reading/writing data to oracle we need cx_Oracle package to be installed. cx_Oracle requires oracle client.
To install CX_Oracle
- install rpm from home/opc/download/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm
- install rpm from  cx_Oracle-5.2.1-12c-py27-1.x86_64.rpm



== Reader

To Execute Reader:

cd /pocpython
python pivotalDBReader.py >> ../outputs/pivotalDBReader.log

Note: pivotalDBReader used property file inquirer.properties. This can be overrided by python pivotalDBReader <properyfile>

PropertyFile structure

Query=<Actual SQL you want to execute>

e.g. 
ALL HYB_MEMBERS COUNT QUERY=select * from HYB_MEMBERS
ALL HYB_PROVIDERS COUNT QUERY=select * from HYB_PROVIDERS
ALL HYB_INSTCLAIMS COUNT QUERY=select * from HYB_INSTCLAIMS
ALL 


== Load EpisodeClaims from rxClaims, professionalClaims and instClaims tables
Staging:
python populateEpisodeClaims.py > populateEpisodeClaims.log

Hyb:
python populateHybEpisodeClaims.py > populateHybEpisodeClaims.log

PJ:
python populatepjEpisodeClaims.py > populatepjEpisodeClaims.log



=== Process EpisodeClaims
Staging:
python populateAndProcessEpisodeClaims.py > populateAndProcessEpisodeClaims.log

hyb:
python populateAndProcesshybEpisodeClaims.py > populateAndProcesshybEpisodeClaims.log

Pure json:
python populateAndProcesspjEpisodeClaims.py > populateAndProcesspjEpisodeClaims.log


