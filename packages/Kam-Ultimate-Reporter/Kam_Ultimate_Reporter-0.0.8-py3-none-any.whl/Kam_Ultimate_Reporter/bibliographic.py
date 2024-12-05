import pandas as pd
from functions import (extract_alternative_titles, extract_editions, tenantlogin, makeDfList, make_items, make_holdings,
                       series
, extract_identifier_values, safe_parse, extract_contributor_names,
extract_subject_values,extract_classification_numbers,parse_publication_info_adaptive,
locations,mtypes,statisticalcode,extract_publication_frequencies,
extract_uris,clean_and_concatenate_languages,extract_and_concatenate_notes,fetch_username,map_uuids_to_names,parse_uuid_entry,make_loans,fetch_loan_type_name)
import json
from datetime import datetime, timedelta
import ast
import time
import os
# Get today's date in the specified format
today_date = datetime.now().astimezone().strftime('%Y-%m-%dT20:59:59.999')

url=''
tenant=''
username=''
password=''

token= tenantlogin(url,tenant,username,password)

header_dict = {"x-okapi-tenant": tenant,"x-okapi-token": token }

# Fetch bibliographic records that have been updated since the last run

query = f"metadata.updatedDate>=1900-01-01T21:00:00.000 and metadata.updatedDate<={today_date}"



instances_df=makeDfList(url,header_dict,token,query)

Holdings_df = make_holdings(url,header_dict,token,query)

Items_df = make_items(url,header_dict,token,query)

df_location = locations(url,header_dict,token)

df_mtypes = mtypes(url,header_dict,token)

df_statcode = statisticalcode(url,header_dict,token)

df_loans = make_loans(url,header_dict,token)
######################################################################################################################################
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
    instances_df['extracted_classifications'] = instances_df['classifications'].apply(extract_classification_numbers)
else:
    instances_df['extracted_classifications'] = ''


if 'publication' in instances_df.columns:
    instances_df[['publisher', 'place', 'dateOfPublication']] = instances_df['publication'].apply(parse_publication_info_adaptive).tolist()
else:
    instances_df[['publisher', 'place', 'dateOfPublication']] = ''

location_name = df_location.set_index('id')['name']
material_types = df_mtypes.set_index('id')['name']


if 'publicationFrequency' in instances_df.columns:
    instances_df['publicationFrequency'] = instances_df['publicationFrequency'].apply(safe_parse)
    instances_df['extracted_publicationFrequency'] = instances_df['publicationFrequency'].apply(extract_publication_frequencies)
else:
    instances_df['extracted_publicationFrequency'] = ''

if 'publicationRange' in instances_df.columns:
    instances_df['publicationRange'] = instances_df['publicationRange'].apply(safe_parse)
    instances_df['extracted_publicationRange'] = instances_df['publicationRange'].apply(extract_publication_frequencies)
else:
    instances_df['extracted_publicationRange'] = ''

if 'electronicAccess' in instances_df.columns:
    instances_df['electronicAccess'] = instances_df['electronicAccess'].apply(safe_parse)
    instances_df['extracted_uris'] = instances_df['electronicAccess'].apply(extract_uris)
else:
    instances_df['extracted_uris'] = ''

if 'physicalDescriptions' in instances_df.columns:
    instances_df['physicalDescriptions'] = instances_df['physicalDescriptions'].apply(safe_parse)
    instances_df['extracted_physicalDescriptions'] = instances_df['physicalDescriptions'].apply(extract_publication_frequencies)
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
        username = fetch_username(uuid, header_dict)
        uuid_to_username_created[uuid] = username
        # To avoid hitting rate limits, it's good practice to pause between requests
        time.sleep(0.2)  # Adjust sleep time as needed

    # Replace UUIDs with usernames using the mapping
    instances_df['metadata.createdByUserId'] = instances_df['metadata.createdByUserId'].map(uuid_to_username_created)

    uuid_to_username_updated = {}
    for idx, uuid in enumerate(unique_uuids_updated, start=1):
        print(f'Fetching username for UUID {idx}/{len(unique_uuids_created)}: {uuid}')
        username = fetch_username(uuid, header_dict)
        uuid_to_username_updated[uuid] = username
        # To avoid hitting rate limits, it's good practice to pause between requests
        time.sleep(0.2)  # Adjust sleep time as needed

    instances_df['metadata.updatedByUserId'] = instances_df['metadata.updatedByUserId'].map(uuid_to_username_updated)
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
        name = fetch_loan_type_name(uuid, header_dict)
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
df_merged = pd.merge(final_df, loan_counts, left_on='id',right_on='itemId', how='left')
df_merged['loan_count'] = df_merged['loan_count'].fillna(0).astype(int)
df_merged['lastCheckIn.dateTime'] = pd.to_datetime(df_merged['lastCheckIn.dateTime']).dt.strftime('%d/%m/%Y')
final_df = df_merged.copy()

# Define the CSV file path
excel_file_path = f'Bibliographic_Report_{tenant}.xlsx'
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
    'permanentLoanTypeName' : 'Loan Type',
    'loan_count' : 'Number of Loans'
}

# Apply the renaming in place
final_df.rename(columns=rename_dict, inplace=True)
#################################################################REPORTS############################################################

######################################################REPORTS###########################################################
# Ensure date columns are converted to datetime, handling any errors
final_df['Created Date'] = pd.to_datetime(final_df['Created Date'], errors='coerce').dt.tz_localize(None)
final_df['Updated Date'] = pd.to_datetime(final_df['Updated Date'], errors='coerce').dt.tz_localize(None)

