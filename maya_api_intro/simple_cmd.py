import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass



class SimpleCmd(om.MPxCommand):

    COMMAND_NAME = "SimpleCmd"
    
    VERSION_FLAG = ["-v", "-version"]
    
    # a good way to define the flag data type
    TRANSLATE_FLAG = ["-t", "-translation", (om.MSyntax.kDouble,om.MSyntax.kDouble,om.MSyntax.kDouble)]
    
    NAME_FLAG = ["-n","-name"]
    def __init__(self):
        super(SimpleCmd, self).__init__()
        self.undoable = False
        
    def doIt(self, arg_list):
        
        # # get the flag syntax obj from the arg database and actual arg list(the args from the user input)
        # try:
        #     arg_db = om.MArgDatabase(self.syntax(),arg_list)
        # except:
        #     self.displayError("Error parsing arguments")
        #     raise
            
        # version_flag_enabled = arg_db.isFlagSet(SimpleCmd.VERSION_FLAG[0])
        # if version_flag_enabled:
        #     #self.displayInfo("1.0.0")
        #     self.setResult("1.0.0")
        # else:
        #     # name = "SimpleCmd"
        #     # if arg_db.isFlagSet(SimpleCmd.NAME_FLAG[0]):
        #     #     # get the user input string value
        #     #     first_name = arg_db.flagArgumentString(SimpleCmd.NAME_FLAG[0],0)
        #     #     last_name = arg_db.flagArgumentString(SimpleCmd.NAME_FLAG[0],1)
        #     # try:
        #     #     first_name = arg_db.commandArgumentString(0)
        #     #     last_name = arg_db.commandArgumentInt(1)
        #     # except:
        #     #     first_name = "SimpleCmd"
        #     #     last_name = ""
        #     # self.displayInfo("Hello {0} {1}".format(first_name,last_name))
            
        #     selection_list = arg_db.getObjectList()
        #     for i in range(selection_list.length()):
        #         # ever obj in scene is a node yeah
        #         depend_fn = om.MFnDependencyNode(selection_list.getDependNode(i))
        #         print(depend_fn.name())
        try:
            arg_db = om.MArgDatabase(self.syntax(), arg_list)
        except:
            self.displayError("Error parsing arguments")
            raise

        selection_list = arg_db.getObjectList()

        self.selected_obj = selection_list.getDependNode(0)
        # check if the selection node is transform node or not
        if self.selected_obj.apiType() != om.MFn.kTransform:
            raise RuntimeError("This command requires a transform node")
        
        self.edit = arg_db.isEdit
        self.query = arg_db.isQuery
        
        self.translate = arg_db.isFlagSet(SimpleCmd.TRANSLATE_FLAG[0])
        if self.translate:
            transform_fn = om.MFnTransform(self.selected_obj)
            #get translate in the current space, this is a translate state (undo)
            self.orig_translation = transform_fn.translation(om.MSpace.kTransform)
            
            if self.edit:
                self.new_translation = [arg_db.flagArgumentDouble(SimpleCmd.TRANSLATE_FLAG[0],0),
                                        arg_db.flagArgumentDouble(SimpleCmd.TRANSLATE_FLAG[0],1),
                                        arg_db.flagArgumentDouble(SimpleCmd.TRANSLATE_FLAG[0],2)]
                
                self.undoable = True
            
        self.version = arg_db.isFlagSet(SimpleCmd.VERSION_FLAG[0])

        self.redoIt()
            
    def undoIt(self):
        # will record each stack obj state
        transform_fn =  om.MFnTransform(self.selected_obj)
        # so it will always relate to that stack attr state value
        transform_fn.setTranslation(om.MVector(self.orig_translation),om.MSpace.kTransform)

    def redoIt(self):
        transform_fn = om.MFnTransform(self.selected_obj)
        if self.query:
            if self.translate:
                self.setResult(self.orig_translation)
            else:
                raise RuntimeError("Flag does not support query")
                
        elif self.edit:
            if self.translate:
                # convert to a vector type (c++ binding)
                transform_fn.setTranslation(om.MVector(self.new_translation),om.MSpace.kTransform)
            else:
                raise RuntimeError("Flag does not support edit")
        elif self.version:
            self.setResult("1.0.0")
        else:
            self.setResult(transform_fn.name())

    def isUndoable(self):
        return self.undoable

    @classmethod
    def creator(cls):
        return SimpleCmd()

    @classmethod
    def create_syntax(cls):

        syntax = om.MSyntax()
        syntax.enableEdit = True
        syntax.enableQuery = True
        # Add flags here
        # pointing to the args list ,optimized way
        syntax.addFlag(*cls.VERSION_FLAG)
        syntax.addFlag(*cls.TRANSLATE_FLAG)
        
        # syntax.addFlag(SimpleCmd.NAME_FLAG[0],SimpleCmd.NAME_FLAG[1],(om.MSyntax.kString,om.MSyntax.kString))
   
        # syntax.addArg(om.MSyntax.kString)
        # syntax.addArg(om.MSyntax.kUnsigned)
        
        syntax.setObjectType(om.MSyntax.kSelectionList,1,1)
        syntax.useSelectionAsDefault(True)
     
        return syntax



def initializePlugin(plugin):
    """
    """
    vendor = "Marshall"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerCommand(SimpleCmd.COMMAND_NAME, SimpleCmd.creator, SimpleCmd.create_syntax)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format(SimpleCmd.COMMAND_NAME))


def uninitializePlugin(plugin):
    """
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(SimpleCmd.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to deregister command: {0}".format(SimpleCmd.COMMAND_NAME))


if __name__ == "__main__":

    cmds.file(new=True, force=True)

    plugin_name = "simple_cmd.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
    
    cmds.evalDeferred('cmds.polyCube()')