################################################################
####controllers#################################################
################################################################

################################
####about#######################
################################
def about():

    return dict()
    
################################
####account#####################
################################
def account():

    if session.auth is None:
        redirect(URL(''))        

    else:
        address_array = [r.address for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.address)]
        description_array = [r.description for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.description)]
        complete_address_array = [r.complete_address for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.complete_address)]
        location_id_array = [r.id for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.id)]
        start_availability_array = [r.start_availability for r in db(db.member_availability.user_id==session.auth.user.id).select(db.member_availability.start_availability)]
        end_availability_array = [r.end_availability for r in db(db.member_availability.user_id==session.auth.user.id).select(db.member_availability.end_availability)]
        availability_id_array = [r.id for r in db(db.member_availability.user_id==session.auth.user.id).select(db.member_availability.id)]
        member_picture_array = [r.picture for r in db(db.member_images.user_id==session.auth.user.id).select(db.member_images.picture)] 
        member_picture_id_array = [r.id for r in db(db.member_images.user_id==session.auth.user.id).select(db.member_images.id)]             
        flat_rate_array = [r.flat_rate for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.flat_rate)]
        percentage_array = [r.percentage for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.percentage)]
        per_distance_array = [r.per_distance for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.per_distance)]
        per_hour_array = [r.per_hour for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.per_hour)]
        min_amount_array = [r.min_amount for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.min_amount)]
        max_amount_array = [r.max_amount for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.max_amount)]
        is_active_array = [r.is_active for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.is_active)]
        member_currency = [r.member_currency for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.member_currency)]
        member_units = [r.member_units for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.member_units)]
        fee_id_array = [r.id for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.id)]
        fee_title_array = [r.title for r in db(db.member_fees.user_id==session.auth.user.id).select(db.member_fees.title)]

        complete_fee_array=[fee_id_array, flat_rate_array, percentage_array, per_distance_array, per_hour_array, min_amount_array, max_amount_array, is_active_array, member_currency, member_units, fee_title_array]
        delivery_profile_id = db(db.delivery_profile.user_id==session.auth.user.id).select()
        
        from gluon.tools import geocode
        for thecounter, complete_address in enumerate(complete_address_array):
            (latitude, longitude) = geocode(complete_address)
            lat_lng_array.append((latitude, longitude, complete_address, description_array[thecounter], description_array[thecounter]))

        #new location form
        form_newlocation = SQLFORM(db.member_locations, col3 = {'special_instructions':A('[?]',
          _href='http://www.google.com/search?q=define:address')})
        if form_newlocation.process(formname='member_locations').accepted:
            session.flash = 'Location Added'
            redirect(URL('/account'))        
        elif form_newlocation.errors:
            response.flash = 'Error'

        #location edit / delete forms
        form_location_edit_array = []
        for counter, x in enumerate(location_id_array):
            form_location_edit_array.append(SQLFORM(db.member_locations, x, deletable=True, submit_button = 'Save Location', showid = False))
            if form_location_edit_array[counter].process(formname='form_location_edit_array-' + str(counter)).accepted:
                response.flash = 'Location Updated'
                redirect(URL('/account'))        
            elif form_location_edit_array[counter].errors:
                response.flash = 'Error'
            
        member_settings_id = db(db.member_settings.user_id==session.auth.user.id).select()             
        if member_settings_id:
          hi=''
        else:
            db.member_settings.insert(member_language="English", member_currency="$ USD", member_units="Imperial") 
        
            
        member_settings_record = db(db.member_settings.user_id==session.auth.user.id).select(db.member_settings.id)[0]['id']  
        form_member_settings_general = SQLFORM(db.member_settings, member_settings_record, fields = ['member_language', 'member_currency', 'member_units'], separator = ' ', submit_button = 'Save profile', showid = False, labels = {'member_language':P('Language' ,_class='head'), 'member_currency':P('Currency', _class='head'), 'member_units':P('Units', _class='head')})           
        if form_member_settings_general.process(formname='form_member_settings_general').accepted:
            session.flash = 'Settings Updated'
            redirect(URL('/account'))        
        elif form_member_settings_general.errors:
            response.flash = 'Error'
        form_member_settings_notifications = SQLFORM(db.member_settings, member_settings_record, formstyle = 'divs', fields = ['member_accepts_email', 'member_phone_number'], submit_button = 'Save profile', showid = False, separator = ' ', labels = {'member_accepts_email':'', 'member_phone_number':P('Send text updates to this number', _class='head')}, col3 = {'member_accepts_email':P('Recieve news and update emails from deliveryfor', _class='head', _style="margin-left:5px;margin-top:20px;")})
        if form_member_settings_notifications.process(formname='form_member_settings_notifications').accepted:
            session.flash = 'Settings Updated'
            redirect(URL('/account'))        
        elif form_member_settings_notifications.errors:
            response.flash = 'Error'

        form_create_delivery_profile = SQLFORM(db.delivery_profile)
        terms = TR(LABEL('I agree to the terms and conditions'), INPUT(_name='agree',value=True,_type='checkbox'))
        form_create_delivery_profile[0].insert(-1,terms)
        if form_create_delivery_profile.process(formname='create_delivery_profile').accepted:
            session.flash = 'Profile Created'
            redirect(URL('/account'))        
        elif form_create_delivery_profile.errors:
            response.flash = 'Error'

        if delivery_profile_id:
            delivery_profile_record = db(db.delivery_profile.user_id==session.auth.user.id).select(db.delivery_profile.id)[0]['id']
            form_delivery_profile_update=SQLFORM(db.delivery_profile, delivery_profile_record, submit_button = 'Save profile', showid = False)
            if form_delivery_profile_update.process(formname='form_delivery_profile_update').accepted:
                session.flash = 'Profile Updated'
                redirect(URL('/member/'+session.auth.user.username))        
            elif form_delivery_profile_update.errors:
                response.flash = 'Error'
        else:
            form_delivery_profile_update=''
                
        form_upload_member_images = SQLFORM(db.member_images)
        if form_upload_member_images.process(formname='form_member_images').accepted:
            session.flash = 'Image Uploaded'
            redirect(URL('/account'))        
        elif form_upload_member_images.errors:
            response.flash = 'Error'

        form_edit_member_picture_array = []
        for counter, x in enumerate(member_picture_id_array):
            form_edit_member_picture_array.append(SQLFORM(db.member_images, x, deletable=True, submit_button = 'Save Picture', showid = False))
            if form_edit_member_picture_array[counter].process(formname='form_edit_member_picture_array-' + str(counter)).accepted:
                session.flash = 'Image Updated'
                redirect(URL('/account'))        
            elif form_edit_member_picture_array[counter].errors:
                response.flash = 'Error'
                                                                                                                                      
        form_create_member_availability = SQLFORM(db.member_availability)
        if form_create_member_availability.process(formname='form_create_member_availability', onvalidation=__onvalidation_availability).accepted:
            session.flash = 'Availability Added'
            redirect(URL('/account'))        
        elif form_create_member_availability.errors:
            response.flash = 'Error'
                                                           
        form_edit_member_availability_array = []
        for counter, x in enumerate(availability_id_array):

            form_edit_member_availability_array.append(SQLFORM(db.member_availability, x, deletable=True, submit_button = 'Save Availability', showid = False))
            if form_edit_member_availability_array[counter].process(formname='form_edit_member_availability_array-' + str(counter), onvalidation=__onvalidation_availability).accepted:
                session.flash = 'Availability Updated'
                redirect(URL('/account'))        
            elif form_edit_member_availability_array[counter].errors:
                response.flash = 'Error'
               
        form_create_member_fee = SQLFORM(db.member_fees)
        if form_create_member_fee.process(formname='form_create_member_fee').accepted:
            session.flash = 'Fee Added'
            redirect(URL('/account'))        
        elif form_create_member_fee.errors:
            response.flash = 'Error'    
            
        form_edit_member_fee_array = []
        for counter, x in enumerate(fee_id_array):
            form_edit_member_fee_array.append(SQLFORM(db.member_fees, x, deletable=True, submit_button = 'Save Fee', showid = False))
            if form_edit_member_fee_array[counter].process(formname='form_edit_member_fee_array-' + str(counter)).accepted:
                session.flash = 'Fee Updated'
                redirect(URL('/account'))        
            elif form_edit_member_fee_array[counter].errors:
                response.flash = 'Error'
    
    
    edit_member_information=SQLFORM(db.auth_user, auth.user_id, fields = ['first_name','last_name','email', 'username'], submit_button = 'save profile', showid = False)

    
    return dict(
    form_member_settings_notifications=form_member_settings_notifications,
    form_member_settings_general=form_member_settings_general,
    edit_member_information=edit_member_information,
        
    form_edit_member_picture_array=form_edit_member_picture_array,
    member_picture_array=member_picture_array,
    
    delivery_profile_id=delivery_profile_id,
    form_edit_member_fee_array=form_edit_member_fee_array,
    fee_id_array=fee_id_array,
    complete_fee_array=complete_fee_array,
    
    start_availability_array=start_availability_array,
    end_availability_array=end_availability_array,
    availability_id_array=availability_id_array,

    form_edit_member_availability_array=form_edit_member_availability_array,
    form_create_member_fee=form_create_member_fee,
    form_create_member_availability=form_create_member_availability,
    form_upload_member_images = form_upload_member_images,
    form_location_edit_array=form_location_edit_array,
    form_delivery_profile_update=form_delivery_profile_update,
    form_create_delivery_profile=form_create_delivery_profile,
    form_newlocation=form_newlocation,
    location_id_array=location_id_array,
    address_array = address_array,
    description_array = description_array,
    complete_address_array = complete_address_array,
    lat_lng_array = lat_lng_array,

    )

