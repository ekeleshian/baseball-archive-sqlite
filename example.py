import pandas as pd
import sqlite3
import matplotlib.pyplot as plt 

conn = sqlite3.connect('lahman2016.sqlite')

query = '''select * from Teams
inner join TeamsFranchises
on Teams.franchID == TeamsFranchises.franchID
where Teams.G >= 150 and TeamsFranchises.active == 'Y';
'''

Teams = conn.execute(query).fetchall()

teams_df = pd.DataFrame(Teams)

cols = ['yearID','lgID','teamID',
'franchID','divID','Rank','G','Ghome','W','L','DivWin',
'WCWin','LgWin','WSWin','R','AB','H','2B','3B','HR','BB',
'SO','SB','CS','HBP','SF','RA','ER','ERA','CG','SHO','SV',
'IPouts','HA','HRA','BBA','SOA','E','DP','FP','name','park',
'attendance','BPF','PPF','teamIDBR','teamIDlahman45','teamIDretro',
'franchID','franchName','active','NAassoc']

teams_df.columns = cols

drop_cols = ['lgID','franchID','divID','Rank','Ghome','L',
'DivWin','WCWin','LgWin','WSWin','SF','name','park','attendance',
'BPF','PPF','teamIDBR','teamIDlahman45','teamIDretro','franchID',
'franchName','active','NAassoc']

df = teams_df.drop(drop_cols, axis = 1)

df = df.drop(['CS', 'HBP'], axis =1)

df['SO'] = df['SO'].fillna(df['SO'].median())
df['DP'] = df['DP'].fillna(df['DP'].median())

def assign_win_bins(W):
	if W<50:
		return 1
	if W >= 50 and W <= 69:
		return 2
	if W >= 70 and W <= 89:
		return 3
	if W >= 90 and W <= 109:
		return 4
	if W >= 110:
		return 5


# print(df['teamID'])


def create_win_bins_graph():
	df['win_bins']= df['W'].apply(assign_win_bins)
	plt.scatter(df['yearID'], df['W'], c=df['win_bins'])
	plt.title('Wins Scatter Plot')
	plt.xlabel('Year')
	plt.ylabel('Wins')

	plt.annotate(label, xy = (x, y), xytext = (0, 0), textcoords = 'offset points')

	plt.show()

def create_age_of_team_graph():
	conn = sqlite3.connect('lahman2016.sqlite')
	query = '''Select yearid,teamid, count(teamid), name 
	from Teams 
	group by teamid;'''
	teamid = conn.execute(query).fetchall()
	teamid_df = pd.DataFrame(teamid)
	cols = ['yearid','teamid', 'count(teamid)', 'name']
	teamid_df.columns =cols

	plt.scatter(teamid_df['yearid'], teamid_df['count(teamid)'])
	plt.xlabel('Year')
	plt.ylabel('Count(teamid)')
	plt.annotate(teamid_df['name'], xy = (teamid_df['yearid'], teamid_df['count(teamid)']))
	plt.show()


# create_win_bins_graph()
# create_age_of_team_graph()