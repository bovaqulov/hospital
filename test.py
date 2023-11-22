
# Run tis file

from  loader import db

lst: list = ["Pediatricians", "Cardiologists", "Neurologists", "Dentists", "Oncologists"]
for i in lst:
    db.insert_category(i)