################################
####blog########################
################################
def blog():
    return dict()
    
################################
####business####################
################################
def business():
    return dict()
    
################################
####contact#####################
################################
def contact():
    return dict()
    
################################
####deals#######################
################################
def deals():
    return dict()
        
################################
####faq#########################
################################
def faq():
    return dict()                

################################
####index#######################
################################
def index():
    from gluon.tools import geocode
    import random
    #make function to go to nice long / lat
    latitude = longtitude = ''
    if session.auth is None:
        complete_address_array = ''
        delivery_member_array = []
        current_location_array = [r.current_location for r in db(db.delivery_profile).select(db.delivery_profile.current_location)]
        for location in current_location_array:
            delivery_profile_info = db(db.delivery_profile.current_location==location).select(db.delivery_profile.ALL).as_list()
            user_id_at_location = db(db.delivery_profile.current_location==location).select(db.delivery_profile.user_id).as_list()[0]['user_id']
            delivery_profile_pictures_array = [r.picture for r in db(db.member_images.user_id==user_id_at_location).select(db.member_images.picture)] 
            delivery_profile_username = db(db.auth_user.id==user_id_at_location).select(db.auth_user.username).as_list()[0]['username']
            (latitude, longitude) = geocode(location)
            delivery_member_array.append((latitude, longitude, location, delivery_profile_pictures_array, delivery_profile_username))
    else:
        complete_address_array = [r.complete_address for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.complete_address)]
        description_array = [r.description for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.description)]
        delivery_member_array = []    
        current_location_array = [r.current_location for r in db(db.delivery_profile).select(db.delivery_profile.current_location)]
        for location in current_location_array:
            delivery_profile_info = db(db.delivery_profile.current_location==location).select(db.delivery_profile.ALL).as_list()
            user_id_at_location = db(db.delivery_profile.current_location==location).select(db.delivery_profile.user_id).as_list()[0]['user_id']
            delivery_profile_pictures_array = [r.picture for r in db(db.member_images.user_id==user_id_at_location).select(db.member_images.picture)] 
            delivery_profile_username = db(db.auth_user.id==user_id_at_location).select(db.auth_user.username).as_list()[0]['username']
            (latitude, longitude) = geocode(location)
            delivery_member_array.append((latitude, longitude, location, delivery_profile_pictures_array, delivery_profile_username))
    search_form=SQLFORM(db.member_search)
    if search_form.process(session=None, formname='test').accepted:
        session.search_form_member_locations = search_form.vars.member_locations
        session.search_form_radius = search_form.vars.radius
        session.search_form_details = search_form.vars.details
        redirect(URL('search/' + search_form.vars.member_locations + '/' + search_form.vars.radius + 'mi/' + search_form.vars.details))  
    elif search_form.errors:
        response.flash = 'There\'s a problem!'
    session.flash = 'welcome to deliveryfor!'
    member_picture_array = [r.picture for r in db(db.member_images).select(db.member_images.picture)] 

    location_list = db(db.locations).select()
    location_array = []
    location_image_array=[]
    location_tag_list = []
    for location in location_list:
        location_image=db(db.location_images.location_id == location['id']).select()
        location_tag_list.append(db(db.location_tag.location_id == location['id']).select())

        location_tag=db(db.location_tag.location_id == location['id']).select()
        if location_image:
            location_array.append([location,location_image,location_tag])
    location_tag_list_array = []
    for tag_list in location_tag_list:
        for tag in tag_list:
            location_tag_list_array.append(tag['tag'])   



    set_location_tag_list = set(location_tag_list_array)
    tag_location_list_unsorted = list(set_location_tag_list)
    combined_count_and_tag_array=[]
    for tag in tag_location_list_unsorted:
        combined_count_and_tag_array.append([tag, location_tag_list_array.count(tag)])
    from operator import itemgetter
    tag_location_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))  




    index_block_list = db(db.html_block.html_type == 'index').select().as_list()
    random.shuffle(index_block_list)
    index_header_block_list = db(db.html_block.html_type == 'index-header').select().as_list()
    random.shuffle(index_header_block_list)
    index_header_block_list = index_header_block_list[0]['html_content']






    #for location in location_list:
        #location_tag_list.append(db(db.location_tag.location_id == location['id']).select())
        #location_picture_list.append(db(db.location_images.location_id == location['id']).select())

    




    
    return dict(
        tag_location_list_sorted_by_total_count=tag_location_list_sorted_by_total_count,
        index_header_block_list=index_header_block_list,
        delivery_member_array=delivery_member_array,
        search_form=search_form,
        at_lng_array = lat_lng_array,
        member_picture_array=member_picture_array,
        location_array=location_array,
        index_block_list=index_block_list,
    )

    
