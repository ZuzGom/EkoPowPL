from numpy import rad2deg
import math
import ephem



def isstrack():
    """
    Calculates data pictures coordinates by using pyephem and reverse-geocoder libraries
    """
    # global obslat, obslong, dn, latlong, country, admin, city, opisgeo1
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   20316.41516162  .00001589  00000+0  36499-4 0  9995"
    line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"

    iss = ephem.readtle(name, line1, line2)
    iss.compute()

    obs = ephem.Observer()
    # iss = ephem.readtle(name, line1, line2) # Puts data to ephem
    sun = ephem.Sun()  # Imports ephem's sun as sun
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