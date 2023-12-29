import sqlparse

def translate_sql_query(sql_query):
    parsed = sqlparse.parse(sql_query)[0]
    tokens = list(parsed.flatten())

    translation = "This query will "
    if tokens[0].ttype is sqlparse.tokens.DML and tokens[0].value.upper() == 'SELECT':
        columns = []
        table_name = ""
        order_by_column = ""
        order_direction = "ascending"  # Default ordering

        # Flags to manage different sections of SELECT statement
        in_select_clause = True
        in_from_clause = False
        in_order_by_clause = False

        for i, token in enumerate(tokens):
            if token.ttype is sqlparse.tokens.Keyword:
                if token.value.upper() == 'FROM':
                    in_select_clause = False
                    in_from_clause = True
                    # Assuming next significant token is table name
                    table_name = next((t.value for t in tokens[i+1:] if t.ttype is sqlparse.tokens.Name), "")
                elif token.value.upper() == 'ORDER BY':
                    in_order_by_clause = True
                    # Assuming next significant token is column name for ordering
                    order_by_column = next((t.value for t in tokens[i+1:] if t.ttype is sqlparse.tokens.Name), "")
                    # Checking the token right after column name for direction
                    direction_token = next((t for t in tokens[i+2:] if t.ttype is sqlparse.tokens.Keyword), None)
                    if direction_token and direction_token.value.upper() in ['ASC', 'DESC']:
                        order_direction = "descending" if direction_token.value.upper() == 'DESC' else "ascending"

            elif token.ttype is sqlparse.tokens.Wildcard and in_select_clause:
                columns = ["all columns"]  # Translate '*' to 'all columns'
                break  # No need to add more columns after '*'

            elif token.ttype is sqlparse.tokens.Name and in_select_clause:
                columns.append(token.value)

        columns_part = ", ".join(columns) if columns else "all columns"
        translation += f"select {columns_part} from {table_name} table"
        if order_by_column:
            translation += f" ordered by {order_by_column} in {order_direction} order"

    elif tokens[0].ttype is sqlparse.tokens.DML and tokens[0].value.upper() == 'UPDATE':
        table_name = tokens[1].value
        set_clauses = []
        where_clause = ""
        in_set_clause = False
        in_where_clause = False

        for i, token in enumerate(tokens[2:]):  # Skip 'UPDATE' and table_name tokens
            if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'SET':
                in_set_clause = True
                in_where_clause = False
            elif token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'WHERE':
                in_set_clause = False
                in_where_clause = True
            elif in_set_clause and token.ttype is sqlparse.tokens.Name:
                column = token.value
                # Skip to value (assuming format is Name '=' Value)
                value = tokens[i + 4].value  # +4 to account for column, '=', and any potential whitespace
                set_clauses.append(f"{column} to {value}")
            elif in_where_clause:
                where_clause += token.value + " "

        translation += f"update {table_name} table setting " + ", ".join(set_clauses)
        if where_clause:
            translation += " " + where_clause

    return translation.strip()

def translate_multiple_queries(sql_queries):
    queries = [query.strip() for query in sql_queries.split(";") if query.strip()]
    translations = []
    
    for query in queries:
        translation = translate_sql_query(query)
        translations.append((query, translation))
    
    return translations

def main():
    try:
        with open("ascii-text-art.txt", "r") as file:
            ascii_art = file.read()
        print(ascii_art)
    except Exception as e:
        print("Error reading ASCII art file:", e)

    while True:
        user_queries = input("Please enter your SQL queries separated by ';' or type 'exit' to quit: ")
        if user_queries.lower() == 'exit':
            print("Exiting the translator...")
            break

        translations = translate_multiple_queries(user_queries)
        print("Translating SQL to English...")
        for i, (original, translation) in enumerate(translations):
            print(f"Query {i + 1}:")
            print(f"Original: {original}")
            print(f"Translation: {translation}")

if __name__ == "__main__":
    main()