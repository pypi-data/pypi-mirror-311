from PySide6.QtWidgets import QDialog, QHBoxLayout, QFrame, QVBoxLayout

from ..frameless_window import FramelessWindow
from ...modern_titlebar import ModernTitleBar
from ....configurations import preferences
from ....core import logger
from ....utils.qss_loader import load_stylesheet


class ModernDialog(FramelessWindow, QDialog):
    def __init__(self, *args, **kwargs):
        logger.debug('ModernDialog init')
        super().__init__(*args, **kwargs)

    def apply_modern(self):
        logger.debug('ModernMessageBox apply_modern')

        # #########################################################
        # 0. 无框架
        # #########################################################
        # 应用无框架模式，需要在所有基类都完成初始化之后再执行这些操作
        # 受继承顺序影响，在FramelessWindow的init中执行这些操作会丢失部分特性
        # 这里选择将这些操作单独封装成一个方法，在此处手动调用
        self.apply_frameless()
        self.windowEffect.disableMaximizeButton(self.winId())
        self._resizeable = False

        # #########################################################
        # 1. 样式
        # #########################################################
        # 应用样式表
        style_path = f':themes/{preferences.style.lower()}/styles/{preferences.theme.lower()}'
        style_sheets = load_stylesheet(style_path)
        # logger.debug(style_sheets)
        self.setStyleSheet(style_sheets)

        # #########################################################
        # 2. 创建好各个容器和组件
        # #########################################################
        # 新的内容容器
        self.frm_content = QFrame()
        self.frm_content.setObjectName("ModernContent")

        # 迁移控件到新的内容容器
        if self.layout():
            self.frm_content.setLayout(self.layout())
        else:
            for child in self.children():
                if child.parent() == self:
                    child.setParent(self.frm_content)

        # 创建顶级布局
        layout = QHBoxLayout(self)
        layout.setSpacing(0)  # 内间距
        layout.setContentsMargins(0, 0, 0, 0)  # 内边距
        self.setLayout(layout)

        # 创建容器
        self.container = QFrame(self)  # 创建modern容器，无父
        self.container.setObjectName('ModernContainer')
        self.container.setLayout(QVBoxLayout())  # 创建垂直布局
        self.container.layout().setSpacing(0)  # 内间距
        self.container.layout().setContentsMargins(0, 0, 0, 0)  # 内边距
        self.layout().addWidget(self.container)

        # Container垂直结构--TitleBar控件
        self.titlebar = ModernTitleBar(self.container)  # 创建标题栏
        self.container.layout().addWidget(self.titlebar)  # 加入布局
        self.titlebar.btn_settings.hide()  # 隐藏按钮
        self.titlebar.btn_maximize.hide()  # 隐藏按钮

        # Container垂直结构--Content
        self.container.layout().addWidget(self.frm_content)

        # self.adjustSize()

    def after_modern(self):
        pass
