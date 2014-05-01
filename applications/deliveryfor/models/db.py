################################################################
####db.py#######################################################
################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

################################
####database_conntection########
################################  

if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'


from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'mail@deliveryfor.com'
mail.settings.login = 'troverman:?><DFtrev77922'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
db.auth_user.first_name.readable = False
db.auth_user.last_name.readable = False 

################################################################
####database_tables#############################################
################################################################

################################
####delivery_profile############
################################ 
db.define_table('delivery_profile',
   Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
   Field('delivery_radius', 'double', requires=IS_NOT_EMPTY()),
   Field('phone_number', 'string' , requires=IS_NOT_EMPTY()),
   Field('about', 'text', requires=IS_NOT_EMPTY()),
   Field('current_location', 'string', requires=IS_NOT_EMPTY()),
   Field('minimum_order_price', 'string', requires=IS_NOT_EMPTY()),
   Field('maximum_concurrent_orders', 'string', requires=IS_NOT_EMPTY()),
   Field('time_zone', 'integer', requires=IS_NOT_EMPTY()),
   Field('home', 'string', requires=IS_NOT_EMPTY()),
   Field('max_radius_from_home', 'string', requires=IS_NOT_EMPTY()),
   Field('location_restriction', 'list:string'),

)

################################
####html_block##################
################################
db.define_table('html_block',
    Field('html_content','text'),
    Field('html_type','string'),
)

################################
####item_images#################
################################
db.define_table('item_images',
    Field('item_id', 'reference location_item', default=auth.user_id, readable=False, writable=False),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)

################################
####locations###################
################################
db.define_table('locations',
    Field('url_title','string'),
    Field('name','string'),
    Field('days_of_operation','string'),
    Field('description','string'),
    Field('address', 'string', requires=IS_NOT_EMPTY()),
    Field('city', 'string', requires=IS_NOT_EMPTY()),
    Field('location_state', 'string', requires=IS_NOT_EMPTY()),
    Field('zipcode', 'string', requires=IS_NOT_EMPTY()),
    Field('phone_number', 'string', requires=IS_NOT_EMPTY()),
    Field('complete_address', 'string', compute=lambda r: '%(address)s , %(city)s , %(location_state)s %(zipcode)s' % r, readable=False, writable=False),   
    Field('json_data','json'),
    Field('official_driver_id_array', 'integer', readable=False, writable=False),
    Field('admin_id_array', 'string', readable=False, writable=False),

)

################################
####location_hours##############
################################
#db.define_table('location_hours',
#    Field('location_id', 'reference locations'),
#    Field('opening_time', 'time'),
#    Field('closing_time', 'time'),
#    Field('week_day', 'datetime')
 #   Field('specific_day', 'datetime'),
#)

################################
####location_images#############
################################
db.define_table('location_images',
    Field('location_id', 'reference locations'),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)

################################
####location_tag################
################################
db.define_table('location_tag',
    Field('location_id', 'string', readable=False, writable=False),
    Field('tag', 'string', readable=False, writable=False),
)
default_location = 0    
location_category_array_modified=[]
location_category_array_modified.append('(None)')    


################################
####location_item###############
################################
db.define_table('location_item',
    Field('location_id','string'),
    Field('title','string'),
)

################################
####location_item_image#########
################################
db.define_table('location_image',
    Field('location_item_id', 'reference locations'),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)

################################
####location_item_option########
################################
db.define_table('location_item_option',
    Field('location_item_id','string'),
    Field('item_option_type','string'),
)

################################
####location_item_option_detail#
################################
db.define_table('location_item_option_detail',
    Field('location_item_option_id', 'string', readable=False, writable=False),
    Field('detail','string'),
    Field('detail_type','text'),
)

################################
####location_item_tag###########
################################
db.define_table('location_item_tag',
    Field('location_item_id', 'string', readable=False, writable=False),
    Field('tag','string'),
)
    
################################
####user_history################
################################ 
#db.define_table('user_history',
    #Field('user_location', 'string', requires=IS_NOT_EMPTY()),
    #Field('details', 'string'),
    #Field('radius','integer', requires=IS_NOT_EMPTY())
#) 
               
