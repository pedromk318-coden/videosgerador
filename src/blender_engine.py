#!/usr/bin/env python3
"""Offline Blender 3D renderer for vertical story videos. No AI or external APIs."""
import argparse, json, math, os, subprocess, sys
from pathlib import Path
import bpy
from mathutils import Vector

def mat(name, color, metallic=0.0, roughness=0.65):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic; bs.inputs["Roughness"].default_value=roughness
    return m

def cube(name, loc, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name
    o.dimensions=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new("Soft edges","BEVEL"); mod.width=bevel; mod.segments=3
        o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
    return o

def uv(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
    bpy.ops.object.shade_smooth(); return o

def cylinder(name, a, b, radius, material):
    mid=(Vector(a)+Vector(b))/2; vec=Vector(b)-Vector(a)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=vec.length, location=mid)
    o=bpy.context.object; o.name=name; o.rotation_mode='QUATERNION'; o.rotation_quaternion=vec.to_track_quat('Z','Y')
    o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o

def look(obj, target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

def key(obj, frame, loc=None, rot=None):
    if loc is not None: obj.location=loc; obj.keyframe_insert(data_path="location",frame=frame)
    if rot is not None: obj.rotation_euler=rot; obj.keyframe_insert(data_path="rotation_euler",frame=frame)

def build_character(mats):
    skin,shirt,pants,shoe,hair=mats
    parts=[]
    # A recognizable stylized 3D human, approximately five metres tall.
    parts.append(uv("Head",(0,0,4.48),(.43,.38,.48),skin))
    parts.append(uv("Hair",(0,-.02,4.77),(.44,.39,.24),hair))
    parts.append(cube("Torso",(0,0,3.35),(.95,.48,1.55),shirt,.16))
    parts.append(cylinder("Neck",(0,0,4.05),(0,0,4.22),.16,skin))
    for s in (-1,1):
        parts.append(cylinder("Upper arm",(s*.52,0,3.82),(s*.72,0,3.05),.16,shirt))
        parts.append(uv("Hand",(s*.72,0,3.00),(.16,.15,.18),skin))
        parts.append(cylinder("Leg",(s*.25,0,2.58),(s*.28,0,.35),.19,pants))
        parts.append(uv("Shoe",(s*.28,-.12,.18),(.28,.43,.16),shoe))
    return parts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="scenes.json"); ap.add_argument("--output",default="output/video.mp4")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    args=ap.parse_args(argv); data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    scenes=data.get("scenes",[])
    if not scenes: raise SystemExit("Projeto sem cenas.")
    res=data.get("resolution",{}); w=int(res.get("width",720)); h=int(res.get("height",1280)); fps=int(data.get("fps",24))
    total=sum(float(s.get("duration",5)) for s in scenes)
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    # Materials
    wall=mat("Warm plaster",(.48,.39,.31)); floor=mat("Oak floor",(.19,.095,.045))
    blue=mat("Deep blue bedding",(.055,.16,.29)); wood=mat("Walnut",(.22,.12,.065))
    glass=mat("Window glass",(.055,.20,.29),.25,.25); skin=mat("Warm skin",(.56,.31,.20))
    shirt=mat("Teal shirt",(.035,.25,.30)); pants=mat("Dark trousers",(.045,.065,.09))
    shoe=mat("Shoes",(.025,.025,.03)); hair=mat("Hair",(.035,.022,.018))
    white=mat("Trim",(.72,.67,.57)); citymat=mat("City silhouettes",(.07,.12,.18))
    # Bedroom set, measured in metres.
    cube("Floor",(0,0,-.12),(12,12,.24),floor,.05)
    cube("Back wall",(0,4,3),(12,.2,6),wall,.04)
    cube("Left wall",(-6,0,3),(.2,8,6),wall,.04)
    # Large window on back wall
    cube("Window frame",(2.2,3.86,3.3),(3.3,.18,3.2),wood,.04)
    cube("Window view",(2.2,3.74,3.3),(3.0,.04,2.9),glass)
    cube("Window mullion",(2.2,3.68,3.3),(.07,.08,2.9),white)
    cube("Window crossbar",(2.2,3.68,3.3),(3.0,.08,.07),white)
    # Bed and furniture
    cube("Bed frame",(-1.6,1.0,.45),(2.5,3.6,.55),wood,.13)
    cube("Mattress",(-1.6,.9,.82),(2.42,3.35,.35),white,.14)
    cube("Duvet",(-1.6,-.05,1.02),(2.4,1.65,.18),blue,.12)
    for x in (-2.4,-.8):
        cube("Pillow",(x,2.0,1.05),(.7,.65,.2),white,.12)
    cube("Nightstand",(-3.35,2.0,.55),(.8,.8,1.1),wood,.08)
    cube("Door",(5.2,3.86,1.45),(1.35,.16,2.9),wood,.05)
    # A city skyline visible through the window, layered at different depths.
    for i in range(9):
        x=-1.2+i*.85; height=1.7+(i*37%17)/10
        cube("Distant building",(x,5.0,1.6+height/2),(.65,.55,height),citymat,.04)
        for z in range(3):
            cube("Lit window",(x,4.70,1.1+z*.38),(.12,.025,.16),white,.01)
    # Giant person in the middle of the room, scaled to 5m.
    person=build_character((skin,shirt,pants,shoe,hair))
    # Soft 3D lighting
    world=bpy.context.scene.world; world.color=(.12,.12,.12)
    bpy.ops.object.light_add(type='AREA', location=(-3,-4,7)); keylight=bpy.context.object
    keylight.data.energy=1150; keylight.data.shape='DISK'; keylight.data.size=6; look(keylight,(0,0,2))
    bpy.ops.object.light_add(type='AREA', location=(4,2,5)); fill=bpy.context.object
    fill.data.energy=800; fill.data.color=(.48,.68,1.0); fill.data.size=5; look(fill,(0,0,2.5))
    bpy.ops.object.camera_add(location=(7,-11,5)); cam=bpy.context.object
    cam.data.lens=42; bpy.context.scene.camera=cam
    # Scene timeline and camera choreography.
    start=1
    for i,s in enumerate(scenes):
        duration=float(s.get("duration",5)); end=start+max(1,round(duration*fps))-1
        words=" ".join(str(s.get(k,"")) for k in ("title","visual_description","environment","action","camera","text","narration")).lower()
        if i==0:
            p1=(6,-10,3.2); target=(0,0,2.3); p2=(4.7,-8,3.0)
        elif any(k in words for k in ("janela","rua","cidade","window","outside")) or i>=2:
            p1=(8,-10,5.4); target=(1.2,1.5,3.0); p2=(6.8,-8.5,4.7)
        else:
            p1=(5,-9,2.4); target=(0,0,2.8); p2=(4.2,-7.8,3.0)
        cam.location=p1; look(cam,target); cam.keyframe_insert(data_path="location",frame=start); cam.keyframe_insert(data_path="rotation_euler",frame=start)
        cam.location=p2; look(cam,(target[0],target[1],target[2]+.25)); cam.keyframe_insert(data_path="location",frame=end); cam.keyframe_insert(data_path="rotation_euler",frame=end)
        # Subtle character movement between shots; character silhouette remains consistent.
        for obj in person:
            obj.keyframe_insert(data_path="location",frame=start)
        start=end+1
    scene=bpy.context.scene
    engine_ids={item.identifier for item in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
    scene.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engine_ids else "BLENDER_EEVEE"
    scene.render.resolution_x=w; scene.render.resolution_y=h; scene.render.resolution_percentage=100
    scene.render.fps=fps; scene.frame_start=1; scene.frame_end=max(2,start-1)
    scene.render.image_settings.file_format='FFMPEG'
    scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'; scene.render.ffmpeg.constant_rate_factor='MEDIUM'
    scene.render.filepath=str(Path(args.output).resolve())
    scene.view_settings.view_transform='Standard'
    scene.render.image_settings.color_mode='RGB'
    scene.camera.data.dof.use_dof=True; scene.camera.data.dof.focus_object=person[0]; scene.camera.data.dof.aperture_fstop=5.6
    # Smooth interpolation for cinematic camera motion.
    for obj in (cam,):
        if obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation='BEZIER'
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    scene.frame_set(1)
    bpy.ops.render.render(animation=True)
    print("Render 3D concluído:",args.output)

if __name__=="__main__": main()
