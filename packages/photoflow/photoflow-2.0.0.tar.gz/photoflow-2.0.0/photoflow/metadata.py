import subprocess
import json
from datetime import datetime

class MissingToolError(Exception):
    pass


def get_metadata(filename):
    # Using exiftool because it's still a lot better than all the native options due to the MakerNotes parsing
    cmd = ['exiftool', '-json', filename]
    try:
        result = subprocess.check_output(cmd)
    except FileNotFoundError:
        raise MissingToolError("exiftool")
    tags = json.loads(result.decode())

    if len(tags) == 0:
        return None

    tags = tags[0]
    result = {}

    if 'Make' in tags and 'Model' in tags:
        make, model = clean_make_model(tags['Make'], tags['Model'])
        result['manufacturer'] = make
        result['model'] = model

    if 'ImageDescription' in tags:
        result['description'] = tags['ImageDescription']
    if 'Title' in tags:
        result['name'] = tags['Title']
    if 'Artist' in tags:
        result['creator'] = tags['Artist']
    if 'Publisher' in tags:
        result['publisher'] = tags['Publisher']
    if 'Copyright' in tags:
        result['rights'] = tags['Copyright']

    if 'DateTimeOriginal' in tags and tags['DateTimeOriginal'].strip() != '':
        result['taken'] = tags['DateTimeOriginal']
    elif 'DateTimeDigitized' in tags and tags['DateTimeDigitized'].strip() != '':
        result['taken'] = tags['DateTimeDigitized']
    elif 'MetadataDate' in tags and tags['MetadataDate'].strip() != '':
        result['taken'] = tags['MetadataDate']
    elif 'DateTime' in tags and tags['DateTime'].strip() != '':
        result['taken'] = tags['DateTime']

    if 'taken' in result:
        if '+' in result['taken']:
            time, zone = result['taken'].split('+', maxsplit=1)
            zone = zone.replace(':', '')
            parsed = datetime.strptime(f"{time}+{zone}", '%Y:%m:%d %H:%M:%S%z')
        else:
            parsed = datetime.strptime(result['taken'], '%Y:%m:%d %H:%M:%S')
        result['taken'] = parsed
    else:
        result['taken'] = datetime.now()

    if 'Software' in tags:
        software = clean_software(tags['Software'])
        if software is not None:
            result['software'] = software

    if 'ISO' in tags:
        result['iso'] = tags['ISO']

    if 'ExposureTime' in tags:
        if isinstance(tags['ExposureTime'], int):
            result['exposure_time'] = float(tags['ExposureTime'])
        elif isinstance(tags['ExposureTime'], float):
            result['exposure_time'] = tags['ExposureTime']
        else:
            nom, den = tags['ExposureTime'].split('/', maxsplit=1)
            result['exposure_time'] = int(nom) / int(den)

    if 'FNumber' in tags:
        result['fnumber'] = tags['FNumber']

    if 'FocalLength' in tags and tags['FocalLength'] != "0.0 mm":
        focal_length = float(tags['FocalLength'].split(' ')[0])
        if focal_length > 0:
            result['focal_length'] = focal_length
            if 'FocalLengthIn35mmFormat' in tags:
                equiv = float(tags['FocalLengthIn35mmFormat'].split(' ')[0])
                result['cropfactor'] = equiv / result['focal_length']

    if 'LensID' in tags:
        result['lensinfo'] = tags['LensID']
    elif 'LensSpec' in tags:
        result['lensinfo'] = tags['LensSpec']
    elif 'Lens' in tags:
        result['lensinfo'] = tags['Lens']

    if 'FlashAction' in tags:
        result['flash'] = tags['FlashAction']
    elif 'FlashMode' in tags:
        result['flash'] = tags['FlashMode']
    elif 'Flash' in tags:
        result['flash'] = tags['Flash']

    if 'ExternalFlashExposureComp' in tags:
        result['flash_compensation'] = tags['ExternalFlashExposureComp']

    if 'ImageWidth' in tags:
        result['width'] = tags['ImageWidth']
    if 'ImageHeight' in tags:
        result['height'] = tags['ImageHeight']

    return result


def clean_make_model(make, model):
    if make.lower() in ['sony', 'panasonic']:
        model = f'{make} {model}'
    rewrites = {
        'NIKON': 'Nikon',
        'FC300C': 'DJI Phantom 3 standard',
        'SONY': 'Sony',
        'ILCE-6': 'α6',
        'ONEPLUS': 'OnePlus',
        'PANASONIC': 'Panasonic'
    }
    for search in rewrites:
        model = model.replace(search, rewrites[search])
    make = make.title()
    return make, model


def clean_software(software):
    # Filter android phones that have HDR+ enabled
    if software.startswith('HDR+'):
        return None

    # A lot of android phones set the editor to the kernel version
    if 'release-keys' in software:
        return None

    rewrites = {
        'darktable': 'Darktable',
        'GIMP': 'Gimp',
    }

    for search in rewrites:
        software = software.replace(search, rewrites[search])
    return software


if __name__ == '__main__':
    result = get_metadata('/workspace/test.jpg')
    if result is None:
        print("No exif")
        exit(0)
    for k in result:
        print(f"{k}: {result[k]}")
