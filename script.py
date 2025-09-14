import bpy # pyright: ignore[reportMissingImports]
import bmesh # type: ignore
import json
import os


"""
# 使用示例
# 选择X坐标接近0的顶点
# select_x_range_vertices(x_min=-0.001, x_max=0.001)

# 选择x负方向
# select_x_range_vertices(x_min=float('-inf'), x_max=0)

# 选择x正方向
# select_x_range_vertices(x_min=0, x_max=float('inf'))
"""
def select_x_range_vertices(x_min=-0.1, x_max=0.1):
    """
    选择X坐标在指定范围内的顶点
    
    参数:
    x_min: X坐标的最小值
    x_max: X坐标的最大值
    """
    # 获取活动对象
    obj = bpy.context.active_object
    
    if obj is None or obj.type != 'MESH':
        print("请选择一个网格对象")
        return
    
    # 进入编辑模式
    bpy.ops.object.mode_set(mode='EDIT')
    
    # 获取网格数据
    mesh = bmesh.from_edit_mesh(obj.data)
    
    # 确保使用顶点选择模式
    if not mesh.select_mode & {'VERT'}:
        mesh.select_mode = {'VERT'}
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
    
    # 取消选择所有顶点
    for v in mesh.verts:
        v.select = False
    
    # 选择X坐标在指定范围内的顶点
    selected_verts = []
    for v in mesh.verts:
        if x_min <= v.co.x <= x_max:
            v.select = True
            selected_verts.append(v)
    
    # 更新视图
    bmesh.update_edit_mesh(obj.data)
    print(f"已选择{len(selected_verts)}个X坐标在[{x_min}, {x_max}]范围内的顶点")

def X_POSITIVE(self):
    select_x_range_vertices(x_min=0, x_max=float('inf'))
    self.report({'INFO'}, "已选择X正方向顶点")
def X_NEGATIVE(self):
    select_x_range_vertices(x_min=float('-inf'), x_max=0)
    self.report({'INFO'}, "已选择X负方向顶点")
def X_ZERO(self):
    select_x_range_vertices(x_min=-0.001, x_max=0.001)
    self.report({'INFO'}, "已选择X接近0的顶点")

def arkit2mmd(self):
    modelKey = bpy.context.object.data.shape_keys
    # 是否有形态键
    if modelKey is None :
        return {'无形态键可用'}

    # 获取插件文件所在目录
    addon_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(addon_directory, 'shapekey_mapping.json')
    
    # 读取JSON文件
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            mapping = json.load(json_file)
            self.report({'INFO'}, f"JSON Data: {mapping}")
    else:
        self.report({'ERROR'}, "JSON file not found")
    
    # 映射生成形态键

    for mapkey in mapping:
        skip = False
        self.report({'INFO'},str(mapkey))
        # self.report({'INFO'},str(mapping[mapkey][0]))
        '''
        if not mapping[mapkey][0] in list(modelKey.key_blocks):
            self.report({'INFO'},"无可用形态键，已跳过")
            continue
        '''
        
        # 将mapping中的所需的形态键启用
        for key in mapping[mapkey]:
            
            # 提供负值下限 
            # 检测是否有对应的形态键
            try:
                modelKey.key_blocks[key].slider_min = -1
            except:  # noqa: E722
                skip = True
                break
            modelKey.key_blocks[key].value = mapping[mapkey][key]
            # 恢复下限
            modelKey.key_blocks[key].slider_min = 0
        if skip :
            self.report({'INFO'}, key)
            self.report({'INFO'},"无匹配形态键，已跳过")
            continue
        
        # 混合为新形状
        bpy.ops.object.shape_key_add(from_mix=True)


        # for key in bpy.context.object.data.shape_keys.key_blocks: key.value =0
        # 清空之前的shapekey
        for key in mapping[mapkey]:
            modelKey.key_blocks[key].value = 0
        
        self.report({'INFO'},str(mapkey))
        
        # 改名
        currentkey = modelKey.key_blocks[len(modelKey.key_blocks)-1]
        #    modelKey.key_blocks[index].name = mapkey.name + "_copy"
        currentkey.name = mapkey
        self.report({'INFO'},mapkey + "已生成")

def copyshapekey(self):
    copy = bpy.context.scene.shapekey_copy_props.copy_bool
    self.report({'INFO'}, f"Another Operator Executed with copy_bool = {copy}")
    key = bpy.context.object.data.shape_keys
    index = bpy.context.object.active_shape_key_index
    name = key.key_blocks[index].name

    #if copy : key.key_blocks[index].value = 1
    bpy.ops.object.shape_key_add(from_mix=True)
    bpy.context.object.active_shape_key_index = index
    if copy :key.key_blocks[index].value = 0

    if not copy : bpy.ops.object.shape_key_remove(all=False)
    bpy.context.object.active_shape_key_index = len(key.key_blocks)-1
    if not copy : key.key_blocks[bpy.context.object.active_shape_key_index].name = name

    bpy.ops.object.shape_key_move(type='TOP')
    for a in range(0,index-1):
        bpy.ops.object.shape_key_move(type='DOWN')

    if copy : key.key_blocks[bpy.context.object.active_shape_key_index].value = 1   

def mirrorshapekey(self):
    # 获取当前活动对象
    obj = bpy.context.object
    if obj is None or obj.type != 'MESH':
        self.report({'ERROR'}, "请选择一个网格对象")
        return {'CANCELLED'}

    # 获取当前顶点组
    vg = obj.vertex_groups.active
    if vg is None:
        self.report({'ERROR'}, "请选择一个顶点组")
        return {'CANCELLED'}
    
    group_name = vg.name

    # 获取形态键数据
    modelKey = obj.data.shape_keys
    if modelKey is None:
        self.report({'ERROR'}, "无可用形态键，已跳过")
        return {'CANCELLED'}
    