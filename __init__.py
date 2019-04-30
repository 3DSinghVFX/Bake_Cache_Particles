bl_info = {
    "name": "Bake Cache Particles",
    "author": "Kuldeep Singh",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "AN Node Editor > Tools",
    "description": "This addon allows to bake the cached particles of active object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy
from bpy.types import Operator
from bpy.props import *

def bake_particles(self):
    scene = bpy.context.scene.name
    obj = bpy.context.active_object.name
    particleSettings = bpy.data.objects[obj].particle_systems.active.name

    particleSystem = bpy.data.objects[obj].particle_systems[particleSettings]
    if particleSystem.point_cache.is_baked is False:       
        startFrame = bpy.data.scenes[scene].frame_start
        if bpy.data.scenes[scene].frame_current == startFrame:
            seed = particleSystem.seed
            particleSystem.seed = seed

    if bpy.data.scenes[scene].frame_current == bpy.data.scenes[scene].frame_end:
        bpy.ops.screen.animation_cancel(restore_frame = False)
        cache = {}
        cache['point_cache'] = particleSystem.point_cache
        bpy.ops.ptcache.bake_from_cache(cache)
        bpy.app.handlers.frame_change_pre.clear()
        
def free_bake_particles(self):
    scene = bpy.context.scene.name
    obj = bpy.context.active_object.name
    particleSettings = bpy.data.objects[obj].particle_systems.active.name

    particleSystem = bpy.data.objects[obj].particle_systems[particleSettings]
    cache = {}
    cache['point_cache'] = particleSystem.point_cache
    bpy.ops.ptcache.free_bake(cache)
    bpy.app.handlers.frame_change_pre.clear()        


class PARTICLES_OT_bake(Operator):
    """Bake particles"""
    bl_idname = "an.bake_particles"
    bl_label = "Bake Cache Particles"

    def execute(self, context):
        scene = bpy.context.scene.name
        bpy.app.handlers.frame_change_pre.clear()
        startFrame = bpy.data.scenes[scene].frame_start
        bpy.data.scenes[scene].frame_current = startFrame
        bake_particles(self)
        bpy.app.handlers.frame_change_pre.append(bake_particles)
        bpy.ops.screen.animation_play()
        return {'FINISHED'}
    
class PARTICLES_OT_free_bake(Operator):
    """Delete Bake particles"""
    bl_idname = "an.free_bake_particles"
    bl_label = "Delete Bake Particles"

    def execute(self, context):
        free_bake_particles(self)
        return {'FINISHED'}

def add_bake_button(self, context):
    self.layout.operator(
        PARTICLES_OT_bake.bl_idname,
        text="Bake Particles",
        icon="PLAY")
    self.layout.operator(
        PARTICLES_OT_free_bake.bl_idname,
        text="Delete Bake",
        icon="PLAY")    

class PARTICLES_PT_bake_unbake_ui(bpy.types.Panel):
    """Bake particles"""
    bl_idname = "AN_PT_bake_particles"
    bl_label = "Bake Particles"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"

    @classmethod
    def poll(cls, context):
        tree = cls.getTree()
        if tree is None: return False
        return tree.bl_idname == "an_AnimationNodeTree"

    def draw(self, context):
        scene = bpy.context.scene.name
        obj = bpy.context.active_object
        if obj.type == "MESH" and bpy.data.objects[obj.name].particle_systems.active is not None:
            particleSettings = bpy.data.objects[obj.name].particle_systems.active.name
            particleSystem = bpy.data.objects[obj.name].particle_systems[particleSettings]        
            tree = self.getTree()
            layout = self.layout

            col = layout.column()
            col.scale_y = 1.5    
            if  particleSystem.point_cache.is_baked is True:
                props = col.operator("an.free_bake_particles", icon = "PLAY")
            else:
                props = col.operator("an.bake_particles", icon = "PLAY")

    @classmethod
    def getTree(cls):
        return bpy.context.space_data.edit_tree



def register():
    bpy.utils.register_class(PARTICLES_OT_bake)
    bpy.utils.register_class(PARTICLES_OT_free_bake)    
    bpy.utils.register_class(PARTICLES_PT_bake_unbake_ui)


def unregister():
    bpy.utils.unregister_class(PARTICLES_OT_bake)
    bpy.utils.unregister_class(PARTICLES_OT_free_bake)    
    bpy.utils.unregister_class(PARTICLES_PT_bake_unbake_ui)


if __name__ == "__main__":
    register()
