
bl_info = {
    "name": "Shapekey Quick",
    "author": "Sinsa",
    "blender": (2, 80, 0),
    "version": (0,1,1),
    "category": "Object",
}


import bpy # type: ignore
from . import shapekey
# from . import select_vertices

# 注册和取消注册类
def register():
    bpy.utils.register_class(shapekey.arkit2mmd)
    bpy.utils.register_class(shapekey.copyshapekey)
    bpy.utils.register_class(shapekey.ShapekeyProperties)
    bpy.types.Scene.shapekey_copy_props = bpy.props.PointerProperty(type=shapekey.ShapekeyProperties)
    bpy.utils.register_class(shapekey.DirctionProperties)
    bpy.types.Scene.select_dirction = bpy.props.PointerProperty(type=shapekey.DirctionProperties)
    bpy.utils.register_class(shapekey.ShapekeyQuickPanel)

    bpy.utils.register_class(shapekey.mirrorshapkey)
    bpy.utils.register_class(shapekey.selectside)
    bpy.utils.register_class(shapekey.selectzero)
    # bpy.utils.register_class(select_vertices.GlobalAxisSelector)
    # bpy.utils.register_class(shapekey.ShapekeyList)
    # bpy.utils.register_class(shapekey.ShapekeyList_UI)
    # bpy.types.Scene.shapekey_props = bpy.props.PointerProperty(type=shapekey.ShapekeyList_UI)

def unregister():
    bpy.utils.unregister_class(shapekey.arkit2mmd)
    bpy.utils.unregister_class(shapekey.copyshapekey)
    bpy.utils.unregister_class(shapekey.ShapekeyProperties)
    del bpy.types.Scene.shapekey_copy_props
    bpy.utils.unregister_class(shapekey.DirctionProperties)
    del bpy.types.Scene.select_dirction
    bpy.utils.unregister_class(shapekey.ShapekeyQuickPanel)

    bpy.utils.unregister_class(shapekey.mirrorshapkey)
    bpy.utils.unregister_class(shapekey.selectside)
    bpy.utils.unregister_class(shapekey.selectzero)
    # bpy.utils.unregister_class(select_vertices.AxisVerticesSelector)
    # bpy.utils.unregister_class(shapekey.ShapekeyList)
    # bpy.utils.unregister_class(shapekey.ShapekeyList_UI)
    # del bpy.types.Scene.shapekey_props
if __name__ == "__main__":
    register()

