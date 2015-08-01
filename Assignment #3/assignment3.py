import csv, sqlite3
import matplotlib.pyplot as plt

with open('datagovdatasetsviewmetrics.csv', 'rb') as vmcsv:
    vmcsv_reader = csv.DictReader(vmcsv)
    vmfields = vmcsv_reader.fieldnames
    to_db = [(unicode(field[vmfields[0]], "utf8"), unicode(field[vmfields[1]], "utf8"), unicode(field[vmfields[2]], "utf8"), unicode(field[vmfields[3]], "utf8"), unicode(field[vmfields[4]], "utf8")) for field in vmcsv_reader]

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS vmtable;')
cur.execute('CREATE TABLE vmtable(id TEXT, dataset TEXT, org TEXT, views INTEGER, date TEXT);')
cur.executemany('INSERT INTO vmtable (id, dataset, org, views, date) VALUES (?, ?, ?, ?, ?);', to_db)
con.commit()

max_org_length = cur.execute('SELECT org_length FROM ( SELECT LENGTH(org) AS org_length, SUM(views) AS sum_views FROM vmtable GROUP BY id ORDER BY sum_views DESC LIMIT 10) as top10views ORDER BY org_length DESC LIMIT 1;').fetchone()[0]
cur.execute('SELECT org, SUM(views) AS sum_views FROM vmtable GROUP BY org ORDER BY sum_views DESC LIMIT 10;')
top_orgs = cur.fetchall()
con.close()

org_names = []
org_views = []
for row in top_orgs:
    org_names.append(row[0][:13]+'.\n'+row[0].split()[-1])
    org_views.append(row[1])
    print "{:<{}}  {}".format(row[0], max_org_length, row[1])

fig = plt.figure()
ax = fig.add_subplot(111)
index = range(len(org_views))
width = .85

rects1 = ax.bar(range(len(org_views)), org_views, width,
                color='black')

ax.set_xlim(-(1-width),len(index))
ax.set_ylabel('Views')
ax.set_title('Views by Organization')
xTickMarks = org_names
ax.set_xticks(range(len(org_views)))
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)

plt.tight_layout()
plt.show()
