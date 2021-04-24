# démarrage du projet
## 1er fois
```shell
git clone https://gitlab.com/sia-insa-lyon/BdEINSALyon/lavotomatic.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py init_demo_db
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

## fois suivantes
```shell
git pull
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
```

# utilisation
il y a deux exemples
 * un script python ``test_api.py``
 * un exemple cURL dans ``test_api.sh``

On peut éditer la base de données avec l'admin Django, disponible à [http://localhost:8000/admin/](http://localhost:8000/admin/)

Il n'y a pas du tout d'authentification pour l'instant

# fonctionnalités
* décrémente le crédit de jetons lors d'un lavage
* coût des machines configurable
* les machines peuvent être désactivées depuis l'admin (si HS par exemple)
* les programmes sont configurables depuis l'admin, avec une durée
* le serveur affiche la date+heure à laquelle la machine sera disponible
* endpoint de lancement de machine
