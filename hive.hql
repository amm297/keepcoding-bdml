DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS airbnb;
DROP TABLE IF EXISTS public_transport;

CREATE TABLE restaurants (
	name STRING, 
	address STRING,
	city STRING,
	latitude FLOAT,
	longitude FLOAT,
	tags ARRAY<STRING>, 
	rating DOUBLE, 
	reviews DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ";";

CREATE TABLE public_transport (
	apt_id STRING,
	latitude FLOAT,
	longitude FLOAT,
	stops ARRAY<STRUCT<stop_id: STRING,
	latitude: FLOAT,
	longitude: FLOAT,
	name: STRING,
	meters: INT,
	lines: ARRAY<STRUCT<code: string,
	label: STRING,
	name_from: STRING,
	name_to: STRING>>,
	type: STRING>>)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe';


CREATE TABLE airbnb (
	id STRING, listing_url STRING, scrape_id STRING, last_scraped STRING, name STRING, summary STRING, space STRING, description STRING, experiences_offered STRING, neighborhood_overview STRING, notes STRING, transit STRING, access STRING, interaction STRING, house_rules STRING, thumbnail_url STRING, medium_url STRING, picture_url STRING, xl_picture_url STRING,  host_id STRING, host_url STRING, host_name STRING, host_since STRING, host_location STRING, host_response_time STRING, host_response_rate INT, host_acceptance_rate STRING, host_thumbnail_url STRING, host_picture_url STRING,  host_neighbourhood STRING,  host_listings_count INT, host_total_listings_count INT, host_verifications STRING, street STRING, neighbourhood STRING, neighbourhood_cleansed STRING, neighbourhood_group_cleansed STRING, city STRING, state STRING, zipcode STRING, market STRING, smart_location STRING, country_code STRING, country STRING, latitude FLOAT, longitude FLOAT, property_type STRING, room_type STRING, accommodates INT, bathrooms FLOAT, bedrooms INT, beds INT, bed_type STRING, amenities STRING, square_feet INT, price INT, weekly_price INT, monthly_price INT, security_deposit INT, cleaning_fee INT, guests_included INT, extra_people INT, minimum_nights INT, maximum_nights INT, calendar_updated STRING, has_availability STRING, availability_30 INT, availability_60 INT, availability_90 INT, availability_365 INT, calendar_last_scraped STRING, number_of_reviews INT, first_review STRING, last_review STRING, review_scores_rating INT, review_scores_accuracy INT, review_scores_cleanliness INT, review_scores_checkin INT, review_scores_communication INT, review_scores_location INT, review_scores_value INT, license STRING, jurisdiction_names STRING, cancellation_policy STRING, calculated_host_listings_count INT, reviews_per_month FLOAT, geolocation STRING, features STRING) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ";" ;

LOAD DATA INPATH 'gs://keepcoding-bootcamp/input/2020/01/19/el-tenedor.csv' INTO TABLE restaurants;
LOAD DATA INPATH 'gs://keepcoding-bootcamp/input/public-transport.json' INTO TABLE public_transport;
LOAD DATA INPATH 'gs://keepcoding-bootcamp/input/airbnb-listings.csv' INTO TABLE airbnb;

INSERT OVERWRITE DIRECTORY 'gs://keepcoding-bootcamp/output'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'
SELECT a.id,
	   a.name,
	   a.house_rules,
	   a.street,
	   a.latitude,
	   a.longitude,
	   a.property_type,
	   a.room_type,
	   a.price,
	   a.security_deposit,
	   a.number_of_reviews,
	   a.review_scores_rating,
	   a.review_scores_cleanliness,
	   a.review_scores_checkin,
	   a.review_scores_communication,
	   a.review_scores_value,
	   a.cancellation_policy,
	   r.name,
	   r.address,
	   r.tags,
	   r.rating,
	   r.reviews,
	   pt.stops
FROM airbnb a 
JOIN public_transport pt ON (pt.apt_id = a.id) 
JOIN restaurants r on (r.city = a.market) 
WHERE ( 
	2 * asin(
		sqrt(
			cos(radians(a.latitude)) * cos(radians(r.latitude)) * 
			pow(
				sin(radians((a.longitude - r.longitude)/2)), 2) + 
			pow(sin(radians((a.latitude - r.latitude)/2)), 2))) 
	* 6371) < 2
AND a.price < 100;



