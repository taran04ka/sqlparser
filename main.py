#Add gramar
#Add description 

import sqlparse
from sql_dictionary import translations

def translate_sql_query(sql_query):
    parsed = sqlparse.parse(sql_query)[0]
    tokens = list(parsed.flatten())

    translation = "This query will "
    columns = []
    table_name = ""
    order_by_column = ""
    order_direction = "ascending"  # Default ordering

    for token in tokens:
        if token.ttype is sqlparse.tokens.DML and token.value.upper() == 'SELECT':
            columns = []  # Reset columns list for each SELECT statement
            translation += "select "

        elif token.ttype is sqlparse.tokens.Wildcard:
            columns = ["all columns"]  # If wildcard is found, we want all columns

        elif token.ttype is sqlparse.tokens.Name:
            if 'from' in translation and 'select' in translation and not table_name:  # Capture the table name
                table_name = token.value
            elif 'select' in translation:  # Otherwise, it's likely a column name
                columns.append(token.value)

        elif token.ttype is sqlparse.tokens.Keyword:
            keyword = token.value.upper()
            if keyword == 'FROM':
                translation += ', '.join(columns) + " from "  # Append columns and FROM clause

            elif keyword == 'ORDER BY':
                order_by_column = tokens[tokens.index(token) + 2].value  # Assuming next significant token is the column name
                next_token = tokens[tokens.index(token) + 4] if tokens.index(token) + 4 < len(tokens) else None
                if next_token and next_token.ttype is sqlparse.tokens.Keyword and next_token.value.upper() in ['ASC', 'DESC']:
                    order_direction = next_token.value.lower()

    # Append table name, order by column and direction to translation
    if table_name:
        translation += table_name + " table"
    if order_by_column:
        translation += f" ordered by {order_by_column} {order_direction}"

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
