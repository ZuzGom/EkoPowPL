import ephem as em
from numpy import rad2deg
import math
from bati import track

def isstrack():
    """
    Calculates data pictures coordinates by using pyephem and reverse-geocoder libraries
    """
    # global obslat, obslong, dn, latlong, country, admin, city, opisgeo1

    # sposob ze strony

    # ^ zmienic przed oddaniem:
    # http://www.celestrak.com/NORAD/elements/stations.txt


    name, line1, line2 = track()

    iss = em.readtle(name, line1, line2)

    iss.compute()

    print(f"{iss.sublat / em.degree} {iss.sublong / em.degree}")

    # sposob z poprzednich lat

    obs = em.Observer()
    # iss = ephem.readtle(name, line1, line2) # Puts data to ephem
    sun = em.Sun()  # Imports ephem's sun as sun
    twilight = math.radians(-6)
    obs.lat = iss.sublat
    obs.long = iss.sublong
    obslat = obs.lat
    obslong = obs.long
    obs.elevation = 0
    sun.compute(obs)
    sun_angle = math.degrees(sun.alt)
    # Day or Night
    dn = 'Day' if sun_angle > twilight else 'Night'

    latlong = ("Lat %s - Long %s" % (iss.sublat, iss.sublong))

    # Searching data of site under ISS
    colat = rad2deg(iss.sublat)
    colong = rad2deg(iss.sublong)
    coordinates = (colat, colong)
    print(coordinates)


isstrack()
