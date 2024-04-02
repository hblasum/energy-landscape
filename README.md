Enhance data scraped from https://github.com/lf-energy/lfenergy-landscape

Files: 

* analyse.py: take the landscape.yml and dump into sqlite3.
* github_stars.py: take the sqlite3, add github stars, dump to tsv.
* license_add.py: take an Excel (generated manually from tsv), add a column for license information
* lastactivity_add.py: take that Excel again add columns for data of last commit, number of commits since 2023-01-01 (limited to 300 by Github API), and number of different committers within these commits
* output-full.xlsx: result of the above steps, that is Linux Foundation Energy landscape enhanced by license, popularity and commit activity information

Notes:

* Support by Google Gemini is acknowledged.
* The Github API access tokens are invalid, use your own (you get 5000 accesses/hour, this suffices for running each step).
	
