# Serveur pour l'application de l'Amicale (Campus)

Partie serveur pour [l'application de l'amicale](https://git.etud.insa-toulouse.fr/vergnet/application-amicale), publiée sous licence GPLv3.

Le serveur est programmé avec python 3.6 en utilisant des [venv](https://docs.python.org/3/tutorial/venv.html).

## Structure

Pour des raisons de compatibilité, 2 versions sont en ligne sur le serveur: une dans `publich_html` et une autre dans `public_html/v2`. La première version est à ignorer et à supprimer dans le futur. La v2 est celle actuellement utilisée.

## Installation

Tout d'abord, clonez ce dépot dans le dossier désiré et déplacez vous dedans.

```shell
git clone https://git.etud.insa-toulouse.fr/vergnet/application-amicale-serveur.git
cd application-amicale-serveur
```

Ensuite, créez le venv:
```shell
python3 -m venv tutorial-env
```

Et enfin, installez les dépendances:

```shell
pip install -r requirements.txt
```

## Mettre à jour les dépendances

Ouvrez le fichier `requirements.txt` et écrivez la nouvelle version de la librairie à utiliser.
Ensuite, chargez le venv dans votre terminal:

```shell
source .venv/bin/activate
```

Cette commande permet d'utiliser le python installé dans le venv au lieu de celui du système.
Il ne reste plus qu'à installer les nouvelles versions référencées dans `requirements.txt`:

```shell
pip install -r requirements.txt
```

## Envoyer les mises à jour sur le serveur

Le serveur est synchronisé avec git, il suffit donc de se connecter sur l'espace web, de se déplacer dans le dossier v2 et de récupérer les derniers changements:

```shell
ssh amicale_app@etud.insa-toulouse.fr
cd public_html/v2
git pull
```

Si vous avez modifié les versions des librairies dans `requirements.txt`, pensez à les mettre à jour sur le serveur avec la commande suivante:

```shell
pip install -r requirements.txt
```

## Mises à jour 'BREAKING'

Si une mise à jour casse la compatibilité avec la version actuelle de l'application, il est nécessaire de garder l'ancienne version du logiciel serveur le temps que tout le monde mette l'application à jour (plusieurs mois).

Pour cela, créez un nouveau dossier pour la nouvelle version dans `public_html`. Par exemple, pour passer de la version 2 (installée dans `public_html/v2`), il faut installer la nouvelle version dans le dossier `public_html/v3`.

Pour cela, il faut tout réinstaller dans ce dossier comme suit:

```shell
ssh amicale_app@etud.insa-toulouse.fr
cd public_html
git clone https://git.etud.insa-toulouse.fr/vergnet/application-amicale-serveur.git v<NUMERO_DE_VERSION>
cd v<NUMERO_DE_VERSION>
```
Ensuite, créez le venv:
```shell
python3 -m venv tutorial-env
```

Et enfin, installez les dépendances:

```shell
pip install -r requirements.txt
```

Pensez ensuite à rediriger l'application vers cette nouvelle version.