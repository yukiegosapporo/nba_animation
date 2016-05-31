import json
import pandas as pd
import os
import numpy as np
from collections import defaultdict
from itertools import compress
import urllib
os.chdir('/Users/yuki/nbamovement')

tid = '1610612744'
gid = '0021500583'

datalink = ("https://raw.githubusercontent.com/neilmj/BasketballData/"
    "master/2016.NBA.Raw.SportVU.Game.Logs/01.13.2016.GSW.at.DEN.7z")

os.system("curl " + datalink + " -o " + os.getcwd() + "/zipped_data")
os.system("7za x " + os.getcwd() + "/zipped_data")

with open('{gid}.json'.format(gid=gid)) as data_file:
    data = json.load(data_file)


home = [data["events"][0]["home"]["players"][i]["playerid"] for 
i in xrange(len(data["events"][0]["home"]["players"]))]

visitors = [data["events"][0]["visitor"]["players"][i]["playerid"] for 
i in xrange(len(data["events"][0]["visitor"]["players"]))]

pids =  home + visitors

os.system('curl "http://stats.nba.com/stats/playbyplayv2?'
    'EndPeriod=0&'
    'EndRange=0&'
    'GameID={gid}&'
    'RangeType=0&'
    'Season=2015-16&'
    'SeasonType=Season&'
    'StartPeriod=0&'
    'StartRange=0" > {cwd}/pbp_{gid}.json'.format(cwd=os.getcwd(), gid=gid))

pbp = pd.DataFrame()
with open("pbp_{gid}.json".format(gid=gid)) as json_file:
    parsed = json.load(json_file)['resultSets'][0]
    pbp = pbp.append(
        pd.DataFrame(parsed['rowSet'], columns=parsed['headers']))

shot_events = pbp[pbp["EVENTMSGTYPE"].isin([1,2,3])]["EVENTNUM"].values
# sub_events = pbp[pbp["EVENTMSGTYPE"]==8]["EVENTNUM"]


raw_json=list()
for event in xrange(len(data['events'])):
    if event in shot_events:
        for num in xrange(0,len(data['events'][event]['moments']),1):
            lstlsts = data['events'][event]['moments'][num][5]
            tmplst=list()
            for pid in [-1]+pids:
                if any(pid in lst for lst in lstlsts)==True:
                    indx = [pid in lst for lst in lstlsts]
                    rw = list(compress(lstlsts,indx))[0]
                    tmplst.append(rw[2])
                    tmplst.append(rw[3])
                else:
                    tmplst.append(None)
                    tmplst.append(None)
            raw_json.append(tmplst)

json_df = pd.DataFrame(raw_json)

# f = lambda x:str(x)
# json_df.fillna(0,inplace=True)
json_df.drop_duplicates(inplace=True)



json_str = json_df.drop_duplicates().values.tolist()
json_str = "var DATA = " + str(json_str)  + "\n"
json_str += "var count1 = " + str(len(home)) + "\n"
json_str += "var count2 = " + str(len(pids)+1) + "\n"
json_str += "var pids = " + str(pids)
with open('nba_data.js', 'w') as f:
     f.write(json_str)








# res=list()
# for event in xrange(len(data['events'])):
#     for num in xrange(len(data['events'][event]['moments'])):
#         for num2 in xrange(len(data['events'][event]['moments'][num][5])):
#             # if ((int(tid) in data['events'][eid]['moments'][num][5][num2]) or 
#             #     (-1 in data['events'][eid]['moments'][num][5][num2])):
#             # if (1610612744 in data['events'][event]['moments'][num][5][num2]):
#             tmplst = data['events'][event]['moments'][num][5][num2]
#             tmplst.append(data['events'][event]['moments'][num][0])
#             tmplst.append(data['events'][event]['moments'][num][2])
#             tmplst.append(data['events'][event]['moments'][num][3])
#             tmplst.append(int(data["events"][event]["eventId"]))
#             res.append(tmplst)


# df = pd.DataFrame(res,columns=
#     ['teamid','playerid','x','y','radius','q','game_clock','shot_clock','eid'])
# df.loc[df["teamid"]==-1,"teamid"] = int(tid)

# df["col"] = df["game_clock"]
# df["col"] = df["col"] + (df["q"]-1)*720
# # df["col"] = df["game_clock"].apply(lambda x:round(x,1))

