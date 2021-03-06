# Serveur pour l'application de l'Amicale (Campus)

Partie serveur pour [l'application de l'amicale](https://github.com/ClubInfoInsaT/application-amicale), publiée sous licence GPLv3.

Le serveur est programmé avec python 3.6 en utilisant des [venv](https://docs.python.org/3/tutorial/venv.html).

⚠ **Ne pas utiliser une version supérieure à python 3.6**. Le serveur utilise cette version, le développement doit donc se faire avec.

## Structure

Pour des raisons de compatibilité, 2 versions sont en ligne sur le serveur : une dans `publich_html` et une autre dans `public_html/v2`. La première version est à ignorer et à supprimer dans le futur. La v2 est celle actuellement utilisée.

## Installation

Tout d'abord, clonez ce dépôt dans le dossier désiré et déplacez-vous dedans.

```shell
git clone git@github.com:ClubInfoInsaT/application-amicale-serveur.git
cd application-amicale-serveur
```

Ensuite, créez le venv. Cette étape a seulement besoin d'être réalisée une fois :
```shell
python3 -m venv venv
```

Activer le venv. Cette commande permet d'utiliser le python installé dans le venv au lieu de celui du système :
```shell
source venv/bin/activate
```
Et enfin, installez les dépendances :

```shell
pip install -r requirements.txt
```

## Mettre à jour les dépendances

Ouvrez le fichier `requirements.txt` et écrivez la nouvelle version de la librairie à utiliser. Ensuite, relancez l'isntallation des dépendances après avoir chargé le venv comme expliqué plus haut.

## Envoyer les mises à jour sur le serveur

Le serveur est synchronisé avec git, il suffit donc de se connecter sur l'espace web, de se déplacer dans le dossier v2 et de récupérer les derniers changements:

```shell
ssh amicale_app@etud.insa-toulouse.fr
cd public_html/v2
git pull
```

Si vous avez modifié les versions des librairies dans `requirements.txt`, pensez à les mettre à jour sur le serveur avec la commande suivante:

```shell
source venv/bin/activate
pip install -r requirements.txt
```

## Mises à jour 'BREAKING'

Si une mise à jour casse la compatibilité avec la version actuelle de l'application, il est nécessaire de garder l'ancienne version du logiciel serveur le temps que tout le monde mette l'application à jour (plusieurs mois).

Pour cela, créez un nouveau dossier pour la nouvelle version dans `public_html`. Par exemple, pour passer de la version 2 (installée dans `public_html/v2`), il faut installer la nouvelle version dans le dossier `public_html/v3`.

Pour cela, il faut tout réinstaller dans ce dossier comme suit:

```shell
ssh amicale_app@etud.insa-toulouse.fr
cd public_html
git clone https://github.com/ClubInfoInsaT/application-amicale-serveur.git v<NUMERO_DE_VERSION>
cd v<NUMERO_DE_VERSION>
```

Noter que la commande `git clone` utilise le lien HTTPS et non pas SSH, car le serveur refuse les connexions SSH autre que pour les sessions.

Ensuite, créez le venv:
```shell
python3 -m venv venv
```

Et enfin, installez les dépendances:

```shell
source venv/bin/activate
pip install -r requirements.txt
```

Pensez ensuite à rediriger l'application vers cette nouvelle version.