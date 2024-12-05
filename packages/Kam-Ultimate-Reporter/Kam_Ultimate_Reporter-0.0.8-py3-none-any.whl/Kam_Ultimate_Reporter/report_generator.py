# report_generator.py

import pandas as pd
from datetime import datetime, timedelta
import time
import inquirer
# from functions import (
#     extract_alternative_titles, extract_editions, tenantlogin, makeDfList, make_items, make_holdings,
#     series, extract_identifier_values, safe_parse, extract_contributor_names, extract_subject_values,
#     extract_classification_numbers, parse_publication_info_adaptive, locations, mtypes,
#     statisticalcode, extract_publication_frequencies, extract_uris, clean_and_concatenate_languages,
#     extract_and_concatenate_notes, fetch_username, map_uuids_to_names, parse_uuid_entry, make_loans,
#     fetch_loan_type_name
# )

from Kam_Ultimate_Reporter.functions import (
    extract_alternative_titles, extract_editions, tenantlogin, makeDfList, make_items, make_holdings,
    series, extract_identifier_values, safe_parse, extract_contributor_names, extract_subject_values,
    extract_classification_numbers, parse_publication_info_adaptive, locations, mtypes,
    statisticalcode, extract_publication_frequencies, extract_uris, clean_and_concatenate_languages,
    extract_and_concatenate_notes, fetch_username, map_uuids_to_names, parse_uuid_entry, make_loans,
    fetch_loan_type_name
)

import ast



def fetch_data(url, tenant, username, password):
    today_date = datetime.now().astimezone().strftime('%Y-%m-%dT20:59:59.999')
    token = tenantlogin(url, tenant, username, password)
    header_dict = {"x-okapi-tenant": tenant, "x-okapi-token": token}

    # Fetch DataFrames from the API
    instances_df = makeDfList(url, header_dict, token,
                              f"metadata.updatedDate>=1900-01-01T21:00:00.000 and metadata.updatedDate<={today_date}")
    Holdings_df = make_holdings(url, header_dict, token,
                                f"metadata.updatedDate>=1900-01-01T21:00:00.000 and metadata.updatedDate<={today_date}")
    Items_df = make_items(url, header_dict, token,
                          f"metadata.updatedDate>=1900-01-01T21:00:00.000 and metadata.updatedDate<={today_date}")
    df_location = locations(url, header_dict, token)
    df_mtypes = mtypes(url, header_dict, token)
    df_statcode = statisticalcode(url, header_dict, token)
    df_loans = make_loans(url, header_dict, token)

    return instances_df, Holdings_df, Items_df, df_location, df_mtypes, df_statcode, df_loans,header_dict


