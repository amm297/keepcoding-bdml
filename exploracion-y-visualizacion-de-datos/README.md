# Exploracion de datos tableau
Para la realización de la practica hemos empleado el dataset de la practica anterior de `Arquitecture Big Data`.
Se ha creado una base de datos en google SQL con las siguientes tablas:

```sql
CREATE TABE airbnb(
	id VARCHAR(50),
	scrape_id VARCHAR(200),
	last_scraped DATE,
	calendar_last_scraped DATE,
	summary TEXT,
	space TEXT,
	description TEXT,ac
	experiences_offered VARCHAR(200),
	notes TEXT,
	transit TEXT,
	access TEXT,
	interaction TEXT,
	house_rules TEXT,
	amenities VARCHAR(5000),
	license VARCHAR(500),
	jurisdiction_names VARCHAR(100),
	features TEXT,
	calendar_updated VARCHAR(80),
	has_availability VARCHAR(80),
	availability_30 INT,
	availability_60 INT,
	availability_90 INT,
	availability_365 INT,
	name VARCHAR(500),
	property_type VARCHAR(100),
	room_type VARCHAR(100),
	accommodates SMALLINT,
	bathrooms FLOAT,
	bedrooms SMALLINT,
	beds SMALLINT,
	bed_type VARCHAR(80),
	square_feet BIGINT,
	host_id VARCHAR(50),
	host_url VARCHAR(200),
	host_name VARCHAR(150),
	host_since DATE,
	host_location VARCHAR(200),
	host_response_time VARCHAR(80),
	host_response_rate INT,
	host_acceptance_rate VARCHAR(200),
	host_thumbnail_url VARCHAR(500),
	host_picture_url VARCHAR(500),
	host_neighbourhood VARCHAR(200),
	host_listings_count INT,
	host_total_listings_count INT,
	host_verifications VARCHAR(500),
	calculated_host_listings_count INT,
	listing_url VARCHAR(500),
	thumbnail_url VARCHAR(1000),
	medium_url VARCHAR(1000),
	picture_url VARCHAR(1000),
	xl_picture_url VARCHAR(1000),
	street VARCHAR(500),
	neighbourhood VARCHAR(100),
	neighbourhood_cleansed VARCHAR(100),
	neighbourhood_group_cleansed VARCHAR(100),
	neighborhood_overview TEXT,
	city VARCHAR(100),
	state VARCHAR(100),
	zipcode VARCHAR(100),
	market VARCHAR(100),
	smart_location VARCHAR(100),
	country_code VARCHAR(20),
	country VARCHAR(100),
	latitude FLOAT,
	longitude FLOAT,
	geolocation VARCHAR(200),
	price INT,
	weekly_price INT,
	monthly_price INT,
	security_deposit INT,
	cleaning_fee INT,
	guests_included SMALLINT,
	extra_people SMALLINT,
	minimum_nights INT,
	maximum_nights INT,
	cancellation_policy VARCHAR(100),
	first_review DATE,
	last_review DATE,
	review_scores_rating INT,
	review_scores_accuracy INT,
	review_scores_cleanliness INT,
	review_scores_checkin INT,
	review_scores_communication INT,
	review_scores_location INT,
	review_scores_value INT,
	number_of_reviews INT,
	reviews_per_month FLOAT)
```

```sql
CREATE TABLE restaurants (
	name VARCHAR(500), 
	address VARCHAR(250),
	zipcode VARCHAR(100),
	city VARCHAR(50),
	latitude FLOAT,
	longitude FLOAT,
	tags VARCHAR(500), 
	rating DOUBLE, 
	reviews DOUBLE)
```

Posteriormente a su llenado con los archivos del cloud `airbnb-listings.csv` y `el-tenedor.csv` hemos creado la connexión en Tableau (una vez hecha la conexión se han extraido los datos para trabajar en local) y procedido al desarrollo de las hojas y el dashboad que se pueden ver en el archivo `practica_tableau.twbx`.

