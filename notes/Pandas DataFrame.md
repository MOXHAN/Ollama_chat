---
tags:
  - DataScience
  - Python
slides: pandas_I
---
- **Pandas Series** is basically a list, whereas the **Pandas DataFrame** is a table (combination of multiple Series)
- Series comes with index as an attribute
- DataFrame comes with index as an attribute and column names
- mixed datatypes possible
- **Indexing** Label and position based
- **Mutability** in-place

## Attributes

- **df.columns** => column names
- **df.shape and df.size()** => does not include index attribute
- Its possible to turn column into index
- DataFrame uses more space due to actual storing of index value
- **Only 2 dimensions**


## Read-In Data

- **pd.read_csv("path", sep=",")
- **pd.read_excel("path", sheet_name="sheet")


## Selecting columns and operations on columns

Consider a DataFrame with multiple cols like "Price", "amount", "product"
### Selection

- df[ ["price"] ] --> returns DataFrame with 1 col
- df["price"] or df.price --> returns Series
### Comparisons & Logic operators

- df.attribute < number comparisons
- | and & for logical expressions
### Math operations, re-assign, sorting

- calculate with cols like so: df["price"] * df["amount"] (using df.price is not possible)
- df["sales"] = df["price"] * df["amount"] => modifies existing DF
- df = df.assign(sales = df["price"] * df["amount"]) => creates new DF
- **sort_values(colun_name, ascending=bool)
- **sort_index()** 
- **reset_index(drop=bool)** --> drop means to drop old index

### Arranging Columns

- **rename(columns={"old_name:new_name, ..})
- **melt**(frame, id_vars=column_names for id, value_vars=column_names to unpivot var_name=name for new var,) (problemset 3) --> can unpivot a wide DataFrame to long one, transforms multiple cols into one, example: cols: 2020, 2021, 2022 can be turned into one "Year" col with the years as values

### Merge Dataframes

- merge(left=data_1, right=data_2 , on=cols_to_join_on, how=left/right ) --> HOW
	- **Inner:** Use only intersection of both DFs
	- **Left/Right:** Use only keys from left/right table --%3E NaN for missing values
	- **Outer:** All keys --> NaN for missing values
	- arguments left_on / right_on for merging on cols with different names>)

### Concatenation

- using pd.concat([df1, df2], axis=0)
	- axis = 0 means vertically stacking --> adding new rows
	- axis = 1 means horizontal stacking --> adding new columns

### Statistic functions and aggregation

- **axis argument** for statistic functions like df.mean(): axis = 0 is vertical, axis = 1 is horizontal
- **agg()** method for more complex aggregations --> agg(["max","mean","min"])
- **sum()**, **mean()**
- apply() --> apply user defined function to DataFrame or col of DataFrame
### Grouping

- **df.groupby("column_name")** => splits table into multiple new tables (subset) based on values in "column_name"
- grouping returns a **[[DataFrameGroupBy]]** object, which are sequences (as in [[Collections]])
- many methods behave the same as for normal DataFrames, but there are additional attributes and methods
- GroupBy.size() --> returns amount of datapoints per group

### Accessors

- **Index based on Labels:** df.loc[row_lables, col_labels]
- **Index based on Integer position**:** df.iloc[row_indices, col_indices]
- possible to use slicing: df.iloc[0:2, 0:1] => first 2 rows, first column