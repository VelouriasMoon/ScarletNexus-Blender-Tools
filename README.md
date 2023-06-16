# ScarletNexus Blender Tools
A [Blender](https://www.blender.org/) Plugin for assisting with Scarlet Nexus Modding.  

Features tools for dealing with separating outline meshes by visibility and generating outline meshes from an existing mesh.

## Navigation
- [Installation](#installation)
- [Split Outline Mesh](#split-outline-mesh-by-visibility)
- [Make Outlines](#making-outlines)

## Installation
1. Download python file from Release (https://github.com/VelouriasMoon/ScarletNexus-Blender-Tools/releases/latest) or the [source code](https://github.com/VelouriasMoon/ScarletNexus-Blender-Tools/blob/main/SNTools.py)
2. In Blender, open the Preferences window (Edit>Preferences) and select the Add-ons tab.
3. Press the 'Install...' button and select the python file you downloaded.
4. Enable the add-on and save preferences. If you want to uninstall the addon, simply disable it in preferences and then delete the python file.
<p align="middle">
  <img src="https://github.com/VelouriasMoon/ScarletNexus-Blender-Tools/blob/main/Images/Settings.png" width="480">
</p>

## Split Outline Mesh By Visibility
Select the outline mesh in blender sperated out from the base model mesh and press the "Split Outline Mesh By Visibility" to split the outline mesh by Hidden With Hood (Vertex Color.b > 0.90, usually 1.0), Visible With Hood (Vertex Color.b > 0.70 and < 0.90), and Always Visible (Vertex Color.b == 0.0)
<p align="middle">
  <img src="https://github.com/VelouriasMoon/ScarletNexus-Blender-Tools/blob/main/Images/SplitOutline.gif" width="480">
</p>

## Making Outlines
1. Select a Mesh which you want to make an outline mesh for
2. (Optional) Pick if Mesh should be shown only with hood or be hidden with hood, select none for just meshes that are always visible
3. (Optional) Select the outline Material to automatically set the material of new outline mesh, leave empty if you want to do that manually
4. Press "Generate Outline Mesh" to automatically generate the outline mesh sperate from your original mesh, Outline thickness has some basic caluations for angles softening on sharper angles
<p align="middle">
  <img src="https://github.com/VelouriasMoon/ScarletNexus-Blender-Tools/blob/main/Images/MakeOutline.gif" width="480">
</p>