################################
####item########################
################################
def item():
    return dict()
    
################################
####items#######################
################################
def items():
    item_picture_array = db(db.location_images).select()                                                                                                        

    return dict(item_picture_array=item_picture_array)
          
################################
####location####################
################################
def location():
    
    location_from_url = db(db.locations.url_title==request.args(0)).select()
    id_from_url = db(db.locations.url_title==request.args(0)).select(db.locations.id)[0]['id']
    item_array = db(db.location_item.location_id==id_from_url).select()
    item_array = db(db.location_item.location_id==id_from_url).select()
    
    form_rate_location = SQLFORM(db.ratings)

    if form_rate_location.process(formname='form_rate_location', onvalidation=__onvalidation_rating).accepted:
        session.flash = 'Location Rated'
        redirect(URL('location/' + request.args(0))) 
    elif form_rate_location.errors:
        response.flash = 'Error'
                                                                  
    location_rating_array=db((db.ratings.ratee_id==id_from_url) & (db.ratings.ratee_type=='location')).select() 
                                                                                        
    from gluon.tools import geocode
    lat_lng_array_location = []
    lat_lng_array_member = []
    (latitude, longitude) = geocode(location_from_url[0]['complete_address'])
    lat_lng_array_location.append((latitude, longitude, location_from_url[0]['name'], location_from_url[0]['name'], location_from_url[0]['description'], 0))
    

    ####find near_by delivery drivers, need to restict to active. na meen yeah
    import math
    (lat1, long1) = geocode(location_from_url[0]['complete_address'])
    location_from_member = db(db.delivery_profile).select()
    distance_meter_array = []
    for location in location_from_member:
        (lat2, long2) = geocode(location['current_location'])
        degrees_to_radians = math.pi / 180.0
        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians   
        theta1 = long1  * degrees_to_radians
        theta2 = long2 * degrees_to_radians
        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
        distance_in_meters = math.acos(cos) * 6378100

        distance_meter_array.append([float(location['delivery_radius']) - distance_in_meters, float(location['max_radius_from_home']) - distance_in_meters, location])
    available_member_array = []
    for element in distance_meter_array:
        if element[0] > 0: 
            if element[1] > 0:
                available_member_array.append(element[2])
                (lat2, long2) = geocode(element[2]['current_location'])
                username = db(db.auth_user.id == element[2]['user_id']).select()[0]['username']
                member_images = db(db.member_images.user_id == element[2]['user_id']).select()
                lat_lng_array_member.append((lat2, long2, element[2]['current_location'], element[2]['current_location'], username, element[2]['delivery_radius'],member_images))

    location_picture_array = db(db.location_images.location_id == id_from_url).select()  
    items_from_location = db(db.location_item.location_id == id_from_url).select()


    #member_orders_from_location = db((db.member_orders.location_id == id_from_url) & (db.member_orders.member_id == auth.user_id)).select()
    member_orders_from_location = db(db.member_orders.location_id == id_from_url).select()

                                                                                                        
    return dict(
    location_picture_array=location_picture_array,
    available_member_array=available_member_array,
    distance_meter_array=distance_meter_array,
    location_from_url=location_from_url,
    id_from_url=id_from_url,
    lat_lng_array_member=lat_lng_array_member,
    lat_lng_array_location=lat_lng_array_location,
    items_from_location=items_from_location,
    member_orders_from_location=member_orders_from_location,
    )


