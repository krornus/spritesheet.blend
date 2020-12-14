# Prerequisites
Download [requirements.txt](https://github.com/krornus/spritesheet.blend/releases/latest/download/requirements.txt)

```sh
cd "<path to blender's python>/bin"
./python.exe -m pip install --upgrade -r <path to requirements.txt>
```

The path to blender's python may be found by opening the scripting layout in
blender, then in the python console, typing `import sys; print(sys.exec_prefix)`.

# Installing the plugin
Download [spritesheet.zip](https://github.com/krornus/spritesheet.blend/releases/latest/download/spritesheet.zip)

In blender, go to `Edit -> Preferences -> Add-ons` and click the `Install`
button in the top right. Choose `spritesheet.zip`, and ensure it is enabled by
looking for the `Sprite Sheet Renderer` and seeing if it checked.

# Using the plugin
The plugin should appear in the `Active Tool and Workspace settings` section of
the Properties panel on the right. You must set an output file path for your
sprite sheet. The `Default Render Settings` button will modify your current
render settings to output pixel art.
