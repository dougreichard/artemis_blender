import os
import bpy
from mathutils import Euler

from bpy.props import (BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    )
from bpy_extras.io_utils import (ImportHelper,
    ExportHelper,
    unpack_list,
    unpack_face_list,
    axis_conversion,
    )


class ImportAretmis(bpy.types.Operator, ImportHelper):
    """Load an Artemis ship data"""
    bl_idname = "import_sbs.ships"
    bl_label = "Import Artemis ships"
    filename_ext = ".json"
    filter_glob = StringProperty(
        default="*.json",
        options={'HIDDEN'},
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        mesh =  self.load(context)
        if not mesh:
            return {'CANCELLED'}
        return {'FINISHED'}

    def load(self, context):
        # self.filepath is set by blender???
        file_loc = self.filepath

        # import the obj
        _ = bpy.ops.import_scene.obj(filepath=file_loc)
        obj_object = bpy.context.selected_objects[0]
        bpy.context.view_layer.objects.active= obj_object
        obj_object.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')


        print('Imported name: ', obj_object.name)
        # Create the material + shader
        mat = bpy.data.materials.new(name="New_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
            # Get and connect the diffuse
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image =  bpy.data.images.load(self.filepath.replace('.obj', '_diffuse.png'))
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        texImage.location = (-750,800)
        # Get and connect the Emission Map
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image =  bpy.data.images.load(self.filepath.replace('.obj', '_diffuse-EMISSIVE.png'))
        mat.node_tree.links.new(bsdf.inputs['Emission'], texImage.outputs['Color'])
        texImage.location = (-750,500)
        # Get and connect the Specular Map
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image =  bpy.data.images.load(self.filepath.replace('.obj', '_diffuse-SPECULAR.png'))
        mat.node_tree.links.new(bsdf.inputs['Specular'], texImage.outputs['Color'])
        texImage.location = (-750,200)
        # Get and connect the Normal Map
        normalMap = mat.node_tree.nodes.new("ShaderNodeNormalMap")
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image =  bpy.data.images.load(self.filepath.replace('.obj', '_diffuse-NORMAL.png'))
    
        mat.node_tree.links.new(normalMap.inputs['Color'], texImage.outputs['Color'])
        mat.node_tree.links.new(bsdf.inputs['Normal'], normalMap.outputs['Normal'])
        texImage.location = (-750,-70)
        normalMap.location = (-320,-70)


        # Assign it to object
        if obj_object.data.materials:
            obj_object.data.materials[0] = mat
        else:
            obj_object.data.materials.append(mat)
            



def menu_func_import(self, context):
    self.layout.operator(ImportAretmis.bl_idname, text="Artemis ship (.obj)")


def register():
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)