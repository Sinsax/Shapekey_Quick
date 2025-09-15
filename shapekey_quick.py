import bpy # type: ignore
from . import script
# arkit表情转为mmd的格式
class arkit2mmd(bpy.types.Operator):
    bl_idname = "object.arkit2mmd"
    bl_label = "arkit2mmd"
    bl_description = "将arkit形态键转为mmd格式"
    
    def execute(self,context):
        script.arkit2mmd(self)
        return {'FINISHED'}

class copyshapekey(bpy.types.Operator):
    bl_idname = "object.copyshapekey"
    bl_label = "copy shapekey"
    bl_description = "混合当前表情形态键到当前的位置"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls,context):
        return True

    def execute(self,context):
        script.copyshapekey(self)
        return {'FINISHED'}


class selectside(bpy.types.Operator):
    bl_idname = "object.selectside"  # 使用小写字母
    bl_label = "X axis Vertices"
    bl_description = "选择x轴正向或负向的顶点"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    
    def execute(self,context):
        scene = context.scene
        select_dirction = scene.select_dirction
        
        # 根据选择执行不同操作
        if select_dirction.select_dirction == 'OPTION1':
            script.X_POSITIVE(self)
            self.report({'INFO'}, "选择X正向的顶点")
        elif select_dirction.select_dirction == 'OPTION2':
            script.X_NEGATIVE(self)
            self.report({'INFO'}, "选择X负向的顶点")
        return {'FINISHED'}

class selectzero(bpy.types.Operator):
    bl_idname = "object.selectzero"  # 使用小写字母
    bl_label = "zero Vertices"
    bl_description = "选择x轴接近0的顶点"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    
    def execute(self,context):
        script.X_ZERO(self)
        return {'FINISHED'}
        
# 定义属性
class CopyBoolProperties(bpy.types.PropertyGroup):
    
    copy_bool: bpy.props.BoolProperty(
        name="是否复制",
        description="不选择则为覆盖",
        default=True
    ) # type: ignore

class DirctionProperties(bpy.types.PropertyGroup):
    # 定义单选按钮的选项
    select_dirction: bpy.props.EnumProperty(
        name="选项",
        description="选择一个选项",
        items=[
            ('OPTION1', "X正向", "选择X正向的顶点"),
            ('OPTION2', "X负向", "选择X负向的顶点"),
        ],
        default='OPTION1'
    ) # type: ignore

def get_shape_key_items(self, context):
    """获取形态键枚举项"""
    items = [('NONE', '无', '没有形态键')]
    
    obj = context.active_object
    if obj and obj.data.shape_keys and obj.data.shape_keys.key_blocks:
        for key in obj.data.shape_keys.key_blocks:
            items.append((key.name, key.name, f"形态键: {key.name}"))
    
    return items

class ShapekeyProperties(bpy.types.PropertyGroup):
    """插件属性组"""
    selected_shape_key: bpy.props.EnumProperty(
        name="形态键",
        description="选择要操作的形态键",
        items=get_shape_key_items
    ) # type: ignore

class mirrorshapekey(bpy.types.Operator):
    bl_idname = "object.mirrorshapkey"  # 使用小写字母
    bl_label = "mirror shapkey Select Axis Vertices"
    bl_description = "镜像当前顶点组到对应的形态键"
    bl_options = {"REGISTER"}

    @classmethod
    
    def poll(cls,context):
        return True

    
    def execute(self,context):
        shapekey_name = context.scene.selected_shape_key
        script.mirrorshapekey(self=self,shapekey_name=shapekey_name)
        return {'FINISHED'}

# 定义一个面板
class ShapekeyQuickPanel(bpy.types.Panel):
    bl_label = "Shapekey Quick"
    bl_idname = "OBJECT_PT_Shapekey_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shapekey Quick'
    
    def draw(self, context):
        layout = self.layout
        selectrow = layout.row()
        layout.operator("object.arkit2mmd")
        layout.prop(context.scene.copy_bool, "copy_bool")
        layout.operator("object.copyshapekey")
        
        # mirrorshapkey
        layout.prop(context.scene.select_dirction, "select_dirction", expand=True)
        layout.operator("object.mirrorshapkey")
        selectrow.operator("object.selectside")
        selectrow.operator("object.selectzero")
        # 显示形态键滑块
        layout.prop(context.scene.selected_shape_key, "selected_shape_key", text="形态键")