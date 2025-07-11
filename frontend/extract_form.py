from pathlib import Path
import time
import traceback

import tkinter as tk

from .xtk.FlatButton import FlatButton
from .xtk.EntryWithPlaceholder import EntryWithPlaceholder
from .xtk.InputComponentList import InputComponentFrameList
from .xtk.CompactCheckbox import CompactCheckbox
from .xtk.PathPicker import PathPicker
from .xtk.ScrollableFrame import ScrollableFrame

from .style import brighter
from .state import State

from backend.config.Config import Config
from backend.analysis.FrameAnalysis import FrameAnalysis
from backend.utils import is_valid_hash
from backend.analysis import targeted_analysis


class ExtractForm(tk.Frame):
    def __init__(self, parent, variant, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.config(*args, **kwargs)
        self.config(bg='#111')
        self.parent = parent
        self.variant = variant

        if   self.variant.value == 'hsr': self.accent_color = '#7a6ce0'
        elif self.variant.value == 'zzz': self.accent_color = '#e2751e'
        elif self.variant.value ==  'gi': self.accent_color = '#5fb970'
        elif self.variant.value == 'hi3': self.accent_color = '#c660cf'

        self.cfg = Config.get_instance()
        self.state = State.get_instance()
        self.state.register_extract_form(self)

        self.terminal = self.state.get_terminal()

        self.configure_grid()
        self.create_widgets()
        self.grid_widgets()

    def configure_grid(self):
        self   .grid_rowconfigure(0, weight=0)
        self   .grid_rowconfigure(1, weight=0)
        self   .grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def create_widgets(self):
        self.component_options_frame = ScrollableFrame(self, bg='#222', width=600)
        self.extract_options_frame   = tk.Frame(self, bg='#222', padx=16, pady=16)
        self.targeted_dump           = tk.Frame(self, bg='#222', padx=16, pady=16)
        self.extract_frame           = tk.Frame(self, bg='#111')

        self.create_component_options()
        self.create_extract_options()
        self.create_targeted_options()

        extract_button = FlatButton(self.extract_frame, text='提取', bg='#A00', hover_bg='#F00')
        extract_button.bind('<Button-1>', lambda _: self.start_extraction())
        extract_button.pack(fill='x', side='bottom', anchor='e', ipadx=16, ipady=16)

    def create_component_options(self):
        self.input_component_list = InputComponentFrameList(self.component_options_frame.interior)
        self.input_component_list.pack(anchor='w', padx=(0,4), pady=(16,0), fill='both')

    def create_targeted_options(self):
        targeted_dump_frame_title = tk.Label(self.targeted_dump, text='目标帧分析', bg='#222', fg='#555', anchor='w', font=('Microsoft YaHei', '16', 'bold'))
        targeted_dump_frame_title.pack(fill='x')
        
        pp = PathPicker(self.targeted_dump, value=Path('include', 'auto_generated.ini'), callback=None, bg='#333', button_bg=self.accent_color)
        pp.pack(side='top', fill='x', pady=(0, 12))

        targeted_options = self.cfg.data.game[self.variant.value].targeted_options
        def handle_change_0(newValue: bool):
            self.terminal.print('设置配置: /game/{}/targeted_options/force_dump_dds = {}'.format(self.variant.value, newValue))
            targeted_options.force_dump_dds = newValue
        def handle_change_1(newValue: bool):
            self.terminal.print('设置配置: /game/{}/targeted_options/dump_rt = {}'.format(self.variant.value, newValue))
            targeted_options.dump_rt = newValue
        def handle_change_2(newValue: bool):
            self.terminal.print('设置配置: /game/{}/targeted_options/symlink = {}'.format(self.variant.value, newValue))
            targeted_options.symlink = newValue
        def handle_change_3(newValue: bool):
            self.terminal.print('设置配置: /game/{}/targeted_options/share_dupes = {}'.format(self.variant.value, newValue))
            targeted_options.share_dupes = newValue

        checkbox_frame = tk.Frame(self.targeted_dump, height=100,  bg=self.targeted_dump['bg'])
        checkbox_frame.pack(fill='both', expand=True, pady=(0, 12))
        checkbox_frame.grid_rowconfigure(0, weight=1)
        checkbox_frame.grid_rowconfigure(1, weight=1)
        checkbox_frame.grid_columnconfigure(0, weight=1)
        checkbox_frame.grid_columnconfigure(1, weight=0)

        checkbox_0 = CompactCheckbox(
            checkbox_frame, height=30, width=260, bg='#222', active_bg=self.accent_color, on_change=handle_change_0,
            active=targeted_options.force_dump_dds, text='强制将纹理转储为 .dds',
            tooltip_text='某些纹理默认转储为 .jpg 格式。启用此选项可让 3dm 将所有纹理转储为 .dds 格式，这可能会比 .jpg 格式的纹理质量更高。'
        )
        checkbox_1 = CompactCheckbox(
            checkbox_frame, height=30, width=260, bg='#222', active_bg=self.accent_color, on_change=handle_change_1,
            active=targeted_options.dump_rt, text='转储渲染目标',
            tooltip_text=(
                '渲染目标有助于猜测哪个绘制调用具有所需的纹理，并将其作为纹理选择器中初始选定的绘制调用。 '
                '这并非完美无缺，也不是强制选项，它会略微增加 F8 键的完成时间。 '
                '请务必检查除初始选定的绘制调用之外的其他绘制调用，以查找您感兴趣的纹理。如果您禁用了转储渲染目标，那么检查其他绘制调用就显得尤为重要。'
            )
        )
        checkbox_2 = CompactCheckbox(
            checkbox_frame, height=30, width=170, bg='#222', active_bg=self.accent_color, on_change=handle_change_2,
            active=targeted_options.symlink, text='符号链接',
            tooltip_text=(
                '在目标帧分析中设置 symlink 选项。可以显著减少帧分析文件的大小。 '
                '如果不支持符号链接，则将回退到硬链接。使用硬链接提取将无法与 gui_collect 配合使用。'
                '有关 symlink 选项的更多信息，请参阅 d3dx.ini。'
            )
        )
        checkbox_3 = CompactCheckbox(
            checkbox_frame, height=30, width=170, bg='#222', active_bg=self.accent_color, on_change=handle_change_3,
            active=targeted_options.share_dupes, text='分享重复内容',
            tooltip_text='在目标帧分析中设置 share_dupes 选项。有关 share_dupes 选项的更多信息，请参阅 d3dx.ini 文件。'
        )

        checkbox_0.grid(row=0, column=0, padx=(3, 8), pady=(3, 0), sticky='nsew')
        checkbox_1.grid(row=1, column=0, padx=(3, 8), pady=(3, 0), sticky='nsew')
        checkbox_2.grid(row=0, column=1, padx=(3, 8), pady=(3, 0), sticky='nsew')
        checkbox_3.grid(row=1, column=1, padx=(3, 8), pady=(3, 3), sticky='nsew')

        generate_targeted_button = FlatButton(self.targeted_dump, text='生成', bg=self.accent_color, hover_bg=brighter(self.accent_color))
        generate_targeted_button.bind('<Button-1>', lambda _: self.generated_targeted_dump_ini())
        generate_targeted_button.pack(side='right', ipadx=10, ipady=10, padx=(8,0))

        clear_targeted_button = FlatButton(self.targeted_dump, text='清空', bg=self.accent_color, hover_bg=brighter(self.accent_color))
        clear_targeted_button.bind('<Button-1>', lambda _: self.clear_targeted_dump_ini())
        clear_targeted_button.pack(side='right', ipadx=10, ipady=10)

    def create_extract_options(self):
        self.extract_name = EntryWithPlaceholder(
            self.extract_options_frame, placeholder='提取名称',
            color='#555', font=('Microsoft YaHei', '24', 'bold'),
            bg='#333', relief='flat', width=30
        )
        self.extract_name.pack(side='top', fill='x', pady=(0, 2))

        def handle_path_change(newPath: str):
            self.cfg.data.game[self.variant.value].extract_path = newPath
            self.terminal.print('设置配置: /game/extract/{}/extract_path = <PATH>{}</PATH>'.format(self.variant.value, newPath))

        pp = PathPicker(self.extract_options_frame, value=self.cfg.data.game[self.variant.value].extract_path, callback=handle_path_change, bg='#333', button_bg=self.accent_color)
        pp.pack(side='top', fill='x', pady=(0, 12))

        game_options = self.cfg.data.game[self.variant.value].game_options
        def handle_change_0(newValue: bool):
            self.terminal.print('设置配置: /game/{}/clean_extract_folder = {}'.format(self.variant.value, newValue))
            game_options.clean_extract_folder  = newValue
        def handle_change_1(newValue: bool):
            self.terminal.print('设置配置: /game/{}/open_extract_folder = {}'.format(self.variant.value, newValue))
            game_options.open_extract_folder   = newValue
        def handle_change_2(newValue: bool):
            self.terminal.print('设置配置: /game/{}/delete_frame_analysis = {}'.format(self.variant.value, newValue))
            game_options.delete_frame_analysis = newValue

        checkbox_0 = CompactCheckbox(self.extract_options_frame, height=30, active_bg=self.accent_color, active=game_options.clean_extract_folder,  on_change=handle_change_0, text='提取前清理提取文件夹')
        checkbox_1 = CompactCheckbox(self.extract_options_frame, height=30, active_bg=self.accent_color, active=game_options.open_extract_folder,   on_change=handle_change_1, text='提取后打开提取文件夹')
        checkbox_2 = CompactCheckbox(self.extract_options_frame, height=30, active_bg=self.accent_color, active=game_options.delete_frame_analysis, on_change=handle_change_2, text='提取后删除帧分析文件夹')
        checkbox_0.pack(side='top', pady=(3, 0), anchor='w', fill='x')
        checkbox_1.pack(side='top', pady=(3, 0), anchor='w', fill='x')
        checkbox_2.pack(side='top', pady=(3, 0), anchor='w', fill='x')



    def grid_forget_widgets(self):
        for child in self.winfo_children():
            child.grid_forget()
            # print('Forgot {}'.format(child))

    def grid_widgets(self):
        self.component_options_frame .grid(column=0, row=0, padx=(16, 0), pady=16, sticky='nsew', rowspan=3)
        self.extract_options_frame   .grid(column=1, row=0, padx=16, pady=(16, 0), sticky='nsew')
        if self.cfg.data.targeted_analysis_enabled:
            self.targeted_dump.grid(column=1, row=1, padx=16, pady=(16, 0), sticky='nsew')
            self.extract_frame.grid(column=1, row=2, padx=16, pady=16, sticky='nsew')
        else:
            self.extract_frame.grid(column=1, row=1, rowspan=2, padx=16, pady=16, sticky='nsew')

    def collect_input(self, skip_collect_nothing=True):
        path = Path(self.parent.address_frame.path)
        extract_name = self.extract_name.get().strip().replace(' ', '')

        input_component_hashes   = []
        input_component_names    = []
        input_components_options = []
        for input_component in self.input_component_list.get():
            if not input_component.hash: continue
            if not is_valid_hash(input_component.hash):
                self.terminal.print('<ERROR>无效的hash: {}</ERROR>'.format(input_component.hash))
                return None, None, None, None, None
            
            # Don't include components with none of the collect options enabled
            if skip_collect_nothing:
                collect_nothing = all(option_value is False for option_value in input_component.options.values())
                if collect_nothing: continue

            input_component_hashes  .append(input_component.hash)
            input_component_names   .append(input_component.name)
            input_components_options.append(input_component.options)

        # all_options = {
        #     'collect_model_data': True, 'collect_model_hashes': True,
        #     'collect_texture_data': True, 'collect_texture_hashes': True,
        # }
        # return (
        #     'Castorice',
        #     ['c5794477', 'f2584f98', 'fd990f82', '82e3ac33'],
        #     ['Hair', 'Face', 'Body', 'Scythe'],
        #     [{**all_options}] * 4,
        #     path
        # )
        # return (
        #     'Anaxa',
        #     ['88914f28', 'e0d51cde', '62a2c7ac', '364073b1', '7dd2153f'],
        #     ['Hair', 'Face', 'Body', 'Gun', 'Core'],
        #     [{**all_options}] * 5,
        #     path
        # )
        return extract_name, input_component_hashes, input_component_names, input_components_options, path

    def generated_targeted_dump_ini(self):
        extract_name, input_component_hashes, input_component_names, _, path = self.collect_input(skip_collect_nothing=False)
        if not input_component_hashes:
            self.terminal.print('<ERROR>目标 Ini 生成已中止！未提供有效hash值。</ERROR>')
            return

        d3dx_path = path.parent
        if not (d3dx_path/'d3dx.ini').exists():
            d3dx_path = None

        targeted_options = self.cfg.data.game[self.variant.value].targeted_options
        targeted_analysis.generate(
            extract_name,
            input_component_hashes,
            input_component_names,
            d3dx_path,
            self.terminal,
            dump_rt        = targeted_options.dump_rt,
            force_dump_dds = targeted_options.force_dump_dds,
            symlink        = targeted_options.symlink,
            share_dupes    = targeted_options.share_dupes,
        )

    def clear_targeted_dump_ini(self):
        targeted_analysis.clear(self.terminal)

    def start_extraction(self):
        st = time.time()

        extract_name, input_component_hashes, input_component_names, input_components_options, path = self.collect_input()
        if not input_component_hashes:
            self.terminal.print('<ERROR>帧分析已中止！未提供有效的hash值。</ERROR>')
            return
        if not extract_name:
            self.terminal.print('<ERROR>帧分析已中止！您必须为提取的模型提供一个名称。</ERROR>')
            return
        if not (path/'log.txt').exists():
            self.terminal.print('<ERROR>帧分析已中止！无效的帧分析路径: "{}".</ERROR>'.format(str(path)))
            return

        frame_analysis = FrameAnalysis(path)
        self.state.set_var(State.K.FRAME_ANALYSIS, frame_analysis)
        extracted_components = frame_analysis.extract(
            input_component_hashes, input_component_names, input_components_options,
            game=self.variant.value,
            reverse_shapekeys=(
                     self.cfg.data.reverse_shapekeys_hsr if self.variant.value == 'hsr'
                else self.cfg.data.reverse_shapekeys_zzz if self.variant.value == 'zzz'
                else False
            )
        )
        if extracted_components is None:
            self.terminal.print('<ERROR>帧分析失败！</ERROR>')
            return

        # Create list with indices of components that need their textures to be selected in the texture picker
        # The other components should not show up in the texture picker, but should still be exported
        textures_component_idx = [
            idx for idx, extracted_component in enumerate(extracted_components)
            if extracted_component.options['collect_texture_data'] or extracted_component.options['collect_texture_hashes']
        ]

        if len(textures_component_idx) > 0:
            self.state.lock_sidebar()
            self.parent.texture_picker.load(extract_name, extracted_components, textures_component_idx, finish_extraction_callback=self.finish_extraction)
            self.parent.texture_picker.focus_set()
            self.update_idletasks()
            self.parent.show_texture_picker()
            self.update_idletasks()
            self.terminal.print('就绪 {:.3}s'.format(time.time() - st))
        else:
            self.finish_extraction(extract_name, extracted_components)

    def finish_extraction(self, extract_name, extracted_components, collected_textures=None):
        try:
            frame_analysis = self.state.get_var(State.K.FRAME_ANALYSIS)
            frame_analysis.export(extract_name, extracted_components, collected_textures, game=self.variant.value)
            if not frame_analysis.path.exists():
                self.parent.address_frame.load_latest_frame_analysis()
            self.state.del_var(State.K.FRAME_ANALYSIS)

        except Exception as X:
            self.terminal.print(f'<ERROR>{X}</ERROR>')
            self.terminal.print(f'<ERROR>{traceback.format_exc()}</ERROR>')
            self.terminal.print('<ERROR>帧分析失败！</ERROR>')

        self.state.unlock_sidebar()

    def cancel_extraction(self):
        self.terminal.print('<WARNING>帧分析已取消。</WARNING>')
        self.state.unlock_sidebar()
