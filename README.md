# Sistema de Gestion de Tickets

Aplicacion web desarrollada con Django para administrar tickets de soporte tecnico, clientes, tecnicos asignados, comentarios e informes generales. El sistema esta pensado para centralizar solicitudes de soporte, dar seguimiento a su estado y revisar metricas basicas de operacion.

El codigo principal esta dentro de la carpeta `PAGINA DE TICKETS/`.

## Tecnologias usadas

- **Python**: lenguaje principal del backend.
- **Django 3.2**: framework web usado para rutas, vistas, modelos, formularios, autenticacion y panel administrativo.
- **MySQL**: base de datos configurada para guardar clientes, tickets, comentarios y usuarios.
- **Bootstrap 5**: framework CSS usado para la interfaz, grillas, formularios, botones, tablas y componentes responsivos.
- **Bootstrap Icons**: iconos usados en el menu lateral, acciones y elementos visuales.
- **HTML, CSS y JavaScript**: plantillas, estilos personalizados y comportamiento basico de la interfaz.
- **Sistema de autenticacion de Django**: manejo de usuarios, login, logout, permisos de staff y superusuario.

## Para que sirve

Este proyecto sirve para gestionar solicitudes de soporte desde una interfaz web. Permite registrar clientes, crear tickets asociados a esos clientes, asignar tecnicos, controlar prioridades, cambiar estados, agregar comentarios y consultar estadisticas de seguimiento.

Puede usarse como base para un sistema interno de mesa de ayuda, soporte tecnico, atencion a clientes o administracion de incidencias.

## Funcionalidades principales

- **Inicio y cierre de sesion**: acceso al sistema mediante usuarios registrados en Django.
- **Dashboard**: resumen de tickets totales, abiertos, en proceso, resueltos, cerrados, criticos, de alta prioridad y clientes activos.
- **Gestion de tickets**:
  - Crear tickets.
  - Listar tickets.
  - Buscar por titulo, descripcion o cliente.
  - Filtrar por estado, prioridad y tecnico.
  - Ver detalle de cada ticket.
  - Editar ticket.
  - Eliminar ticket.
  - Asignar tecnico responsable.
  - Registrar prioridad y estado.
- **Estados de ticket**:
  - Abierto.
  - En proceso.
  - Resuelto.
  - Cerrado.
- **Prioridades de ticket**:
  - Baja.
  - Media.
  - Alta.
  - Critica.
- **Comentarios en tickets**: permite agregar comentarios asociados a un ticket, incluyendo comentarios internos para tecnicos.
- **Gestion de clientes**:
  - Crear clientes.
  - Listar clientes.
  - Buscar clientes por nombre, email o empresa.
  - Editar clientes.
  - Eliminar clientes sin tickets asociados.
- **Informes**:
  - Tickets por estado.
  - Tickets por prioridad.
  - Tickets por tecnico.
  - Tiempo promedio de resolucion.
  - Tickets creados durante el ultimo mes.
  - Clientes con mas tickets.
- **Panel de administracion de Django**: administracion avanzada de clientes, tickets y comentarios desde `/admin/`.

## Estructura del proyecto

```text
PAGINA DE TICKETS/
  manage.py
  sistema/
    settings.py
    urls.py
    wsgi.py
    asgi.py
  tickets/
    models.py
    views.py
    forms.py
    urls.py
    admin.py
    migrations/
  usuarios/
    views.py
    models.py
    admin.py
    templates/
  templates/
    base.html
    tickets/
```

## Modulos principales

- **sistema**: configuracion general del proyecto Django, rutas principales, base de datos, idioma, zona horaria y archivos estaticos.
- **tickets**: modulo principal del sistema. Contiene modelos, formularios, vistas, rutas y administracion de tickets, clientes y comentarios.
- **usuarios**: modulo encargado del inicio y cierre de sesion.
- **templates**: plantillas HTML de la interfaz, incluyendo layout base, dashboard, listas, formularios, detalles e informes.

## Modelos de datos

- **Cliente**: guarda nombre, email, telefono, empresa, fecha de registro y estado activo.
- **Ticket**: guarda titulo, descripcion, cliente, prioridad, estado, tecnico asignado, usuario creador y fechas de seguimiento.
- **Comentario**: guarda comentarios asociados a un ticket, usuario autor, fecha y si el comentario es interno.

## Requisitos

- Python 3.x
- Django 3.2
- MySQL
- Conector MySQL para Python, por ejemplo `mysqlclient` o `pymysql`

## Configuracion de base de datos

La base de datos esta configurada en `PAGINA DE TICKETS/sistema/settings.py` con estos datos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema_dbo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3307',
    }
}
```

Antes de ejecutar el proyecto, crea la base de datos `sistema_dbo` en MySQL y verifica que el puerto, usuario y contrasena coincidan con tu entorno.

## Como ejecutar el proyecto

Desde la carpeta principal del proyecto Django:

```bash
cd "PAGINA DE TICKETS"
pip install django==3.2
pip install mysqlclient
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego abre:

```text
http://127.0.0.1:8000/
```

## Accesos utiles

- `/`: login o dashboard segun la sesion.
- `/tickets/`: listado de tickets.
- `/tickets/crear/`: crear ticket.
- `/clientes/`: listado de clientes.
- `/clientes/crear/`: crear cliente.
- `/informes/`: reportes del sistema.
- `/admin/`: panel administrativo de Django.

## Notas

- El sistema usa `America/Santiago` como zona horaria.
- La interfaz esta en espanol.
- Solo usuarios autenticados pueden acceder al dashboard, tickets, clientes e informes.
- Los tecnicos se toman desde usuarios de Django marcados como `is_staff=True`.
