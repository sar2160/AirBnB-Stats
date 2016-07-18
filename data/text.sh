###  

for f in */ ; do
	state=${f///}
	for ff in $f*; do
		city=${ff##*/}	

	echo "http://data.insideairbnb.com/united-states/$state/$city/2016-04-18/visualisations/listings.csv"
	done
done

