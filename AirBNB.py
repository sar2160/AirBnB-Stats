
import pandas as pd
import datetime as dt
from numpy import where, linspace

def process_city_data():

    listings = pd.read_csv('listings.csv')
    reviews = pd.read_csv('reviews.csv')
    
    reviews.date = pd.to_datetime(reviews.date)


    ## Confining the reviews to year 2015 + 

    reviews.set_index('date',inplace=True)
    reviews.sort(ascending=True,inplace=True)


    start = reviews.index.searchsorted(dt.datetime(2015, 1, 1)) ; #print Reviews.ix[start]
    end   = reviews.index.searchsorted(dt.datetime(2016, 1, 1)) ; #print Reviews.ix[end]

    year_reviews = reviews.ix[start:end]

    print year_reviews.idxmin() 
    print year_reviews.idxmax()


    year_reviews['counter'] = 1
    reviews_in_period = year_reviews.groupby(['listing_id',pd.TimeGrouper('M')]).count()['counter']

    reviews_per_month_period = pd.DataFrame(reviews_in_period.unstack().fillna(0).mean(axis=1))
    reviews_per_month_period.columns = ['reviews_per_month_period']

    reviews_per_month_period.fillna(0,inplace = True)

    joined = listings.merge(reviews_per_month_period, left_on='id',right_index=True, how='left')

    joined.reviews_per_month_period.fillna(0,inplace=True)

    joined = joined[joined.last_review >= start]  ## keep reviews in period 

    ## filtering out listings with price > 2500, not scientifically based but that seems like a high limit for believable
    ## listings
    joined = joined[joined.price < 2501]

    ## 3 night avg stay, unless the minimum is higher
    joined['avg_stay_nights'] = where(joined.minimum_nights > 3, joined.minimum_nights, 3) 


    review_rate = .5 # sourced from insideAirbnb, conservative estimate

    ## capping occupany at 70% = 21 days
    joined['occupancy_nights_month'] = joined.reviews_per_month_period * (1/review_rate) * joined.avg_stay_nights


    joined['occupancy_nights_month'] = where(joined.occupancy_nights_month <= 21,joined.occupancy_nights_month,21 )

    joined['annual_revenue'] = joined.occupancy_nights_month * joined.price * 12

    return joined    
    
def count_listings(pivot):
    return len(pivot) - pivot.isnull().sum()

    
def create_market_share(df,col = 'neighbourhood_group' ,groupby='id', values = 'annual_revenue',filter_wholehome=True,filter_boro=False, normalize=True):
    if filter_wholehome:
        df = df[(df.room_type == 'Entire home/apt')]
    if filter_boro:
        df = df[(df.neighbourhood_group == filter_boro)]
        
    my_pivot = df.pivot_table(index=groupby,columns=col,values=values)
    if normalize:
        my_pivot = my_pivot.apply(lambda x: x/x.sum())
    
    print "Number of Listings Counted: "  
    print count_listings(my_pivot)
    return my_pivot

def create_city_cdf(data,city_name,return_hhi=False):
    data['city'] = city_name
    my_pivot = create_market_share(data,col='city')
    my_cumsum = my_pivot.sort_values(city_name,ascending=False)
    my_cumsum.reset_index(drop=True,inplace=True)
    
    if return_hhi:
        return my_cumsum
    my_cumsum['pct_rank'] = my_cumsum.index.value_counts(normalize=True)
   
    my_cumsum['pct_rank'] = my_cumsum['pct_rank'].cumsum()
    bins = linspace(0,1.001,num=101)
    my_cumsum['bins'] = pd.cut(my_cumsum.pct_rank,bins)

    return my_cumsum.groupby('bins')[city_name].sum().cumsum()


def plotly_cdf(df,y_title='% of Revenue', x_title="% of Listings",chart_title='Whale Chart',use_matplot=False,just_data=False):
    
    data = [{
        'x': df[col].dropna().index.value_counts(normalize=True).cumsum(),
        'y': df[col].sort_values(ascending=False).cumsum().dropna(),
        'name': col
    }  for col in df.columns]
    
    if just_data:
        return data
   
    ## default to matplotlib if not connected to internet like I am right now on this flight ':(
    if use_matplot:
        plt.legend(df.columns.values)
        for d in data:
            plt.plot(d['x'],d['y'])
    
    else:
        layout=go.Layout(title= chart_title, xaxis={'title':x_title}, yaxis={'title': y_title})
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig)