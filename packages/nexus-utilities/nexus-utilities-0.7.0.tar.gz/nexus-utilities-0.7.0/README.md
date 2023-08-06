# nexus-utilities<!-- omit in toc -->
This package is meant to hold various useful utilities for functionality I find myself using across multiple projects.  I will try to keep this documentation updated as I expand the toolkit.  Feel free to use these if you find them valuable and I welcome any feedback.

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [config\_utils.py](#config_utilspy)
  - [**read\_config\_file(config\_filepath)**](#read_config_fileconfig_filepath)
- [database\_utils.py](#database_utilspy)
  - [**build\_engine(connect\_type, server\_address, server\_port, server\_name, user\_name, password, schema=None)**](#build_engineconnect_type-server_address-server_port-server_name-user_name-password-schemanone)
  - [**check\_engine\_read(engine, schema=None, table\_name=None)**](#check_engine_readengine-schemanone-table_namenone)
  - [**check\_engine\_write\_delete(engine, schema=None)**](#check_engine_write_deleteengine-schemanone)
  - [**clean\_sql\_statement(sql\_statement)**](#clean_sql_statementsql_statement)
- [datetime\_utils.py](#datetime_utilspy)
  - [**get\_current\_timestamp()**](#get_current_timestamp)
  - [**get\_duration(then, now=datetime.datetime.now())**](#get_durationthen-nowdatetimedatetimenow)
  - [**determine\_date\_format(date\_list)**](#determine_date_formatdate_list)
- [flatfile\_utils.py](#flatfile_utilspy)
  - [**detect\_encoding(file\_path)**](#detect_encodingfile_path)
  - [**analyze\_dataframe(df)**](#analyze_dataframedf)
  - [**check\_primary\_key\_fields(df, field\_list, print\_results=True)**](#check_primary_key_fieldsdf-field_list-print_resultstrue)
- [package\_utils.py](#package_utilspy)
  - [**add\_package\_to\_path()**](#add_package_to_path)
  - [**import\_relative(package\_root\_name, module\_path, import\_name, alias=None)**](#import_relativepackage_root_name-module_path-import_name-aliasnone)
  - [**extract\_from\_error(full\_error\_message, error\_keyword)**](#extract_from_errorfull_error_message-error_keyword)
- [password\_utils.py](#password_utilspy)
  - [**get\_password(password\_method, password\_key, account\_name=None, access\_key=None, secret\_key=None, endpoint\_url=None, region\_name=None, password\_path=None, encoding='utf-8')**](#get_passwordpassword_method-password_key-account_namenone-access_keynone-secret_keynone-endpoint_urlnone-region_namenone-password_pathnone-encodingutf-8)
- [string\_utils.py](#string_utilspy)
  - [**string\_to\_bool(bool\_string)**](#string_to_boolbool_string)
  - [**cleanse\_string(string, remove\_symbols=True, title\_to\_snake\_case=False, hyphen\_to\_underscore=True, period\_to\_underscore=True, to\_upper=False, to\_lower=True)**](#cleanse_stringstring-remove_symbolstrue-title_to_snake_casefalse-hyphen_to_underscoretrue-period_to_underscoretrue-to_upperfalse-to_lowertrue)
- [About the Author](#about-the-author)

---

## Installation

```python
pip3 install nexus-utilities
```

After installation, use "import nexus_utils" to access the various functions.

---

## config_utils.py

This module contains functions for working with configuration files.  Currently limited to using configparser to read .ini files.

### **read_config_file(config_filepath)**

Arguments:
 * ***config_filepath (str):*** File path to the .ini file to be read

Returns:
 * ***config (ConfigParser Class):*** ConfigParser Class containing the read configuration data

Takes a path to a specific .ini file and reads it.  Will also check if there is a "_local" version and uses that instead if found.  Eg. if you pass in "/path/to/file/database_config.ini", it will check for the presence of "/path/to/file/database_config_local.ini" and use it instead

---

## database_utils.py

This module contains functions for working with databases and related functions.

### **build_engine(connect_type, server_address, server_port, server_name, user_name, password, schema=None)**

Arguments:
 * ***connect_type (str):*** SQLAlchemy connection type, Eg. "postgresql" or "postgresql+psycopg2"
 * ***server_address (str):*** Database server address
 * ***server_port (str):*** Database port
 * ***server_name (str):*** Database name
 * ***user_name (str):*** Username
 * ***password (str):*** Password
 * ***schema (str):*** Default database schema (optional)

Returns:
 * ***engine (sqlalchemy.engine.Engine Class):*** SQLAlchemy Engine Class for interacting with the database

Creates a SQLAlchemy Engine Class object for interacting with your database.

### **check_engine_read(engine, schema=None, table_name=None)**

Arguments:
 * ***engine (sqlalchemy.engine.Engine Class):*** Engine object to attempt connection
 * ***schema (str):*** Optional argument to specify the schema to test
 * ***table_name (str):*** Optional argument to specify a table to test  
*Note:*  Both schema and table_name must be provided to utilize that functionality

Returns:
 * ***result (str):*** "Success" or the text content of any error encountered

Checks that an established SQLAlchemy Engine Class object has select access to the default schema.  If a schema and table_name is provided, ity will use a "SELECT COUNT(*) FROM {schema}.{table_name}" to confirm, otherwise it utilizes a simple "SELECT 1" from the default schema.

### **check_engine_write_delete(engine, schema=None)**

Arguments:
 * ***engine (sqlalchemy.engine.Engine Class):*** Engine object to attempt connection
 * ***schema (str):*** Optional argument to specify the schema to test

Returns:
 * ***result (str):*** "Success" or the text content of any error encountered

Checks that an established SQLAlchemy Engine Class object has create, write, delete and drop permissions on the specified schema.  It does this by creating a "nexus_access_test" table, inserting into it, updating it, deleting from it, then dropping it.  Helpful for checking the functionality of a connection object designed for ETL activities.

### **clean_sql_statement(sql_statement)**

Arguments:
 * ***sql_statement (str):*** SQL script to be cleansed

Returns:
 * ***sql_statements_output (list):*** List of cleansed SQL statements in the order they appeared in the provided script

The primary purpose of this function is to remove comments from a SQL script.  Any lines prefixed with "--" and all text surrounded by "/*" and "*/" will be removed.  Will also separate each distinct statement in the script to its own list item for iterating though.

---

## datetime_utils.py

This module contains functions for working with dates and times.

### **get_current_timestamp()**

Arguments:
 * None

Returns:
 * ***current_timestamp (datetime Class):*** Datetime Class object - Used for difference calculations
 * ***filename_timestamp (str):*** Timestamp string formated 'YYYY-MM-DD_HHMMSS' - Used for filenames
 * ***log_timestamp (str):*** Timestamp string formated 'YYYY-MM-DD HH:MM:SS' - Used for logs

Calculates the current time in UTC timezone and returns 3 variations to be used for different purposes.

### **get_duration(then, now=datetime.datetime.now())**

Arguments:
 * ***then (datetime Class):*** Datetime Class object representing the lower limit of a time comparison
 * ***now (datetime Class):*** Datetime Class object representing the upper limit of a time comparison

Returns:
 * ***days_between (int):*** Days between two timestamps
 * ***hours_between (int):*** Hours between two timestamps
 * ***minutes_between (int):*** Minutes between two timestamps
 * ***seconds_between (int):*** Seconds between two timestamps
 * ***duration_string (str):*** String representation of difference between two timestamps

Calculates the difference between two timestamps.  Provides absolute number of total days, hours, minutes, and seconds, as well as a string representation of the normalized difference, Eg. "5 days, 4 hours, 3 minutes, 2 seconds" or "32 seconds".

### **determine_date_format(date_list)**

Arguments:
 * ***date_list (list):*** List of dates to analyze

Returns:
 * ***date_format (str):*** Determined date format in plain text (Eg. "MM/DD/YYYY")
 * ***format_string (str)*** Date format string to be passed into the Python "datetime" library (Eg. "%m/%d/%Y")

Attempts to isolate the date portion of a list of string values, and return the likely format.  Some sample return values are "MM/DD/YYYY", "DD-MM-YYYY or "YYYYMMDD".  The primary value of this function is to tell MM/DD from DD/MM formats, which many more traditional means of date parsing may struggle with.

***Notes:***

* Only delimiters supported are "-", "/" and no delimiter
* It is assumed that all dates in a given list are the same format.  For example, the function will not work properly if a list contains both "05/06/2000" and "05-07-2000"
* Timestamp portions are ignored
* Only works for numerical dates.  For example, will not work with "June 5, 2000"
* Limited support for 2 digit years
* Requires some form of differentiation between the included dates.  For example, if all dates in the list are "05/06/2000", it will be impossible to infer the date format.  However, if it sees "05/06/2000", "05/07/2000" and "05/08/2000" in the list, it will assume a "MM/DD" format based on the limited variance in one segment, and a higher variance in another segment

---

## flatfile_utils.py

This module contains functions for working with flat files.

### **detect_encoding(file_path)**

Arguments:
 * ***file_path (str):*** Path to flat file to read

Returns:
 * ***encoding (str):*** String representation of encoding, such as 'utf-8' or 'ascii'

Attempts to detect the encoding of a flat file.  It will scan the first 2,000 records of the file.  If the result is 'ascii', it will scan the entire file to confirm.  This is to prevent a false positive of 'ascii' if a non-ascii character happens to not be present in the first 2,000 rows.

### **analyze_dataframe(df)**

Arguments:
 * ***df (pandas dataframe):*** Pandas dataframe of the flat file to be analyzed

Returns:
 * ***df_results (pandas dataframe):*** Pandas dataframe representing the analysis results

Performs basic field profiling for a flat file read into a pandas dataframe.  Results come in 3-column groupings:

|||||||
| :--- | :--- | :--- | :--- | :--- | :--- |
|*{column_name_01}*|*{summary_metric}*|&nbsp;|*{column_name_02}*|*{summary_metric}*|&nbsp;|
|Distinct Values|Occurrences|&nbsp;|Distinct Values|Occurrences|&nbsp;|
|*{value_01}*|*{occurrence_count}*|&nbsp;|*{value_01}*|*{occurrence_count}*|&nbsp;|
|*{value_02}*|*{occurrence_count}*|&nbsp;|*{value_02}*|*{occurrence_count}*|&nbsp;|
|...|...|&nbsp;|*{value_03}*|*{occurrence_count}*|&nbsp;|
|*{value_50}*|*{occurrence_count}*|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|More than 50 distinct values|Distinct Values: *{count}*|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|||||||

***Notes:***
 * *{summary_metric}*: Will either be "Max Length: {value}" for strings, or "Max Value: {value}" for numeric values and dates.  Can be useful for estimating field size when designing tables
 * Will show up to 50 distinct values, sorted by number of occurrences descending.  If there are more than 50 distinct values, a note will be shown at the bottom of the list, along with the total number of distinct values

### **check_primary_key_fields(df, field_list, print_results=True)**

Arguments:
 * ***df (pandas dataframe):*** Dataframe to check
 * ***field_list (list):*** List of fields to check for duplicate values
 * ***print_results (bool):*** Whether to print results to the terminal

Returns:
 * ***is_unique (bool):*** Indicator of whether the provided set of fields are unique in the data frame
 * ***no_nulls (bool):*** Indicator of whether the provided set of fields have any NULL values
 * ***sample_issue_rows (pandas dataframe):*** Sample rows from the data frame showing duplicates or NULLs

Checks a data frame given a list of fields to see if they have duplicates or contain any NULL values.  Useful when trying to determine a Primary Key for a table to land data into.

---

## package_utils.py

This module contains functions for working with Python packages.

### **add_package_to_path()**

Arguments:
 * None

Returns:
 * ***package_root_dir (str):***  Full path leading up to the parent-level package folder
 * ***package_root_name (str):***  Name of the parent-level package folder

Programmatically determines the most likely root folder of the current running program, adds the parent folder to the system PATH, and returns the root folder name.  This can be helpful for resolving package-relative paths, particularly for programs with multiple possible entry points.  It achieves this by starting from the current working directory, and traversing upwards, counting the instances of the below files and folders:

```python
["src", "tests", "templates", "docs", "dist", "build", "readme.md", "license.txt", ".gitignore", "pyproject.toml", "requirements.txt", "poetry.lock", "setup.py", "manifest.in", ".editorconfig"]
```

In the case of a tie, it takes the folder deeper into the path.  The returned "package_root_name" is meant to be used with the "import_relative()" function below, while the "package_root_dir" can be useful for dertermining absolute-paths relative to the application.

### **import_relative(package_root_name, module_path, import_name, alias=None)**

Example:  
***/app/flat_file_loader/src/utils/config_reader.py***

***import_relative('flat_file_loader', 'src.utils', 'config_reader', alias='cr')***

Arguments:
 * ***package_root_name (str):*** Folder name of package root folder.  Meant to be used with the output of the "add_package_to_path()" function
 * ***module_path (str):*** Dot-separated path from the package root to the library to be imported
 * ***import_name (str):*** Name of the object to be imported.  Can be a ".py" file name, or a function within a ".py" file (in the latter case, make sure the ".py" file name is part of the "module_path" above)
* ***alias (str):*** Optional alias for the imported library or function

Allows for importing package-relative libraries or functions given a programmatically-determined package root folder.  Useful for programs with multiple entry points and utilities called from multiple libraries.

***Important note: Pylance will show an error since the imports are done at runtime.  These can be avoided by attaching "# type: ignore" to any line using one of these relative imports.***

### **extract_from_error(full_error_message, error_keyword)**

Arguments:
 * ***full_error_message (str):*** Full error text 
 * ***error_keyword (str):*** Dot-separated path from the package root to the library to be imported

Returns:
 * ***error_message (str):***  Single line error message

Accepts a full error message, identifies the first line containing a provided keyword, and returns only that line.  Can be helpful if you want to capture the most important portion of an error without printing the entire stack trace.

---

## password_utils.py

This module contains functions for working with passwords and other sensitive information.

### **get_password(password_method, password_key, account_name=None, access_key=None, secret_key=None, endpoint_url=None, region_name=None, password_path=None, encoding='utf-8')**

Arguments:
 * ***password_method (str):*** Desired password method.  Options include:
     * keyring:  Use the "keyring" python library
     * ssm:  Use the AWS Parameter Store method
     * secretsmanager:  Use the AWS Secrets Manager method
 * ***password_key (str):*** Unique identifier of the password or secret
 * ***account_name (str):*** Account name associated with the password (primarily used by keyring)
 * ***access_key (str):*** AWS access key
 * ***secret_key (str):*** AWS secret key
 * ***endpoint_url (str):*** AWS endpoint url
 * ***region_name (str):*** AWS region name
 * ***password_path (str):*** AWS path to secret (primarily used by AWS Parameter Store)
 * ***encoding (str):*** Password encoding.  Supports the following, but uses utf-8 as the default: 'utf-8', 'ascii', 'latin-1', 'utf-16'

Returns:
 * ***secret_value (str):*** Secret in plain text

Allows multiple methods of retrieving sensitive information.

Note:  If you prefer to use environment variables instead of passing the sensitive information directly, you can use the below.  They will be used in place of the function arguments when present:

```python
AWS Parameter Store:
access_key = 'AWS_SSM_ACCESS_KEY_ID'
secret_key = 'AWS_SSM_SECRETACCESS_KEY_ID'
endpoint_url = 'AWS_SSM_ENDPOINT_URL'
region_name = 'AWS_SSM_REGION_NAME'
password_path = 'AWS_SSM_PASSWORD_PATH'

AWS Secrets Manager:
access_key = 'AWS_SM_SECRET_ACCESS_KEY'
secret_key = 'AWS_SM_ACCESS_KEY_ID'
endpoint_url = 'AWS_SM_ENDPOINT_URL'
region_name = 'AWS_SM_REGION_NAME'
password_key = 'AWS_SM_PASSWORD_KEY'
```

---

## string_utils.py

This module contains functions for working with strings.

### **string_to_bool(bool_string)**

Arguments:
 * ***bool_string (str):*** String to attempt to convert to a boolean

Returns:
 * ***string (bool or str):*** Will return booleans True or False if conversion is successful, or a string explaining why the conversion failed, either due to an invalid input type provided, or an unrecognized value

Takes a string input and attempts to interpret it as a boolean value based on the below recognized values (after converting to lowercase):
* **True:**  ['true', 't', 'yes', 'y', 'yep', 'yeah', 'affirmative', 'x', '1', '1.0', 'on', 'enabled']
* **False:**  ['false', 'f', 'no', 'n', 'nope', 'nah', '', '0', '0.0', 'off', 'disabled']

### **cleanse_string(string, remove_symbols=True, title_to_snake_case=False, hyphen_to_underscore=True, period_to_underscore=True, to_upper=False, to_lower=True)**

Arguments:
 * ***string (str):*** String to be cleansed
 * ***remove_symbols (bool):*** Remove some symbols, and replace others with "_"
 * ***title_to_snake_case (bool):*** Convert TitleCase to Snake_Case
 * ***hyphen_to_underscore (bool):*** Change hypehens to underscores
 * ***period_to_underscore (bool):*** Change periods to underscores
 * ***to_upper (bool):*** Change string to uppercase
 * ***to_lower (bool):*** Change string to lowercase

Returns:
 * ***string (str):*** Transformed string value

Below is additional details about what each transformation does:
 * ***remove_symbols*** - Removes or converts to "_" based on the below rules.  Will also attempt to preserve multiple underscores in the original field without adding to them (using the '†' symbol).  Eg. "Field__(Name)" will become "Field__Name", not "Field___Name"
     * characters_to_replace_with_underscore  
' ', ':', ';', '&', '@', '^', '+', '=', '~', '/', '\\', '|', '(', '{', '[', '<'
     * characters_to_remove  
',', '`', '#', '$', '%', '*', ''', '"', '?', '!', ')', '}', ']', '>'
 * ***title_to_snake_case*** - Convert TitleCase to SnakeCase.  Attempts to account for clusters of uppercase letters.  For example, "SalesForNBCUniversal" will return "sales_for_nbc_universal"
 * ***hyphen_to_underscore*** - Converts "-" to "_", otherwise leaves them alone
 * ***period_to_underscore*** - Converts "." to "_", otherwise leaves them alone
 * ***to_upper*** - Converts string to UPPERCASE
 * ***to_lower*** - Converts string to lowercase, takes precedence over "to_upper"

## About the Author

My name is James Larsen, and I have been working professionally as a Business Analyst, Database Architect and Data Engineer since 2007.  While I specialize in Data Modeling and SQL, I am working to improve my knowledge in different data engineering technologies, particularly Python.

[https://www.linkedin.com/in/jameslarsen42/](https://www.linkedin.com/in/jameslarsen42/)