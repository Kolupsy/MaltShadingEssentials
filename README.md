# MaltShadingEssentials
Plugin for BlenderMalt that enables an Eevee-like workflow.

**About**:
This Plugin is currently not supporting any backwards-compatibility whatsoever. It is still in its very early stages.
The goal is to always be up to date with Malt's Development version which means that it only supports that branch. Older versions of Malt may be too outdated.
The Plugin is also dependent on the NPR Pipeline used by Malt by default. Some nodes use features from that pipeline so using another pipeline will brake a few nodes.

Please send any bug reports related to the plugin to this github page and not to Malt's unless the bug is actually caused by Malt.

**How to install:**

- Download project as .zip
- Locate your BlenderMalt `Global Plugins` folder (you can find it under Edit>Preferences>Add-ons>BlenderMalt>Preferences)
- If not set in the addon preferences, set this folder to a convenient location, eg `[Your Main Blender Folder]/Malt/Plugins`
- Unzip MaltShadingEssentials into the `Global Plugins` folder like this: `[Global Plugins Folder]/MaltShadingEssentials`
- Restart Blender or open it
- Check the shift-A menu in a Malt Node Tree to confirm that the installation has worked

You can now use the MaltShadingEssentials plugin in your Malt workflow!

*Alternative Method:*

- Clone the repository into your `Global Plugins` folder

OR

- Clone the repository into a convenient location and set up a Symlink of the folder inside the `Global Plugins` folder

**Documentation:**

Right now the plugin mostly consists of custom nodes for Malt. Custom nodes for Malt have a Python and GLSL part.
The Python code takes care of the visual layout of the node, its metadata, property and malt updates and wraps the GLSL code.
A good example to study how the custom Malt nodes work is the Map Range node [nodes/map_range.py]. It has input and output definitions,
as well as properties (`interpolation_type` and `clamp`) that dynamically affect the node visually and functionally.
To create a new custom node, add a new file in the same directory that all the other custom nodes are defined.
Write a minimal setup like the following:

```py
from .utils import *    #This gets you kind of the 'Starter Pack' for creating custom Malt nodes. To see all imports, see the source file [nodes/utils.py]

class MaltNodeMapRange( EssentialsNode ):   #the EssentialsNode class gives you all the needed functions and properties to override
    bl_idname = 'MaltNodeMapRange'    #Use the same name as the class name, use camelcase and the prefix 'MaltNode...' by convention
    bl_label = 'Map Range'            #Display name of the node
    menu_category = 'CONVERTOR'       #Chose from a limited set of categories defined in [nodes/utils.py]
    
    def define_sockets( self ) -> dict:
        return {}
    
    def get_function( self ) -> str:
        return ''


NODES = [ MaltNodeMapRange ]    #All Custom node classes need to added to this list. Define this global variable for every file in the nodes directory
```
The two empty functions are all that is needed to write a custom node. 

`define_sockets` should return a dictionary containing the data for static sockets of the node.
All dict values need to be either `MaltVariableIn` (imported as `I`) or `MaltVariableOut` (imported as `O`). 
The input or output should describe the socket with type, name and optionally subtype and default value.

`get_function` should return a string that represents valid GLSL code. The goal of the function is to set all the output variables using all the input variables.
For convenience the GLSL snippets assumes that all the variables have been declared and that all the input variables have been initialized.
Try to keep the `get_function` method as compact as possible. The recommended workflow is to write the code for the node into the `Shaders` library. 
That way your shader function becomes globally accessible and keeps writing GLSL code as a python string to a minimum.
A good example for this is the `MaltNodeBrightContrast` under [nodes/bright_contrast.py]. There you can also get another example of how to format the string for the `get_function` method required by your custom node.

`update_socket_visibility` is an optional method which can be defined by a `EssentialsNode` subclass to trigger updates to your node sockets. By default this method has to be manually called.

If you have a dynamically changing shader function (like the real `MaltNodeMapRange`), then you need to make sure that the Malt node tree updates when the return value of `get_function` changes. In most cases this will be triggered by updating a node property (like `clamp` or `interpolation_type` for the `MaltNodeMapRange`).
The `EssentialsNode` provides a function for that called `update_tree( self )`. For convenience, the `utils.py` module provides callbacks that trigger updates when properties change: `malt_update` and `socket_update`. These callbacks can be used to either update the Malt node tree or call the `update_socket_visibility` method on your node.

**Updating plugin changes:**

Malt provides an operator that reloads the python part of a MaltPlugin. It can be called from the F3 Search menu by typing 'Malt Reload Plugins' and can be bound to a shortcut or integrated into the Blender UI manually.
