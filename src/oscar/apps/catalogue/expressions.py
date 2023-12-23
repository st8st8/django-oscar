from django.db.models.expressions import Subquery

EXPAND_UPWARDS_CATEGORY_QUERY = """
(SELECT "CATALOGUE_CATEGORY_JOIN"."id" FROM "catalogue_category" AS "CATALOGUE_CATEGORY_BASE"
LEFT JOIN "catalogue_category" AS "CATALOGUE_CATEGORY_JOIN" ON (
    "CATALOGUE_CATEGORY_BASE"."path" LIKE "CATALOGUE_CATEGORY_JOIN"."path" || '%%%%'
    AND "CATALOGUE_CATEGORY_BASE"."depth" >= "CATALOGUE_CATEGORY_JOIN"."depth"
)
WHERE "CATALOGUE_CATEGORY_BASE"."id" IN (%(subquery)s))
"""
EXPAND_UPWARDS_CATEGORY_QUERY_MYSQL = EXPAND_UPWARDS_CATEGORY_QUERY.replace('"', '`')

EXPAND_DOWNWARDS_CATEGORY_QUERY = """
(SELECT "CATALOGUE_CATEGORY_JOIN"."id" FROM "catalogue_category" AS "CATALOGUE_CATEGORY_BASE"
LEFT JOIN "catalogue_category" AS "CATALOGUE_CATEGORY_JOIN" ON (
    "CATALOGUE_CATEGORY_JOIN"."path" LIKE "CATALOGUE_CATEGORY_BASE"."path" || '%%%%'
    AND "CATALOGUE_CATEGORY_BASE"."depth" <= "CATALOGUE_CATEGORY_JOIN"."depth"
)
WHERE "CATALOGUE_CATEGORY_BASE"."id" IN (%(subquery)s))
"""
EXPAND_DOWNWARDS_CATEGORY_QUERY_MYSQL = EXPAND_DOWNWARDS_CATEGORY_QUERY.replace('"', '`')


# pylint: disable=abstract-method
class ExpandUpwardsCategoryQueryset(Subquery):
    template = EXPAND_UPWARDS_CATEGORY_QUERY
    mysql_template = EXPAND_UPWARDS_CATEGORY_QUERY_MYSQL

    def as_sql(self, compiler, connection, template=None, **extra_context):
        if connection.vendor == "mysql":
            return super().as_sql(compiler, connection, self.mysql_template, **extra_context)
        return super().as_sql(compiler, connection, self.template, **extra_context)

    def as_sqlite(self, compiler, connection):
        return super().as_sql(compiler, connection, self.template[1:-1])


# pylint: disable=abstract-method
class ExpandDownwardsCategoryQueryset(Subquery):
    template = EXPAND_DOWNWARDS_CATEGORY_QUERY
    mysql_template = EXPAND_DOWNWARDS_CATEGORY_QUERY_MYSQL

    def as_sql(self, compiler, connection, template=None, **extra_context):
        if connection.vendor == "mysql":
            return super().as_sql(compiler, connection, self.mysql_template, **extra_context)
        return super().as_sql(compiler, connection, self.template, **extra_context)

    def as_sqlite(self, compiler, connection):
        return super().as_sql(compiler, connection, self.template[1:-1])
