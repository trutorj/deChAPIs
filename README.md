# deChAPIs
#### *API para la gestión y análisis de chats*

## Introducción
Este proyecto tiene como objetivo la creación de una API que permite la gestión de chats a través de una base de datos MongoDB.

## Materiales y métodos

### La estructura de la base de datos

Se ha creado una base de datos con una única collección con tres tipos de documentos cuya estructura se define a continuación:

* User: documento para almacenar los usuarios de los chats
  * `_id`
  * `type`: user
  * `user_name`: nombre o alias del usuario

* Chat
  * `_id`
  * `type`: chat
  * `chat_name`: nombre o alias del chat

* Message
  * `_id`
  * `type`: message
  * `chat_id`: id del chat al que pertenece
  * `user_id`: id del usuario al que pertenece

La base de datos se ha rellenado con los comentarios de las noticias del periódico metro(https://metro.co.uk/).