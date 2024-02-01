import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui

import maya.cmds as cmds


def maya_useNewAPI():
    """
    Tell Maya this plugin uses the Python API 2.0.
    """
    pass

class HelloWorldNode(omui.MPxLocatorNode):
    # save to maya ascii format
    TYPE_NAME = "helloworld"
    # save to binary format
    TYPE_ID = om.MTypeId(0x0007f7f7f)
    
    def __init__(self):
        super(HelloWorldNode,self).__init__()
        
    @classmethod
    def creator(cls):
        return HelloWorldNode()
    
    @classmethod
    def initialize(cls):
        pass

def initializePlugin(plugin):
    """
    """
    vendor = "Marshall"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(HelloWorldNode.TYPE_NAME,
                               HelloWorldNode.TYPE_ID,
                               HelloWorldNode.creator,
                               HelloWorldNode.initialize,
                               om.MPxNode.kLocatorNode)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(HelloWorldNode.TYPE_NAME))
        
def uninitializePlugin(plugin):
    """
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(HelloWorldNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(HelloWorldNode.TYPE_NAME))

if __name__ == "__main__":
    # refresh the new scene
    cmds.file(new-True,force=True)
    
    plugin_name = "hello_world_node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
    
    
    cmds.evalDeferred('cmds.createNode("helloworld")')
    