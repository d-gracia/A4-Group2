# %%
import requests #use to get data from apis

lat="42.360081"
lon="-71.058884"

zenith_dec = lat
zenith_ra = "cake"

sky_coords = "12 30 +10 20"
skyradius = "5"
skyunit = "arcmin"
#sky_api_url = "http://simbad.u-strasbg.fr/simbad/sim-coo?OutputMode=LIST&maxObject=20000&output.format=ASCII&Coord="\
#    +sky_coords+"&Radius="+skyradius+"&Radius.unit="+skyunit

#
#"http://simbad.u-strasbg.fr/simbad/sim-coo?OutputMode=LIST&maxObject=20000&output.format=ASCII&Coord=12 30 +10 20&Vmag<6.0&Radius=5&Radius.unit=arcmin
#

"""
ra > 15 & ra < 30
& dec > 15 & dec < 30
& Vmag < 6
"""


ramin=  "0"
ramax = "100"
decmin = "0"
decmax = "100"
limitingmag = "6"
sky_api_url="http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra+%3E+"+ramin+"+%26+ra+%3C+"+ramax+"%0D%0A%26+dec+%3E+"+decmin+"+%26+dec+%3C+"+decmax+"%0D%0A%26+Vmag+%3C+"+limitingmag+"&submit=submit+query&OutputMode=LIST&maxObject=2000&output.format=ASCII"

#sky_api_url="https://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=Vmag<6&region(circle,ICRS,J2000,12 31 %2B10 20,5d)&submit=submit+query&OutputMode=LIST&maxObject=2000&output.format=ASCII"


#sky_api_url="http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=region%28circle%2cICRS%2cJ2000%2c12%2031%20%2b10%2020%2c30d%29%0d%0a%26%28Vmag%3C6%29&submit=submit%20query&OutputMode=list&maxObject=10000&CriteriaFile=&output.format=ASCII"

skyreturn = requests.get(sky_api_url)
skyresponse = skyreturn.text


#print(skyresponse) #this prints out the ascii table

#print(skyresponse) #this prints out the ascii table

lines = skyresponse.split('\n')

object_list_len = int(lines[7][20:])

#print(lines[9:]) #
print()
print(object_list_len)


#for line in lines:
#    print(line)

#print(lines[11])


objects = lines[11:-3]

#for line in objects:
#    print(line)

#print(objects[0])

box = [ [None]*(13) for k in range(object_list_len)]

for i in range(object_list_len):
    for j in range(12):
        test = objects[i].split('|')
        box[i][j] = test[j]

# %% 
print(lines[9])
print()

for i in range(object_list_len):
    print(box[i][1])



# %%
print(object_list_len)
# %%
