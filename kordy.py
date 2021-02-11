import ephem as em
import reverse_geocoder as rg


def isstrack():
    """
    Calculates data pictures coordinates by using pyephem and reverse-geocoder libraries
    """

    # sposob ze strony

    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   21042.30870520  .00003041  00000-0  63421-4 0  9992"
    line2 = "2 25544  51.6440 245.3345 0002839 359.6306 175.5159 15.48962705269087"

    iss = em.readtle(name, line1, line2)

    iss.compute()

    lon = iss.sublat / em.degree
    lat = iss.sublong / em.degree

    results = rg.search((lon, lat), mode=1)

    country = str([row['cc'] for row in results][0])
    city = str([row['name'] for row in results][0])
    admin = str([row['admin1'] for row in results][0])
    opisgeo = country + '-' + admin + '-' + city
    return lon, lat, opisgeo
