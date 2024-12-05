# cli_entry.py

import argparse
# from report_generator import fetch_data, preprocess_data, generate_report, prompt_report_selection
from Kam_Ultimate_Reporter.report_generator import (
    fetch_data, preprocess_data, generate_report, prompt_report_selection
)
def main():
    parser = argparse.ArgumentParser(description="Generate library system reports.")
    parser.add_argument("--url", required=True, help="Base URL for the library system")
    parser.add_argument("--tenant", required=True, help="Tenant identifier")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")

    args = parser.parse_args()

    # Fetch data from API, including header_dict
    dataframes = fetch_data(args.url, args.tenant, args.username, args.password)
    instances_df, Holdings_df, Items_df, df_location, df_mtypes, df_statcode, df_loans, header_dict = dataframes

    # Preprocess data, passing tenant to be used for file naming
    final_df = preprocess_data(instances_df, Holdings_df, Items_df, df_location, df_mtypes, df_statcode, df_loans, header_dict, args.tenant,args.url)

    # Prompt user to select multiple reports
    selected_reports = prompt_report_selection()

    # Loop through each selected report and generate it
    for report_name in selected_reports:
        generate_report(final_df, report_name, args.tenant)

if __name__ == "__main__":
    main()