################################
####locations###################
################################
def locations():
    location_list = db(db.locations).select()
    location_picture_array = db(db.location_images).select()   
    delivery_member_array = db(db.delivery_profile).select()







    location_tag_list = []
    location_picture_list = []
    for location in location_list:
        location_tag_list.append(db(db.location_tag.location_id == location['id']).select())
        location_picture_list.append(db(db.location_images.location_id == location['id']).select())

    location_tag_list_array = []
    for tag_list in location_tag_list:
        for tag in tag_list:
            location_tag_list_array.append(tag['tag'])   

    set_location_tag_list = set(location_tag_list_array)
    tag_location_list_unsorted = list(set_location_tag_list)
    combined_count_and_tag_array=[]
    for tag in tag_location_list_unsorted:
        combined_count_and_tag_array.append([tag, location_tag_list_array.count(tag)])
    from operator import itemgetter
    tag_location_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))  














    from gluon.tools import geocode
    lat_lng_array = []
    location_array = []

    for location in location_list:
        (latitude, longitude) = geocode(location['complete_address'])
        lat_lng_array.append([latitude, longitude, location['name']])

        location_image=db(db.location_images.location_id == location['id']).select()
        location_tag=db(db.location_tag.location_id == location['id']).select()

        if location_image:
            location_array.append([location,location_image,location_tag])
        else:
            location_array.append([location,"null",location_tag])


    
    return dict(
        lat_lng_array=lat_lng_array,
        location_list=location_list,
        location_picture_array=location_picture_array,
        location_array=location_array,
        tag_location_list_sorted_by_total_count=tag_location_list_sorted_by_total_count,
        delivery_member_array=delivery_member_array,
        )
  
