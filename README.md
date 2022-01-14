# TO52_helice_holographique

Dépôt du projet de l'UV TO52 (projet de développement) de l'[Université de Technologie de Belfort-Montbéliard](https://www.utbm.fr) qui consiste à concevoir et fabriquer un affichage holographique à hélice tournante.

## Etudiants
* Valentin Mercy
* Sandra Levayer

## Enseignant  responsable
Franck Gechter

## Sujet initial
Suite à la restructuration de l'offre pédagogique de la formation informatique, il est maintenant prévu de mettre en place des éléments de communication innovants. L'objectif de ce travail est de réaliser un outil de projection holographique de type Helice rotative s'appuyant sur la limitation de la persistence rétinienne. Outre la partie matériel qu'il faudra réaliser et assembler en s'appuyant sur les plate-formes disponibles au sein du Crunch Lab, il s'agira de mettre en place les modèles 3D à afficher de façon à ce qu'il soit diffusable avec la puissance limitée d'un raspberry Pi 4.
* Voici une vidéo d'exemple : https://www.youtube.com/watch?v=rq9-5jfW0lU
* Voici une de vulgarisation en français: https://www.youtube.com/watch?v=GEywumyEaT4 

# Installation
Pour que l'hélice fonctionne correctement, la Raspberry doit être sous Raspbian.
Il suffit ensuite de suivre les étapes suivantes via un terminal :
1. Connecter la Raspberry à internet
```
sudo raspi-config
Choisir "2. Network Options", saisir le SSID et le mot de passe du réseau Wi-Fi et valider
```
2. Cloner le dépôt Git sur celle-ci
```
git clone https://github.com/vmercy/TO52_helice_holographique.git
```
3. Créer le fichier d'environnement ```.env``` :
```
cd main/
nano .env
```
Et écrire à l'intérieur du fichier : 
```
flask_secret = "<INSERER_CARACTERES_ALEATOIRES>"
```
Enregistrer et quitter le fichier : Ctrl + X et "Oui"
4. Installer la version de WiringPi modifiée par nos soins :
```
cd CustomWiringPi
make clean
make install
cd ../
```
5. Installer python flask pour Python 3
```
sudo pip3 install flask python-dotenv
```
6. Afficher et prendre note de l'adresse IP de la Raspberry sur le réseau : 
```
ifconfig
```
7. Créer un dossier dossier **bin** dans **main/displayer** et un dossier **img_uploaded** dans **main** :
```
mkdir main/displayer/bin
mkdir main/img_uploaded
```
8. Compiler *displayer.c* et *flash_strip.c* :
```
make main/displayer
make main/flash_strip
```
7. Installer le service systemd :
```
cp main/displayer/displayWebServer.service /lib/systemd/system/displayWebServer.service
sudo chmod 644 /lib/systemd/system/displayWebServer.service
sudo systemctl daemon-reload
sudo systemctl enable displayWebServer.service
```
8. Redémarrer la raspberry
```
sudo reboot now
```

## Utilisation
Désormais, à chaque redémarrage l'hélice peut être commandée via un autre PC sur le même réseau en saisissant son adresse IP (voir étape 6 ci-dessus) dans le navigateur sous la forme ```http://<IP>:5000```