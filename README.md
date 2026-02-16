![Planit Logo](/assets/planit_logo_white2.png)
# 💬 Planit - Aplicación de Organización de Eventos

Planit es una aplicación web que permite a los usuarios **organizar**, **editar** y **asistir a Eventos** con el objetivo de **fomentar la socialización** y promover la **creación de nuevas comunidades con intereses comunes**.

Creada con las herramientas proporcionadas por Django y Python, Plaint se compromete a ofrecerte **nuevas oportunidades de conocer a nuevas personas** y descubrir **nuevos intereses y comunidades** mediante las diversas funcionalidades que ofrece nuestra aplicación.

---

## 📌 Asistencia y Descubrimiento de Eventos

Todos los usuarios de Planit pueden **explorar los diferentes Eventos organizados** en nuestra aplicación, pudiendo **asistir a los Eventos** que deseen. Para descubrir nuevos Eventos, Planit ofrece una sección de **Últimos Eventos** organizados en su página principal, además de una sección de **Lista de Eventos** donde se mostrarán todos los Eventos organizados a lo largo de la historia de la aplicación.
<br><br>
Casos a detallar sobre la asistencia y estado de los Eventos:

  * Los usuarios solo pueden asistir a un Evento si este está activo y tiene espacios disponibles. No se podrá asistir a un Evento finalizado o lleno.

  * Los organizadores del Evento no podrán asistir a su propio Evento

## 📅 Organización de Eventos

Una vez registrados, los usuarios de Planit pueden empezar a participar en nuestra comunidad organizando nuevos Eventos en los que puedan participar el resto de usuarios. Los Eventos se definen por:

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

### 👤 User Authentication

* User registration and login system.
* Secure authentication using Django’s built-in authentication framework.
* Profile-based event participation.
* Only authenticated users can create or attend events.

---

## 🛠 Instalación del Proyecto

1. Clone the repository:

```
git clone https://github.com/antoniobenitez01/planit
```

2. Navigate to the project folder:

```
cd planit
```

3. Apply migrations:

```
python manage.py migrate
```

4. Run the server:

```
python manage.py runserver
```

---

## 📬 Contribution

Contributions are welcome. Feel free to:

* Submit issues.
* Suggest improvements.
* Add new features.

---

## 📄 License

This project is open-source and available for educational and personal use.

---

## ✨ Author

Developed as a full-stack Django learning and portfolio project.