################################
####logout######################
################################
def logout():
    auth.logout
    return dict()     

################################
####mission#####################
################################
def mission():
    return dict()                
        
################################
####member######################
################################
def member():
    if session.auth is None:
        delivery_profile_id=''
    else:
        delivery_profile_id = db(db.delivery_profile.user_id==session.auth.user.id).select()

    id_from_username = db(db.auth_user.username==request.args(0)).select(db.auth_user.id)[0]['id']
    current_location = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.current_location)[0]['current_location']
    profile_firstname = db(db.auth_user.id==id_from_username).select(db.auth_user.first_name).as_list()[0]['first_name']
    profile_lastname = db(db.auth_user.id==id_from_username).select(db.auth_user.last_name)[0]['last_name']
    
    start_availability_array = [r.start_availability for r in db(db.member_availability.user_id==id_from_username).select(db.member_availability.start_availability)]
    end_availability_array = [r.end_availability for r in db(db.member_availability.user_id==id_from_username).select(db.member_availability.end_availability)]
    availability_id_array = [r.id for r in db(db.member_availability.user_id==id_from_username).select(db.member_availability.id)]

    member_picture_array = [r.picture for r in db(db.member_images.user_id==id_from_username).select(db.member_images.picture)]    
    
    flat_rate_array = [r.flat_rate for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.flat_rate)]
    percentage_array = [r.percentage for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.percentage)]
    per_distance_array = [r.per_distance for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.per_distance)]
    per_hour_array = [r.per_hour for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.per_hour)]
    min_amount_array = [r.min_amount for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.min_amount)]
    max_amount_array = [r.max_amount for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.max_amount)]
    is_active_array = [r.is_active for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.is_active)]
    member_currency = [r.member_currency for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.member_currency)]
    member_units = [r.member_units for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.member_units)]
    fee_id_array = [r.id for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.id)]
    fee_title_array = [r.title for r in db(db.member_fees.user_id==id_from_username).select(db.member_fees.title)]
  
    complete_fee_array=[fee_id_array, flat_rate_array, percentage_array, per_distance_array, per_hour_array, min_amount_array, max_amount_array, is_active_array, member_currency, member_units, fee_title_array]
    
    location_rating_array=db((db.ratings.ratee_id==id_from_username) & (db.ratings.ratee_type=='member')).select() 
    
    about = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.about)[0]['about']
    radius = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.delivery_radius)[0]['delivery_radius']
    max_radius_from_home = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.delivery_radius)[0]['max_radius_from_home']

    lat_lng_array_member = []
    lat_lng_array_location = []
    from gluon.tools import geocode
    (latitude, longitude) = geocode(current_location)
    delivery_username = db(db.auth_user.username==request.args(0)).select().as_list()[0]['username']
    current_location_new = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.current_location).as_list()[0]['current_location']
    
    lat_lng_array_member.append((latitude, longitude, current_location_new, member_picture_array, delivery_username, radius))
    member_ratings = db(db.ratings.ratee_id==str(id_from_username)).select()




    import math
    (lat1, long1) = geocode(current_location)
    location_list = db(db.locations).select()
    distance_meter_array = []
    for location in location_list:
        (lat2, long2) = geocode(location['complete_address'])
        degrees_to_radians = math.pi / 180.0
        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians   
        theta1 = long1  * degrees_to_radians
        theta2 = long2 * degrees_to_radians
        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
        distance_in_meters = math.acos(cos) * 6378100
        distance_meter_array.append([float(radius) - distance_in_meters, float(max_radius_from_home) - distance_in_meters, location])
    available_location_array = []
    for element in distance_meter_array:
        if element[0] > 0: 
            if element[1] > 0:
                available_location_array.append(element[2])
                (lat2, long2) = geocode(element[2]['complete_address'])
                lat_lng_array_location.append((lat2, long2, element[2]['name'], element[2]['address'], element[2]['phone_number'], 0))









    return dict(
    
    location_rating_array=location_rating_array,
    profile_firstname = profile_firstname,
    profile_lastname = profile_lastname,
    member_picture_array=member_picture_array,
    complete_fee_array=complete_fee_array,
    fee_id_array=fee_id_array,
    start_availability_array=start_availability_array,
    end_availability_array=end_availability_array,
    availability_id_array=availability_id_array,
    
    delivery_profile_id = delivery_profile_id,
    lat_lng_array_member=lat_lng_array_member,
    lat_lng_array_location=lat_lng_array_location,
    current_location = current_location,
    about = about,
    id_from_username=id_from_username,
    radius=radius,
    member_ratings=member_ratings,
    available_location_array=available_location_array,

    )



