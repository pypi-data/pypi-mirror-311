from zgui import *
from tkinter.ttk import Notebook
from xl_word import WordFile
from utility import SuperWordFile
import sys
import time


class WordTemplateEditor:
    def __init__(self):
        self.app = App({'title': 'WordX模板工具箱', 'size': (420, 330), 'loc': (500, 300)})
        self.root = self.app.instance
        self._init_ui()

    def _init_ui(self):
        self._create_notebook()
        self._create_edit_tab()
        self._create_test_tab()

    def _create_notebook(self):
        self.notebook = Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.edit_frame = Frame(self.root, relief='ridge', borderwidth=1)
        self.test_frame = Frame(self.root, relief='ridge', borderwidth=1)

        self.notebook.add(self.edit_frame, text='编辑')
        self.notebook.add(self.test_frame, text='测试')

    def _create_edit_tab(self):
        # 创建标签和输入框
        labels = [('模板目录', 5), ('模板文件', 30), ('资源文件', 55), ('写入路径', 80)]
        self.inputs = {}
        
        for label_text, y_pos in labels:
            label = Label(self.edit_frame, text=label_text)
            label.pack()
            label.place(x=5, y=y_pos)
            
            input_field = self.app.input(self.edit_frame, print, width=48)
            input_field.pack()
            input_field.place(x=65, y=y_pos)
            self.inputs[label_text] = input_field

        # 创建按钮
        extract_buttons = [
            ('提取document', self._extract_document, 30, 110),
            ('提取header', self._extract_header, 155, 110),
            ('提取footer', self._extract_footer, 280, 110)
        ]
        
        for text, command, x, y in extract_buttons:
            btn = self.app.button(self.edit_frame, text, command, width=13)
            btn.pack()
            btn.place(x=x, y=y)

        middle_buttons = [
            ('组装', self._generate, 30, 145, 22),
            ('测试', self._test, 220, 145, 22),
            ('渲染', self._render, 30, 180, 49),
            ('写入', self._write, 30, 215, 49)
        ]

        for text, command, x, y, width in middle_buttons:
            btn = self.app.button(self.edit_frame, text, command, width=width)
            btn.pack()
            btn.place(x=x, y=y)

    def _create_test_tab(self):
        test_buttons = [
            ('word转xml(竖向)', self._word2xml_v, 30),
            ('word转xml(横向)', self._word2xml_h, 80),
            ('xml转word(竖向)', self._xml2word_v, 130),
            ('xml转word(横向)', self._xml2word_h, 180)
        ]

        for text, command, y in test_buttons:
            btn = self.app.button(self.test_frame, text, command, width=49)
            btn.pack()
            btn.place(x=30, y=y)

    def _get_edit_input(self):
        return (self.inputs['模板目录'].get(),
                self.inputs['模板文件'].get())

    def _extract_document(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).extract('document.xml')

    def _extract_header(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).extract('header.xml')

    def _extract_footer(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).extract('footer.xml')

    def _generate(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).generate()

    def _test(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).test()

    def _write(self):
        wf = SuperWordFile(
            self.inputs['模板目录'].get(),
            self.inputs['模板文件'].get()
        )
        wf.write(
            self.inputs['资源文件'].get(),
            self.inputs['写入路径'].get()
        )

    def _render(self):
        folder, file = self._get_edit_input()
        SuperWordFile(folder, file).render()

    def _word2xml_h(self):
        SuperWordFile.word2xml('h')

    def _word2xml_v(self):
        SuperWordFile.word2xml('v')

    def _xml2word_h(self):
        SuperWordFile.xml2word('h')

    def _xml2word_v(self):
        SuperWordFile.xml2word('v')

    def run(self):
        self.app.run()


if __name__ == '__main__':
    editor = WordTemplateEditor()
    editor.run()