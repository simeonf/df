from django.db import connection, transaction

def rebuild_recent():
    """Rebuild the multi-table index on save"""
    
    cursor = connection.cursor()
    drop = "drop table recent"    
    create = """CREATE TABLE recent (id int(11) NOT NULL auto_increment,
                                              title VARCHAR(255) NOT NULL,
                                              blurb longtext NOT NULL, 
                                              slug VARCHAR(255) NOT NULL,
                                              category ENUM('ARTICLE','REVIEW','POST','MAILBAG') NOT NULL,
                                              dt datetime NOT NULL,
                                              primary key (id),
                                              KEY recent_dt (dt))"""


    insert_blogs = """insert into recent(title, blurb, slug, category, dt)
                         select title, blurb, filename, category, dt from blog
                                  where display=1
                                  order by dt desc
                                  limit 0,200"""

    insert_mailbags = """insert into recent(title, blurb, slug, category, dt)
                         select title, blurb, slug, "MAILBAG", dt from mailbag_mailbag
                                  where display=1
                                  order by dt desc
                                  limit 0,200"""

    sql = [drop, create, insert_blogs, insert_mailbags]
    for statement in sql:
        try:
            cursor.execute(statement)
        except:
            pass # Maybe table still exists, etc
    transaction.commit_unless_managed()

    