################################
####members#####################
################################
def members():
    return dict()
    
################################
####order#######################
################################
def order():
    if auth.is_logged_in():
        order_list = db((db.member_orders.member_id == auth.user_id) & (db.member_orders.id == request.args(0))).select()
    else:
        redirect(URL('')) 
    return dict(order_list=order_list)
    
################################
####orders######################
################################
def orders():
    if auth.is_logged_in():
        order_list = db(db.member_orders.member_id == auth.user_id).select()
        order_list_delivery = db(db.member_orders.delivery_member_id == auth.user_id).select()
        order_items = dict()
        for order in order_list:
            order_items[order['id']] = db(db.member_order_items.order_id == order['id']).select()
    else:
        redirect(URL(''))        


    return dict(
    order_list=order_list,
    order_items=order_items,
    )
    
################################
####privacy#####################
################################
def privacy():
    return dict()                
     
################################
####stats#######################
################################
def stats():
    return dict()                
        
################################
####search######################
################################
def search():
    from gluon.tools import geocode
    search_form=SQLFORM(db.member_search)
    if search_form.process(session=None, formname='search_form').accepted:
        #session.flash = 'results'
        redirect(URL('search'))        
    elif search_form.errors:
        response.flash = 'Error'
    selected_locations = db(db.locations.id==1).select(db.locations.ALL)
                    
    search_form_member_location = request.args(0)
    search_form_radius = request.args(1)
    search_form_details = request.args(2)    

    location_list = db(db.locations).select()
    location_array = []
    for location in location_list:
        (latitude, longitude) = geocode(location['complete_address'])
        lat_lng_array.append([latitude, longitude, location['name']])

        location_image=db(db.location_images.location_id == location['id']).select()
        location_tag=db(db.location_tag.location_id == location['id']).select()
        location_item=db(db.location_item.location_id == location['id']).select()

        if location_image:
            location_array.append([location,location_image,location_tag,location_item])
        else:
            location_array.append([location,"null",location_tag,location_item])

  
   
    return dict(
    
    search_form=search_form, 
    selected_locations=selected_locations,
    search_form_member_location=search_form_member_location,
    search_form_radius=search_form_radius,
    search_form_details=search_form_details,
    location_array=location_array,
    lat_lng_array=lat_lng_array,
    
    )
    
