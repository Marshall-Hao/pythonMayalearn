import maya.api.OpenMaya as om

node_name = "pCube1"
attribute_name = "translateY"

selection_list = om.MSelectionList()
selection_list.add(node_name)

# since the list has only one obj,so the obj index is 0
obj = selection_list.getDependNode(0)

if obj.hasFn(om.MFn.kTransform):
    transform_fn = om.MFnTransform(obj)
    # non-network plug, every attribute is a plug, (shape like)
    plug = transform_fn.findPlug(attribute_name,False)
    
    attribute_value = plug.asDouble()
    
    plug.setDouble(2.0)
    print("{0}: {1}".format(plug,attribute_value))
    
    
    # return a vector
    translation = transform_fn.translation(om.MSpace.kTransform)
    translation[1] = 3.0
    # need to set the space for 2nd param
    transform_fn.setTranslation(translation, om.MSpace.kTransform)