from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
        'secure_connect_bundle': '/Users/simratjaggi/Desktop/Big Data Work/Movie Lens Recommendation and Analytics/security/secure-connect-simrat-personal.zip'
}
auth_provider = PlainTextAuthProvider(<<CLIENT_ID>>, <<CLIENT_PASS>>)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

rows = session.execute("select item_other from simrat_personal_keyspace.similarity where item='$5 a Day (2008)' order by sim desc per partition limit 10;")
for row in rows:
	print(row.item_other)