################################
####member_orders###############
################################ 
db.define_table('member_orders',
    Field('member_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('location_id', 'string', readable=False, writable=False),
    Field('order_status', 'string', default='pending', readable=False, writable=False),
    Field('delivery_member_id', 'string', readable=False, writable=False)
)

################################
####member_order_items##########
################################   
db.define_table('member_order_items',
    Field('order_id', 'reference user_order_items'),
    Field('member_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('location_id','integer', default=default_location, readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('item_id','integer', readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('order_item_title', 'string'),
    Field('order_item_description', 'string'),
    Field('order_item_price', 'string'),
    Field('order_item_input', 'string')
            
)                                     

################################
####member_search###############
################################ 
db.define_table('member_search',
    Field('member_location', 'string', requires=IS_NOT_EMPTY()),
    Field('details', 'string'),
    Field('radius','integer', requires=IS_NOT_EMPTY())
) 

################################
####member_availability#########
################################ 
import datetime
db.define_table('member_availability',
   Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
   Field('start_availability', 'datetime', requires=IS_DATETIME()),
   Field('end_availability', 'datetime', requires=IS_DATETIME()),
   Field('is_available', 'string', readable=False, writable=False),   
   )   

################################
####member_fees#################
################################ 
db.define_table('member_fees',
   Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
   Field('title', 'string', requires=IS_NOT_EMPTY()),
   Field('flat_rate', 'double' , default=0, requires=IS_NOT_EMPTY()),
   Field('percentage', 'double' , default=0, requires=IS_NOT_EMPTY()),
   Field('per_distance','double', default=0, requires=IS_NOT_EMPTY()),
   Field('per_hour','double', default=0, requires=IS_NOT_EMPTY()),
   Field('min_amount','double', default=0, requires=IS_NOT_EMPTY()),
   Field('max_amount','double', requires=IS_NOT_EMPTY()),
   Field('is_active','boolean', requires=IS_NOT_EMPTY()),
   Field('member_currency','string', requires=IS_NOT_EMPTY()),
   Field('member_units','string', requires=IS_NOT_EMPTY()))

################################
####member_locations############
################################ 
db.define_table('member_locations', 
   Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
   Field('address', 'string', requires=IS_NOT_EMPTY()),
   Field('city', 'string', requires=IS_NOT_EMPTY()),
   Field('location_state', 'string', requires=IS_NOT_EMPTY()),
   Field('zipcode', 'string', requires=IS_NOT_EMPTY()),
   Field('phone_number', 'string', requires=IS_NOT_EMPTY()),
   Field('complete_address', 'string', compute=lambda r: '%(address)s , %(city)s , %(location_state)s %(zipcode)s' % r, readable=False, writable=False),   
   Field('special_instructions', 'text',length=100),
   Field('description', 'text', requires=IS_NOT_EMPTY()))

################################
####member_images###############
################################  
db.define_table('member_images',
    Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)
                        
################################
####member_report###############
################################ 
db.define_table('member_report',
    Field('user_id', 'string', readable=False, writable=False),
    Field('delivery_user_id','integer', default="", readable=True, writable=True, requires=IS_NOT_EMPTY()),
    Field('rating_report_reason', 'boolean', readable=False, writable=False, requires=IS_NOT_EMPTY()))     
                   
################################
####member_settings#############
################################     
db.define_table('member_settings',
    Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('member_language', 'string', requires= IS_IN_SET(['Español', 'ру́сский язы́к'],zero=T('English'), error_message='must be a or b or c')),
    Field('member_currency', 'string', requires= IS_IN_SET(['€ EUR', '¥ JPY', '£ GBP', 'Fr CHF', '$ HKD', 'kr SEK', '₩ KRW', '$ SGD', 'kr NOK', '$ MXN', '₹ INR'],zero=T('$ USD'))),
    Field('member_units', 'string', requires= IS_IN_SET(['Metric'],zero=T('Imperial'))),
    Field('member_phone_number', 'string', requires=IS_NOT_EMPTY()),
    Field('member_accepts_email', 'boolean', requires=IS_NOT_EMPTY()))
  

################################
####ratings#####################
################################ 
from plugin_rating_widget import RatingWidget
db.define_table('ratings',
    Field('rater_id', 'string', readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('ratee_id', 'string', readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('ratee_type', 'string', readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('rating', 'integer', requires=IS_IN_SET(range(1,11))),
    Field('description', 'text'),
    Field('sort_alg', 'integer',default=0, readable=False, writable=False, requires=IS_NOT_EMPTY())
)       
db.ratings.rating.widget = RatingWidget()

################################
####rating_report###############
################################ 
db.define_table('rating_report',
    Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('rating_id','integer', default="", readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('rating_report_reason', 'string', requires=IS_NOT_EMPTY())
)  
      
################################
####rating_votes################
################################ 
db.define_table('rating_votes',
    Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('rating_id','integer', default=0, readable=False, writable=False, requires=IS_NOT_EMPTY()),
    Field('rating_vote', 'string', widget=SQLFORM.widgets.radio.widget, requires=IS_IN_SET(['like','dislike'])))  
      
################################
####record_versioning###########
################################ 
auth.enable_record_versioning(db)