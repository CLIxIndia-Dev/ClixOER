from .base_imports import *
from .history_manager import HistoryManager
# 
from gnowsys_ndf.ndf.gstudio_es.es import *
# from gnowsys_ndf.ndf.views.es_queries import save_to_es
from gnowsys_ndf.settings import GSTUDIO_ELASTIC_SEARCH,GSTUDIO_ELASTIC_SEARCH_IN_NODE_CLASS,GSTUDIO_SITE_NAME
#from gnowsys_ndf.ndf.models.models_utils import NodeJSONEncoder,CustomNodeJSONEncoder

#@connection.register
#print("db:",db['Nodes'])
def _not_empty(val):
    if val.strip() in [None, '']:
        print(val)
        raise ValidationError('name value can not be empty')
def _chk_type_not_empty(val):
    if val in [None, '']:
        raise ValidationError('created_by value can not be empty')

def _chk_access_policy(val):
    if val.strip() in [None, '']:
        raise ValidationError('access_policy value can not be empty')


class Status(EmbeddedDocument):
    score = IntField()
    user_id = IntField()
    ip_address = StringField()


class Node(DynamicDocument):
    #print("db:",db['Nodes'])
    #objects = models.Manager() 
    
    meta = {
        'collection' : 'Nodes',
        'allow_inheritance' : True,
        'abstract' : True,
        }
    """
        'indexes' : [
            {
            # 1: Compound index                                                                                                                                        
        'fields' : [
            ('+_type','-name')
        ]
            }, {
                # 2: Compound index                                                                                                                                    
        'fields' : [
            ('+_type','+created_by')
        ]
            },
    ]
    } """

    #collection_name = 'Nodes'
    STATUS_CHOICES_TU = (u'DRAFT', u'HIDDEN', u'PUBLISHED', u'DELETED', u'MODERATION')
    #structure = {
    #_type = StringField(Required = True) # check required: required field, Possible
                          # values are to be taken only from the list
                          # NODE_TYPE_CHOICES
    name = StringField(Required = True, default = u'',validation=_not_empty)
    altnames =  StringField(default = u'')
    plural =  StringField(default = u'')
    prior_node =  ListField(ObjectIdField(), default = list)
    post_node =  ListField(ObjectIdField(), default = list)

        # 'language =  StringField(),  # previously it was  StringField().
    language = ListField(StringField(), default = ['en','Engilish'])  # Tuple are converted into a simple list
                                               # ref: https://github.com/namlook/mongokit/wiki/Structure#tuples

    type_of =  ListField(ObjectIdField(), default = list) # check required: only ObjectIDs of GSystemType
    member_of =  ListField(ObjectIdField(), default = list) # check required: only ObjectIDs of
                                 # GSystemType for GSystems, or only
                                 # ObjectIDs of MetaTypes for
                                 # GSystemTypes
    access_policy =  StringField(default = 'public', validation=_chk_access_policy) # check required: only possible
                                  # values are Public or Private.  Why
                                  # is this  StringField()?

    created_at = DateTimeField(Required = True, default = datetime.datetime.now)
    created_by = IntField(validation=_chk_type_not_empty) # test required: only ids of Users

    last_update = DateTimeField(default = datetime.datetime.now)
    modified_by = IntField(), # test required: only ids of Users

    contributors = ListField(IntField(), default = list) # test required: set of all ids of
                               # Users of created_by and modified_by
                               # fields
    location = ListField(DictField(), default = list) # check required: this dict should be a
                            # valid GeoJason format
    content =  StringField(default = u'')
    content_org =  StringField(default = u'')
    group_set =  ListField(ObjectIdField(), default = list) # check required: should not be
                                 # empty. For type nodes it should be
                                 # set to a Factory Group called
                                 # Administration
    collection_set =  ListField(ObjectIdField(), default = list)  # check required: to exclude
                                       # parent nodes as children, use
                                       # MPTT logic
    property_order = ListField(default = list)  # Determines the order & grouping in
                               # which attribute(s)/relation(s) are
                               # displayed in the form

    start_publication = DateTimeField()
    tags = ListField(StringField(), default = list)
    featured = BooleanField()
    url =  StringField(default = u'')
    comment_enabled = BooleanField()
    login_required = BooleanField()

    status = StringField(choices = STATUS_CHOICES_TU)
    rating = ListField(EmbeddedDocumentField('Status'))
    snapshot = DictField()

#    use_dot_notation = True
    index = 'nodes'

# DATABASE Variables
node_collection     = db['Nodes']
