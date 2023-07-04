import sqlite3
import sys
from contextlib import closing

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
def search(inputs):
    """Given a list of string inputs, generate certain type of query."""

    DATABASE_URL = 'file:lux.sqlite?mode=ro'

    def item_text_query(cursor, lbl, agt, dep, cls):
        """Query for all the objects that will populate the list widget item text"""

        headers = ["ID", "Label", "Produced By", "Date", "Classified As"]
        formats = ["p", "p", "p", "p", "p"]

        sql_str = """
        WITH class as 
            (
                select id, group_concat(distinct name || "") as classified 
                from (select o.id, lower(c.name) as name
                from objects o
                left outer join objects_classifiers oc on o.id = oc.obj_id
                left outer join classifiers c on oc.cls_id = c.id
                order by lower(c.name)
                )
                group by id
            ),

        agts as 
            (
                select id, group_concat(distinct name || ' (' || part || ')') as agent_names
                from (select o.id, a.name as name, p.part as part
                from objects o
                left outer join productions p on o.id = p.obj_id
                left outer join agents a on p.agt_id = a.id
                order by name, part
                )
                group by id
            ),
        
        dpts as
            (
                select o.id, group_concat(distinct d.name || '') as dep_names
                from objects o
                left outer join objects_departments od on o.id = od.obj_id
                left outer join departments d on od.dep_id = d.id
                group by o.id
                order by lower(d.name)
            ) 
        """

        sql_str += """
        select id, label, date, a.agent_names, c.classified
        from objects natural join class c natural join dpts d natural join agts a
        """

        sql_str += "WHERE true "
        if lbl != "":
            sql_str += " AND label LIKE '%' || :inputlabel || '%'"
        if cls != "":
            sql_str += " AND c.classified LIKE '%' || :inputcls || '%'"
        if agt != "":
            sql_str += " AND a.agent_names LIKE '%' || :inputagt || '%'"
        if dep != "":
            sql_str += " AND d.dep_names LIKE '%' || :inputdep || '%'"

        sql_str += " ORDER BY label, date"

        # Sorting based on linesList
        unseen_keywords = [agt, dep, cls]
        # first, sort by agent
        if agt != "":
            sql_str += ", a.agent_names"
            unseen_keywords.remove(agt)
        # second, sort by department
        if dep != "":
            sql_str += ", d.dep_names"
            unseen_keywords.remove(dep)
        # third, sort by classifier
        if cls != "":
            sql_str += ", c.classified"
            unseen_keywords.remove(cls)

        # Tertiary sorting
        for keyword in unseen_keywords:
            if keyword == agt:
                sql_str += ", a.agent_names"
            elif keyword == dep:
                sql_str += ", d.dep_names"
            elif keyword == cls:
                sql_str += ", c.classified"

        # Limit the number of output rows to 1000
        sql_str += " LIMIT 1000"

        # Fetch the results from the query search
        cursor.execute(sql_str, {"inputdep":dep, "inputagt":agt,
                                    "inputcls":cls, "inputlabel":lbl})
        rows = cursor.fetchall()

        rows_str = []
        for row in rows:
            rows_str.append([str(x) for x in row])

        return rows_str

    def object_info_query(cursor, obj_id):
        """Query for the object information of the objects corresponding to given object id."""

        stmt_str = "SELECT objects.accession_no, objects.date, places.label "
        stmt_str += "from objects "
        stmt_str += "outer left join objects_places "
        stmt_str += "on objects.id = objects_places.obj_id "
        stmt_str += "outer left join places "
        stmt_str += "on objects_places.pl_id = places.id "
        stmt_str += "where objects.id = :inputid "
        stmt_str += " ORDER BY objects.date;"

        cursor.execute(stmt_str, {"inputid":obj_id})

        rows = cursor.fetchall()

        rows_str = []
        for row in rows:
            rows_str.append([str(x) for x in row])

        return rows_str

    def object_label_query(cursor, obj_id):
        """Query for the object label corresponding to the given object id. Outputs as a string. """
        stmt_str = "select objects.label "
        stmt_str += "from objects "
        stmt_str += "where objects.id = :inputid "
        
        cursor.execute(stmt_str, {"inputid":obj_id})
        
        label = cursor.fetchone()
        return label

    def prod_by_query(cursor, obj_id):
        """Query for the agents and part of the objects corresponding to given object id."""

        stmt_str = "SELECT productions.part, agents.name, "
        # groups all nationality descriptors for one object
        stmt_str += "GROUP_CONCAT(DISTINCT nationalities.descriptor || ''), "
        # Uses coalesce to account for when substring of begin and/or end are null
        stmt_str += "COALESCE (SUBSTRING (agents.begin_date, 1, 4), '') || '-' || "
        stmt_str += "COALESCE (SUBSTRING (agents.end_date, 1, 4), '') "
        stmt_str += "FROM objects "
        stmt_str += "OUTER LEFT JOIN productions "
        stmt_str += "ON objects.id = productions.obj_id "
        stmt_str += "OUTER LEFT JOIN agents "
        stmt_str += "ON productions.agt_id = agents.id "
        stmt_str += "OUTER LEFT JOIN agents_nationalities "
        stmt_str += "ON agents.id = agents_nationalities.agt_id "
        stmt_str += "OUTER LEFT JOIN nationalities "
        stmt_str += "ON agents_nationalities.nat_id = nationalities.id "
        stmt_str += "WHERE objects.id = :inputid "
        stmt_str += "GROUP BY agents.id "
        stmt_str += "ORDER BY productions.part"

        cursor.execute(stmt_str, {"inputid":obj_id})

        # create data array for Produced By
        data = []

        all_prod = cursor.fetchall()
        for prod in all_prod:
            data.append(prod)

        # new data arrays replaces Nones with empty strings to avoid split error
        prod_by_data = []
        for tup in data:
            new_tup = []
            for element in tup:
                if element is None:
                    new_tup.append("")
                else:
                    new_tup.append(element)
            prod_by_data.append(tuple(new_tup))

        return prod_by_data

    def classifiers_query(cursor, obj_id):
        """""Query for the classifiers of the objects corresponding to given object id."""""

        stmt_str = "SELECT GROUP_CONCAT(DISTINCT name || '') as classified "
        stmt_str += "FROM (SELECT lower(classifiers.name) as name "
        stmt_str += "FROM objects "
        stmt_str += "LEFT OUTER JOIN objects_classifiers "
        stmt_str += "ON objects.id = objects_classifiers.obj_id "
        stmt_str += "LEFT OUTER JOIN classifiers "
        stmt_str += "ON objects_classifiers.cls_id = classifiers.id "
        stmt_str += "WHERE objects.id = :inputid "
        stmt_str += "ORDER BY classifiers.name)"

        cursor.execute(stmt_str, {"inputid":obj_id})

        rows = cursor.fetchall()

        return rows

    def information_query(cursor, obj_id):
        """Query for the references of the objects corresponding to given object id."""

        stmt_str = "SELECT 'references'.type, 'references'.content "
        stmt_str += "FROM objects "
        stmt_str += "INNER JOIN 'references' "
        stmt_str += "ON objects.id = 'references'.obj_id "
        stmt_str += "WHERE objects.id = :inputid "
        stmt_str += "ORDER BY 'references'.type, 'references'.content ASC;"
        cursor.execute(stmt_str, {"inputid":obj_id})

        rows_str = []
        all_info = cursor.fetchall()
        for info in all_info:
            rows_str.append(info)

        return rows_str
    
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                if len(inputs) == 4:
                    lbl = inputs[0]
                    agt = inputs[1]
                    dep = inputs[2]
                    cls = inputs[3]
                    item_text_table = item_text_query(cursor, lbl, agt, dep, cls)
                    return item_text_table
                elif len(inputs) == 1:
                    obj_id = inputs[0]
                    object_info_table = object_info_query(cursor, obj_id)
                    label = object_label_query(cursor, obj_id)
                    prod_by_table = prod_by_query(cursor, obj_id)
                    classifiers_table = classifiers_query(cursor, obj_id)
                    information_table = information_query(cursor, obj_id)
                    tables = [object_info_table, label, prod_by_table,
                              classifiers_table, information_table]                    
                    
                    return tables
                else:
                    print("Failed query. Try again.", sys.stderr)
    except sqlite3.OperationalError as ex:
        raise ex