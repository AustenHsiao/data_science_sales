## This project was created for an "Explorations in Data Science" course at PSU
The goal of our project is to understand vizualization techniques used in industry. Since it's only an 8-week course, we focused on comparing and contrasting Python libraries (Seaborn, Matplotlib, and Pandas) with Tableau. 

Some of the pitfalls with using Python come in the details-- for example, we have very basic graph types with Matplotlib. This is remedied by Seaborn, but in both libraries, often times the label positions are difficult to get right and the documentation can be cryptic. 

Some graph-specific issues occur especially in the case of x-labels for bar-charts, when we we're plotting dates, theres no easy way to arrange the tick marks such that the space between tick marks is proportional to the time between labels. In other words, the distance between a tick mark for 2021-01 and 2021-04 would be the same as the distance between 1800-01 and 2021-01, if our data only has these points. The "easy" fix would be to list every date between a start- and end-date, but having too many labels will cause the text to overlap on the graph. 
