GUIDE D’INSTALLATION
Application Web de Cotation – Honey Group
Version 1.0

1. Introduction
Le présent document décrit la procédure d’installation de l’application web de cotation développée pour Honey Group.
L’application a été développée avec les technologies suivantes :
Python
Django
MySQL
Django Jazzmin
L’installation permet d’exécuter l’application dans un environnement local afin d’assurer son exploitation et sa maintenance.

2. Configuration minimale requise
Avant l’installation, vérifier que le poste dispose des éléments suivants :
Composant	Configuration recommandée
Système d’exploitation	Windows 10/11
Processeur	Intel Core i3 ou supérieur
Mémoire RAM	4 Go minimum
Espace disque	2 Go disponibles
Navigateur	Google Chrome, Microsoft Edge ou Mozilla Firefox
Connexion Internet	Recommandée pour l’installation initiale

3. Logiciels requis
Les logiciels suivants doivent être installés avant la mise en service de l’application :
Logiciel	Version recommandée
Python	3.10 ou supérieur
MySQL Server	8.0 ou supérieur
Git	Dernière version stable

4. Installation de Python
Étape 1 : Téléchargement
Télécharger Python depuis :
https://www.python.org/downloads/
Étape 2 : Installation
Exécuter le programme d’installation puis cocher :
Add Python to PATH
Cliquer ensuite sur :
Install Now
Étape 3 : Vérification
Ouvrir l’invite de commande puis exécuter :
python --version
Le système doit afficher la version installée de Python.

5. Installation de Git
Télécharger Git depuis :
https://git-scm.com/downloads
Après installation, vérifier :
git --version

6. Installation de MySQL
Télécharger MySQL Community Server :
https://dev.mysql.com/downloads/mysql/
Lors de l’installation :
Choisir une installation standard.
Définir le mot de passe de l’utilisateur root.
Conserver le port par défaut : 3306.
Vérifier l’installation :
mysql --version

7. Récupération du projet
Depuis GitHub
Cloner le dépôt :
git clone URL_DU_DEPOT_GITHUB
Accéder au dossier du projet :
cd honey_group_manager
Ou depuis une archive ZIP
1.Décompresser le dossier fourni.
2.Ouvrir un terminal dans le dossier :
honey_group_manager

8. Création de l’environnement virtuel Python
Créer l’environnement virtuel :
python -m venv venv
Activation sous Windows :
venv\Scripts\activate
Une fois activé, le préfixe (venv) apparaît dans le terminal.

9. Installation des dépendances
Installer l’ensemble des bibliothèques du projet :
pip install -r requirements.txt
Cette commande installera automatiquement :
Django 4.2.30
Django Jazzmin 3.0.4
mysqlclient
mysql-connector-python
PyMySQL
Pillow
ReportLab
FPDF2
WhiteNoise
Gunicorn
ainsi que toutes les dépendances nécessaires au fonctionnement de l’application.
Vérification
pip list
Les bibliothèques installées doivent apparaître dans la liste.

10. Création de la base de données
Se connecter à MySQL puis créer la base de données :
CREATE DATABASE honeygroup_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

11. Configuration de la connexion MySQL
Ouvrir le fichier :
core/settings.py
Vérifier ou adapter les paramètres suivants :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'honeygroup_db',
        'USER': 'root',
        'PASSWORD': 'mot_de_passe_mysql',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Enregistrer les modifications.

12. Restauration de la base de données
Si un fichier de sauvegarde est fourni :
honeygroup_db.sql
Restaurer la base de données :
mysql -u root -p honeygroup_db < honeygroup_db.sql
Cette opération permet de récupérer :
les utilisateurs ;
les destinations ;
les circuits ;
les prestations ;
les paramètres globaux ;
les cotations enregistrées.

13. Application des migrations
Si nécessaire, exécuter :
python manage.py migrate
Cette commande crée ou met à jour les tables nécessaires au fonctionnement de l’application.

14. Création d’un compte administrateur
Si aucun compte administrateur n’est présent dans la base :
Méthode 1
python manage.py createsuperuser
Méthode 2
Utiliser le script fourni :
python create_superuser.py
Compte par défaut :
Nom d'utilisateur : admin
Mot de passe : admin12345
Il est recommandé de modifier ce mot de passe après la première connexion.

15. Démarrage de l’application
Lancer le serveur Django :
python manage.py runserver
Si le démarrage est réussi, le message suivant apparaît :
Starting development server at http://127.0.0.1:8000/

16. Accès à l’application
Interface utilisateur
http://127.0.0.1:8000
Interface d’administration
http://127.0.0.1:8000/admin
L’administration utilise le thème Django Jazzmin afin d’offrir une interface moderne et ergonomique.

17. Sauvegarde de la base de données
Export
mysqldump -u root -p honeygroup_db > honeygroup_db.sql
Restauration
mysql -u root -p honeygroup_db < honeygroup_db.sql
Il est recommandé d’effectuer une sauvegarde régulière afin de garantir la sécurité des données.

18. Structure générale du projet
honey_group_manager/
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── cotation/
│
├── templates/
├── static/
├── media/
│
├── create_superuser.py
├── manage.py
├── requirements.txt
│
└── README.md

19. Assistance technique
En cas de problème lors de l’installation :
1.Vérifier que Python et MySQL sont correctement installés.
2.Vérifier la configuration de la base de données dans settings.py.
3.Vérifier que toutes les dépendances ont été installées via requirements.txt.
4.Consulter la documentation technique du projet.

20. Fin de l’installation
Lorsque toutes les étapes précédentes ont été réalisées avec succès, l’application est prête à être utilisée.
L’utilisateur peut alors accéder au système, gérer les données de référence et générer des cotations à partir des circuits configurés.
