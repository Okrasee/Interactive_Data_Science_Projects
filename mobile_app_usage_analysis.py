import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('My mobile data.csv')

# clean and aggregate data to figure out each app usage by day
df = df.groupby(['day', 'application'])['package_name'].count().reset_index()

df = df.rename(columns={"package_name": "count"})

df['day'] =pd.to_datetime(df['day'])

df = df.sort_values(by = 'day')

# Initialize figure
fig, fig1, fig2 = go.Figure(), go.Figure(), go.Figure()

application_list = list(set(df.application))

app_annotations = []

# aggregate data to figure out each app usage in overall over the two weeks
df_grouped = df.groupby('application')['count'].sum().reset_index()

df_grouped = df_grouped.sort_values(by = 'count', ascending = False)

fig1.add_trace(go.Bar(x = df_grouped['application'], y = df_grouped['count']))

fig1.update_layout(title_text="Mobile Apps Usage Comparison 09/28-10/12")

fig1.show()

df_day = df.groupby('day')['count'].sum().reset_index()

# this figure shows the total amount of (instead of individual) app usage by day
fig2.add_trace(go.Scatter(x=list(df_day['day']),
       			          y=list(df_day['count']),
       			          name='Total App Usage By Day',
           		          line=dict(color="#003366")))

fig2.update_layout(title_text="Total App Usage By Day")

fig2.show()

# add trace for each app trace, i.e. trend over the two weeks
# loop through the application list
for app in application_list:

	df1 = df[df['application'] == app]

	fig.add_trace(
    	go.Scatter(x=list(df1['day']),
       			   y=list(df1['count']),
       			   name=str(app),
           		   line=dict(color="#003366")))

	# Add Annotations and Buttons
	app_annotations.append([dict(x="2019-09-28",
	                         y=sum(list(df1['count']))/len(list(df1['count'])),
	                         xref="x", yref="y",
	                         text="Average:<br> %.3f" % float(sum(list(df1['count']))/len(list(df1['count']))),
	                         ax=-20, ay=0),
	                    dict(x=df1['day'][df1['count'].idxmax()],
	                         y=max(list(df1['count'])),
	                         xref="x", yref="y",
	                         text="Max:<br> %.3f" % float(max(list(df1['count']))),
	                         ax=0, ay=-20),
	                    dict(x=df1['day'][df1['count'].idxmin()],
	                         y=min(list(df1['count'])),
	                         xref="x", yref="y",
	                         text="Min:<br> %.3f" % float(min(list(df1['count']))),
	                         ax=0, ay=20)])

def enable_button(i):

	button_lst = [False] * len(app_annotations)

	button_lst[i] = True

	return button_lst

# create a dropdown menu which includes all apps
# pick an app from the menu, one will see the trend of its usage
menu = []

for i in range(len(app_annotations)):

	app = list(set(df.application))[i]

	curr_menu = dict(label = str(app),
				 method = "update",
				 args=[{"visible": enable_button(i)},
                           {"title": "App: " + str(app),
                            "annotations": app_annotations[i]}])

	menu.append(curr_menu)

fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            active=0,
            buttons=list([dict(label = "All",
				 method = "update",
				 args=[{"visible": enable_button(i)},
                           {"title": "My Mobile Apps",
                            "annotations": []}])] + menu)
        )
    ])

# Set title
fig.update_layout(title_text="My Mobile Apps Usage")

fig.show()