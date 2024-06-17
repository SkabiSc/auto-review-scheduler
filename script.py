import requests
import json
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_ID = os.getenv("BASE_ID")
table_name = "Daily Validations Project Teams"
view_name = 'Auto-agree view'
field_name = 'QC_VALIDATION'
new_value = 'Auto-agree'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

base_url = f'https://api.airtable.com/v0/{BASE_ID}/{table_name}'

def get_records():
    records = []
    offset = None

    while True:
        params = {'view': view_name}
        if offset:
            params['offset'] = offset

        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        records.extend(data['records'])

        offset = data.get('offset')
        if not offset:
            break

    return records

def update_record(record_id, fields):
    url = f'{base_url}/{record_id}'
    payload = {
        'fields': fields
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

records = get_records()

updated_count = 0
not_updated_count = 0
errors = []

for record in records:
    record_id = record['id']
    record_fields = record['fields']

    try:
        if record_fields.get(field_name) == 'Not reviewed':
            update_record(record_id, {field_name: new_value})
            updated_count += 1
        else:
            not_updated_count += 1
    except Exception as e:
        errors.append((record_id, str(e)))

print(f"Total records processed: {len(records)}")
print(f"Records successfully updated: {updated_count}")
print(f"Records not updated (value was not 'Not reviewed'): {not_updated_count}")
if errors:
    print(f"Errors encountered: {len(errors)}")
    for error in errors:
        print(f"Record ID {error[0]}: {error[1]}")
else:
    print("No errors encountered.")

print("Update process completed.")

