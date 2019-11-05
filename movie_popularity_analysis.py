import pandas as pd

import ast

import matplotlib

import matplotlib.pyplot as plt

import numpy as np

import operator 

matplotlib.use('Agg')

df = pd.read_csv('Movies.csv', low_memory = False)

# drop duplicates
df = df.drop_duplicates()

# remove invalid genre entries
df = df[df['genres'] != '[]']

df = df[df['genres'].notnull()]

# remove zero runtime movies
df = df[df['runtime'] != 0]

genres = list(df.genres)

genres_lst = []

# loop through each row
for curr_genre in genres:

    # remove the quote marks
	curr_genre = curr_genre[1:-1]

	lst = []

	# loop through the genres for each movie
	for i in range(len(curr_genre)):

		# a new genre type
		if curr_genre[i] == "{": substr = "{"

		# the last characteristic of a genre type
		elif curr_genre[i] == "}":

			substr += "}"

			# convert string to a dictionary
			my_dict = ast.literal_eval(substr)

			# append the genre type to a list as a dictionary item
			lst.append(my_dict)

		else: 

			substr += curr_genre[i]

	genres_lst.append(lst)

# convert the column from string type into list type 
df['genres'] = genres_lst

# create a dictionary with genres as keys and revenue as values
rev_dict = {}

genres = list(df.genres)

rev = list(df.revenue)

for i in range(len(genres)):

	for j in genres[i]:

		# create a new key if the genre does not exist in the dictionary
		if j['name'] in rev_dict: rev_dict[j['name']] += rev[i] / (10 ** 9)

		# add the revenue to its corresponding genre key
		else: rev_dict[j['name']] = rev[i] / (10 ** 9) 

# sort the dictionary in descending order by total revenue
sorted_d = dict(sorted(rev_dict.items(), key=operator.itemgetter(1), reverse=True))

for key in sorted_d:

	sorted_d[key] = float("{0:.2f}".format(sorted_d[key]))

# plot the bar chart in a vertical fashion
plt.rcdefaults()

plt.tight_layout()

fig, ax = plt.subplots()

ax.barh(list(sorted_d.keys()), list(sorted_d.values()), align='center')

ax.set_yticks(np.arange(len(list(sorted_d.keys()))))

ax.set_yticklabels(list(sorted_d.keys()))

ax.invert_yaxis()  

ax.set_xlabel('Total revenue in billion U.S. dollars')

ax.set_title('Which movie genre makes the most money?')

rects = ax.patches

for rect in rects:

    # Get X and Y placement of label from rect
    x_value = rect.get_width()
    
    y_value = rect.get_y() + rect.get_height() / 2

    # Use X value as label 
    label = "{:.1f}".format(x_value)

    # Create annotation
    plt.annotate(
        label,                      
        (x_value, y_value),         
        xytext=(3, 0),          
        fontsize = 6,
        textcoords="offset points", 
        va='center',                
        ha='left')           

plt.savefig('distribution.png', bbox_inches = "tight")




