"""Translation of PHP search script to Python and Django. Probably
should use q where possible but sticking with .raw() for now"""

from MySQLdb import escape_string as esc

from article.models import Genre, Tags


class Ratings(object):
    overall = ['A+','A','A-', 'B+','B','B-','C+','C','C-','D+','D','D-','F',]
    stars = ['40','35','30','25','20','15','10','05','00']
    artistic = ['40','35','30','25','20','15','10','05','00']
    moral = ['4','3','2','1','0','-1','-2','-3','-4']
    age = ['K','T','A','Z']
    mpaa = ['G','PG','PG-13','R','NR']
    usccb = ["A-I","A-II","A-III",'O', 'NR']
    
    @staticmethod
    def locate(tagnames, values, join=" or "):
        """
        given some values and some tagnames generate the
        sql to find the tags.
        >>> locate(['overall'], ['A', 'B'])
        "(overall='A' or overall='B')"
        
        """
        template = "%s='%s'"
        clause = []
        for value in map(esc, values):
            for tag in tagnames:
                clause.append(template % (tag, value))
        sql = join.join(clause)
        if "or" in join:
            sql = "({})".format(sql)
        return sql
        
    @classmethod
    def sql(cls, tagnames, value, modifier):
        """ build where clause sql to select matching records by ratings tag.
        
        >>> Ratings.sql(["overall"], "A", ">=")
        "(overall='A+' or overall='A')"

        """
        # shortcut the == case
        if modifier == "=":
            return cls.locate(tagnames, [value])
        values = getattr(cls, tagnames[0])
        try:
            index = values.index(value)
        except ValueError:
            return None
        if modifier == '>=':
            values_used = values[:index +1]
        elif modifier == '<=':
            values_used = values[index:]
        else:
            values_used = []
        return cls.locate(tagnames, values_used)


def build_query(get):
    where = []  # holds where clauses, will be joined by and
    orderby = []  # holds order by clauses needed for hit relevance only.
    placeholders = {}  # sql interpolated values

    def simple_where(data, field):
      if data:
          where.append(field + " like '%%" + esc(data) + "%%'")
    
    # title search
    if get.get('title'):
        title  = esc(get['title'])
        orderby.append("title='%s' DESC" % title)
        orderby.append("title like ' %%{}%% ' DESC".format(title))
        orderby.append("title like '%%{}%%' DESC".format(title))
        # now search by word in title, alt, and cast
        for i, word in enumerate(title.split()):
            where.append("""(title like '%%{0}%%'
                         or alttitle like '%%{0}%%'
                         or cast like '%%{0}%%')""".format(esc(word)))

    # cast search
    simple_where(get.get('cast'), 'cast')

    # keywords in entry
    for word in get.get('keywords', '').split():
        simple_where(word, 'entry')

    # genre query. some manual queries "?genre=action&genre2=adventure" to account for
    # i'm fetching all article ids and issuing an id in [...] query cause that's how php did it.
    genres = get.getlist('genre') + [get.get('genre2')]
    genres = filter(None, [Genre.name_to_id(genre) for genre in genres])
    if genres:
        article_ids = [str(row[0]) for row in Genre.objects.filter(id__in=genres).values_list('article__id')]
        where.append('id in (' + ', '.join(article_ids) + ')')

    # labels
    labels = get.getlist('labels')
    if labels:
        article_ids = [str(row[0]) for row in Tags.objects.filter(id__in=labels).values_list('article__id')]
        where.append('id in (' + article_ids.join(',') + ')')

    # year tags
    year = get.get('year_from', '')
    if year and year.isdigit():
        where.append('year >=%(year_from)s')
        placeholders['year_from'] = year
                 
    year = get.get('year_to', '')
    if year and year.isdigit():
        where.append('year <=%(year_to)s')
        placeholders['year_to'] = year

    ratings = dict(overall=['overall'],
                   artistic=['stars'],
                   moral=['moral', 'spiritual'],
                   age=['age'],
                   mpaa=['mpaa'],
                   usccb=['usccb']
               )
    for field, tagnames in ratings.items():
        if get.get(field):
            where.append(Ratings.sql(tagnames, get.get(field), get.get('%s_modifier' % field, '=')))

    if get.get('fletter'):
        letter = get['fletter']
        where.append("""(%(fletter)s= LEFT(TRIM(leading "The " from
                                                TRIM(leading "A " from
                                                  TRIM(leading "An " from
                                                    TRIM(leading '"' from title)
                                                      )
                                                    )
                                                  ),1))""")
        placeholders['fletter'] = letter

    # Manually selected ordering
    orderings = {
        'title': """TRIM(leading "The " from TRIM(leading "A " from TRIM(leading "An " from TRIM(leading '"' from title)))) ASC""",
        'date': ' dt_modified DESC',
        'overall': Ratings.locate(['overall'], Ratings.overall, join=","),
        'artistic': Ratings.locate(['artistic'], Ratings.artistic, join=","),
        'year': "year DESC",
        }

    if get.get('order','') in orderings:
        orderby = [orderings[get.get('order')]]

    if orderby:
        orderby = ' ORDER BY ' + ', '.join(orderby)
    else:
        orderby = ''
    where.append('exclude_from_search=0')
    where = ' AND '.join(filter(None, where))
    
    sql = 'select * from blog where ' + where + orderby
    print sql
    return sql, placeholders

    # if((get['title']))
    # {
    #     sql = "select mailbag_mailbagentry.*, mailbag_mailbag.slug,
    #                               mailbag_mailbag.title as mtitle
    #                                  from mailbag_mailbag
    #                                    inner join mailbag_mailbagentry
    #                                    on mailbag_mailbag.id=mailbag_mailbagentry.mail_bag_id
    #                                    where search=1 and mailbag_mailbagentry.display=1
    #                                    and mailbag_mailbagentry.title like ?
    #                                    order by mailbag_mailbag.dt desc"
    #     mailbags = this->db->getAll(sql, array('%' . get['title'] . '%'))
    #     if(count(mailbags))
    #     {
    #         obj->records = array_merge(obj->records, mailbags)
    #         num = num + count(mailbags)
    #     }
    # }