def preprocess_data(instances_df, Holdings_df, Items_df, df_location, df_mtypes, df_statcode, df_loans,header_dict,tenant,url):
    # Applying various transformations and extracting specific fields as in the original code.
    # Preprocessing code omitted for brevity; include your extraction and merging logic here
    # Check if 'alternativeTitles' column exists, and apply extraction if present
    if 'alternativeTitles' in instances_df.columns:
        instances_df['alternativeTitlesExtracted'] = instances_df['alternativeTitles'].apply(extract_alternative_titles)
    else:
        instances_df['alternativeTitlesExtracted'] = ''

    # Check if 'editions' column exists, and apply extraction if present
    if 'editions' in instances_df.columns:
        instances_df['editionsExtracted'] = instances_df['editions'].apply(extract_editions)
    else:
        instances_df['editionsExtracted'] = ''

    if 'series' in instances_df.columns:
        instances_df['extracted_series'] = instances_df['series'].apply(series)
    else:
        instances_df['extracted_series'] = ''

    # Apply the function and create a new column
    if 'identifiers' in instances_df.columns:
        instances_df['identifiers'] = instances_df['identifiers'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        instances_df['extracted_identifiers'] = instances_df['identifiers'].apply(extract_identifier_values)
    else:
        instances_df['extracted_identifiers'] = ''

    if 'contributors' in instances_df.columns:
        instances_df['contributors'] = instances_df['contributors'].apply(safe_parse)
        instances_df['extracted_contributors'] = instances_df['contributors'].apply(extract_contributor_names)
    else:
        instances_df['extracted_contributors'] = ''

    if 'subjects' in instances_df.columns:
        instances_df['subjects'] = instances_df['subjects'].apply(safe_parse)
        instances_df['extracted_subjects'] = instances_df['subjects'].apply(extract_subject_values)
    else:
        instances_df['extracted_subjects'] = ''

    if 'classifications' in instances_df.columns:
        instances_df['classifications'] = instances_df['classifications'].apply(safe_parse)
        instances_df['extracted_classifications'] = instances_df['classifications'].apply(
            extract_classification_numbers)
    else:
        instances_df['extracted_classifications'] = ''

    if 'publication' in instances_df.columns:
        instances_df[['publisher', 'place', 'dateOfPublication']] = instances_df['publication'].apply(
            parse_publication_info_adaptive).tolist()
    else:
        instances_df[['publisher', 'place', 'dateOfPublication']] = ''

    location_name = df_location.set_index('id')['name']
    material_types = df_mtypes.set_index('id')['name']

    if 'publicationFrequency' in instances_df.columns:
        instances_df['publicationFrequency'] = instances_df['publicationFrequency'].apply(safe_parse)
        instances_df['extracted_publicationFrequency'] = instances_df['publicationFrequency'].apply(
            extract_publication_frequencies)
    else:
        instances_df['extracted_publicationFrequency'] = ''

    if 'publicationRange' in instances_df.columns:
        instances_df['publicationRange'] = instances_df['publicationRange'].apply(safe_parse)
        instances_df['extracted_publicationRange'] = instances_df['publicationRange'].apply(
            extract_publication_frequencies)
    else:
        instances_df['extracted_publicationRange'] = ''

    if 'electronicAccess' in instances_df.columns:
        instances_df['electronicAccess'] = instances_df['electronicAccess'].apply(safe_parse)
        instances_df['extracted_uris'] = instances_df['electronicAccess'].apply(extract_uris)
    else:
        instances_df['extracted_uris'] = ''

    if 'physicalDescriptions' in instances_df.columns:
        instances_df['physicalDescriptions'] = instances_df['physicalDescriptions'].apply(safe_parse)
        instances_df['extracted_physicalDescriptions'] = instances_df['physicalDescriptions'].apply(
            extract_publication_frequencies)
    else:
        instances_df['extracted_physicalDescriptions'] = ''

    if 'languages' in instances_df.columns:
        instances_df['languages'] = instances_df['languages'].apply(safe_parse)
        instances_df['extracted_languages'] = instances_df['languages'].apply(clean_and_concatenate_languages)
    else:
        instances_df['extracted_languages'] = ''

    if 'notes' in instances_df.columns:
        instances_df['notes'] = instances_df['notes'].apply(safe_parse)
        instances_df['extracted_notes'] = instances_df['notes'].apply(extract_and_concatenate_notes)
    else:
        instances_df['extracted_notes'] = ''

    if 'metadata.createdByUserId' in instances_df.columns:
        # Extract unique UUIDs, excluding any NaN or empty entries
        unique_uuids_created = instances_df['metadata.createdByUserId'].dropna().unique()
        # Extract unique UUIDs, excluding any NaN or empty entries
        unique_uuids_updated = instances_df['metadata.updatedByUserId'].dropna().unique()

        # Initialize an empty dictionary to store UUID to username mapping
        uuid_to_username_created = {}

        # Iterate over unique UUIDs and fetch usernames
        for idx, uuid in enumerate(unique_uuids_created, start=1):
            print(f'Fetching username for UUID {idx}/{len(unique_uuids_created)}: {uuid}')
            username = fetch_username(uuid, header_dict,url)
            uuid_to_username_created[uuid] = username
            # To avoid hitting rate limits, it's good practice to pause between requests
            time.sleep(0.2)  # Adjust sleep time as needed

        # Replace UUIDs with usernames using the mapping
        instances_df['metadata.createdByUserId'] = instances_df['metadata.createdByUserId'].map(
            uuid_to_username_created)

        uuid_to_username_updated = {}
        for idx, uuid in enumerate(unique_uuids_updated, start=1):
            print(f'Fetching username for UUID {idx}/{len(unique_uuids_created)}: {uuid}')
            username = fetch_username(uuid, header_dict,url)
            uuid_to_username_updated[uuid] = username
            # To avoid hitting rate limits, it's good practice to pause between requests
            time.sleep(0.2)  # Adjust sleep time as needed

        instances_df['metadata.updatedByUserId'] = instances_df['metadata.updatedByUserId'].map(
            uuid_to_username_updated)
    else:
        instances_df['metadata.createdByUserId'] = ''
        instances_df['metadata.updatedByUserId'] = ''
    ########################################################################################################################

    if 'instanceId' in Holdings_df.columns:
        merged_df = instances_df.merge(Holdings_df, left_on='id', right_on='instanceId', how='left', indicator=True,
                                       )
    else:

        merged_df = instances_df.copy()

    # Merge merged instances-holdings with items
    if 'holdingsRecordId' in Items_df.columns:
        final_df = merged_df.merge(
            Items_df,
            left_on='id_y',
            right_on='holdingsRecordId',
            how='left'
        )
    else:
        final_df = merged_df.copy()  # No items data to merge, keep instances-holdings as is

    #####################################################################################################
    if 'permanentLocationId_x' in final_df.columns:
        final_df['location_name'] = final_df['permanentLocationId_x'].map(location_name)
    else:
        final_df['location_name'] = ''

    if 'materialTypeId' in final_df.columns:
        final_df['Material_name'] = final_df['materialTypeId'].map(material_types)
    else:
        final_df['Material_name'] = ''

    if 'accessionNumber' in final_df.columns:
        final_df['Accession Number'] = final_df['accessionNumber']
    else:
        final_df['Accession Number'] = ''

    if 'notes' in final_df.columns:
        final_df['notes'] = final_df['notes'].apply(safe_parse)
        final_df['Item_notes'] = final_df['notes'].apply(extract_and_concatenate_notes)
    else:
        final_df['Item_notes'] = ''

    if 'statisticalCodeIds' in final_df.columns:
        final_df['statisticalCodeIds'] = final_df['statisticalCodeIds'].apply(parse_uuid_entry)

        # Create the mapping dictionary
        id_to_name = df_statcode.set_index('id')['name'].to_dict()

        final_df['statisticalCodeNames'] = final_df['statisticalCodeIds'].apply(
            lambda x: map_uuids_to_names(x, id_to_name, separator='|')
        )

        final_df['statisticalCodeNames'] = final_df['statisticalCodeNames'].fillna('No Statistical Codes')
    else:
        final_df['statisticalCodeNames'] = ''

    if 'circulationNotes' in final_df.columns:
        final_df['circulationNotes'] = final_df['circulationNotes'].apply(safe_parse)
        final_df['extracted_circulationNotes'] = final_df['circulationNotes'].apply(extract_and_concatenate_notes)
    else:
        final_df['extracted_circulationNotes'] = ''

    if 'permanentLoanTypeId' in final_df.columns:
        unique_loan_type_ids = final_df['permanentLoanTypeId'].dropna().unique()
        loan_type_mapping = {}

        for idx, uuid in enumerate(unique_loan_type_ids, start=1):
            print(f'Fetching loan type name for UUID {idx}/{len(unique_loan_type_ids)}: {uuid}')
            name = fetch_loan_type_name(uuid, header_dict,url)
            if name:
                loan_type_mapping[uuid] = name
            else:
                loan_type_mapping[uuid] = 'Unknown'  # Assign a default value or handle as needed
            # To avoid hitting rate limits, it's good practice to pause between requests
            time.sleep(0.1)  # Adjust sleep time as needed
        final_df['permanentLoanTypeName'] = final_df['permanentLoanTypeId'].map(loan_type_mapping)
    else:
        final_df['permanentLoanTypeName'] = ''
    #######################################################################################################
    loan_counts = df_loans.groupby('itemId').size().reset_index(name='loan_count')
    df_merged = pd.merge(final_df, loan_counts, left_on='id', right_on='itemId', how='left')
    df_merged['loan_count'] = df_merged['loan_count'].fillna(0).astype(int)
    df_merged['lastCheckIn.dateTime'] = pd.to_datetime(df_merged['lastCheckIn.dateTime']).dt.strftime('%d/%m/%Y')
    final_df = df_merged.copy()

    # Define the CSV file path
    excel_file_path = f'Bibliographic_Report_{tenant}.csv'
    # List of columns to keep
    columns_to_keep = [
        'hrid_x',
        'title',
        'discoverySuppress_x',
        'metadata.createdDate_x',
        'metadata.createdByUserId_x',
        'metadata.updatedDate_x',
        'metadata.updatedByUserId_x',
        'staffSuppress',
        'alternativeTitlesExtracted',
        'editionsExtracted',
        'extracted_series',
        'extracted_identifiers',
        'extracted_contributors',
        'extracted_subjects',
        'extracted_classifications',
        'publisher',
        'place',
        'dateOfPublication',
        'extracted_publicationFrequency',
        'extracted_publicationRange',
        'extracted_uris',
        'extracted_physicalDescriptions',
        'extracted_languages',
        'extracted_notes',
        'callNumberFull',
        'barcode',
        'Item_notes',
        'extracted_circulationNotes',
        'statisticalCodeNames',
        'status.name',
        'discoverySuppress',
        'itemLevelCallNumberFull',
        'copyNumber_y',
        'lastCheckIn.dateTime',
        'volume',
        'location_name',
        'Material_name',
        'Accession Number',
        'permanentLoanTypeName',
        'loan_count'
    ]
    # Identify missing columns
    missing_cols = set(columns_to_keep) - set(final_df.columns)

    if missing_cols:
        print(f"The following columns are missing and will be ignored: {missing_cols}")
    else:
        print("All specified columns are present in the DataFrame.")

    final_df = final_df[columns_to_keep]

    # Define the renaming mapping
    rename_dict = {

        'hrid_x': 'HRID',
        'title': 'Title',
        'discoverySuppress_x': 'Suppress from Discovery',
        'metadata.createdDate_x': 'Created Date',
        'metadata.createdByUserId_x': 'Created By',
        'metadata.updatedDate_x': 'Updated Date',
        'metadata.updatedByUserId_x': 'Updated By',
        'staffSuppress': 'Staff Suppress',
        'alternativeTitlesExtracted': 'Alternative Title',
        'editionsExtracted': 'Edition',
        'extracted_series': 'Series',
        'extracted_identifiers': 'Identifiers',
        'extracted_contributors': 'Contributors',
        'extracted_subjects': 'Subjects',
        'extracted_classifications': 'Call Number',
        'publisher': 'Publisher',
        'place': 'Publication Place',
        'dateOfPublication': 'Date of Publication',
        'extracted_publicationFrequency': 'Publication Frequency',
        'extracted_publicationRange': 'Publication Range',
        'extracted_uris': 'URLs',
        'extracted_physicalDescriptions': 'Physical Description',
        'extracted_languages': 'Languages',
        'extracted_notes': 'Instance Notes',
        'callNumberFull': 'Holding Call Number',
        'barcode': 'Barcode',
        'Item_notes': 'Item Notes',
        'extracted_circulationNotes': 'Circulation Notes',
        'statisticalCodeNames': 'Statistical Codes',
        'status.name': 'Item Status',
        'discoverySuppress': 'Item Discovery Suppress',
        'itemLevelCallNumberFull': 'Item Call Number',
        'copyNumber_y': 'Copy Number',
        'lastCheckIn.dateTime': 'Last Checkin Date',
        'volume': 'Volume',
        'location_name': 'Location Name',
        'Material_name': 'Material Type',
        'permanentLoanTypeName': 'Loan Type',
        'loan_count': 'Number of Loans'
    }

    # Apply the renaming in place
    final_df.rename(columns=rename_dict, inplace=True)
    # Ensure date columns are converted to datetime, handling any errors
    final_df['Created Date'] = pd.to_datetime(final_df['Created Date'], errors='coerce').dt.tz_localize(None)
    final_df['Updated Date'] = pd.to_datetime(final_df['Updated Date'], errors='coerce').dt.tz_localize(None)
    # Return the final processed DataFrame
    return final_df


def generate_report(final_df, report_name,tenant):
    # Define all reports as dictionary functions
    reports = {
        "Books by Created Month": lambda: final_df.groupby(
            final_df['Created Date'].dt.to_period('M')).size().reset_index(name='Count').to_csv(
            "Books_by_Created_Month.csv", index=False),
        "Suppress Status Summary": lambda: final_df['Suppress from Discovery'].value_counts().reset_index(
            name='Count').to_csv("Suppress_Status_Summary.csv", index=False),
        "Top 10 Most Frequently Updated Titles": lambda: final_df['Title'].value_counts().head(10).reset_index(
            name='Frequency').to_csv("Top_10_Most_Frequently_Updated_Titles.csv", index=False),
        "Books by Material Type": lambda: final_df['Material Type'].value_counts().reset_index(name='Count').to_csv(
            "Books_by_Material_Type.csv", index=False),
        "Average Loan Count": lambda: pd.DataFrame(
            {"Average Loan Count": [final_df['Number of Loans'].mean()]}).to_csv("Average_Loan_Count.csv",
                                                                                   index=False),
        "Recently Added Records": lambda: final_df[
            final_df['Created Date'] >= datetime.now() - timedelta(days=30)].to_csv("Recently_Added_Records.csv",
                                                                                      index=False),
        "Top 5 Most Loaned Titles": lambda: final_df.nlargest(5, 'Number of Loans')[
            ['Title', 'Number of Loans']].to_csv("Top_5_Most_Loaned_Titles.csv", index=False),
        "Staff Suppressed Records": lambda: final_df['Staff Suppress'].value_counts().reset_index(
            name='Count').to_csv("Staff_Suppressed_Records.csv", index=False),
        "Suppressed Records Summary": lambda: final_df[
            (final_df['Suppress from Discovery'] == True) | (final_df['Staff Suppress'] == True)].to_csv(
            "Suppressed_Records_Summary.csv", index=False),
        "Titles with Alternative Titles": lambda: final_df[final_df['Alternative Title'].notnull()].to_csv(
            "Titles_with_Alternative_Titles.csv", index=False),
        "Records with High Loan Counts": lambda: final_df[final_df['Number of Loans'] > 10].to_csv(
            "Records_with_High_Loan_Counts.csv", index=False),
        "Titles by Updated User": lambda: final_df.groupby('Updated By')['Title'].count().reset_index(
            name='Count').to_csv("Titles_by_Updated_User.csv", index=False),
        "Edition Distribution": lambda: final_df['Edition'].value_counts().reset_index(name='Count').to_csv(
            "Edition_Distribution.csv", index=False),
        "Titles with Item Discovery Suppress": lambda: final_df[final_df['Item Discovery Suppress'].notnull()].to_csv(
            "Titles_with_Item_Discovery_Suppress.csv", index=False),
        "Loaned Items by Location": lambda: final_df.groupby('Location Name')[
            'Number of Loans'].sum().reset_index().to_csv("Loaned_Items_by_Location.csv", index=False),
        "Books with Check-in Records": lambda: final_df[final_df['Last Checkin Date'].notnull()].to_csv(
            "Books_with_Checkin_Records.csv", index=False),
        "Titles with Copy Numbers": lambda: final_df[final_df['Copy Number'].notnull()].to_csv(
            "Titles_with_Copy_Numbers.csv", index=False),
        "Records Created by User": lambda: final_df['Created By'].value_counts().reset_index(name='Count').to_csv(
            "Records_Created_by_User.csv", index=False),
        "Books by Loan Type": lambda: final_df['Loan Type'].value_counts().reset_index(name='Count').to_csv(
            "Books_by_Loan_Type.csv", index=False),
        "Titles Without Loans": lambda: final_df[final_df['Number of Loans'] == 0].to_csv("Titles_Without_Loans.csv",
                                                                                            index=False),
        "Loan Activity by Material Type": lambda: final_df.groupby('Material Type')[
            'Number of Loans'].sum().reset_index().to_csv("Loan_Activity_by_Material_Type.csv", index=False),
        "Recently Updated Records": lambda: final_df[
            final_df['Updated Date'] >= datetime.now() - timedelta(days=30)].to_csv("Recently_Updated_Records.csv",
                                                                                      index=False),
        "Full Bibliographic Report": lambda: final_df.to_csv(f"Bibliographic_Report_{tenant}.csv", index=False)
    }

    # Execute the selected report
    if report_name in reports:
        reports[report_name]()
        print(f"{report_name} report generated successfully!")
    else:
        print("Invalid report selection.")


def prompt_report_selection():
    # Define report choices
    report_choices = [
        "Books by Created Month", "Suppress Status Summary", "Top 10 Most Frequently Updated Titles",
        "Books by Material Type", "Average Loan Count", "Recently Added Records", "Top 5 Most Loaned Titles",
        "Staff Suppressed Records", "Suppressed Records Summary", "Titles with Alternative Titles",
        "Records with High Loan Counts", "Titles by Updated User", "Edition Distribution",
        "Titles with Item Discovery Suppress", "Loaned Items by Location", "Books with Check-in Records",
        "Titles with Copy Numbers", "Records Created by User", "Books by Loan Type", "Titles Without Loans",
        "Loan Activity by Material Type", "Recently Updated Records", "Full Bibliographic Report"
    ]

    questions = [
        inquirer.Checkbox("reports", message="Select the reports to generate", choices=report_choices)
    ]
    selected_reports = inquirer.prompt(questions)['reports']
    return selected_reports
