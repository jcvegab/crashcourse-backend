# crashcourse-backend
Crashcourse | Django - Backend 

Primero debes entrar al entorno de desarrollo Virtualenv de Python con: 
```
source venv/bin/activate
```

Luego debes instalar las dependencias del proyecto Django: 
```
pip install -r requirements.txt
```

Antes de arrancar el servidor debes cambiar la 'SECRET_KEY' ubicada en ./core/setting.py:

Actual: os.environ["SECRET_KEY"]
Modificar por el código en el archivo drive: https://drive.google.com/file/d/1mTjLyPR0UuRvfNExyTa1r8YvL1y5yjOW/

Para iniciar el servidor:
```
python3 manage.py runserver
```

El servidor está en línea en la siguiente dirección: https://crashcourse-backend.herokuapp.com/graphql
