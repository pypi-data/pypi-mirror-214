import hashlib
import os
import shutil
import tempfile
from datetime import datetime

from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from photoflow import db
from photoflow.metadata import get_metadata, MissingToolError
from photoflow.extensions import db
from photoflow.models import Picture, AlbumPicture

from flask import current_app

def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as handle:
        while True:
            data = handle.read(2 ** 16)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def check_file_supported(path):
    try:
        with Image.open(path) as im:
            width, height = im.size
        # Only import readable images, skip thumbnails or RAW files detected as only the thumbnail in a tiff
        return width > 200 and height > 200
    except Exception as e:
        print(e)
        return False


def import_image(path, name=None):
    cleanup = False
    if isinstance(path, FileStorage):
        cleanup = True
        fname = secure_filename(path.filename)
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            path.save(tf)
            path = tf.name
    else:
        fname = os.path.basename(path)
    hash = hash_file(path)

    existing = Picture.query.filter_by(hash=hash).first()
    if existing:
        print(f"Picture {hash} already exists, skipping")
        return existing.id

    directory = os.path.join(current_app.instance_path, 'datastore', hash)

    row = Picture()
    row.hash = hash
    if name is not None:
        row.name = name
    else:
        row.name = fname
    row.created = datetime.now()
    row.extension = fname
    target = os.path.join(directory, fname)
    os.makedirs(directory)

    shutil.copy(path, target)
    try:
        metadata = get_metadata(path)
    except MissingToolError:
        shutil.rmtree(directory)
        raise
    for field in metadata:
        setattr(row, field, metadata[field])

    try:
        db.session.add(row)
        db.session.commit()
    except:
        shutil.rmtree(directory)
        raise

    if cleanup:
        os.unlink(path)
    return row.id


def remove_missing_from_datastore():
    print("Looking for database rows that don't have a matching picture in the datastore directory...")
    if not os.path.isdir(os.path.join(current_app.instance_path, 'datastore')):
        print("Cannot find the datastore directory, aborting so database doesn't get completely emptied")
        exit(1)
    counter = 0
    for picture in Picture.query.all():
        if not os.path.isdir(os.path.join(current_app.instance_path, 'datastore', picture.hash)):
            counter += 1
            for link in AlbumPicture.query.filter_by(picture_id=picture.id).all():
                db.session.delete(link)
            db.session.delete(picture)
    db.session.commit()
    print(f"Done, removed {counter} images")
