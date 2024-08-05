###  ([Report](/report.pdf))

# Team Seb 3b Submission
COVID-19 Data Analysis and Visualization

Setup and Running:

1. Data Processing:
	- Install required packages: pip install -r requirements.txt
	- Run:  python .\group_sort_data.py
  	  - ... with logging:  python .\group_sort_data.py > logs.txt 2>&1

2. Frontend Visualization:
	- Navigate to React app: cd covid-data-visualization
	- Add data to public directory: public/grouped_sorted_covid_bubble.json
	- Install dependencies: npm install
	- Start server: npm start
	- View at: http://localhost:3000

Files:
- covid.json: Raw data
- group_sort_data.py: Processing script
- grouped_sorted_covid_bubble.json: Bubble Sort result
- grouped_sorted_covid_merge.json: Merge Sort result
- covid-data-visualization/: React app

Note: Ensure covid.json is in the same directory as group_sort_data.py