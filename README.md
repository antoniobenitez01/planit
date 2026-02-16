![Planit Logo](/assets/planit_logo_white2.png)
# 💬 Planit - Aplicación de Organización de Eventos

<br>

Planit es una aplicación web que permite a los usuarios **organizar**, **editar** y **asistir a Eventos** con el objetivo de **fomentar la socialización** y promover la **creación de nuevas comunidades con intereses comunes**.

Creada con las herramientas proporcionadas por Django y Python, Plaint se compromete a ofrecerte **nuevas oportunidades de conocer a nuevas personas** y descubrir **nuevos intereses y comunidades** mediante las diversas funcionalidades que ofrece nuestra aplicación.

<br>

## 📌 Asistencia y Descubrimiento de Eventos

<br>

Todos los usuarios de Planit pueden **explorar los diferentes Eventos organizados** en nuestra aplicación, pudiendo **asistir a los Eventos** que deseen. Para descubrir nuevos Eventos, Planit ofrece una sección de **Últimos Eventos** organizados en su página principal, además de una sección de **Lista de Eventos** donde se mostrarán todos los Eventos organizados a lo largo de la historia de la aplicación.
<br><br>
Casos a detallar sobre la asistencia y estado de los Eventos:

  * Los usuarios solo pueden asistir a un Evento si este está activo y tiene espacios disponibles. No se podrá asistir a un Evento finalizado o lleno.

  * Los organizadores del Evento no podrán asistir a su propio Evento

<br>

## 📅 Organización de Eventos

<br>

Una vez registrados, los usuarios de Planit pueden empezar a participar en nuestra comunidad **organizando nuevos Eventos** en los que puedan participar el resto de usuarios. Los Eventos se definen por:

  * Título
  * Descripción
  * Fecha y Hora
  * Ubicación
  * Número máximo de Asistentes

Los organizadores de Eventos pueden realizar las siguientes acciones sobre sus propios eventos:

  * Editar los detalles del Evento
  * Subir y Eliminar las imágenes del Evento
  * Establecer como Finalizado el Evento
  * Eliminar el Evento organizado

Casos a detallar sobre la organización de Eventos:

  * El campo Espacios Disponibles debe siempre ser mayor que 0. En el caso de que se edite un Evento ya organizado con asistentes, no se podrá modificar el número de espacios disponibles máximos por debajo del número de usuarios que ya han declarado asistir al Evento.
  
  * El campo Fecha y Hora siempre debe ser una fecha futura. No está permitido crear un Evento en el pasado en torno a la fecha de la creación del Evento.

  * Una vez se ha declarado un Evento como finalizado, el organizador no podrá eliminar el Evento ni modificar sus datos.

  <br>

## 👤 Registro y Login de Usuario

<br>

Planit ofrece una Intranet donde los usuarios pueden registrarse para formar parte de nuestra comunidad y empezar a organizar nuevos Eventos. El Sistema de Autenticación de Planit permite al Usuario realizar las siguientes funciones sobre su cuenta y login:

  * Registrarse en Planit como un nuevo usuario
  * Hacer Login para acceder a funcionalidades exclusivas para miembros
  * Editar los datos de perfil del usuario
  * Cerrar su sesión de la aplicación

<br>

## 📝 Reglas de Negocio

<br>

Las siguientes reglas de negocio son normas que aplican a la hora de utilizar la aplicación. Las normas listadas a continuación se imponen tanto desde la interfaz visual del usuario (Frontend) como desde la base de datos y sistema de administración de la aplicación (Backend)

  * El email de cada usuario es único y no está permitido registrarlo de nuevo
  * El teléfono de cada usuario es único y no está permitido registrarlo de nuevo
  * Un usuario solo podrá modificar sus propios datos de perfil
  * Un usuario solo podrá eliminar su propio perfil
  * Un usuario no puede asistir a un Evento al que ya está asistiendo
  * Un usuario no puede cancelar la asistencia de un Evento que no está asistiendo
  * Un usuario no puede asistir a un Evento lleno sin espacios disponibles
  * El campo Fecha y Hora del Evento debe ser futura en base a la fecha de creación del Evento
  * El campo Fecha y Hora del Evento debe ser futura en base a la fecha de edición del Evento
  * El campo Espacios Disponibles debe ser un número positivo mayor que 0
  * El campo Espacios Disponibles no puede ser menor que el número de usuarios asistiendo a la hora de editar los datos de un Evento ya organizado
  * Los Espacios Disponibles visibles al usuario serán calculados de forma automática en base a los usuarios que estén asisitendo al Evento en el momento en el que el usuario visualiza el Evento
  * Solo el organizador del Evento puede modificar los datos del mismo
  * Solo el organizador del Evento puede eliminar el mismo
  * Solo el organizador del Evento puede finalizar el mismo
  * Una vez finalizado, el organizador del Evento no puede modificar los datos del Evento
  * Una fez finalizado, el organizador del Evento no puede eliminar el Evento
  * Una vez eliminado un Evento, las asistencias sujetas al mismo se eliminarán a continuación

<br>

## ⚙️ Instalación del Proyecto

<br>

1. Clona el Repositorio:

```
git clone https://github.com/antoniobenitez01/planit
```

2. Navega a la carpeta del projecto:

```
cd planit
```

3. Aplica las migraciones del projecto:

```
python manage.py migrate
```

4. Ejecuta el servidor y aplicación:

```
python manage.py runserver
```

<br>

---

<br>

<p style="text-align: center;">
Planit es un Project de Código Abierto desarrollado en 2026 por Antonio Benítez Rodríguez <br>usando Django y Python, disponible en GitHub para uso personal y educativo.
</p>