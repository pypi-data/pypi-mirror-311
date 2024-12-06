# dbshiftSDK

A Python SDK for converting Informatica XML mappings to Snowflake SQL and dbt models.

## Installation

You can install the package using pip:

```bash
pip install dbshiftSDK
```

## Features

- Convert Informatica XML mappings to Snowflake SQL
- Generate dbt models from Snowflake SQL
- Support for various Informatica transformations
- Automatic handling of mapplets and complex transformations

## Usage

```python
from dbshiftSDK import infa_to_dbt

# Convert XML mappings in a directory
infa_to_dbt('/path/to/your/xml/files')
```

## Input Requirements

- Informatica XML mapping files
- Valid XML format with proper transformation tags
- Source and target definitions in the mapping

## Output

The tool generates:
- Converted SQL files in the 'converted_sql' directory
- dbt models in the 'converted_dbt' directory
- A detailed conversion log file

## Dependencies

- google-generativeai
- tabulate
- argparse

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

## Author

Anand (anandt@systechusa.com)