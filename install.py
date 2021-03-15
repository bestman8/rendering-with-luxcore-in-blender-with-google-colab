import bpy
bpy.ops.preferences.addon_install(filepath='/gdrive/MyDrive/luxcore/blendluxcore.zip')
#Enable LuxCore
bpy.ops.preferences.addon_enable(module='BlendLuxCore')

#LuxCore Preferences (set CUDA)
from os.path import basename, dirname
from bpy.types import AddonPreferences
from bpy.props import IntProperty, StringProperty, EnumProperty, BoolProperty



film_device_items = []


class LuxCoreAddonPreferences(AddonPreferences):
    # Must be the addon directory name
    # (by default "BlendLuxCore", but a user/dev might change the folder name)
    # We use dirname() two times to go up one level in the file system
    bl_idname = basename(dirname(dirname(__file__)))

    gpu_backend_items = [
        ("OPENCL", "OpenCL", "Use OpenCL for GPU acceleration", 0),
        ("CUDA", "CUDA", "Use CUDA for GPU acceleration", 1),
    ]
    gpu_backend: EnumProperty(items=gpu_backend_items, default="CUDA")

    def film_device_items_callback(self, context):
        backend_to_type = {
            "OPENCL": "OPENCL_GPU",
            "CUDA": "CUDA_GPU",
        }

        devices = context.scene.luxcore.devices.devices
        device_type_filter = backend_to_type[self.gpu_backend]
        # Omit Intel GPU devices because they can lead to crashes
        gpu_devices = [(index, device) for (index, device) in enumerate(devices)
                       if (device.type == device_type_filter and not "intel" in device.name.lower())]

        items = [(str(index), f"{device.name} ({self.gpu_backend})", "", i)
                 for i, (index, device) in enumerate(gpu_devices)]
        # The first item in the list is the default, so we append the CPU fallback at the end
        items += [("none", "CPU", "", len(items))]

        # There is a known bug with using a callback,
        # Python must keep a reference to the strings
        # returned or Blender will misbehave or even crash.
        global film_device_items
        film_device_items = items
        return items

    film_device: EnumProperty(name="Film Device", items=film_device_items_callback,
                              description="Which device to use to compute the imagepipeline")

    image_node_thumb_default: BoolProperty(
        name="Show Thumbnails by Default", default=True,
        description="Decide wether the thumbnail is visible on new image nodes (changes do not affect existing nodes)"
    )


#Save Blender preferences
bpy.ops.wm.save_userpref()
