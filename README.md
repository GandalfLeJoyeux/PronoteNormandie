# PronoteNormandie

PronoteNormandie est un script python permettant de recevoir une notification [PushBullet](https://www.pushbullet.com/) pour être averti lorsqu'une nouvelle note est ajoutée sur pronote.  

## Pour commencer
Il vous faut un compte [PushBullet](https://www.pushbullet.com/), l'application sur votre téléphone et modifier le fichier login.txt avec en première ligne votre identidiant ENT, en deuxième ligne votre mot de passe et sur la troisième votre token PushBullet.  
Il est recommandé d'utiliser docker pour le déployer sur un serveur.


## Installation

Fichiers requis :
- main.py
- pronote.py
- note.txt
- login.txt
- requirements.txt
- Dockerfile  

Commencez par installer [Docker](https://docs.docker.com/desktop/install/linux-install/) et cloner le repo avec :
```bash
git clone https://github.com/GandalfLeJoyeux/PronoteNormandie.git
```
Maintenant que nous avons ce qu'il nous faut éditer le fichier login.txt et renseigner vos identifiants ligne par ligne de cette manière :  
1. Identifiant ENT (p.nomxx)
2. Mot de passe ENT
3. Token PushBullet

Ensuite il nous faut créer l'image du conteneur avec docker build, éxecutez la commande :  
```bash
docker build -t pronotenormandie:1.0 .
```
Une fois le processus terminé vérifiez que l'image a bien été créé avec la commande :
```bash
docker images
```
Puis enfin vous pouvez lancer le conteneur avec la commande :
```bash
docker run --detach --restart always --name pronote_normandie pronotenormandie:1.0
```
Et voilà c'est prêt vous devriez recevoir les premières notififications d'ici une trentaine de secondes. :ok_hand:
