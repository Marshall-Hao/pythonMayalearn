import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    Tell Maya this plugin uses the Python API 2.0.
    """
    pass


class HelloWorldCmd(om.MPxCommand):

    COMMAND_NAME = "HelloWorld"

    def __init__(self):
        """
        """
        super(HelloWorldCmd, self).__init__()

    def doIt(self, args):
        """
        Called when the command is executed in script
        """
        print("Hello World!")

    @classmethod
    def creator(cls):
        """
        Returns an instance of the HelloWorldCmd
        """
        return HelloWorldCmd()


def initializePlugin(plugin):
    """
    Entry point for a plugin
    """
    vendor = "Marshall"
    version = "1.0.1"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(HelloWorldCmd.COMMAND_NAME, HelloWorldCmd.creator)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format(HelloWorldCmd))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(HelloWorldCmd.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to deregister command: {0}".format(HelloWorldCmd))


if __name__ == "__main__":
    """
    For Development Only
    Specialized code that can be executed through the script editor to speed up the development process.
    """

    plugin_name = "hello_world_cmd.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))