import sqlparse

"""
Extract tables from an SQL query
"""
def extract_tables(query):
    # Parse the SQL query
    parsed = sqlparse.parse(query)
    statement = parsed[0]
    
    tables = []
    tokens = statement.tokens
    
    for token in tokens:
        # Look for 'FROM' or 'JOIN' clauses
        if token.ttype is None and str(token).upper().startswith(("FROM", "JOIN")):
            tables.extend([str(t).strip() for t in token.tokens if t.ttype is None])
    
    return tables