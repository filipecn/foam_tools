import graphics
from pathlib import Path
from foam2houdini.logging import *
from foam2houdini.foam_poly_mesh import FoamPolyMesh


class MeshViewer(graphics.App):
    # path to shaders
    resource_dir = (Path(__file__).parent.parent / 'resources').resolve()
    # foam poly mesh data structure
    foam_poly_mesh: FoamPolyMesh

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = Path("/mnt/windows/Projects/foam_experiments/3d/simple_mix/constant/polyMesh")
        path = Path("/home/filipecn/Desktop/bla/simple_mix/constant/polyMesh")
        log_info("Reading foam mesh")
        self.foam_poly_mesh = FoamPolyMesh(path)

    def render_callback(self, time: float):
        pass


if __name__ == "__main__":
    graphics.run_app(MeshViewer)
    # TODO: use dearpygui instead
    # dpg.setup_dearpygui()
    # while dpg.is_dearpygui_running():
    #     dpg.render_dearpygui_frame()
    # dpg.cleanup_dearpygui()