################################
####tags########################
################################
def tags():
    location_tag_list = db(db.location_tag).select()
    #item_tag_list = db(db.location_tag).select()

    return dict(location_tag_list=location_tag_list)
    
################################
####terms#######################
################################
def terms():
    return dict()   
    
################################
####transparency################
################################
def transparency():
    return dict()

################################################################
####ajax########################################################
################################################################  
def ajaxlivesearch():
    
    if session.auth is None:
    
        items = []
    
    else:
        
        address_array = [r.address for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.address)]
        description_array = [r.description for r in db(db.member_locations.user_id==session.auth.user.id).select(db.member_locations.description)]
         
        locations_array = [r.name for r in db(db.locations).select(db.locations.name)]
        partialstr = request.vars.values()[0]
        items = []
        
        for (counter1,address) in enumerate(address_array):
            if partialstr in address:
                items.append(DIV(A(address, _id="res%s"%counter1, _href="#", _onclick="copyToBox($('#res%s').html())"%counter1), _id="resultLiveSearch"))
        
        for (counter2,description) in enumerate(description_array):
            if partialstr in description:
                items.append(DIV(A(description, _id="res%s"%counter2, _href="#", _onclick="copyToBox($('#res%s').html())"%counter2), _id="resultLiveSearch"))
                                 
    return TAG[''](*items)

################################
####ajax_add_item_to_order######
################################
def ajax_add_item_to_order():

    location_id = str(request.vars.location_id)

    item_id = request.vars.iterkeys()
    for x in item_id:
        if x != "location_id":
            item_id_trim = int(x[8:])

    db.member_order_items.insert(member_id = auth.user_id, item_id = item_id_trim, location_id = location_id)


    item_row = db((db.location_item.location_id == location_id) & (db.location_item.item_id == item_id_trim)).select()

    jquery = "jQuery('.flash').html('added').slideDown().delay(1000).slideUp();"
    jquery += "jQuery('#sidebar-order-item').append(%s); " % item_row

    return jquery


