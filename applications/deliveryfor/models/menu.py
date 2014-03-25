##########################################
####title#################################
##########################################
if request.function == 'index':                                                                                                                                 
    response.title = 'deliveryfor'    
elif request.function == 'location':  
    location_name = db(db.locations.url_title == request.args(0)).select()[0]['name']
    response.title = location_name + ' - deliveryfor'
elif request.function == 'member':  
    response.title = request.args(0) + ' - deliveryfor'                                                                                                                              
else:
    response.title = request.function


##########################################
####markup################################
##########################################
response.meta.author = 'Trevor Overman <troverman@gmail.com>'
response.meta.description = 'deliveryfor you !'
response.meta.keywords = 'delivery, drivers, lazy'
response.meta.generator = 'deliveryfor'


##########################################
####analytics#############################
##########################################
response.google_analytics_id = None


##########################################
####global_variables######################
##########################################
import random
k = random.randint(800, 8047)
k1 = random.randint(0, 100)
k2 = random.randint(0, 100)
     
radius = k
(latitude, longitude) = (k1,k2)
lat_lng_array=[]


##########################################
####avaibility_scan#######################
##########################################

import datetime
if session.auth is None:

    delivery_profile_id=''
    #is_available_array
    #for current_availability in current_availability_array:
        #if end_availability - datetime.datetime.now() < datetime.timedelta(days=0):
            #db(db.user_availability.user_id==session.auth.user.id).update(is_available='false')


else:
    msg=[]
    delivery_profile_id = db(db.delivery_profile.user_id==session.auth.user.id).select()

    if delivery_profile_id:    
                
        start_availability_array = [r.start_availability for r in db(db.member_availability.user_id==session.auth.user.id).select(db.member_availability.start_availability)]
        end_availability_array = [r.end_availability for r in db(db.member_availability.user_id==session.auth.user.id).select(db.member_availability.end_availability)]
       

        
        for end_availability in end_availability_array:
            
            if end_availability - datetime.datetime.now() < datetime.timedelta(days=0):   
                msg.append('this availibility has expired')  
                #db(db.user_availability.user_id==session.auth.user.id).update(end_availability=datetime.datetime.now(),start_availability=datetime.datetime.now(), is_available='false')


            else:
                msg.append('this availibility is active')  
                #db(db.user_availability.user_id==session.auth.user.id).update(is_available='true')  

                #if session is notalready scanned  
                #if is in active database   
                
                delivery_location = db(db.delivery_profile.user_id==session.auth.user.id).select(db.delivery_profile.current_location)[0]['current_location']
                from gluon.tools import geocode
                (latitude, longitude) = geocode(delivery_location)                                        
                                                                
                session.has_scanned = 'false'                                                                                                 
                #####scan when a delivery driver becomes is active
                if session.has_scanned == 'false':
                    session.has_scanned = 'true'
                    import gluon.contrib.simplejson
                    from gluon.tools import fetch
                    lat = latitude
                    lng = longitude
                    radius = 5000
                    places_url = fetch("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&sensor=false&key=AIzaSyCGdFtkeR8egXJvte3eLH3deLKXXmPuXlA")
                    locations_in_radius = gluon.contrib.simplejson.loads(places_url)
                    results_array = locations_in_radius['results']  
                         
                              
                                   
                                        
                                             
                                                       
                         
                             
    #is_available_array
    #for current_availability in current_availability_array:
        #if end_availability - datetime.datetime.now() < datetime.timedelta(days=0):
            #db(db.user_availability.user_id==session.auth.user.id).update(is_available='false')