Para reducir el tamaño de datos se ha realizado una consulta cutomizada sobre la tabla de airbnb para que no traiga datos que no se pensaban unsar desde un princiop, aqui poedemo ver cual seria la query:

```sql
SELECT `airbnb`.`id` AS `id`,
  `airbnb`.`name` AS `name`,
  `airbnb`.`summary` AS `summary`,
  `airbnb`.`street` AS `street`,
  `airbnb`.`neighbourhood` AS `neighbourhood`,
  `airbnb`.`neighbourhood_cleansed` AS `neighbourhood_cleansed`,
  `airbnb`.`neighbourhood_group_cleansed` AS `neighbourhood_group_cleansed`,
  `airbnb`.`city` AS `city`,
  `airbnb`.`state` AS `state`,
  `airbnb`.`zipcode` AS `zipcode`,
  `airbnb`.`market` AS `market`,
  `airbnb`.`smart_location` AS `smart_location`,
  `airbnb`.`country_code` AS `country_code`,
  `airbnb`.`country` AS `country`,
  `airbnb`.`latitude` AS `latitude`,
  `airbnb`.`longitude` AS `longitude`,
  `airbnb`.`property_type` AS `property_type`,
  `airbnb`.`room_type` AS `room_type`,
  `airbnb`.`accommodates` AS `accommodates`,
  `airbnb`.`bathrooms` AS `bathrooms`,
  `airbnb`.`bedrooms` AS `bedrooms`,
  `airbnb`.`beds` AS `beds`,
  `airbnb`.`bed_type` AS `bed_type`,
  `airbnb`.`amenities` AS `amenities`,
  `airbnb`.`square_feet` AS `square_feet`,
  `airbnb`.`price` AS `price`,
  `airbnb`.`weekly_price` AS `weekly_price`,
  `airbnb`.`monthly_price` AS `monthly_price`,
  `airbnb`.`security_deposit` AS `security_deposit`,
  `airbnb`.`cleaning_fee` AS `cleaning_fee`,
  `airbnb`.`guests_included` AS `guests_included`,
  `airbnb`.`extra_people` AS `extra_people`,
  `airbnb`.`minimum_nights` AS `minimum_nights`,
  `airbnb`.`maximum_nights` AS `maximum_nights`,
  `airbnb`.`number_of_reviews` AS `number_of_reviews`,
  `airbnb`.`first_review` AS `first_review`,
  `airbnb`.`last_review` AS `last_review`,
  `airbnb`.`review_scores_rating` AS `review_scores_rating`,
  `airbnb`.`review_scores_accuracy` AS `review_scores_accuracy`,
  `airbnb`.`review_scores_cleanliness` AS `review_scores_cleanliness`,
  `airbnb`.`review_scores_checkin` AS `review_scores_checkin`,
  `airbnb`.`review_scores_communication` AS `review_scores_communication`,
  `airbnb`.`review_scores_location` AS `review_scores_location`,
  `airbnb`.`review_scores_value` AS `review_scores_value`,
  `airbnb`.`cancellation_policy` AS `cancellation_policy`,
  `airbnb`.`calculated_host_listings_count` AS `calculated_host_listings_count`,
  `airbnb`.`reviews_per_month` AS `reviews_per_month`,
  `airbnb`.`geolocation` AS `geolocation`,
  SUBSTRING(`airbnb`.`features`, 1, 1024) AS `features`
FROM `airbnb`
```

Tendremos ha historia con dos Dashboards, uno que contiene todo lo relacionado con los alojamientos y otro con los restaurantes:

- Alojamientos: Este dashboard se compone de tres vistas un mapa, una grafica con la valoracion por alojamiento y una gráfica que compara los alojamientos con el precio y la política de cancelacion. Conforme seleccionemos el barrio en el mapa se actualizaran las gráficas filtrando por el seleccionado.a
- Restaurantes: Tiene dos vistas un mapa y una nube de palabras, así como un filtro con el que seleccionar el barrio que queremos ver. Ambas vistas interactuan de modo que cuando se seleccione un restaurante en una de ellas en la otra se resalta el mismo restaurante.
