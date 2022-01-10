# TO52_helice_holographique

Dépôt du projet de l'UV TO52 (projet de développement) de l'[Université de Technologie de Belfort-Montbéliard](https://www.utbm.fr) qui consiste à concevoir et fabriquer un affichage holographique à hélice tournante

## Etudiants
* Valentin Mercy
* Sandra Levayer

## Enseignant  responsable
Franck Gechter

## Sujet initial
Suite à la restructuration de l'offre pédagogique de la formation informatique, il est maintenant prévu de mettre en place des éléments de communication innovants. L'objectif de ce travail est de réaliser un outil de projection holographique de type Helice rotative s'appuyant sur la limitation de la persistence rétinienne. Outre la partie matériel qu'il faudra réaliser et assembler en s'appuyant sur les plate-formes disponibles au sein du Crunch Lab, il s'agira de mettre en place les modèles 3D à afficher de façon à ce qu'il soit diffusable avec la puissance limitée d'un raspberry Pi 4.
* Voici une vidéo d'exemple : https://www.youtube.com/watch?v=rq9-5jfW0lU
* Voici une vulgarisation en Français: https://www.youtube.com/watch?v=GEywumyEaT4 

# Installation
Pour que l'hélice fonctionne correctement, la Raspberry doit être sous Raspbian.
Il suffit ensuite de suivre les étapes suivantes via un terminal :
1. Connecter la Raspberry à internet
```
sudo raspi-config
Choisir "2. Network Options", saisir le SSID et le mot de passe et valider
```

1. Cloner le dépôt Git sur celle-ci
```
git clone https://github.com/vmercy/TO52_helice_holographique.git
```
3. Installer la version modifiée de WiringPi
```
cd CustomWiringPi
make clean
make install
```
4. Installer python flask pour Python 3
```
sudo pip3 install flask python-dotenv
```
5. Afficher l'adresse IP de la Raspberry sur le réseau : 
```
ifconfig
```
6. Installer le service systemd :
```

```
7. Redémarrer la raspberry
```
sudo reboot now
```

## Utilisation
8. Désormais, à chaque redémarrage l'hélice peut être commandée via un autre PC sur le même réseau en saisissant son adresse IP (voir étape 5 ci-dessus) dans le navigateur.