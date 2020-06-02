# chAPAsso
#### *API para la gestión y análisis de los comentarios de noticias*

## Introducción

Este proyecto tiene como objetivos, por un lado, la creación de una API que permita la gestión de los mensajes que los lectores dejan en los comentarios de las noticias en un periódicos online. Por otro lado, la API permite el análisis de los sentimientos de las conversaciones generadas, así como busca el usuari@ más similar basándose en los comentarios mediante un sistema de recomendación.
La base de datos generada se aloja en un cluster de Mongo Atlas y la API se sirve en la nube mediante Heroku. En

## Materiales y métodos

### 1. La estructura de la base de datos

Se ha creado una base de datos con una única colección (`comments`) con tres tipos de documentos cuya estructura se define a continuación:

* User: documento para almacenar los nombres e id de los lectores
  * `_id`
  * `type`: user
  * `user_name`: nombre o alias del usuario

* Chat
  * `_id`
  * `type`: chat
  * `chat_name`: nombre que permite idenficar la noticia a la que se refieren los comentarios

* Message
  * `_id`
  * `type`: message
  * `chat_id`: id del chat al que pertenece
  * `user_id`: id del usuario al que pertenece
  * `text`: contenido del mensaje

La base de datos se ha rellenado con los comentarios de las noticias del periódico metro (https://metro.co.uk/). Una vez creada la base de datos de forma local, se exportó la colección como un archivo .json para su posterior importación a la base de datos de la nube. 

### 2. La API y sus funcionalidades

A continuación, se muestran los diferentes endpoints y cómo utilizarlos:

#### 2.1. Usuarios

* `/users/create/<username>`: el primer paso en la creación de la base de datos es meter los lectores que participan en los comentarios. La API comprueba que el usuario creado no existe, en caso contrario, lanza un error. Si todo ha ido bien, como respuesta se obtiene el ID del nuevo usuario creado.

* `/users/<user_id>/recommend/`: mediante un sistema de recomendación, la API devuelve el nombre del lector más parecido al especificado por su nombre, basado en las palabras que ha usado en sus mensajes. Si el usuario no existe, la API lanza un error.

#### 2.2. Chats

* `/chat/create?`: endpoint para crear el chat y agregar los lectores que participan en él. Consta de dos argumentos:
  + `n_chat`: nombre del chat
  + `u`: nombre del lector. Tiene que haber sido insertado previamente en la bbdd. Se pueden añadir tantos lectores como sean necesarios añadiendo `&` lector y lector.

* `/chat/<chat_id>/adduser`: añade un nuevo usuario al chat especificado por su nombre en `<chat_id>`._

* `/chat/<chat_id>/sentiment`: analiza el sentimiento de la conversación del chat especificado por su nombre en `<chat_id>`. El resultado devuelve la media de la métrica *compound* para el total de la conversación y su clasificación (neutro, negativo o positivo), así como el desglose del análisis por mensaje.

#### 2.3. Mensajes

* `/chat/<chat_id>/addmessage`: añade a la base de datos un mensaje acompañado del id del chat al que pertenece y del id del lector que lo realiza. Tiene los siguientes parámetros:
  + `u`: usuario que realiza el comentario.
  + `msg`: contenido del mensaje.

* `/chat/<chat_id>/list`: extrae todos los mensajes del chat especificado por su nombre en `<chat_id>`.

### 3. Resultados

Como resultado, la API se encuentra alojada en la siguiente dirección:
https://chapasso.herokuapp.com/

Algunos ejemplos:

* Sacar lista de mensajes de un chat:

https://chapasso.herokuapp.com/chat/Mums_Occupy/list

* Sacar los sentimientos de un chat:

https://chapasso.herokuapp.com/chat/semen_drink/sentiment

* Encontrar el usuario más parecido al usuario "Yoda":

https://chapasso.herokuapp.com/user/Yoda/recommend


#### Bonus. Enlace a las noticias

* https://metro.co.uk/2020/05/01/mum-drinks-sperm-smoothies-fight-off-coronavirus-12639469/

* https://metro.co.uk/2020/05/02/mums-occupy-childrens-playground-protest-lockdown-12643715/

* https://metro.co.uk/2020/05/03/boris-johnson-set-plan-leaving-lockdown-next-week-12648962/
