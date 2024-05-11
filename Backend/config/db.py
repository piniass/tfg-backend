from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:@localhost:3306/tfg")
# engine = create_engine("mysql+pymysql://miguel_pinan:palomeras98@db4free.net/bdd_miguelp")

meta = MetaData()
conn = engine.connect()