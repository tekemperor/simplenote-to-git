from simplenote import Simplenote
from decimal import Decimal
import sys

username = sys.argv[1]
password = sys.argv[2]

simplenote = Simplenote(username, password)

# Retrieve timestamp from .last_update
last_update = Decimal('0')
try:
    with open('notes/.last_update', 'r') as last_update_file:
        last_update = Decimal(last_update_file.read())
except IOError:
    pass

# Get note list (with content)
noteresponse = simplenote.get_note_list()
notes = noteresponse[0]

# Write notes to files
print("Checking %d notes..." % len(notes))
most_recently_updated = last_update
for note in notes:
    if (Decimal(note['modificationDate']) > last_update):
        print('    Writing contents of %s' % note['key'])
        filename = 'notes/%s' % note['key']
        with open(filename, 'w') as f:
            f.write(note['content'])
    else:
        print('    Skipped %s, no changes.' % note['key'])
    if (Decimal(note['modificationDate']) > most_recently_updated):
        most_recently_updated = Decimal(note['modificationDate'])

# Update .last_update timestamp
try:
    with open('notes/.last_update', 'w') as last_update_file:
        last_update_file.write(str(most_recently_updated))
except IOError:
    pass

print('Download of notes complete.')
