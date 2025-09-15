from optparse import Option
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
        script.copyshapekey(self,context.scene.copybool.copy_bool)
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
        script.option(self,context)
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
    dirction: bpy.props.EnumProperty(
        name="选项",
        description="选择一个选项",
        items=[
            ('left', "X正向", "选择X正向的顶点"),
            ('right', "X负向", "选择X负向的顶点"),
        ],
        default='left'
    ) # type: ignore

def get_shape_key_items(self, context):
    """获取形态键枚举项"""
    # items = [('NONE', '无', '没有形态键')]
    items = []
    
    obj = context.active_object
    if obj and obj.data.shape_keys and obj.data.shape_keys.key_blocks:
        for key in obj.data.shape_keys.key_blocks:
            if key.name == "Basis":  # 排除基础形态键
                continue
            items.append((key.name, key.name, f"形态键: {key.name}"))

    return items

class ShapekeyProperties(bpy.types.PropertyGroup):
    """插件属性组"""
    key_name: bpy.props.EnumProperty(
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
        key_name = context.scene.selected_shape_key.key_name

        self.report({'INFO'}, f"{key_name}形态键获取")
        script.mirrorshapekey(self,key_name,context)
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
    
        # 顶部按钮行
        top_row = layout.row()
        top_row.operator("object.arkit2mmd")


        # 复制设置
        copy_box = layout.box()
        copy_box.label(text="复制设置")
        copy_row = copy_box.row()
        copy_row.prop(context.scene.copybool, "copy_bool")
        copy_row.operator("object.copyshapekey")

        # 镜像相关设置
        mirror_box = layout.box()
        mirror_box.label(text="镜像设置")
        mirror_box.prop(context.scene.selected_shape_key, "key_name", text="选择形态键")
        mirror_row1 = mirror_box.row()
        mirror_row1.prop(context.scene.select_dirction, "dirction", expand=True)
        mirror_row2 = mirror_box.row()
        mirror_row2.operator("object.selectside")
        mirror_row2.operator("object.selectzero")
        mirror_box.operator("object.mirrorshapkey")

        
        