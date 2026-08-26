# Data Quality & Reconciliation

A Python project for data quality checks and reconciliation between multiple data sources.

## Overview

This project demonstrates a practical reconciliation workflow using two synthetic transaction datasets.

The script compares two data sources and identifies:

* Duplicate records
* Records missing from one source
* Amount discrepancies
* Status discrepancies
* User mismatches
* Date mismatches
* Exact matches

## Input Data

The project uses two synthetic datasets:

* `source_a.csv`
* `source_b.csv`

Main fields:

* `transaction_id`
* `user_id`
* `transaction_date`
* `amount`
* `status`

The datasets intentionally contain several data quality issues for demonstration purposes.

## Reconciliation Logic

The Python script:

* Loads both datasets
* Checks for duplicate transaction IDs
* Removes duplicates for reconciliation
* Performs an outer join by `transaction_id`
* Identifies records available only in Source A
* Identifies records available only in Source B
* Compares common records field by field
* Separates discrepancies from exact matches
* Builds a reconciliation summary
* Saves the results into an Excel workbook

## Output

The script generates:

`reconciliation_result.xlsx`

The workbook contains the following sheets:

### Summary

High-level reconciliation metrics:

* Rows in Source A
* Rows in Source B
* Duplicate records
* Records available only in Source A
* Records available only in Source B
* Discrepancies
* Exact matches

### Duplicates A

Duplicate transaction IDs found in Source A.

### Duplicates B

Duplicate transaction IDs found in Source B.

### Only in A

Transactions available in Source A but missing from Source B.

### Only in B

Transactions available in Source B but missing from Source A.

### Discrepancies

Transactions available in both sources but containing differences in one or more fields.

### Exact Matches

Transactions that match across both sources.

## Example Data Quality Issues

The synthetic datasets include examples such as:

* Duplicate transaction IDs
* Missing transactions
* Different transaction amounts
* Records existing in only one source

These cases are intentionally included to demonstrate automated reconciliation logic.

## Tech Stack

* Python
* pandas
* openpyxl
* Microsoft Excel

## Project Structure

* `source_a.csv` — synthetic Source A dataset
* `source_b.csv` — synthetic Source B dataset
* `reconciliation.py` — reconciliation script
* `reconciliation_result.xlsx` — generated reconciliation report
* `requirements.txt` — Python dependencies
* `README.md` — project documentation

## How to Run

### 1. Install dependencies

`pip install -r requirements.txt`

### 2. Make sure both datasets are in the project folder

`source_a.csv`

`source_b.csv`

### 3. Run the reconciliation

`python reconciliation.py`

### 4. Check the generated report

`reconciliation_result.xlsx`

## Skills Demonstrated

* Data quality analysis
* Data reconciliation
* Python automation
* Data validation
* Duplicate detection
* Discrepancy analysis
* Data comparison
* Excel reporting
* pandas

## Data Privacy

All data used in this repository is synthetic and created specifically for demonstration purposes.

The repository does not contain confidential, customer, production, or employer data.

## Future Improvements

* Add configurable reconciliation keys
* Add tolerance thresholds for numeric differences
* Add automated Excel formatting
* Add reconciliation status by row
* Add logging
* Add automated summary charts
* Add support for multiple input files
* Add SQL-based reconciliation examples