################################################################
####validation##################################################
################################################################  
def __onvalidation_availability(form):
    import datetime
    if form.vars.start_availability > form.vars.end_availability:
        form.errors.end_availability = 'You have to start before you end!'
    elif form.vars.start_availability - datetime.datetime.now() < datetime.timedelta(days=0):
        form.errors.end_availability = 'Availabilities cannont start in the past'
   
    else:
        if (form.vars.end_availability - form.vars.start_availability) >= datetime.timedelta(days=.5):
            form.errors.end_availability = 'Availabilities can be no longer than 12 hours'
        if (form.vars.end_availability - form.vars.start_availability) <= datetime.timedelta(days=.01388888888):
            form.errors.end_availability = 'Availabilities must be at least 20 minutes'

def __onvalidation_location_sort_id(form):
    
    #unique by parent
    id_from_url = db(db.locations.name==request.args(0)).select(db.locations.id)[0]['id']    
    category_array = db(db.location_category.location_id==id_from_url).select()
    for category in category_array:
        if int(form.vars.sort_id) == category['sort_id']:
            form.errors.sort_id = 'Sort id must be unique'
        elif int(form.vars.sort_id) < 0:
            form.errors.sort_id = 'Sort id must be nonnegative'
                 
                                
def __onvalidation_rating(form):
    
    if form.vars.rating == '':
        form.errors.description = 'Enter a rating'
    if form.vars.description == '':
        form.errors.description = 'Enter a description'
    
    id_from_url = db(db.locations.name==request.args(0)).select(db.locations.id)[0]['id']    
    type_from_id = db(db.ratings.ratee_id==id_from_url).select(db.ratings.ratee_type)
                              
    rating_id_array = db(db.ratings.rater_id==auth.user_id).select()
    rating_id_array_modified = []
    rating_id_array_modified2 = []
    rating_id_array_modified3 = []    
    rating_id_array_modified4 = []
        
    for counter, rating_id in enumerate(rating_id_array):
        rating_id_array_modified.append(rating_id['rater_id'])
        rating_id_array_modified2.append(rating_id['ratee_id'])
        rating_id_array_modified3.append(rating_id['ratee_type'])
        rating_id_array_modified4.append(str(rating_id_array_modified[counter]) + str(rating_id_array_modified2[counter]) + str(rating_id_array_modified3[counter]))
                                      
    rating_id_array_modified_set = set(rating_id_array_modified4)
        
    if len(rating_id_array_modified4) != len(rating_id_array_modified_set):
        if rating_id_array_modified_set != set([]):  
            form.errors.description = 'you can only rate a location once'                                                                              
                                                                                                                       
         
def __onvalidation_rating_update(form): 
    
    if form.vars.rating == '':
        form.errors.description = 'Enter a rating'
    if form.vars.description == '':
        form.errors.description = 'Enter a description'               

def __onvalidation_rating_vote(form):

    rating_vote_id_array = db(db.rating_votes.user_id==auth.user_id).select()
    rating_vote_id_array_modified = []
    rating_vote_id_array_modified2 = []
    rating_vote_id_array_modified3 = []
   
    for counter, rating_vote_id in enumerate(rating_vote_id_array):
        rating_vote_id_array_modified.append(rating_vote_id['user_id'])
        rating_vote_id_array_modified2.append(rating_vote_id['rating_id'])
        rating_vote_id_array_modified3.append(rating_vote_id_array_modified[counter] + rating_vote_id_array_modified2[counter])
    
    rating_vote_id_array_modified_set = set(rating_vote_id_array_modified3)
        
    if len(rating_vote_id_array_modified3) != len(rating_vote_id_array_modified_set):
        if rating_vote_id_array_modified_set != set([]):  
            form.errors.rating_vote = 'you can only vote on a rating once'   


################################################################
####helpers#####################################################
################################################################

################################
####download####################
################################   
@cache.action()
def download():
    return response.download(request, db)

################################
####call########################
################################ 
@auth.requires_login()
def call():
    return service()

################################
####data########################
################################ 
@auth.requires_signature()
def data():
    return dict(form=crud())

@service.jsonrpc2
def test_add(a,b):
    number_sum = a+b
    return a+b

@service.jsonrpc2
def update_coordinates(lat,lng, member_id):
    lat_lng = lat+","+lng
    db(db.delivery_profile.user_id==member_id).update(current_location=lat_lng)
    return 'updated'

