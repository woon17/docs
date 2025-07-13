# connect to kdb+ manually
1. terminal: q dash.q -p 10001 -u 1

## kxDashabord: CSV as the data source
1. terminal: q -p 5050
2. terminal: q)PivotData: ("zffffj"; enlist ",") 0: `:~/Documents/q/data/EURTRY.csv
3. terminal: q)PivotData
4. web kx dashboard to create a new connection with port 5050
5. now able to use the PivotData as the data source
---

## Stream Real Time Data