# 1. Books by Created Month
books_by_created_month = final_df.groupby(final_df['Created Date'].dt.to_period('M')).size().reset_index(name='Count')
books_by_created_month.to_excel(f"Books_by_Created_Month.xlsx", index=False)

# 2. Suppress Status Summary
suppress_status_summary = final_df['Suppress from Discovery'].value_counts().reset_index(name='Count')
suppress_status_summary.to_excel(f"Suppress_Status_Summary.xlsx", index=False)

# 3. Top 10 Most Frequently Updated Titles
top_10_updated_titles = final_df['Title'].value_counts().head(10).reset_index(name='Frequency')
top_10_updated_titles.to_excel(f"Top_10_Most_Frequently_Updated_Titles.xlsx", index=False)

# 4. Books by Material Type
books_by_material_type = final_df['Material Type'].value_counts().reset_index(name='Count')
books_by_material_type.to_excel(f"Books_by_Material_Type.xlsx", index=False)

# 5. Average Loan Count
average_loan_count = pd.DataFrame({"Average Loan Count": [final_df['Number of Loans'].mean()]})
average_loan_count.to_excel(f"Average_Loan_Count.xlsx", index=False)

# 6. Recently Added Records
recently_added_records = final_df[final_df['Created Date'] >= datetime.now() - timedelta(days=30)]
recently_added_records.to_excel(f"Recently_Added_Records.xlsx", index=False)

# 7. Top 5 Most Loaned Titles
top_5_loaned_titles = final_df.nlargest(5, 'Number of Loans')[['Title', 'Number of Loans']]
top_5_loaned_titles.to_excel(f"Top_5_Most_Loaned_Titles.xlsx", index=False)

# 8. Staff Suppressed Records
staff_suppressed_records = final_df['Staff Suppress'].value_counts().reset_index(name='Count')
staff_suppressed_records.to_excel(f"Staff_Suppressed_Records.xlsx", index=False)

# 9. Suppressed Records Summary
# List records where either 'Suppress from Discovery' or 'Staff Suppress' is True
suppressed_records = final_df[(final_df['Suppress from Discovery'] == True) | (final_df['Staff Suppress'] == True)]
suppressed_records.to_excel(f"Suppressed_Records_Summary.xlsx", index=False)


# 10. Titles with Alternative Titles
titles_with_alternative_titles = final_df[final_df['Alternative Title'].notnull()]
titles_with_alternative_titles.to_excel(f"Titles_with_Alternative_Titles.xlsx", index=False)

# 11. Records with High Loan Counts
high_loan_counts = final_df[final_df['Number of Loans'] > 10]
high_loan_counts.to_excel(f"Records_with_High_Loan_Counts.xlsx", index=False)

# 12. Titles by Updated User
titles_by_updated_user = final_df.groupby('Updated By')['Title'].count().reset_index(name='Count')
titles_by_updated_user.to_excel(f"Titles_by_Updated_User.xlsx", index=False)

# 13. Edition Distribution
edition_distribution = final_df['Edition'].value_counts().reset_index(name='Count')
edition_distribution.to_excel(f"Edition_Distribution.xlsx", index=False)

# 14. Titles with Item Discovery Suppress
titles_with_item_discovery_suppress = final_df[final_df['Item Discovery Suppress'].notnull()]
titles_with_item_discovery_suppress.to_excel(f"Titles_with_Item_Discovery_Suppress.xlsx", index=False)

# 15. Loaned Items by Location
loaned_items_by_location = final_df.groupby('Location Name')['Number of Loans'].sum().reset_index()
loaned_items_by_location.to_excel(f"Loaned_Items_by_Location.xlsx", index=False)

# 16. Books with Check-in Records
books_with_checkin_records = final_df[final_df['Last Checkin Date'].notnull()]
books_with_checkin_records.to_excel(f"Books_with_Checkin_Records.xlsx", index=False)

# 17. Titles with Copy Numbers
titles_with_copy_numbers = final_df[final_df['Copy Number'].notnull()]
titles_with_copy_numbers.to_excel(f"Titles_with_Copy_Numbers.xlsx", index=False)

# 18. Records Created by User
records_created_by_user = final_df['Created By'].value_counts().reset_index(name='Count')
records_created_by_user.to_excel(f"Records_Created_by_User.xlsx", index=False)

# 19. Books by Loan Type
books_by_loan_type = final_df['Loan Type'].value_counts().reset_index(name='Count')
books_by_loan_type.to_excel(f"Books_by_Loan_Type.xlsx", index=False)

# 20. Titles Without Loans
titles_without_loans = final_df[final_df['Number of Loans'] == 0]
titles_without_loans.to_excel(f"Titles_Without_Loans.xlsx", index=False)

# 21. Loan Activity by Material Type
# Sum loan counts grouped by 'Material Type'
loan_activity_by_material_type = final_df.groupby('Material Type')['Number of Loans'].sum().reset_index()
loan_activity_by_material_type.to_excel(f"Loan_Activity_by_Material_Type.xlsx", index=False)

# 22. Recently Updated Records
# Filter records updated within the last 30 days
recently_updated_records = final_df[final_df['Updated Date'] >= datetime.now() - timedelta(days=30)]
recently_updated_records.to_excel(f"Recently_Updated_Records.xlsx", index=False)

#23 Full bibliographic report
final_df.to_excel(excel_file_path, index=False)
############################################################################################################

