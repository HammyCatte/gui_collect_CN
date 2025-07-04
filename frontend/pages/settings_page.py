import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font

from pathlib import Path

from backend.config.Config import Config

from ..state import State
from ..xtk.Checkbox import LabeledCheckbox
from ..xtk.FlatImageButton import FlatImageButton

class SettingsPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, padx=16, pady=16)
        self.config(bg='#111')
        self.config(*args, **kwargs)
        self.parent = parent

        self.state    = State.get_instance()
        self.cfg      = Config.get_instance()
        self.terminal = self.state.get_terminal()

        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self, text='警告: 仅当您知道自己在做什么时才启用高级功能！', anchor='center', fg='#FD5', bg=self['bg'], font=('Microsoft YaHei', 20, 'bold'))
        header.pack(pady=(0, 8), fill='x')

        enable_targeted_checkbox = LabeledCheckbox(self, '目标帧分析 (实验性)', ('Microsoft YaHei', 18, 'bold'), initial_state=self.cfg.data.targeted_analysis_enabled)
        enable_targeted_checkbox.on_toggle(lambda v: self.update_cfg('targeted_analysis_enabled', v))
        enable_targeted_checkbox.pack(padx=(8, 0), anchor='nw')

        hsr_shapekey_reversal_checkbox = LabeledCheckbox(
            self, '[HSR] 还原形态键变形效果（需开启dump_cb或目标帧分析）',
            ('Microsoft YaHei', 18, 'bold'), initial_state=self.cfg.data.reverse_shapekeys_hsr
        )
        hsr_shapekey_reversal_checkbox.on_toggle(lambda v: self.update_cfg('reverse_shapekeys_hsr', v))
        hsr_shapekey_reversal_checkbox.pack(padx=(8, 0), anchor='nw')

        zzz_shapekey_reversal_checkbox = LabeledCheckbox(
            self, '[ZZZ] 还原形态键变形效果（需开启dump_cb或目标帧分析）',
            ('Microsoft YaHei', 18, 'bold'), initial_state=self.cfg.data.reverse_shapekeys_zzz
        )
        zzz_shapekey_reversal_checkbox.on_toggle(lambda v: self.update_cfg('reverse_shapekeys_zzz', v))
        zzz_shapekey_reversal_checkbox.pack(padx=(8, 0), anchor='nw')

    def update_cfg(self, key, value):
        self.terminal.print('设置配置: {} = {}'.format(key, value))
        self.cfg.data.__setattr__(key, value)
        self.state.refresh_all_extract_forms()

# class PathPicker(tk.Frame):
#     def __init__(self, parent, placeholder='Path', dialog_title='Select path', *args, **kwargs):
#         tk.Frame.__init__(self, parent)
#         self.config(*args, **kwargs)
#         self.parent = parent
        
#         self.font = Font(family='Arial', size=20, weight='bold')
#         self.placeholder  = placeholder
#         self.dialog_title = dialog_title
#         self.path = ''

#         self.create_widgets()

#     def create_widgets(self):
#         self.folder_path_label = tk.Label(self, text=self.placeholder, fg='#555', font=self.font)
#         if self.path:
#             self.folder_path_label.config(text=self.path)

#         img = tk.PhotoImage(file=Path('./resources/images/buttons/folder_open.256.png').absolute()).subsample(8)
#         pick_folder_btn = FlatImageButton(self, width=40, height=40, img_width=32, img_height=32, bg='#3fb76b', image=img)
#         pick_folder_btn.bind('<Button-1>', lambda _: self.handle_pick_path())

#         self.folder_path_label .pack(side='left')
#         pick_folder_btn        .pack(side='right', padx=0, pady=0)

#     def handle_pick_path(self):
#         path_text = filedialog.askdirectory(mustexist=True, title=self.dialog_title)
#         if path_text:
#             self.set_path(path_text)
    
#     def set_path(self, text: str):
#         self.path = str(Path(text).resolve())
#         print('Set frame analysis path: {}'.format(str(self.path)))
        
#         self.folder_path_label.config(text=self.path)
#         # self.parent.on_address_change(text=self.path)
