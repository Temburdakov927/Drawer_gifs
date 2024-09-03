import os
import sys

import dateutil
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication, QVBoxLayout, QSplitter,
                             QFormLayout, QLabel, QFrame, QPushButton,
                             QMenu, QWidget, QAction, QToolBar, QMessageBox, QColorDialog, QHBoxLayout, QListWidget,
                             QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QColor
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel,QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from lol import PlottingApp
import matplotlib.animation as animation

'''class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("lol kek cheburek")
        #layout.addWidget(self.button)  
        self.setLayout(layout)
    def create_body(self):
        #self.textbox = QLineEdit(self)
        #self.textbox.resize(10000,5000)

        toolbar_layout = QHBoxLayout()

        self.setGeometry(0,0,1000,1000)'''


class Label(QLabel):
    def __init__(
        self, background=QColor("white"), foreground=QColor("blue"), parent=None
    ):
        super().__init__(parent)
        self._background = background
        self._foreground = foreground

        self._change_stylesheet()

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        if self._background == color:
            return
        self._background = color
        self._change_stylesheet()

    @property
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, color):
        if self._foreground == color:
            return
        self._foreground = color
        self._change_stylesheet()

    def _change_stylesheet(self):
        qss = "QLabel{color:%s;background-color:%s}" % (
            self.background.name(),
            self.foreground.name(),
        )
        self.setStyleSheet(qss)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.legend_list = None
        self.line_push_button = None
        self.column = None #Показывает текущий тег
        self.color_update = None
        self.color = None
        self.colors = None
        self.rgb = None
        self.settings_menu = QPushButton("click me")
        self.setCentralWidget(self.settings_menu)
        self.w = None
        self.setWindowTitle("График из CSV")
        self.setGeometry(1000, 1000, 8000, 6000)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.button_on = 0 #Индикатор вызова функции pars_data
        self.file_path = None #Путь открываемого файла
        self.file_name = None #Имя открываемого файла
        # Создаем виджет и компоновщик
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.click_recent = 0 #Триггер на клик по кнопке недавние файлы
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.list_clr_butt = []    #Здесь мы будем хранить сгенерированные цвета для графиков
        self.list_button_menu = [] #Здесь мы храним сгенерированные кнопки легенды
        self.create_menu_bar()
        self.create_body()

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu("File")
        self.open_menu = QAction(QIcon("src/icon/csv.png"), '&Open', self)
        self.open_menu.triggered.connect(self.load_csv)
        self.file_menu.addAction(self.open_menu)
        self.recent_file = QAction(QIcon("src/icon/recent_file.png"), '&Recent', self)
        self.recent_file.triggered.connect(self.open_recent)
        self.file_menu.addAction(self.recent_file)
        self.exit_menu = QAction(QIcon("src/icon/exit.png"), '&Exit', self)
        self.exit_menu.setShortcut('Ctrl+Q')
        self.exit_menu.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_menu)

        self.double_scroll_left = self.menu_bar.addMenu(QIcon("src/icon/arrow_double_left.png"), '&double_scroll_left')
        self.scroll_right = self.menu_bar.addMenu(QIcon("src/icon/arrow_left.png"), '&scroll_left')
        self.scroll_left = self.menu_bar.addMenu(QIcon("src/icon/arrow_right.png"), '&scroll_right')
        self.double_scroll_right = self.menu_bar.addMenu(QIcon("src/icon/arrow_double_right.png"), '&double_scroll_right')

        self.settings_menu = self.menu_bar.addMenu(QIcon("src/icon/settings.png"), '&Setting')

        #self.setCentralWidget(self.settings_menu)
        self.setting_tool = QAction(QIcon("C:/Users/pc180/Downloads/csv2.png"), '&Open', self)
        self.setting_tool.triggered.connect(self.open_settings)
        self.settings_menu.addAction(self.setting_tool)
        self.calendar_menu = self.menu_bar.addMenu(QIcon("src/icon/сalendar.png"), '&calendar_menu')


    '''def show_new_window(self):
        self.dialog = SettingsWindow()
        self.dialog.create_body()
        self.dialog.show()'''

    def open_settings(self):
        item = self.legend_list.currentItem()
        if item:
            color = QColorDialog.getColor()
            if color.isValid():
                self.colors[item.text()] = color.name()
                self.plot_graph()

    def open_recent(self):
        self.click_recent = 1
        if self.file_path == None:

            print("Нет недавних файлов")
        else:
            print("Есть такие файлы")
        self.load_csv()
        self.click_recent = 0



    def create_body(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setMinimumWidth(150)

        '''f_label = QLabel('Welcome')
        s_label = QLabel('Installation')
        p_push = QPushButton('Sign in')
        p_push.setContentsMargins(10, 20, 10, 10)'''

        form_lay = QFormLayout()


        # Область легенды
        self.legend_list = QListWidget()
        form_lay.addWidget(self.legend_list)

        form_frame.setLayout(form_lay)

        ver_frame = QFrame()
        ver_frame.setFrameShape(QFrame.StyledPanel)
        ver_box = QVBoxLayout()
        ver_box.setContentsMargins(25, 20, 25, 25)
        #ver_box.addWidget(intro_label)



        ver_box.addWidget(self.canvas)


        ver_frame.setLayout(ver_box)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(form_frame)
        splitter.addWidget(ver_frame)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(splitter)
        self.setCentralWidget(splitter)
        self.load_button = QPushButton("Загрузить CSV")
        self.load_button.clicked.connect(self.load_csv)


    def contextMenuEvent(self, event):
        men = QMenu()
        men.addAction('New')
        open = men.addAction('Open')
        quit = men.addAction('Quit')
        setting = men.addAction('Setting')

        action = men.exec_(self.mapToGlobal(event.pos()))

        if action is quit:
           self.close()
        if action is open:
            self.load_csv()
        if action is setting:
            self.show_new_window()

    def load_csv(self):
        # Открываем диалоговое окно для выбора файла
        if self.click_recent == 0 or self.file_name is None:
            options = QFileDialog.Options()
            self.file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать CSV файл", "",
                                                       "CSV Files (*.csv);;All Files (*)",
                                                       options=options)
            self.file_path = os.path.abspath(self.file_name)
        if self.file_name:
            # Загружаем данные из CSV файла
            #self.info_label.setText(f"Загружен файл: {file_name}")
            self.data_read = pd.read_csv(self.file_name)

            self.data = self.data_read[['ts_path', 'ts_comment', 'sample_time', 'sample_value']]
            self.data_tags = self.data.ts_path.unique()
            self.data = self.data.dropna()
            self.data['sample_time'] = [dateutil.parser.parse(s) for s in self.data['sample_time']]


        # Выполняем простые проверки
        if self.data.empty:
            self.info_label.setText("CSV файл пустой.")
            return
        # Строим график
        self.plot_data()
    #value_time
    #years = 0, month = 0, days = 0, hours = 0, minutes = 0, seconds = 0

    def rgb_to_hex(self,r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    def plot_data(self):
        #self.colors = {self.data_tags: }
        time_end = self.data['sample_time'].max()
        time_start = time_end - pd.DateOffset(minutes = 100)
        # Очищаем график
        self.ax.clear()
        self.pars_data()
        self.ax.legend()
        self.canvas.draw()
        self.update_legend()

    def pars_data(self):
        for number,tag in enumerate(self.data_tags):
            if self.button_on == 0:
                self.rgb = list(np.random.choice(range(256), size=3))
                r = self.rgb[0]
                g = self.rgb[1]
                b = self.rgb[2]
                self.colors = self.rgb_to_hex(r,g,b)
                self.list_clr_butt.append(self.colors)
            data_graph = self.data[self.data['ts_path'].isin([tag])]
            self.ax.plot(data_graph['sample_time'], data_graph['sample_value'], color=self.list_clr_butt[number])
        self.button_on = 1

    def update_legend(self):
        self.legend_list.clear()
        for i, column in enumerate(self.data_tags):

            self.color_update = self.list_clr_butt[i]
            item = QListWidgetItem()
            item_widget = QWidget()
            comment = self.data['ts_comment'][self.data['ts_path'].isin([column])]
            comment = str(comment[0:1])
            comment = comment.split(' ')
            comment_join = ' '.join(comment[4:-4])
            comment_join2 = comment[-4:-3]
            comment_join2 = str(comment_join2[0]).split('\n')[0]
            comment_join = comment_join + " " + comment_join2 + "\n" + str(column)
            line_text = Label()
            line_text.setText(comment_join)
            line_text.setAlignment(Qt.AlignCenter)
            line_text.setFont(QFont("Arial", 10))
            line_text.foreground = QColor(self.color_update)
            #self.list_button_menu.append(line_push_button)
            self.line_push_button = self.draw_button(i)
            self.line_push_button.clicked.connect(self.clicked)
            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(self.line_push_button)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.legend_list.addItem(item)
            self.legend_list.setItemWidget(item, item_widget)
        self.clicked_return()


    def draw_button(self, number):
        line_push_button = QPushButton("Показать график")
        line_push_button.setObjectName(str(number))
        return line_push_button

    def clicked(self):
        sender = self.sender()
        number_button = int(sender.objectName())
        self.column = self.data_tags[number_button]
        self.color = self.list_clr_butt[number_button]
        self.ax.clear()
        data_graph = self.data[self.data['ts_path'].isin([self.column])]
        self.ax.plot(data_graph['sample_time'], data_graph['sample_value'], color=self.color)
        self.ax.legend()
        self.canvas.draw()
        #sender = self.sender()
        #push_button = self.findChild(QPushButton, sender.objectName())
        #print(f'click: {push_button.objectName()}')

    def clicked_return(self):
        item = QListWidgetItem()
        item_widget = QWidget()
        item_layout = QHBoxLayout()
        # if i == len(self.data_tags)-1:
        self.return_push_button = QPushButton("Вернуться к общему графику")
        self.return_push_button.setObjectName('Button_return')
        self.return_push_button.clicked.connect(self.plot_data)
        item_layout.addWidget(self.return_push_button)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self.legend_list.addItem(item)
        self.legend_list.setItemWidget(item, item_widget)

StyleSheet = '''
QMainWindow {
    background-color: #333;
    color: red;
}

/* QMenuBar --------------------------------------------------------------- */

QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 lightgray, stop:1 darkgray);
}
QMenuBar::item {
    spacing: 3px;           
    padding: 2px 10px;
    background-color: rgb(210,105,30);
    color: rgb(255,255,255);  
    border-radius: 5px;
}
QMenuBar::item:selected {    
    background-color: rgb(244,164,96);
}
QMenuBar::item:pressed {
    background: rgb(128,0,0);
}

/* QMenu ------------------------------------------------------------------ */

QMenu {
    font: 12pt;
    background-color: white;
    color: black;
}
QMenu::item:selected {
    color: gray;
}

/* QSplitter -------------------------------------------------------------- */

QSplitter::handle:horizontal {
    width: 2px;
    background-color : green;
}

QSplitter::handle:vertical {
    height: 2px;
    background-color : green;
}

/*  ------------------------------------------------------------------------ */

QLabel {
/*    background-color : blue;*/
    color: #ccc;
}

QPushButton {
    min-width: 36px;
    min-height: 36px;
    border-radius: 7px;
    background: #777;
}
QPushButton:hover {
    color: white;
    background: #999;
}
QPushButton:pressed {
    background-color: #bbdefb;
    color: green;
}

'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    win = Window()
    win.setWindowTitle('First Porgram')
    win.setWindowIcon(QIcon("D:/_Qt/img/qt-logo.png"))
    win.setGeometry(0, 0, 8000, 6000)
    win.show()

    sys.exit(app.exec_())


