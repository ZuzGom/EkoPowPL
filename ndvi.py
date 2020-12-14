def takePicture():
    global picname, notice, noticew
    # resolutions: 2592x1944, 1296x972, 640x480
    #camera.framerate=Fraction(1, 6)
    #camera.shutter_speed=100000
    #camera.exposure_mode='off'
    #camera.iso=800
    notice = "  "
    noticew = "  "
    NDVI = 0
    NDWI = 0
    sumR = 0
    sumG = 0
    sumB = 0
    sumNDVI = 0
    sumNDWI = 0
    sumaNDVI = 0
    sumaNDWI = 0
    camera.resolution = (1296,972)
    #dla tej rozdzielczosci mamy 330 Mb na godzine co daje nam 1GB na 3 godziny
    sleep(3)
    
    #isstrack()
    #timestamp()
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    print(time_stamp)
    print (timestamp)

    
    camera.annotate_text = "PL_Moons_" + time_stamp + latlong + " " + dn
    picname = "PL_Moons_" + timestamp + ".jpg"
    camera.capture(picname)
    #camera.close
    
    picname1 = "PL_Moons_" + timestamp + "proc.jpg"
 
    print(picname)
    if dn == 'Day':
        # processing image
        print(picname1)
        imag=Image.open(picname)
    
        imag=imag.convert("RGB")
        pixels = imag.load()
        #X,Y=0,0
        for x in range(0, 1296):
            for y in range(0, 972):
                pixelRGB=imag.getpixel((x,y))
                R,G,B=pixelRGB
                sumR = R + sumR
                sumG = G + sumG
                sumB = B + sumB
                if (R+B) != 0:
                    NDVI=(R-B)/(R+B)
                else:
                    NDVI = 0
                if  NDVI > 0.6:
                    pixelRGB = (0, 109, 58)
                elif NDVI > 0.2 and NDVI < 0.6 :
                    pixelRGB = (0, 165, 20)
                elif NDVI < -0.2:
                    pixels[x, y] = (0, 125, 125)
                #That will work in PIL 1.1.6 and up. If you have the bad luck of having to support an older version,
                # you can sacrifice performance and replace pix[x, y] = value with im.putpixel((x, y), value).
                if (G+R) != 0:
                    NDWI=(G-R)/(G+R)
                else:
                    NDWI = 0
                if NDVI < -0.2 and NDWI < -0.2:
                    pixels[x, y] = (0, 125, 125)
                sumNDVI = NDVI + sumNDVI
                sumNDWI = NDWI + sumaNDWI
                
            
        sumaNDVI = sumNDVI/1259712
        if sumaNDVI < -0.2 :
            print("water or clouds, NDVI= ", sumaNDVI)
            notice = "water or clouds"
        elif sumaNDVI < 0.2 and sumaNDVI > -0.2:
            print("other, NDVI= ", sumaNDVI)
            notice = "other"
        elif sumaNDVI > 0.2 and sumaNDVI < 0.6 :
            print("agriculture, NDVI= ", sumaNDVI)
            notice = "agriculture"
        elif sumaNDVI > 0.6:
            print("forest, NDVI= ", sumaNDVI)
            notice = "forest"
        print ("")
        sumaNDWI = sumaNDWI/1259712
        if sumaNDWI < 0 :
            print("no water or vegetation, NDWI= ", sumaNDWI)
            noticew = "water or clouds"
        elif sumaNDWI < 0.2 and sumaNDVI > -0.2:
            print("other, NDWI= ", sumaNDWI)
            notice = "other"
        elif sumaNDWI < -0.2 and sumaNDVI < -0.2:
            print("clouds, NDWI= ", sumaNDWI)
            noticew = "clouds"
        imag=imag.save(picname1)
        
    # Normalized difference vegetation index
    # In general, NDVI values range from -1.0 to 1.0, with negative values
    #indicating clouds and water, positive values near zero indicating bare soil, 
    #and higher positive values of NDVI ranging from sparse vegetation (0.1 - 0.5)
    #to dense green vegetation (0.6 and above).
    # NDVI = (NIR — VIS)/(NIR + VIS)
    #one or less                ---  barren rock, sand or snow 
    #approximately 0.2 to 0.5   ---- shrubs or agriculture
    #approximately 0.6 to 0.9   ---Dense vegetation (Forest)
    # https://ipad.fas.usda.gov/cropexplorer/description.aspx?legendid=6

    # Normalized difference water index
    # NDWI=(G-IR)/(G+IR)
    # -1 to 0 - Bright surface with no vegetation or water content
    # +1 - represent water content
    # from: http://www.aari.ru/docs/pub/060804/xuh06.pdf
    #NDWI > 0.4 = water