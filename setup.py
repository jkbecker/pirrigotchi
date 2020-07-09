import sqlite3
import os
from pathlib import Path

conn = sqlite3.connect(os.sep.join([str(Path.home()), '.pirrigotchi-data.sqlite']))

conn.execute('''CREATE TABLE data (
		_id integer primary key autoincrement,
		timestamp date default CURRENT_TIMESTAMP,
		soiltemp real, 
		soilhum real, 
		lum real, 
		airtemp real, 
		sensor text
	)''')
