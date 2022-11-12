# Interactive_Data_Science_Projects
05-389 Interactive Data Science (Fall 2019) is a project-oriented course which aims at providing students with the tools to understand data and build data-driven interactive systems. In this course, students learn about data science and the entire data pipeline from collecting, analyzing to interacting with data.

The projects more or less follow these steps:
1. Propose a question;
2. Clean, modify raw data;
3. Create exploratory analysis including data visualization to answer the question.

## Project 1 - Cleaning, Exploring, and Answering Questions with Data
**Question**

Which movie genre makes the most money? 

**Visualization**

<p align = "center">
<img src="https://github.com/Okrasee/Interactive_Data_Science_Projects/blob/master/distribution.jpeg" alt="alt text">
</p>

Use `pandas`, `matplotlib`, `operator` packages

## Project 2 - Querying and Structuring Data from the Twitter API
**Question**

What do people think about Taylor Swift’s latest album ‘Lover’?

**Visualization**


<p align = "center">
<img src="https://github.com/Okrasee/Interactive_Data_Science_Projects/blob/master/pie_chart.jpeg" alt="alt text" width="600">
</p>


Use sentiment analysis by Vader to find out the percentages of positive, neutral, positive tweets

```
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentiment = SentimentIntensityAnalyzer()

score = sentiment.polarity_scores(text)

lb = score['compound']
```

## Project 3 - Visual Narrative of Personal Mobile Data Set
**Question**

Which mobile apps I use most frequently over the past two weeks? Was the trend consistent?

**Visualization**

<p align = "center">
<img src="https://github.com/Okrasee/Interactive_Data_Science_Projects/blob/master/instragram.jpeg" alt="alt text">
</p>

Use `plotly` library to create dropdown menu
```
import plotly.graph_objects as go
fig = go.Figure()
```
