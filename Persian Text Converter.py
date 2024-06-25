bl_info = {
    "name": "Convert Persian Text",
    "blender": (4, 1, 0),
    "version": (0, 1, 0),
    "category": "Object",
    "author": "Ahmad Zaghaghi",
    "description": "This is an add-on for writing in Persian in Blender."
}

import bpy
import sys
import subprocess
import importlib

# لیست پکیج‌هایی که باید نصب شوند
packages = ['arabic_reshaper', 'python-bidi']

def install_packages():
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            python_executable = sys.executable
            subprocess.check_call([python_executable, "-m", "pip", "install", package])

install_packages()

import arabic_reshaper
from bidi.algorithm import get_display

class OBJECT_OT_convert_persian_text(bpy.types.Operator):
    bl_idname = "object.convert_persian_text"
    bl_label = "Convert Persian Text"
    bl_options = {'REGISTER', 'UNDO'}
    
    text: bpy.props.StringProperty(name="Persian Text")
    use_geometry_nodes: bpy.props.BoolProperty(name="Geometry Nodes", default=False)
    
    def execute(self, context):
        unicode_text = self.convert_to_unicode(self.text)
        
        selected_objects = bpy.context.selected_objects
        text_obj = None
        
        # Check if there is a selected text object
        for obj in selected_objects:
            if obj.type == 'FONT':
                text_obj = obj
                break
        
        if text_obj:
            text_obj.data.body = unicode_text
        else:
            if self.use_geometry_nodes:
                bpy.context.window_manager.clipboard = unicode_text
            else:
                bpy.ops.object.text_add()
                text_obj = bpy.context.object
                text_obj.data.body = unicode_text
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Enter Persian Text:")
        layout.prop(self, "text", text="")
        layout.prop(self, "use_geometry_nodes", text="Geometry Nodes")

    def convert_to_unicode(self, text):
        # Reshape Persian text and reverse its direction
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_convert_persian_text.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_convert_persian_text)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_convert_persian_text)
    bpy.types.VIEW3D_MT_add.remove(menu_func)

if __name__ == "__main__":
    register()
