import ephem as em
from numpy import rad2deg
import math


def isstrack():
    """
    Calculates data pictures coordinates by using pyephem and reverse-geocoder libraries
    """
    # global obslat, obslong, dn, latlong, country, admin, city, opisgeo1

    # sposob ze strony

    name = "ISS (ZARYA)"

    line1 = "1 25544U 98067A   21016.23305200  .00001366  00000-0  32598-4 0  9992"
    line2 = "2 25544  51.6457  14.3113 0000235 231.0982 239.8264 15.49297436265049"

    # ^ zmienic przed oddaniem:
    # http://www.celestrak.com/NORAD/elements/stations.txt

    # line1 = "1 25544U 98067A   20316.41516162  .00001589  00000+0  36499-4 0  9995"
    # line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"

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
