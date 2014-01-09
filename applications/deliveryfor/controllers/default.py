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
        redirect(URL('/'))        

    else:

        address_array = [r.address for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.address)]
        description_array = [r.description for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.description)]
        complete_address_array = [r.complete_address for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.complete_address)]
        location_id_array = [r.id for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.id)]

        start_availability_array = [r.start_availability for r in db(db.user_availability.user_id==session.auth.user.id).select(db.user_availability.start_availability)]
        end_availability_array = [r.end_availability for r in db(db.user_availability.user_id==session.auth.user.id).select(db.user_availability.end_availability)]
              
        availability_id_array = [r.id for r in db(db.user_availability.user_id==session.auth.user.id).select(db.user_availability.id)]
        
        user_picture_array = [r.picture for r in db(db.user_images.user_id==session.auth.user.id).select(db.user_images.picture)] 
        user_picture_id_array = [r.id for r in db(db.user_images.user_id==session.auth.user.id).select(db.user_images.id)]    
   
                             
        flat_rate_array = [r.flat_rate for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.flat_rate)]
        percentage_array = [r.percentage for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.percentage)]
        per_distance_array = [r.per_distance for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.per_distance)]
        per_hour_array = [r.per_hour for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.per_hour)]
        min_amount_array = [r.min_amount for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.min_amount)]
        max_amount_array = [r.max_amount for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.max_amount)]
        is_active_array = [r.is_active for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.is_active)]
        user_currency = [r.user_currency for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.user_currency)]
        user_units = [r.user_units for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.user_units)]
        fee_id_array = [r.id for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.id)]
        fee_title_array = [r.title for r in db(db.user_fees.user_id==session.auth.user.id).select(db.user_fees.title)]

  
        complete_fee_array=[fee_id_array, flat_rate_array, percentage_array, per_distance_array, per_hour_array, min_amount_array, max_amount_array, is_active_array, user_currency, user_units, fee_title_array]
        delivery_profile_id = db(db.delivery_profile.user_id==session.auth.user.id).select()
        
        #set map as a list of saved places at the complete address
        lat_lng_array = []
        from gluon.tools import geocode
        
        thecounter = 0
        for complete_address in complete_address_array:
             
            (latitude, longitude) = geocode(complete_address)
            lat_lng_array.append((latitude, longitude, complete_address, description_array[thecounter], description_array[thecounter]))
            thecounter = thecounter + 1

        #new location form
        form_newlocation = SQLFORM(db.user_locations, col3 = {'special_instructions':A('[?]',
          _href='http://www.google.com/search?q=define:address')})
        if form_newlocation.process(formname='user_locations').accepted:
            session.flash = 'Location Added'
            redirect(URL('/account'))        
        elif form_newlocation.errors:
            response.flash = 'Error'

        #new location edit / delete forms
        form_location_edit_array = []
        for counter, x in enumerate(location_id_array):
            form_location_edit_array.append(SQLFORM(db.user_locations, x, deletable=True, submit_button = 'Save Location', showid = False))
            if form_location_edit_array[counter].process(formname='form_location_edit_array-' + str(counter)).accepted:
                response.flash = 'Location Updated'
                redirect(URL('/account'))        
            elif form_location_edit_array[counter].errors:
                response.flash = 'Error'
            
        user_settings_id = db(db.user_settings.user_id==session.auth.user.id).select()             
        if user_settings_id:
          hi=''
        else:
            db.user_settings.insert(user_language="English", user_currency="$ USD", user_units="Imperial") 
        
            
        user_settings_record = db(db.user_settings.user_id==session.auth.user.id).select(db.user_settings.id)[0]['id']  
        form_user_settings_general = SQLFORM(db.user_settings, user_settings_record, fields = ['user_language', 'user_currency', 'user_units'], separator = ' ', submit_button = 'Save profile', showid = False, labels = {'user_language':P('Language' ,_class='head'), 'user_currency':P('Currency', _class='head'), 'user_units':P('Units', _class='head')})           
        if form_user_settings_general.process(formname='form_user_settings_general').accepted:
            session.flash = 'Settings Updated'
            redirect(URL('/account'))        
        elif form_user_settings_general.errors:
            response.flash = 'Error'
        form_user_settings_notifications = SQLFORM(db.user_settings, user_settings_record, formstyle = 'divs', fields = ['user_accepts_email', 'user_phone_number'], submit_button = 'Save profile', showid = False, separator = ' ', labels = {'user_accepts_email':'', 'user_phone_number':P('Send text updates to this number', _class='head')}, col3 = {'user_accepts_email':P('Recieve news and update emails from deliveryfor', _class='head', _style="margin-left:5px;margin-top:20px;")})
        if form_user_settings_notifications.process(formname='form_user_settings_notifications').accepted:
            session.flash = 'Settings Updated'
            redirect(URL('/account'))        
        elif form_user_settings_notifications.errors:
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
                
        form_upload_user_images = SQLFORM(db.user_images)
        if form_upload_user_images.process(formname='form_user_images').accepted:
            session.flash = 'Image Uploaded'
            redirect(URL('/account'))        
        elif form_upload_user_images.errors:
            response.flash = 'Error'

        form_edit_user_picture_array = []
        counter = 0
        for x in user_picture_id_array:
            form_edit_user_picture_array.append(SQLFORM(db.user_images, x, deletable=True, submit_button = 'Save Picture', showid = False))
            if form_edit_user_picture_array[counter].process(formname='form_edit_user_picture_array-' + str(counter)).accepted:
                session.flash = 'Image Updated'
                redirect(URL('/account'))        
            elif form_edit_user_picture_array[counter].errors:
                response.flash = 'Error'
            counter = counter + 1
                                                                                                                                      
        form_create_user_availability = SQLFORM(db.user_availability)
        if form_create_user_availability.process(formname='form_create_user_availability', onvalidation=__onvalidation_availability).accepted:
            session.flash = 'Availability Added'
            redirect(URL('/account'))        
        elif form_create_user_availability.errors:
            response.flash = 'Error'
                                                           
        form_edit_user_availability_array = []
        for counter, x in enumerate(availability_id_array):

            form_edit_user_availability_array.append(SQLFORM(db.user_availability, x, deletable=True, submit_button = 'Save Availability', showid = False))
            if form_edit_user_availability_array[counter].process(formname='form_edit_user_availability_array-' + str(counter), onvalidation=__onvalidation_availability).accepted:
                session.flash = 'Availability Updated'
                redirect(URL('/account'))        
            elif form_edit_user_availability_array[counter].errors:
                response.flash = 'Error'
               
        form_create_user_fee = SQLFORM(db.user_fees)
        if form_create_user_fee.process(formname='form_create_user_fee').accepted:
            session.flash = 'Fee Added'
            redirect(URL('/account'))        
        elif form_create_user_fee.errors:
            response.flash = 'Error'    
            
        form_edit_user_fee_array = []
        counter = 0
        for x in fee_id_array:
            form_edit_user_fee_array.append(SQLFORM(db.user_fees, x, deletable=True, submit_button = 'Save Fee', showid = False))
            if form_edit_user_fee_array[counter].process(formname='form_edit_user_fee_array-' + str(counter)).accepted:
                session.flash = 'Fee Updated'
                redirect(URL('/account'))        
            elif form_edit_user_fee_array[counter].errors:
                response.flash = 'Error'
            counter = counter + 1  
    
    
    edit_user_information=SQLFORM(db.auth_user, auth.user_id, fields = ['first_name','last_name','email', 'username'], submit_button = 'save profile', showid = False)

    
    return dict(
    form_user_settings_notifications=form_user_settings_notifications,
    form_user_settings_general=form_user_settings_general,
    edit_user_information=edit_user_information,
        
    form_edit_user_picture_array=form_edit_user_picture_array,
    user_picture_array=user_picture_array,
    
    delivery_profile_id=delivery_profile_id,
    form_edit_user_fee_array=form_edit_user_fee_array,
    fee_id_array=fee_id_array,
    complete_fee_array=complete_fee_array,
    
    start_availability_array=start_availability_array,
    end_availability_array=end_availability_array,
    availability_id_array=availability_id_array,

    form_edit_user_availability_array=form_edit_user_availability_array,
    form_create_user_fee=form_create_user_fee,
    form_create_user_availability=form_create_user_availability,
    form_upload_user_images = form_upload_user_images,
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
    #make function to go to nice long / lat
    latitude = longtitude = ''
    if session.auth is None:
        complete_address_array = ''
        lat_lng_array = []
        current_location_array = [r.current_location for r in db(db.delivery_profile).select(db.delivery_profile.current_location)]
        for location in current_location_array:
            delivery_profile_info = db(db.delivery_profile.current_location==location).select(db.delivery_profile.ALL).as_list()
            user_id_at_location = db(db.delivery_profile.current_location==location).select(db.delivery_profile.user_id).as_list()[0]['user_id']
            delivery_profile_pictures_array = [r.picture for r in db(db.user_images.user_id==user_id_at_location).select(db.user_images.picture)] 
            delivery_profile_username = db(db.auth_user.id==user_id_at_location).select(db.auth_user.username).as_list()[0]['username']
            (latitude, longitude) = geocode(location)
            lat_lng_array.append((latitude, longitude, location, delivery_profile_pictures_array, delivery_profile_username))
    else:
        complete_address_array = [r.complete_address for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.complete_address)]
        description_array = [r.description for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.description)]
        lat_lng_array = []    
        current_location_array = [r.current_location for r in db(db.delivery_profile).select(db.delivery_profile.current_location)]
        for location in current_location_array:
            delivery_profile_info = db(db.delivery_profile.current_location==location).select(db.delivery_profile.ALL).as_list()
            user_id_at_location = db(db.delivery_profile.current_location==location).select(db.delivery_profile.user_id).as_list()[0]['user_id']
            delivery_profile_pictures_array = [r.picture for r in db(db.user_images.user_id==user_id_at_location).select(db.user_images.picture)] 
            delivery_profile_username = db(db.auth_user.id==user_id_at_location).select(db.auth_user.username).as_list()[0]['username']
            (latitude, longitude) = geocode(location)
            lat_lng_array.append((latitude, longitude, location, delivery_profile_pictures_array, delivery_profile_username))
    search_form=SQLFORM(db.user_search)
    if search_form.process(session=None, formname='test').accepted:
        session.search_form_user_location = search_form.vars.user_location
        session.search_form_radius = search_form.vars.radius
        session.search_form_details = search_form.vars.details
        redirect(URL('search/' + search_form.vars.user_location + '/' + search_form.vars.radius + 'mi/' + search_form.vars.details))  
    elif search_form.errors:
        response.flash = 'There\'s a problem!'
    response.flash = 'welcome to deliveryfor!'
    user_picture_array = [r.picture for r in db(db.user_images).select(db.user_images.picture)] 
    location_list = db(db.locations).select()

    return dict(
        search_form=search_form,
        at_lng_array = lat_lng_array,
        user_picture_array=user_picture_array,
        location_list=location_list,
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
    
    if session.auth is None:
        can_vote='false'
        can_vote_rating='false'
    else:
        user_rating_history = db(db.ratings.rater_id==auth.user_id).select().as_list()           
        can_vote_rating='true'
        if user_rating_history == []:
            can_vote='true'
        else:     
            can_vote='false'

    location_from_url = db(db.locations.url_title==request.args(0)).select()
    id_from_url = db(db.locations.url_title==request.args(0)).select(db.locations.id)[0]['id']
    category_array = db(db.location_category.location_id==id_from_url).select()
    item_array = db(db.location_item.location_id==id_from_url).select()
    category_array_modified = []
    sorted_category_array = sorted(category_array.as_list(), key=lambda category: category['sort_id'])
    item_array = db(db.location_item.location_id==id_from_url).select()
    sorted_item_array = sorted(item_array.as_list(), key=lambda item: item['sort_id'])
    
    form_rate_location = SQLFORM(db.ratings)

    if form_rate_location.process(formname='form_rate_location', onvalidation=__onvalidation_rating).accepted:
        session.flash = 'Location Rated'
        redirect(URL('location/' + request.args(0))) 
    elif form_rate_location.errors:
        response.flash = 'Error'
                                                                  
    location_rating_array=db((db.ratings.ratee_id==id_from_url) & (db.ratings.ratee_type=='location')).select() 
    location_rating_array_modified=[]
    
    for location_rating in location_rating_array:
        if location_rating['ratee_type']=='location':
            location_rating_array_modified.append(location_rating)                            

          
    votes_from_location_array1=[]
    likes_array=[]
    total_array=[]
    sort_alg_array=[]  
    sorted_location_rating_array_modified=[]
    for counter, location_rating_modified_sort in enumerate(location_rating_array_modified):                            
        votes_from_location_array1.append(db(db.rating_votes.rating_id==location_rating_modified_sort['id']).select(db.rating_votes.rating_vote).as_list())
        likes=0 
        for votes in votes_from_location_array1[counter]:
            if votes['rating_vote'] == 'like':
                likes = likes + 1   
                                                 
        likes_array.append(likes*likes)                                         
        total_array.append(len(votes_from_location_array1[counter])*5)                                         
        sort_alg_array.append(-total_array[counter] - likes_array[counter])
        
        db(db.ratings.id==location_rating_modified_sort['id']).update(sort_alg=sort_alg_array[counter])    

    sorted_location_rating_array_modified = sorted(location_rating_array_modified, key=lambda sort_alg: sort_alg['sort_alg'])
                                                                                     
    form_rate_location_edit_array=[]                                                                                           
    form_create_rating_votes_array=[]
    form_edit_rating_votes_array=[]                         
    form_create_rating_report_array=[]
    form_edit_rating_report_array=[]   
    vote_id_from_user = db(db.rating_votes.user_id==auth.user_id).select(db.rating_votes.id).as_list()
    report_id_from_user = db(db.rating_report.user_id==auth.user_id).select(db.rating_report.id).as_list()
    votes_from_location_array=[]

    for the_counter, location_rating_modified in enumerate(sorted_location_rating_array_modified):
        form_rate_location_edit_array.append(SQLFORM(db.ratings, location_rating_modified['id'], onvalidation=__onvalidation_rating_update, showid = False, deletable=True))
        form_create_rating_votes_array.append(SQLFORM(db.rating_votes))
        form_create_rating_report_array.append(SQLFORM(db.rating_report))
        votes_from_location_array.append(db(db.rating_votes.rating_id==location_rating_modified['id']).select(db.rating_votes.rating_vote).as_list())
        
        if vote_id_from_user == []:
            form_edit_rating_votes_array.append('null')

        else:
            try:
                form_edit_rating_votes_array.append(SQLFORM(db.rating_votes, vote_id_from_user[the_counter]['id'], formstyle = 'divs', showid = False, deletable=True, labels = {'rating_vote':''}))
                if form_edit_rating_votes_array[the_counter].process(formname='form_edit_rating_votes-' + str(the_counter)).accepted:
                    session.flash = 'Vote Updated'
                    redirect(URL('location/' + request.args(0))) 
                elif form_edit_rating_votes_array[the_counter].errors:
                    response.flash ='Error'
            except IndexError:
                form_edit_rating_votes_array.append('null') 
                          
                                           
        if form_create_rating_votes_array[the_counter].process(formname='form_create_rating_votes-' + str(the_counter), onvalidation=__onvalidation_rating_vote, formstyle = 'divs', showid = False, labels = {'rating_vote':''}).accepted:
            db(db.rating_votes.id==form_create_rating_votes_array[the_counter].vars.id).update(rating_id=location_rating_modified['id'])    
            session.flash = 'Voted'
            redirect(URL('location/' + request.args(0))) 
        elif form_create_rating_votes_array[the_counter].errors:
            response.flash = 'Error'
            
            
        if report_id_from_user == []:
            form_edit_rating_report_array.append('null')

        else:
            try:
                form_edit_rating_report_array.append(SQLFORM(db.rating_report, report_id_from_user[the_counter]['id'], formstyle = 'divs', showid = False, deletable=True))
                if form_edit_rating_report_array[the_counter].process(formname='form_edit_rating_report-' + str(the_counter)).accepted:
                    session.flash = 'Report Updated'
                    redirect(URL('location/' + request.args(0))) 
                elif form_edit_rating_report_array[the_counter].errors:
                    response.flash ='Error'
            except IndexError:
                form_edit_rating_report_array.append('null')              

                        
        if form_create_rating_report_array[the_counter].process(formname='form_create_rating_report-' + str(the_counter)).accepted:
            db(db.rating_report.id==form_create_rating_report_array[the_counter].vars.id).update(rating_id=location_rating_modified['id'])    
            session.flash = 'Reported'
            redirect(URL('location/' + request.args(0))) 
        elif form_create_rating_report_array[the_counter].errors:
            response.flash = 'Error'                                                
                        
        if form_rate_location_edit_array[the_counter].process(formname='form_rate_location_edit_array-' + str(the_counter)).accepted:
            session.flash = 'Rating Updated'
            redirect(URL('location/' + request.args(0))) 
        elif form_rate_location_edit_array[the_counter].errors:
            response.flash = 'Error' 
                                                                                                                            
                              
    form_create_category = SQLFORM(db.location_category)
    location_category_array = db(db.locations.url_title==request.args(0)).select(db.location_category.title)
    location_category_array_modified = []
 
    if form_create_category.process(formname='form_create_category', onvalidation=__onvalidation_location_sort_id).accepted:
        session.flash = 'Category Created'
        redirect(URL('location/' + request.args(0))) 
    elif form_create_category.errors:
        response.flash = 'Error'
                                  
    form_edit_category_array = []                          
    for counter, category in enumerate(sorted_category_array):  
        form_edit_category_array.append(SQLFORM(db.location_category, category['id'], deletable=True))

        if form_edit_category_array[counter].process(formname='form_edit_category-' + str(counter), onvalidation=__onvalidation_location_sort_id).accepted:
            session.flash = 'Category Updated'
            redirect(URL('location/' + request.args(0))) 
        elif form_edit_category_array[counter].errors:
            response.flash = 'Error'   

                              
    form_create_item = SQLFORM(db.location_item)

    if form_create_item.process(formname='form_create_item').accepted:
        session.flash = 'Item Created'        
        redirect(URL('location/' + request.args(0))) 
    elif form_create_item.errors:
        response.flash = 'Error'
                                  
                                  
    form_edit_item_array = []                          
    for counter, item in enumerate(sorted_item_array):  
        form_edit_item_array.append(SQLFORM(db.location_item, item['id'], deletable=True))

        if form_edit_item_array[counter].process(formname='form_edit_item_array-' + str(counter), onvalidation=__onvalidation_location_sort_id).accepted:
            session.flash = 'Item Updated'
            redirect(URL('location/' + request.args(0))) 
        elif form_edit_item_array[counter].errors:
            response.flash = 'Error'
      
                
    form_create_item_option_array = []                                                      
    form_edit_item_options_array = []
    form_add_item_option_to_order_array = []
    item_option_array = []
    
    for counter, item in enumerate(sorted_item_array): 
        form_add_item_option_to_order_array.append([])           
        form_edit_item_options_array.append([])        
        form_create_item_option_array.append(SQLFORM(db.location_item_options))   
        item_option_array.append(db((db.location_item_options.location_id==id_from_url) & (db.location_item_options.item_id==item['id'])).select().as_list())

        if form_create_item_option_array[counter].process(formname='form_create_item_option-' + str(counter)).accepted:
            db(db.location_item_options.id==form_create_item_option_array[counter].vars.id).update(item_id=item['id'])    
            session.flash = 'Item Option Created'
            redirect(URL('location/' + request.args(0))) 
        elif form_create_item_option_array[counter].errors:
            response.flash = 'Error'    
        
################################################sort by sort_id ##########################
        
        
        sorted_item_option_array = item_option_array
        for the_counter, item_option in enumerate(sorted_item_option_array[counter]):
                             
            try:
                form_edit_item_options_array[counter].append(SQLFORM(db.location_item_options, item_option['id']))   
                if form_edit_item_options_array[counter][the_counter].process(formname='form_edit_item_options-' + str(counter) + str(the_counter)).accepted:
                    session.flash = 'Item Option Updated'
                    redirect(URL('location/' + request.args(0))) 
                elif form_edit_item_options_array[counter][the_counter].errors:
                    response.flash = 'Error' 
            except IndexError:
                form_edit_item_options_array.append('null')
                
            try:
                form_add_item_option_to_order_array[counter].append(SQLFORM(db.user_order_items))   
                 
                if form_add_item_option_to_order_array[counter][the_counter].process(formname='form_add_item_option_to_order_array-' + str(counter) + str(the_counter)).accepted:
                    session.flash = 'Item Added to Order'
                    redirect(URL('location/' + request.args(0))) 
                elif form_add_item_option_to_order_array[counter][the_counter].errors:
                    response.flash = 'Error' 
            except IndexError:
                form_add_item_option_to_order_array.append('null')
                
    from gluon.tools import geocode
    lat_lng_array = []
    (latitude, longitude) = geocode(location_from_url[0]['complete_address'])
    lat_lng_array.append((latitude, longitude, location_from_url[0]['name'], location_from_url[0]['name'], location_from_url[0]['description']))
    
    import math
    (lat1, long1) = geocode(location_from_url[0]['complete_address'])
    
    location_from_user = db(db.delivery_profile).select()
    distance_meter_array = []
    for location in location_from_user:
        (lat2, long2) = geocode(location['current_location'])
    
        degrees_to_radians = math.pi/180.0
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians   
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
        distance_meter_array.append([float(location['delivery_radius']) - math.acos( cos ) * 6378100, float(location['max_radius_from_home']) - math.acos( cos ) * 6378100, location])

    available_member_array = []
    for element in distance_meter_array:
        if element[0] > 0: 
            if element[1] > 0:
                available_member_array.append(element[2])
    location_picture_array = db(db.location_images.location_id == id_from_url).select()                                                                                                        
                                                                                                        
    return dict(
    location_picture_array=location_picture_array,
    available_member_array=available_member_array,
    distance_meter_array=distance_meter_array,
    location_from_url=location_from_url,
    form_add_item_option_to_order_array=form_add_item_option_to_order_array,
    sorted_location_rating_array_modified=sorted_location_rating_array_modified,
    can_vote=can_vote,
    votes_from_location_array=votes_from_location_array,
    form_create_rating_report_array=form_create_rating_report_array,
    form_edit_rating_report_array=form_edit_rating_report_array,
    form_rate_location_edit_array=form_rate_location_edit_array,
    vote_id_from_user=vote_id_from_user,
    form_edit_rating_votes_array=form_edit_rating_votes_array,
    form_create_rating_votes_array=form_create_rating_votes_array,
    item_option_array=item_option_array,
    location_rating_array_modified=location_rating_array_modified,
    form_edit_item_options_array=form_edit_item_options_array,
    id_from_url=id_from_url,
    sorted_item_array=sorted_item_array,
    form_edit_category_array=form_edit_category_array,
    sorted_category_array=sorted_category_array,
    category_array_modified=category_array_modified,
    form_create_category=form_create_category,
    form_create_item=form_create_item,
    form_rate_location=form_rate_location,
    form_create_item_option_array=form_create_item_option_array,
    form_edit_item_array=form_edit_item_array,
    lat_lng_array=lat_lng_array,
    
    )


################################
####locations###################
################################
def locations():
    location_list = db(db.locations).select()
    location_picture_array = db(db.location_images).select()                                                                                                        
    from gluon.tools import geocode
    lat_lng_array = []
    for location in location_list:
        (latitude, longitude) = geocode(location['complete_address'])
        lat_lng_array.append([latitude, longitude, location['name']])
    
    return dict(
        lat_lng_array=lat_lng_array,
        location_list=location_list,
        location_picture_array=location_picture_array,
        )
    
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

    id_from_username = db(db.auth_user.username==request.args(0)).select(db.auth_user.id).__str__()[13:] 
    current_location = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.current_location).__str__()[34:]
    
    profile_firstname = db(db.auth_user.id==id_from_username).select(db.auth_user.first_name).as_list()[0]['first_name']
    profile_lastname = db(db.auth_user.id==id_from_username).select(db.auth_user.last_name)[0]['last_name']
    
    start_availability_array = [r.start_availability for r in db(db.user_availability.user_id==id_from_username).select(db.user_availability.start_availability)]
    end_availability_array = [r.end_availability for r in db(db.user_availability.user_id==id_from_username).select(db.user_availability.end_availability)]
    availability_id_array = [r.id for r in db(db.user_availability.user_id==id_from_username).select(db.user_availability.id)]
        
    user_picture_array = [r.picture for r in db(db.user_images.user_id==id_from_username).select(db.user_images.picture)]    
    
    flat_rate_array = [r.flat_rate for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.flat_rate)]
    percentage_array = [r.percentage for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.percentage)]
    per_distance_array = [r.per_distance for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.per_distance)]
    per_hour_array = [r.per_hour for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.per_hour)]
    min_amount_array = [r.min_amount for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.min_amount)]
    max_amount_array = [r.max_amount for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.max_amount)]
    is_active_array = [r.is_active for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.is_active)]
    user_currency = [r.user_currency for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.user_currency)]
    user_units = [r.user_units for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.user_units)]
    fee_id_array = [r.id for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.id)]
    fee_title_array = [r.title for r in db(db.user_fees.user_id==id_from_username).select(db.user_fees.title)]
  
    complete_fee_array=[fee_id_array, flat_rate_array, percentage_array, per_distance_array, per_hour_array, min_amount_array, max_amount_array, is_active_array, user_currency, user_units, fee_title_array]
    
    location_rating_array=db((db.ratings.ratee_id==id_from_username) & (db.ratings.ratee_type=='member')).select() 
    
    about = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.about).__str__()[23:]
    radius = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.delivery_radius).__str__()[33:]
    
    lat_lng_array = []
    from gluon.tools import geocode
    (latitude, longitude) = geocode(current_location)
    delivery_username = db(db.auth_user.username==request.args(0)).select().as_list()[0]['username']
    current_location_new = db(db.delivery_profile.user_id==id_from_username).select(db.delivery_profile.current_location).as_list()[0]['current_location']
    
    lat_lng_array.append((latitude, longitude, current_location_new, user_picture_array, delivery_username))
    



    return dict(
    
    location_rating_array=location_rating_array,
    profile_firstname = profile_firstname,
    profile_lastname = profile_lastname,
    user_picture_array=user_picture_array,
    complete_fee_array=complete_fee_array,
    fee_id_array=fee_id_array,
    start_availability_array=start_availability_array,
    end_availability_array=end_availability_array,
    availability_id_array=availability_id_array,
    
    delivery_profile_id = delivery_profile_id,
    lat_lng_array=lat_lng_array,
    current_location = current_location,
    about = about,
    id_from_username=id_from_username,
    radius=radius

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
    order_list = db((db.user_orders.user_id == auth.user_id) & (db.user_orders.id == request.args(0))).select()

    return dict(order_list=order_list)
    
################################
####orders######################
################################
def orders():
    order_list = db((db.user_orders.user_id == auth.user_id) | (db.user_orders.delivery_member_id == auth.user_id)).select()
    order_items = dict()
    for order in order_list:
        order_items[order['id']] = db(db.user_order_items.order_id == order['id']).select()


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
    
    search_form=SQLFORM(db.user_search)
    if search_form.process(session=None, formname='search_form').accepted:
        #session.flash = 'results'
        redirect(URL('search'))        
    elif search_form.errors:
        response.flash = 'Error'
    selected_locations = db(db.locations.id==1).select(db.locations.ALL)
                    
    search_form_user_location = request.args(0)
    search_form_radius = request.args(1)
    search_form_details = request.args(2)     
    
    #search_form_user_location = session.search_form_user_location
    #search_form_radius = session.search_form_radius
    #search_form_details = session.search_form_details      
   
    return dict(
    
    search_form=search_form, 
    selected_locations=selected_locations,
    search_form_user_location=search_form_user_location,
    search_form_radius=search_form_radius,
    search_form_details=search_form_details
    
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
####helpers#####################################################
################################################################    

################################################################
####ajax########################################################
################################################################  
def ajaxlivesearch():
    
    if session.auth is None:
    
        items = []
    
    else:
        
        address_array = [r.address for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.address)]
        description_array = [r.description for r in db(db.user_locations.user_id==session.auth.user.id).select(db.user_locations.description)]
         
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


def download():
    return response.download(request, db)

def call():
    return service()

@auth.requires_signature()
def data():
    return dict(form=crud())