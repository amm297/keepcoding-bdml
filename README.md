## Práctica BDA 

### Idea general

Coger datos de diversos sitios, el tenedor y openlabs (emt Madrid), y combinarlos bajo demanda con el dataset de Airbnb

### Nombre del producto

Recomendador de Airbnb por Restaurantes (El tenedor) y Transporte (MobilityLabs)

### Estrategia del DAaaS

Sacar un reporte diario de los 10 mejores sitios para alquitar por Airbnb en funcion de unos filtros predefinidos de zona, restaurantes cerca y valoracion de los mismos y comunicacion del sitio (transporte público)

### Arquitectura

Todo el proyecto se alojará en la nube (Google cloud), y contará con:

* Descargaremos el dataset de airbnb de [aquí](https://public.opendatasoft.com/explore/dataset/airbnb-listings/export/?disjunctive.host_verifications&disjunctive.amenities&disjunctive.features&q=Madrid&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJ5QXhpcyI6Imhvc3RfbGlzdGluZ3NfY291bnQiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1jdXN0b20ifV0sInhBeGlzIjoiY2l0eSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6IiIsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd24iOiJyb29tX3R5cGUiLCJjb25maWciOnsiZGF0YXNldCI6ImFpcmJuYi1saXN0aW5ncyIsIm9wdGlvbnMiOnsiZGlzanVuY3RpdmUuaG9zdF92ZXJpZmljYXRpb25zIjp0cnVlLCJkaXNqdW5jdGl2ZS5hbWVuaXRpZXMiOnRydWUsImRpc2p1bmN0aXZlLmZlYXR1cmVzIjp0cnVlfX19XSwidGltZXNjYWxlIjoiIiwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&refine.city=Madrid&location=16,41.38377,2.15774&basemap=jawg.streets) una vez descargado se procesara para procesar los campos y sustitur los caracteres ';' por ',' de todos aquellos campos que los contengan ya que este sera el delimitador de campo ademas de borrar las columnas que no deseemos, en este caso se ha borrado: 'host_about'.
* Crawler con scrapy de 'El tenedor' para sacar Restaurantes. Será un cloud function ejecutado semanalmente mediante un job cuyo resultado en formato csv se almacenara en el google cloud storage.
* LLamadas a API de transporte con un pequeño script en python a partir del dataset de Airbnb, este se ejecutrá manualmente (de manera inicial) y el resultado en formato json se subira al google cloud storage.

Habrá un cloud function ejecutado bajo demanta que inserte los datos del Storage en HIVE, realize un JOIN de las tablas para obtener los alojamientos mejores conectados, es decir con mejor comunicacion y buenos restaurantes a su alrededor.

** como mejora:
	- meter actividades (Civitatis y o similar)
	- informacion meteorologica
	- pagina web que permita realizar una query especifica

### Operating Model

Distinguimos 3 partes:

* Tendremos un job alojado en la nube que se ejecute semanalmente ( los Lunes a las 7 de la mañana), la lógica de este será llamar a la cloud function que almacene el Crawler, el cúal recorrera la web de el tenedor para obtener una lista de los restaurantes. Este resultado se almacenará en el storage dentro de un segmento llamado 'keepcoding-bootcamp en una carpeta llamada 'input' bajo el nombre de 'restaurants-YYYY-MM-DD.csv', el nombre contrendrá la fecha a modo de marca temporal para que se use siempre el mas reciente.

* Hay un pequeño script ejecutado manualmente que genere un archivo JSON, este contendrá las paradas de transporte público cercanas a cada uno de los alojamientos del dataset original de airbnb. El resultado que se genere será subido al segmento de la nube llamado 'keepcoding-bootcamp en una carpeta llamada 'input' bajo el nombre de 'public-transport.json'

* Dentro del segmento 'keepcoding-bootcamp' en la carpeta 'input' tendremos el dataset inicial 'airbnb-listings.csv' el cúal, junto a los dos anteriores, mediante a una cloud function se cargaran en HIVE, se ejecutara una la query que los procese y el resultado se almacenara en el mismo segmento en la crpeta 'output' bajo el rombre 'retults.csv'.

### Desarrollo

Crawler de [El tenedor](https://www.eltenedor.es/restaurante+madrid) éste se ejecutara internamente en el cloud de google mediante un cron-job todos los Lunes a las 7:00, para ello se ha creado un 'Cloud Schedule' con la expresion: __0 7 * * 1__
	
```python
from google.cloud import storage
from scrapy.crawler import CrawlerProcess
from datetime import datetime, date
import scrapy
import json
import tempfile

TEMPORARY_FILE = tempfile.NamedTemporaryFile(delete=False, mode='w+t')

def upload_file_to_bucket(bucket_name, blob_file, destination_file_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(blob_file.name, content_type='text/csv')

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # Podeis cambiar la url inicial por otra u otras paginas
    start_urls = ['https://www.eltenedor.es/restaurante+madrid?page=1']
    def parse(self, response):
        # Aqui scrapeamos los datos y los imprimimos a un fichero        
        for article in response.css('li.resultItem'):
            title = article.css('h3 a ::text').extract_first()
            address = article.css('div.resultItem-address ::text').extract_first().strip().replace(',', '')
            tags = article.css('li span.restaurantTag ::text').getall()
            ratings = article.css('div.rating a span.rating-ratingValue ::text').get(default = 0)
            reviews = article.css('div.reviewsCount--small a.js_rating ::text').extract_first(default='0 reviews').split(' ')[0]
            # Print a un fichero
            if (ratings != 0 or reviews != 0):
            	TEMPORARY_FILE.writelines(f"{title};{address};{tags};{ratings};{reviews}\n")

        # Aqui hacemos crawling (con el follow)
        next_page_url = response.css('div.pagination a[rel="next"] ::attr(href)').extract_first()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse)

def activate(request):
    now = datetime.now() 
    request_json = request.get_json()
    BUCKET_NAME = 'keepcoding-bootcamp'
    DESTINATION_FILE_NAME = 'input/el-tenedor-{}.csv'.format(now.strftime('%Y-%m-%d'))
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(BlogSpider)
    process.start()
    TEMPORARY_FILE.seek(0)
    upload_file_to_bucket(BUCKET_NAME, TEMPORARY_FILE, DESTINATION_FILE_NAME)
    TEMPORARY_FILE.close()
    return "Success!"
```
### Diagrama

El diagrama se puede ver aqui [aqui](https://docs.google.com/drawings/d/1ov2LZrDwERI5lJ5_CiS-FDTd-ixvamkJSBWM0X_brjM/edit?usp=sharing)
