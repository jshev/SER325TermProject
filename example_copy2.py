# code by Julianna Shevchenko & Adam Curley

import sys
sys.path.insert(0,"/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
import pymysql as ps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
#%matplotlib inline

conn=ps.connect(host='database-3.cykngyhgdi6y.us-east-1.rds.amazonaws.com',user='admin',passwd='admin123',port=3306,db='SuperbowlDB',autocommit=True);

df=pd.read_sql('SELECT Date, Winner_Pts, Loser_Pts FROM Superbowl ORDER BY Date DESC',conn);
fig1=px.line(x=df['Date'],y=df['Winner_Pts'],title='Points Scored by Winning Team',labels={"x": "Date","y": "Points"});
fig2=px.line(x=df['Date'],y=df['Loser_Pts'],title='Points Scored by Losing Team',labels={"x": "Date","y": "Points"});
#fig1.show();
#fig2.show();

df2=pd.read_sql('SELECT Winner, COUNT(*) FROM Superbowl GROUP BY Winner ORDER BY COUNT(*) DESC',conn);
fig3=px.pie(values=df2['COUNT(*)'],names=df2['Winner'],title='Superbowl Wins By Team');
#fig3.show();

df3=pd.read_sql('SELECT MVP, COUNT(*) FROM Superbowl GROUP BY MVP HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC',conn);
fig4=px.pie(values=df3['COUNT(*)'],names=df3['MVP'],title='Multiple Time MVPs');
#fig4.show();

df4=pd.read_sql('SELECT S.State, Count(*) FROM Superbowl SB, Stadium S WHERE SB.Stadium = S.Name GROUP BY S.State ORDER BY COUNT(*) DESC',conn);
fig5=px.bar(x=df4['State'],y=df4['Count(*)'],title='Superbowls Hosted by States',labels={"x": "States","y": "No of Superbowls Hosted"});
#fig5.show();

df5=pd.read_sql('SELECT Month(Date), COUNT(*) FROM Superbowl GROUP BY Month(Date) ORDER BY Month(Date)',conn);
fig6=px.bar(x=df5['Month(Date)'],y=df5['COUNT(*)'],title='Month of Superbowl',labels={"x": "Numeric Months","y": "No of Superbowls"});
#fig6.show();

with open('p_graph.html', 'a') as f:
    f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig6.to_html(full_html=False, include_plotlyjs='cdn'))

conn.close();

