import bpy
from bpy.types import Operator, Panel, PropertyGroup

bl_info = {
    "name": "Scarlet Nexus Tools",
    "blender": (3, 5, 1),
    "author": "Moonling",
    "location": "View3D",
    "description": "Tools for Scarlet Nexus Modding",
    "category": "Tools",
}

class SNTool_PropertyGroup(PropertyGroup):
    outline_hood_on : bpy.props.BoolProperty(
        name="Visible With Hood",
        description="Outline will be visible duing Brain Drive/Crush",
        default=False,
    )

    outline_hood_off : bpy.props.BoolProperty(
        name="Hidden With Hood",
        description="Outline will be Hidden duing Brain Drive/Crush",
        default=False,
    )

    outline_material : bpy.props.PointerProperty(
        type=bpy.types.Material,
    )

class SNTool_SplitOutline(Operator):
    bl_idname = "sntool.split_outlines"
    bl_label = "Split Outline by Visiblity"
    bl_description = "Splits the selected outline mesh based on ingame Visibilty based on vertex colours" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i, polygon in enumerate(obj.data.polygons):
            for i1, loopindex in enumerate(polygon.loop_indices):
                dolor_data = obj.data.vertex_colors.active.data[loopindex]
                if dolor_data.color[2] > 0.90:
                    obj.data.vertices[obj.data.polygons[i].vertices[i1]].select = True

        bpy.ops.object.mode_set(mode = 'EDIT')           
        bpy.ops.mesh.separate(type = 'SELECTED')

        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i, polygon in enumerate(obj.data.polygons):
            for i1, loopindex in enumerate(polygon.loop_indices):
                dolor_data = obj.data.vertex_colors.active.data[loopindex]
                if dolor_data.color[2] > 0.70:
                    obj.data.vertices[obj.data.polygons[i].vertices[i1]].select = True
                    
        bpy.ops.object.mode_set(mode = 'EDIT')           
        bpy.ops.mesh.separate(type = 'SELECTED')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}
    
class SNTool_MakeOutline(Operator):
    bl_idname = "sntool.make_outline"
    bl_label = "Generate Outline Mesh"
    bl_description = "Dupicates the selected mesh and sets the vertex colours for use with outlines" 
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.sntool_settings

        #Get Active object
        obj = bpy.context.active_object
        outline_name = f'Outline_{obj.name}'

        if obj.type == 'MESH':
            #Dupicate Obejct
            bpy.ops.object.duplicate()
            obj = bpy.context.active_object
            
            #Set vertex color base for outline
            for i, polygon in enumerate(obj.data.polygons):
                for i1, loopindex in enumerate(polygon.loop_indices):
                    dolor_data = obj.data.vertex_colors.active.data[loopindex]
                    dolor_data.color[0] = 0.7
                    dolor_data.color[1] = 0.0
                    dolor_data.color[2] = 0.0
                    dolor_data.color[3] = 1.0
                    
            #Dirty Vertex Colors for better outlines
            bpy.ops.object.mode_set(mode = 'VERTEX_PAINT')
            for i in range (0,2):
                bpy.ops.paint.vertex_color_dirt(blur_strength=1.0, blur_iterations=1, clean_angle=3.14159, dirt_angle=0.0, dirt_only=True, normalize=True)
            bpy.ops.object.mode_set(mode = 'OBJECT')

            #Set Outline Visiblity
            if settings.outline_hood_on or settings.outline_hood_off:
                for i, polygon in enumerate(obj.data.polygons):
                    for i1, loopindex in enumerate(polygon.loop_indices):
                        dolor_data = obj.data.vertex_colors.active.data[loopindex]
                        if settings.outline_hood_on:
                            dolor_data.color[2] = 0.733
                        elif settings.outline_hood_off:
                            dolor_data.color[2] = 1.0

            #Clear any custom normals we don't need those
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            polygons = obj.data.polygons
            polygons.foreach_set('use_smooth',  [True] * len(polygons))
            obj.data.update()

            if not settings.outline_material == None:
                obj.data.materials.clear()
                obj.data.materials.append(settings.outline_material)
            
            obj.name = outline_name
            obj.data.name = outline_name

        return {'FINISHED'}

class SNTool_Menu_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SN Tools"
    bl_label = "SN Tools Menu"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.sntool_settings

        row = layout.row()
        row.operator('sntool.split_outlines', text='Split Outline Mesh by Visiblity')
        row = layout.row()
        col = layout.column(align=True)
        col.label(text="Make Outlines")
        row = col.row(align=True)
        row.prop(settings, "outline_hood_on", toggle=True, text="Visible With Hood")
        row.prop(settings, "outline_hood_off", toggle=True, text="Hidden With Hood")
        row = col.row(align=True)
        row.prop(settings, "outline_material", text="Mat", icon='MATERIAL')
        row = col.row(align=True)
        row.operator('sntool.make_outline', text='Generate Outline Mesh')

classes = (
    SNTool_PropertyGroup,
    SNTool_SplitOutline,
    SNTool_MakeOutline,
    SNTool_Menu_Panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sntool_settings = bpy.props.PointerProperty(type=SNTool_PropertyGroup)

def unregister():
    del bpy.types.Scene.sntool_settings
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()