<h1> AirBnB Stats </h1>

Update: adding some city comparisons at the moment. 

Plot.ly charts don't render on GitHub. Follow this link to see everything: 


<h2> New York City </h2>
http://nbviewer.jupyter.org/github/sar2160/AirBnB-Stats/blob/master/AirBnB.ipynb

<h2> City Comparisons (work in progress) </h2>
http://nbviewer.jupyter.org/github/sar2160/AirBnB-Stats/blob/master/city_comparisons.ipynb




<h1> The Revenue Model </h1>

I am using the InsideAirBnB "San Francisco" Revenue Model, found here http://insideairbnb.com/about.html

Key Assumptions, shared with SF Model: 
* The average stay is 3 nights
* Every other customer leaves a review i.e., review rate of 50%
* The occupancy rate is capped at 70% i.e., each AirBnB can be occupied a max of 21 days a month
    
Key Assumptions, **not** shared with SF Model: 
* Throw out all listings with nightly price > 2500. This number is somewhat arbitrary but prices
        higher than this do not seem believable for a 'nightly' rental, even for the most opulent apartment.
        They may be long-term listings (2500 a month seems reasonable) that are being classified incorrectly 
        by the scraper. 
        

    

<h1> Whale Charts! </h1>

My functions are plotting a kind of Cumulative Distribution that I've heard referred to as a "Whale Chart". They plot the percentage of a total variable of interest e.g., AirBnB revenue in NYC that is captured by a percentage of unique listings. They serve as a way to visualize market structure; a whale chart that is very steep near the left side of the picture shows a market dominated by a few large actors. A more egalitarian market structure would have a more gentle slope.

