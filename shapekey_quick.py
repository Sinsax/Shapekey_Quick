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

class mirrorshapkey(bpy.types.Operator):
    bl_idname = "object.mirrorshapkey"  # 使用小写字母
    bl_label = "mirror shapkey Select Axis Vertices"
    bl_description = "镜像当前顶点组到对应的形态键"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls,context):
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
        
        bpy.ops.object.vertex_group_add()
        bpy.context.scene.tool_settings.vertex_group_weight = 1
        bpy.ops.object.vertex_group_assign()
        # 获取当前顶点组的名称
        group_name = bpy.context.object.vertex_groups.active.name
        script.X_ZERO(self)
        bpy.context.scene.tool_settings.vertex_group_weight = 0.5
        bpy.ops.object.vertex_group_assign()

        # 将顶点组分配给指定的形态键
        modelKey = bpy.context.object.data.shape_keys
        # 当前活动的形态键
        index = bpy.context.object.active_shape_key_index
        name = modelKey.key_blocks[index].name
        try:
            modelKey.key_blocks[name].vertex_group = group_name
        except:  # noqa: E722
            self.report({'INFO'}, "无可用形态键，已跳过")

        # 镜像顶点组
        bpy.ops.object.shape_key_mirror(use_topology=False)
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
class ShapekeyProperties(bpy.types.PropertyGroup):
    
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
        layout.prop(context.scene.shapekey_copy_props, "copy_bool")
        layout.operator("object.copyshapekey")
        
        # mirrorshapkey
        layout.prop(context.scene.select_dirction, "select_dirction", expand=True)
        layout.operator("object.mirrorshapkey")
        selectrow.operator("object.selectside")
        selectrow.operator("object.selectzero")
        # 显示形态键滑块
        