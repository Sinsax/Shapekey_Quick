bl_info = {
    "name": "Shapekey_Quick",
    "author": "Sinsa",
    "blender": (4, 5, 3),
    "version": (1,1,0),
    "category": "Object",
}


import bpy # type: ignore
from . import shapekey_quick
# from . import select_vertices

scripts = [
    shapekey_quick.arkit2mmd,
    shapekey_quick.copyshapekey,
    shapekey_quick.ShapekeyProperties,
    shapekey_quick.CopyBoolProperties,
    shapekey_quick.DirctionProperties,
    shapekey_quick.ShapekeyQuickPanel,
    shapekey_quick.mirrorshapekey,
    shapekey_quick.selectside,
    shapekey_quick.selectzero,
]
# 注册和取消注册类
def register():
    for script in scripts:
        bpy.utils.register_class(script)

    bpy.types.Scene.copy_bool = bpy.props.PointerProperty(type=shapekey_quick.CopyBoolProperties)
    bpy.types.Scene.select_dirction = bpy.props.PointerProperty(type=shapekey_quick.DirctionProperties)
    bpy.types.Scene.selected_shape_key = bpy.props.PointerProperty(type=shapekey_quick.ShapekeyProperties)


def unregister():
    for script in scripts:
        bpy.utils.unregister_class(script)

    del bpy.types.Scene.copy_bool
    del bpy.types.Scene.select_dirction
    del bpy.types.Scene.selected_shape_key

if __name__ == "__main__":
    register()