# minx = df["x"].min()
# maxx = df["x"].max()
# miny = df["y"].min()
# maxy = df["y"].max()

# plt.cla()
# plt.clf()
# plt.close()
# # 
# for col in df['col'].drop_duplicates():
#     sns.set()
#     sns.set_style("white")
#     g = sns.FacetGrid(df[(df["col"]==col)&(df["playerid"]==-1)], hue="radius")
#     g.map(plt.scatter,"x","y")
#     # pl = sns.regplot(x='x',y='y',color='hue',data=dd[dd['eid']==e],fit_reg=False)
#     plt.xlim(minx, maxx)
#     plt.ylim(miny, maxy)
#     plt.axis('off')
#     # g.add_legend();
#     g.savefig('images/mov_{gid}_{eid}.png'.format(eid=col,gid=gid))
#     # pl.figure.savefig('images/mov_{gid}_{eid}.png'.format(eid=e,gid=gid))
#     plt.cla()
#     plt.clf()
#     plt.close()

# jso = list()
# for col in df['col'].drop_duplicates():
#     jso.append(df[(df["col"]==col)&(df["playerid"]==-1)][["x","y"]])


# if str(data['events'][0]['home']['teamid'])==tid:
#     team1='HOMEDESCRIPTION'
#     team2='VISITORDESCRIPTION'
#     name1=data["events"][0]["home"]["abbreviation"]
#     name2=data["events"][0]["visitor"]["abbreviation"]    
# else:
#     team1='VISITORDESCRIPTION'
#     team2='HOMEDESCRIPTION'
#     name1=data["events"][0]["visitor"]["abbreviation"]
#     name2=data["events"][0]["home"]["abbreviation"]    


# os.system('curl "http://stats.nba.com/stats/playbyplayv2?'
#     'EndPeriod=0&'
#     'EndRange=0&'
#     'GameID={gid}&'
#     'RangeType=0&'
#     'Season=2015-16&'
#     'SeasonType=Season&'
#     'StartPeriod=0&'
#     'StartRange=0" > pbp_{gid}.json'.format(gid=gid))

# pbp = pd.DataFrame()
# with open("pbp_{gid}.json".format(gid=gid)) as json_file:
#     parsed = json.load(json_file)['resultSets'][0]
#     pbp = pbp.append(
#         pd.DataFrame(parsed['rowSet'], columns=parsed['headers']))



# rawlabel = list()
# for index, row in pbp.iterrows():
#     # if row['EVENTMSGTYPE'] in [1,2]:
#     if str(data['events'][0]['home']['teamid'])==tid:
#         if ((row[team1] is  None) & (row[team2] is not None)):
#             rawlabel.append([row['PLAYER1_NAME'],row['EVENTNUM']])
#     else:
#         if ((row[team1] is  not None) & (row[team2] is None)):
#             rawlabel.append([row['PLAYER1_NAME'],row['EVENTNUM']])


# label = pd.DataFrame(rawlabel,columns=['label','eid'])

# dd = pd.merge(df,label,on='eid',how='inner')
# dd["hue"] = np.where(dd["playerid"]<0,"ball","player")
# dd = dd[dd["shot_clock"]!=24]
# dd["sec"]=dd["shot_clock"].apply(lambda x:round(x))
# dd["col"] = dd["game_clock"].apply(lambda x:round(x,1))

# os.system('mkdir images')

# minx = df["x"].min()
# maxx = df["x"].max()
# miny = df["y"].min()
# maxy = df["y"].max()


# plt.cla()
# plt.clf()
# plt.close()
# # 
# for col in dd['col'].drop_duplicates():
#     sns.set()
#     sns.set_style("white")
#     g = sns.FacetGrid(dd[dd["col"]==col], hue="playerid")
#     g.map(plt.scatter,"x","y")
#     # pl = sns.regplot(x='x',y='y',color='hue',data=dd[dd['eid']==e],fit_reg=False)
#     plt.xlim(minx, maxx)
#     plt.ylim(miny, maxy)
#     plt.axis('off')
#     # g.add_legend();
#     g.savefig('images/mov_{gid}_{eid}.png'.format(eid=col,gid=gid))
#     # pl.figure.savefig('images/mov_{gid}_{eid}.png'.format(eid=e,gid=gid))
#     plt.cla()
#     plt.clf()
#     plt.close()