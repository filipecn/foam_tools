import glfw
import OpenGL.GL as gl
import moderngl_window as mglw
from imgui.integrations.glfw import GlfwRenderer
import imgui
from pathlib import Path
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from abc import ABC, abstractmethod


def app(render, width=1280, height=720, window_name="Viewer"):
    """

    :param render:
    :param width:
    :param height:
    :param window_name:
    :return:
    """
    imgui.create_context()
    window = impl_glfw_init(width, height, window_name)
    impl = GlfwRenderer(window)
    # dpg.setup_dearpygui()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        gl.glClearColor(0.3, 0.5, 0.4, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # impl.process_inputs()
        # imgui.new_frame()
        render()
        # dpg.render_dearpygui_frame()
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)
    impl.shutdown()
    # dpg.cleanup_dearpygui()
    glfw.terminate()


def impl_glfw_init(width, height, window_name):
    """

    :param width:
    :param height:
    :param window_name:
    :return:
    """
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


class App(mglw.WindowConfig, ABC):
    gl_version = (3, 3)
    title = "App"
    resource_dir = (Path(__file__).parent.parent / 'resources').resolve()
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

    def render(self, time: float, frame_time: float):
        imgui.new_frame()
        self.render_callback(time)
        imgui.render()
        self.imgui.render(imgui.get_draw_data())
        pass

    @abstractmethod
    def render_callback(self, time: float):
        pass

    def resize(self, width: int, height: int):
        self.imgui.resize(width, height)

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)
        if not imgui.get_io().want_capture_mouse:
            pass

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)
        if not imgui.get_io().want_capture_mouse:
            pass

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)
        if not imgui.get_io().want_capture_mouse:
            pass

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)
        if not imgui.get_io().want_capture_mouse:
            pass

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)


def run_app(application):
    mglw.run_window_config(application)
