from base_imports import *
from node import *
from meta_type import *
from process_type import *
from attribute_type import *
from meta_type import *


from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections, Q
client = Elasticsearch('banta_i:9200')
from gnowsys_ndf.settings import GSTUDIO_ELASTICSEARCH
#GSTUDIO_ELASTICSEARCH = True
# user should have a list of groups attributeType added should
# automatically be added to the attribute_type_set of GSystemType
@connection.register
class GSystemType(Node):
    """Class to generalize GSystems
    """

    structure = {
        'meta_type_set': [MetaType],            # List of Metatypes
        'attribute_type_set': [AttributeType],  # Embed list of Attribute Type Class as Documents
        'relation_type_set': [RelationType],    # Holds list of Relation Types
        'process_type_set': [ProcessType],      # List of Process Types
        'property_order': []                    # List of user-defined attributes in template-view order
    }

    use_dot_notation = True
    use_autorefs = True                         # To support Embedding of Documents

    @staticmethod
    def get_gst_name_id(gst_name_or_id):
        # if cached result exists return it
        #print "in get_gst_name_id"
        slug = slugify(gst_name_or_id)
        cache_key = 'gst_name_id' + str(slug)
        cache_result = cache.get(cache_key)

        if cache_result:
            return (cache_result[0], ObjectId(cache_result[1]))
        # ---------------------------------

         #gst_id = ObjectId(gst_name_or_id) if ObjectId.is_valid(gst_name_or_id) else None
        '''    gst_obj = node_collection.one({
                                        "_type": {"$in": ["GSystemType", "MetaType"]},
                                        "$or":[
                                            {"_id": gst_id},
                                            {"name": unicode(gst_name_or_id)}
                                        ]
                                    })'''
        
        if GSTUDIO_ELASTICSEARCH:
            #print "essssssssssssssssssssssssssssssssssssss"
            q1 = Q("match", type="GSystemType") | Q("match", type="MetaType")
            if isinstance(gst_name_or_id,ObjectId):
                q2 = Q("match", id=str(gst_name_or_id))
            else:
                q2 = Q("match", name=gst_name_or_id)
            s = Search(index='nodes').using(client).query(q1).query(q2)
            response  = s.scan()
            for hit in response:
                gst_obj = hit

            if gst_obj:
                gst_name = gst_obj.name 
                gst_id = gst_obj.id
                print gst_id,type(gst_id)
                cache_key = u'gst_name_id' + str(slugify(gst_id))
                cache.set(cache_key, (gst_name, gst_id), 60 * 60)

            # setting cache with gst_name
                cache_key = u'gst_name_id' + str(slugify(gst_name))
                cache.set(cache_key, (gst_name, gst_id), 60 * 60)
                #print gst_id
                return gst_name, gst_id
        else:
            #print "mongooooooooooooooooooooooooooooooooooo"
            gst_id = ObjectId(gst_name_or_id) if ObjectId.is_valid(gst_name_or_id) else None
            gst_obj = node_collection.one({
                                        "_type": {"$in": ["GSystemType", "MetaType"]},
                                        "$or":[
                                            {"_id": gst_id},
                                            {"name": unicode(gst_name_or_id)}
                                        ]
                                    })
            if gst_obj:
                gst_name = gst_obj.name 
                gst_id = gst_obj._id
                print gst_id,type(gst_id)
                cache_key = u'gst_name_id' + str(slugify(gst_id))
                cache.set(cache_key, (gst_name, gst_id), 60 * 60)

            # setting cache with gst_name
                cache_key = u'gst_name_id' + str(slugify(gst_name))
                cache.set(cache_key, (gst_name, gst_id), 60 * 60)
                print gst_id
                return gst_name, gst_id


        return None, None
