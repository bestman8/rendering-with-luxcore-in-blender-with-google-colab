import bpy
bpy.ops.preferences.addon_install(filepath='/gdrive/MyDrive/luxcore/BlendLuxCore-latest-linux64.zip')
bpy.ops.preferences.addon_enable(module='BlendLuxCore')
bpy.ops.wm.save_userpref()
