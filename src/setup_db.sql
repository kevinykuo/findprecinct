-- Create db:
-- sqlite3 $db_file ".databases"

.separator ,

-- Create people file
CREATE TABLE people (
	fname TEXT NOT NULL
	, lname TEXT NOT NULL
	, addr TEXT
	, city TEXT
	, zip TEXT
	, email TEXT
	, precinct TEXT
);

