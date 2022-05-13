# This is my RGB Mesh script
# This script represents my journey through learning how to manipulate an object and a scene 
# utilizing python in Blender. The tool itself was a challange to myself in which I decided
# I wanted to create a mix of modifiers and get a random result and this one turned out to be an
# interesting looking combination.
#  
# User can change the values of 4 properties related to the 4 modifiers applied after the script
# runs and the the operator pop-up comes up. Using F3 and searching 'RGB Mesh' and selecting it 
# will allow you to use the properties after this script has been added to the list of add-ons. 

import bpy 
from math import radians
from bpy.props import *

def main(context):
    for ob in context.scene.objects:
        print(ob)

class SimpleOperator(bpy.types.Operator):
    
    # Create Properties for pop-up
    bl_idname = "object.rgb_mesh"
    bl_label = "RGB Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    branch_smoothing : bpy.props.FloatProperty(
        name = "Skin Scale",
        description = "Adjust the strength of the smoothing applied by the Skin Modifier.",
        default = 1.0,
        min = 0.0,
        max = 2.0
    )
    
    voxel_size : bpy.props.FloatProperty(
        name = "Remesh Scale",
        description = "Adjust voxel size in the Remesh Modifier.",
        default = 0.39,
        min = 0.0,
        max = 0.5
    )
    
    levels : bpy.props.IntProperty(
        name = "Subdiv",
        description = "Adjust Subdiv levels.",
        default = 3,
        min = 0,
        max = 5
    )
    thickness : bpy.props.FloatProperty(
        name = "Wireframe Thickness",
        description = "Adjust wireframe thickness.",
        default = 0.007,
        min = 0.0,
        max = 2
    )
    
    # Makes it so it only shows up over the 3D Viewport
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return True
        
    def execute(self, context):
        
        # Changing scene settings
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 120
        bpy.context.scene.frame_current = 1
        
        # Deleting other things in this scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Creating and selecting the cube
        sphere = bpy.ops.mesh.primitive_cube_add()
        so = bpy.context.active_object

        # Adding modifiers and changing different seetings related to them individually
        mod_skin = so.modifiers.new("Skin Modifier", 'SKIN')
        mod_skin.branch_smoothing = self.branch_smoothing #1
        mod_remesh = so.modifiers.new("Remesh Modifier", 'REMESH')
        mod_remesh.voxel_size = self.voxel_size #0.39
        mod_subdiv = so.modifiers.new("Subdiv Modifier", 'SUBSURF')
        mod_subdiv.levels = self.levels #3
        mod_wireframe = so.modifiers.new("Wireframe Modifier", 'WIREFRAME')
        mod_wireframe.thickness = self.thickness

        # Checking if material exists and if not creating a material
        new_mat = bpy.data.materials.get("RGB Material")
        
        if new_mat is None:
            new_mat = bpy.data.materials.new(name = "RGB Material")
            bpy.context.active_object.data.materials.append(new_mat)  
        else:
            new_mat = bpy.data.materials.get("RGB Material")
            bpy.context.active_object.data.materials.append(new_mat)

        # Activate nodes
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

        # Create emission node
        emission_node = nodes.new(type='ShaderNodeEmission')

        # Changing the values of the node
        input_1 = emission_node.inputs[0]
        input_1.default_value = (0.095, 0.382, 1, 1) # Color Blue
        input_1.keyframe_insert(data_path='default_value', frame= 1)
        input_1.default_value = (0.421, 0.171, 1, 1) # Color Purple
        input_1.keyframe_insert(data_path='default_value', frame= 20)
        input_1.default_value = (1, 0.213, 0.627, 1) # Color Pink
        input_1.keyframe_insert(data_path='default_value', frame= 40)
        input_1.default_value = (1, 0.287, 0.187, 1) # Color Orange
        input_1.keyframe_insert(data_path='default_value', frame= 60)
        input_1.default_value = (0.696, 1, 0.148, 1) # Color Yellow
        input_1.keyframe_insert(data_path='default_value', frame= 80)
        input_1.default_value = (0.162, 1, 0.084, 1) # Color Green
        input_1.keyframe_insert(data_path='default_value', frame= 100)
        input_1.default_value = (0.095, 0.382, 1, 1) # Color Blue Again
        input_1.keyframe_insert(data_path='default_value', frame= 120)
        
        emission_node.inputs[1].default_value = 5.0 # Strength

        # Selecting the links of the present nodes
        links = new_mat.node_tree.links

        # Creating new link
        material_output = nodes.get("Material Output")
        new_link = links.new(emission_node.outputs[0], material_output.inputs[0])

        # Change to Shading mode.

        for area in bpy.context.screen.areas:  # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces:  # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D':  # check if space is a 3D view
                        space.shading.type = 'MATERIAL'  # set the viewport shading to material
                        
        # Turn on Bloom
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.use_bloom = True
        
        # Pressing play button
        bpy.ops.screen.animation_cancel()
        bpy.ops.screen.animation_play()
        
        return {'FINISHED'}

classes = (
    SimpleOperator
)

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)

# Register and add to the "object" menu (required to also be able to use F3 search "RGB Mesh" for quick access)
def register():
    
    bpy.utils.register_class(classes)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    
    bpy.utils.unregister_class(classes)    
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()