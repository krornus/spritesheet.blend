import os
from pathlib import Path

import bpy
from bpy.props import StringProperty, IntProperty, PointerProperty, EnumProperty
from bpy.types import PropertyGroup, RenderSettings, Panel

from .packer import Packer

def extensions():
    from PIL import features, Image
    if not Image.EXTENSION:
        # force-load available extensions
        with open(os.devnull, "w") as f:
            features.pilinfo(out=f)
    return Image.EXTENSION

def pilformats():
    yield ("auto", "Automatic", "Choose format based on extension")
    for ext,fmt in extensions().items():
        yield (fmt, "%s" % (fmt), "%s image format (%s)" % (fmt, ext))

class Properties(PropertyGroup):
    spritepath: StringProperty(
        name="Sprite File",
        description="Output filepath for sprite sheet",
        subtype='FILE_PATH',
        default="",
    )

    image_format: EnumProperty(
        name="Format",
        description="Image format for sprite sheet",
        default="auto",
        items=list(pilformats()),
    )

    frames_x: IntProperty(
        name="Columns",
        description="Number of frames per row",
        default=8,
    )


class OBJECT_PT_SpritePanel(Panel):
    bl_label = "Sprite Sheet Renderer"
    bl_idname = "OBJECT_PT_sprite_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_context = ""

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        spt_render = scene.spt_render
        render = scene.render

        layout.prop(spt_render, "spritepath")
        layout.prop(spt_render, "image_format")
        layout.prop(spt_render, "frames_x")
        layout.operator("wm.rendersheet")
        layout.operator("wm.spritesettings")


class OBJECT_PT_SpriteRenderSettingsPanel(Panel):
    bl_parent_id = "OBJECT_PT_sprite_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Render Settings"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        render = scene.render
        layout.prop(render, "resolution_x")
        layout.prop(render, "resolution_y")
        layout.prop(render, "filter_size")
        layout.prop(render, "film_transparent")


class OBJECT_PT_SpriteAnimSettingsPanel(Panel):
    bl_parent_id = "OBJECT_PT_sprite_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Animation Settings"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "frame_start")
        layout.prop(scene, "frame_end")
        layout.prop(scene, "frame_step")


class WM_OT_RenderSpriteDefaults(bpy.types.Operator):
    bl_idname = "wm.spritesettings"
    bl_label = "Default Render Settings"

    def execute(self, context):
        scene = context.scene
        render = scene.render

        scene.frame_start = 1
        scene.frame_end = 30
        scene.frame_step = 3

        render.resolution_x = 64
        render.resolution_y = 64
        render.filter_size = 0.1
        render.film_transparent = True

        return {'FINISHED'}


class WM_OT_RenderSpriteSheet(bpy.types.Operator):
    bl_idname = "wm.rendersheet"
    bl_label = "Render Sprite Sheet"

    def checkpath(self, path, format):
        if path == "":
            raise ValueError("Must provide output path")

        path = Path(path)
        if format == "auto" and path.suffix not in extensions():
            raise ValueError(
                "Automatic image format not supported for path:"
                " '%s'" % path)

        if not os.access(path.parent, os.W_OK):
            raise ValueError(
                "Permission denied (cannot write output file):"
                " '%s'" % path)

    def execute(self, context):
        scene = context.scene
        render = scene.render
        spt_render = scene.spt_render

        try:
            self.checkpath(spt_render.spritepath, spt_render.image_format)
            self.report({'INFO'}, "Saving sprite sheet to %s." %
                                   spt_render.spritepath)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        start = scene.frame_start
        end = scene.frame_end
        step = scene.frame_step

        def fpath(x):
            return render.frame_path(frame=x)

        files = list(map(fpath, range(start, end, step)))
        
        rv = bpy.ops.render.render(animation=True)
        if 'FINISHED' not in rv:
            return rv

        packer = Packer(files, maxcol=spt_render.frames_x)
        out = packer.pack()
        try:
            out.save(spt_render.spritepath)
        except Exception as e:
            self.report({'ERROR'}, "failed to save output file: %s" % str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

classes = (
    Properties,
    WM_OT_RenderSpriteSheet,
    WM_OT_RenderSpriteDefaults,
    OBJECT_PT_SpritePanel,
    OBJECT_PT_SpriteRenderSettingsPanel,
    OBJECT_PT_SpriteAnimSettingsPanel,
)

def register():
    from bpy.utils import register_class, unregister_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.spt_render = PointerProperty(type=Properties)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.spt_render

if __name__ == "__main__":
    register()
