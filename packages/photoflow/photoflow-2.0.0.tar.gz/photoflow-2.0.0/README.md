# Photoflow

Photoflow is a photo hosting solution for uploading and sharing pictures including the accompanying raw files and with
the metadata extracted and displayed.

The user interface is somewhat inspired by google photos and the main photo gallery rendering is done by the
great [pig.js](https://github.com/schlosser/pig.js) library.

![Photoflow main screen](http://brixitcdn.net/metainfo/photoflow.png)

## Technical details

This is a Flask based Python webapplication. The application stores duplicates of the imported files in the datastore
directory. The datastore is the `datastore` directory inside the source folder, symlink this to whereever you want to
store the pictures. This is also used to store the generated thumbnails and the uploaded raw files.

## Installing

```shell-session
From the distribution package manager install exiftool and python3-waitress, these are the 
only external tools.
$ pip3 install -r requirements.txt # or use the OS package manager
$ export DATABASE=/path/to/your/desired/sqlite.db
$ export FLASK_APP=photoflow
$ export SECRET=totallyrandomsecretkeyusedforsecretthings
$ flask db upgrade
$ flask create-user [username] --admin
$ serve.py run
```

## Importing images

There are multiple ways to get images into Photoflow.

### Through the shell

```shell-session
make sure the environment variables are set from above
$ cd /path/to/photoflow
$ flask import-image image1.jpg image2.jpg image3.jpg
```

### Through the webinterface

The webinterface has an upload tab with a multi-upload field which also lets you create an album from the upload batch.

### Through Darktable

It is possible to upload images directly through Darktable by using the Piwigo upload plugin.

Use the hostname for the Photoflow deployment as the server in the Piwigo settings. If the deployment does not have
https then you'll need to prefix the hostname with http:// in the server field.

The album selection dialog will list all the albums in Photoflow and allows creating a new one for the current upload.
Nested albums are not supported. When visibility is set to "everyone" the album will be public in Photoflow. All other
options will make the album private.

## Service file

For running in a systemd distribution:

```systemd
[Unit]
Description=Photoflow picture host

[Service]
Type=simple
ExecStart=/usr/bin/env DATABASE=/srv/photoflow/app.db SECRET=hereisthesecret URL_SCHEME=https python3 serve.py run
Restart=on-failure
WorkingDirectory=/srv/photoflow

[Install]
WantedBy=multi-user.target
```