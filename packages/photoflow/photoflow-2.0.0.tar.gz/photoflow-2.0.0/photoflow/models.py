from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from photoflow import db


class BaseRow(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)


class User(BaseRow, UserMixin):
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get(cls, id):
        return cls.query.get(int(id))


class Album(BaseRow):
    name = db.Column(db.String)
    hash = db.Column(db.String)
    visibility = db.Column(db.Integer, nullable=False, default=0)
    cover = db.Column(db.Integer, db.ForeignKey('picture.id', name='fk_cover_id'))
    coverref = db.relationship('Picture')
    pictures = db.relationship("AlbumPicture")


class Picture(BaseRow):
    name = db.Column(db.String)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    taken = db.Column(db.DateTime)
    visibility = db.Column(db.Integer, nullable=False, default=0)
    hash = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    extension = db.Column(db.String, nullable=False)
    raw_extension = db.Column(db.String)
    meta_extension = db.Column(db.String)

    # Positional metadata
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Camera metadata
    manufacturer = db.Column(db.Text)  # Camera or scanner manufacturer
    model = db.Column(db.Text)  # Camera or scanner model
    imagenumber = db.Column(db.Integer)  # Index within a burst/bracket
    exposure_time = db.Column(db.Float)  # Exposure time in seconds
    fnumber = db.Column(db.Float)  # Fnumber in 1/fnumber
    cropfactor = db.Column(db.Float)  # Ratio to 35mm equivalent
    iso = db.Column(db.Float)  # Iso rating
    lensinfo = db.Column(db.Text)  # Lens identification
    flash = db.Column(db.Text)  # Flash information
    focal_length = db.Column(db.Float)  # Lens focal length
    exposure_compensation = db.Column(db.Float)  # Exposure compensation in stops
    flash_compensation = db.Column(db.Float)  # Flash compensation in stops

    # Extra metadata for analog film scans
    original_manufacturer = db.Column(db.Text)  # Camera manufacturer before the film scan
    original_model = db.Column(db.Text)  # Camera model before the film scan
    original_lens = db.Column(db.Text)  # Lens on the camera before the film scan
    original_flash = db.Column(db.Text)  # Flash information
    original_focal_length = db.Column(db.Float)  # Original camera focal length
    original_exposure_compensation = db.Column(db.Float)  # Exposure compensation in stops
    original_flash_compensation = db.Column(db.Float)  # Flash compensation in stops
    original_cropfactor = db.Column(db.Float)  # Ratio to 35mm equivalent
    frame_number = db.Column(db.Integer)  # Image number on the film roll, 1-indexed
    film_stock = db.Column(db.Text)  # Film roll name
    film_format = db.Column(db.Text)  # Firm roll type
    film_notes = db.Column(db.Text)  # Extra notes field

    # Editing software
    software = db.Column(db.Text)

    # License information
    publisher = db.Column(db.Text)
    creator = db.Column(db.Text)
    rights = db.Column(db.Text)


class AlbumPicture(db.Model):
    album_id = db.Column(db.ForeignKey('album.id'), primary_key=True)
    picture_id = db.Column(db.ForeignKey('picture.id'), primary_key=True)
    album = db.relationship("Album")
    picture = db.relationship("Picture")
    index = db.Column(db.Integer)
