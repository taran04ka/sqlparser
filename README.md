# SQL to Human Language Translator

## Project Overview

This project aims to develop a software tool capable of translating SQL (Structured Query Language) queries into human-readable language. The tool's primary objective is to assist individuals who are not proficient in SQL to understand complex queries easily.

## Technical Stack

- Python: Python's vast ecosystem and libraries make it an ideal choice for processing and translating SQL queries.

## Features

- SQL Query Input: Users can input SQL queries which the system will process.
- Human-Readable Translation: The core feature, translating SQL queries into simple, understandable language.

## Grammar

The following is the formal grammar used by the translator:

```

<Query> --> <SelectStatement> | <InsertStatement> | <UpdateStatement> | <DeleteStatement>

<SelectStatement> --> "SELECT " <Columns> <FromClause> <WhereClauseOptional> <OrderByClauseOptional> <GroupByClauseOptional> <LimitClauseOptional>

<Columns> --> "all columns " | <ColumnList>

<ColumnList> --> <ColumnName> | <ColumnName> ", " <ColumnList>

<FromClause> --> "from " <TableName>

<WhereClauseOptional> --> <WhereClause> | ε

<WhereClause> --> "where " <Condition>

<Condition> --> <SingleCondition> | <SingleCondition> " and " <Condition> | <SingleCondition> " or " <Condition>

<SingleCondition> --> <ColumnName> <Operator> <Value>

<OrderByClauseOptional> --> <OrderByClause> | ε

<OrderByClause> --> "ordered by " <ColumnName> <OrderDirection> | ε

<OrderDirection> --> "ascending " | "descending "

<GroupByClauseOptional> --> <GroupByClause> | ε

<GroupByClause> --> "grouped by " <ColumnName> | ε

<LimitClauseOptional> --> <LimitClause> | ε

<LimitClause> --> "limit " <Number> | ε

<InsertStatement> --> "insert " "into " <TableName> "values " <Values>

<UpdateStatement> --> "update " <TableName> "set " <SetClause> <WhereClauseOptional>

<DeleteStatement> --> "delete rows " <FromClause> <WhereClauseOptional>

<SetClause> --> <ColumnName> " = " <Value> | <ColumnName> " = " <Value> ", " <SetClause>

<Value> --> <Literal> | <Number>

<Literal> --> '"' <Alphanumeric> '"'

<Number> --> [0-9]+

<TableName> --> <Alphanumeric>

<ColumnName> --> <Alphanumeric>

<Alphanumeric> --> [A-Za-z0-9_]+

```

## How to Run the Program

To run the program, follow these steps:

1. Ensure Python is installed on your system.
2. Navigate to the directory containing the script.
3. Run the script using the command: `python3 main.py`
4. Enter SQL queries as prompted.

## Example Commands

Here are some example SQL queries and their corresponding translations:

- SQL Query: `SELECT * FROM clients`
- Translation: `This query will select all columns from clients table`

- SQL Query: `INSERT INTO employees VALUES ('John', 'Doe', 'Manager')`
- Translation: `This query will insert values into employees table`
