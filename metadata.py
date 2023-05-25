from PIL import ExifTags
from PIL.ExifTags import TAGS, GPSTAGS


def exifData(exif):
    try:
        metadata = {}
        for key, value in exif.items():
            decodeKey = TAGS.get(key, key)
            metadata[decodeKey] = value
        return metadata
    except:
        return None


def exifGPS(exif):
    gpsinfo = {}
    for key, value in (exif.get_ifd(ExifTags.IFD.GPSInfo)).items():
        decodeKey = GPSTAGS.get(key)
        gpsinfo[decodeKey] = value
    return gpsinfo


def moreExifData(exif):
    try:
        metadata = {}
        for key, value in exif.get_ifd(0x8769).items():
            decodeKey = TAGS.get(key, key)
            metadata[decodeKey] = value
        return metadata
    except:
        return None


def convertToDecimal(coords, coordRef):
    d, m, s = coords
    decimal = float(d) + float(m/60) + float(s/3600)
    if (coordRef == 'S' or coordRef == 'W'):
        return -decimal
    else:
        return decimal


def GPScoords(exif):
    gpsdata = exifGPS(exif)

    try:
        long = convertToDecimal(
            gpsdata["GPSLongitude"], gpsdata["GPSLongitudeRef"])
        lat = convertToDecimal(
            gpsdata["GPSLatitude"], gpsdata["GPSLatitudeRef"])
        return (long, lat)
    except KeyError:
        return None
