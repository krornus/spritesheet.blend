bl_info = {
    "name": "Sprite Sheet Renderer",
    "description": "Converts rendered animation to sprite sheet",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "category": "Rendering",
}

from . import render

modules = (
    render,
)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()

if __name__ == "__main__":
    register()
