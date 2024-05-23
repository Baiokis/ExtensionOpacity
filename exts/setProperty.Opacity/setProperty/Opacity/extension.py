import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Gf, Sdf, Usd


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[setProperty.Opacity] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class SetpropertyOpacityExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[setProperty.Opacity] setProperty Opacity startup")

        self._window = ui.Window("ExOpacity", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                def on_click():

                    omni.kit.commands.execute('SelectPrims',
                        old_selected_paths=[],
                        new_selected_paths=['/World'],
                        expand_in_stage=True)

                    omni.kit.commands.execute('ChangeProperty',
                        prop_path=Sdf.Path('/World/Leather_Black/Shader.inputs:enable_opacity'),
                        value=False,
                        prev=None,
                        target_layer=Sdf.Find('anon:000001E3EE58CDD0:World0.usd'))

                    omni.kit.commands.execute('ChangeProperty',
                        prop_path=Sdf.Path('/World/Leather_Black/Shader.inputs:opacity_constant'),
                        value=0.8,
                        prev=1.0,
                        target_layer=Sdf.Find('anon:000001E3EE58CDD0:World0.usd'))

                ui.Button("Spawn Cube", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[setProperty.Opacity] setProperty Opacity shutdown")
