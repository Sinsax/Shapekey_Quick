bl_info = {
    "name": "Shapekey Quick",
    "author": "Sinsa",
    "blender": (4, 5, 3),
    "version": (1,1,0),
    "category": "Object",
}


import bpy # type: ignore
from . import shapekey_quick
# from . import select_vertices

functions = [
    shapekey_quick.arkit2mmd,
    shapekey_quick.copyshapekey,
    shapekey_quick.ShapekeyProperties,
    shapekey_quick.DirctionProperties,
    shapekey_quick.ShapekeyQuickPanel,
    shapekey_quick.mirrorshapkey,
    shapekey_quick.selectside,
    shapekey_quick.selectzero,
]
# 注册和取消注册类
def register():
    for func in functions:
        bpy.utils.register_class(func)
    
    bpy.types.Scene.shapekey_copy_props = bpy.props.PointerProperty(type=shapekey_quick.ShapekeyProperties)
    bpy.types.Scene.select_dirction = bpy.props.PointerProperty(type=shapekey_quick.DirctionProperties)

    # bpy.utils.register_class(select_vertices.GlobalAxisSelector)
    # bpy.utils.register_class(shapekey.ShapekeyList)
    # bpy.utils.register_class(shapekey.ShapekeyList_UI)
    # bpy.types.Scene.shapekey_props = bpy.props.PointerProperty(type=shapekey.ShapekeyList_UI)

def unregister():
    for func in functions:
        bpy.utils.unregister_class(func)

    del bpy.types.Scene.shapekey_copy_props
    del bpy.types.Scene.select_dirction

    # bpy.utils.unregister_class(select_vertices.AxisVerticesSelector)
    # bpy.utils.unregister_class(shapekey.ShapekeyList)
    # bpy.utils.unregister_class(shapekey.ShapekeyList_UI)
    # del bpy.types.Scene.shapekey_props
if __name__ == "__main__":
    register()

