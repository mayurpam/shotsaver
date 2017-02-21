

from PySide import QtGui, QtCore
from shiboken import wrapInstance

import maya.OpenMayaUI as omui

import shot as mod_shot
reload(mod_shot)

# root path of the episode directory
ROOT_PATH = r'E:/mayur/brownbag/PipelineTDTest-master/PipelineTDTest-master/episodes'


def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)


class ShotSaverUI(QtGui.QMainWindow):
    def __init__(self, parent=maya_main_window()):
        super(ShotSaverUI, self).__init__(parent)

        self.setup_controls()
        self.setup_layout()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.load_item('epi')
        self.setup_connection()

    def setup_controls(self):
        '''Create all qt gui elements '''

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Shot Saver')

        self.main_widget = QtGui.QWidget(self)

        self.ql_ep = QtGui.QLabel('Episode')
        # self.ql_sq = QtGui.QLabel('Sequence')
        self.ql_sq = QtGui.QLabel('Shot')

        self.lw_episode = QtGui.QListView()
        # self.lw_seq = QtGui.QListWidget()
        self.lw_shot = QtGui.QListView()

        self.lw_fileList = QtGui.QListView()
        self.lw_fileList.setMinimumHeight(30)
        self.lw_fileList.setMaximumHeight(90)
        self.lw_fileList.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.pb_save = QtGui.QPushButton('Version Up And Save')

    def setup_model_view(self, path, view):
        '''
        setup directory structure model
        '''
        model = QtGui.QFileSystemModel()
        model.setRootPath(path)
        view.setModel(model)
        view.setRootIndex(model.index(path))
        

    def setup_layout(self):
        '''
        setup all the qt layouts
        :return:
        '''

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.lw_episode)
        self.hbox.addWidget(self.lw_shot)

        self.hbox_label = QtGui.QHBoxLayout()
        # self.hbox_label.addStretch(1)
        self.hbox_label.addWidget(QtGui.QLabel('Episode'))
        self.hbox_label.addWidget(QtGui.QLabel('Shot'))

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(QtGui.QLabel(''))
        self.vbox.addLayout(self.hbox_label)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.lw_fileList)
        self.vbox.addWidget(self.pb_save)

        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)

    def confirm_dialog(self,msg,button_type=0):
        '''
        Qmessagebox widget function to raise user error and prompts
        :param msg:
        :param button_type:
        :return:
        '''

        self.msg_box = QtGui.QMessageBox()
        self.msg_box.setText(msg)
        if button_type == 1:
            self.msg_box.addButton("Version Up", QtGui.QMessageBox.ActionRole)
        self.msg_box.addButton(QtGui.QMessageBox.Cancel)
        ret = self.msg_box.exec_()
        return ret

    def setup_connection(self):
        '''
        setup qt connections between controls and functions
        :return:
        '''
        self.lw_episode.clicked.connect(lambda: self.load_item('shot'))

        self.lw_shot.clicked.connect(lambda: self.get_file_list())

        self.pb_save.clicked.connect(lambda: self.save_file())


    def load_item(self, ui_type):
        '''
        Function to populated given uiType with appropriate data.
        :param ui_type:
        :return:
        '''

        dir_path = ROOT_PATH
        if ui_type == 'epi':
            dir_path = ROOT_PATH
            list_wgt = self.lw_episode
        elif ui_type == 'shot':
            dir_path = '{0}/{1}'.format(ROOT_PATH, self.lw_episode.currentIndex().data())
            list_wgt = self.lw_shot
        
        self.setup_model_view(dir_path, list_wgt)


    def get_file_list(self):
        '''
        gathers all the files from the shot path and displays in the list view
        :return:
        '''

        self.shot_path = '{0}/{1}/{2}/work/scenes'.format(ROOT_PATH, self.lw_episode.currentIndex().data(),
                                                    self.lw_shot.currentIndex().data())      
        self.setup_model_view(self.shot_path,self.lw_fileList)


    def save_file(self):
        '''
        Sets the Maya projects and save the file as version up also raise error msg if the given file does not follow
        given naming conventions
        :return:
        '''

        ui_episode = self.lw_episode.currentIndex().data()
        ui_shot = self.lw_shot.currentIndex().data()

        shot_obj = mod_shot.SHOT(self.shot_path, episode=ui_episode, shot=ui_shot)
        if not shot_obj.check_current_filename_from_ui():
            msg = 'Shot Name not valid!!\n\n{}\n\nSelect Valid Project From UI!'.format(shot_obj.cur_filename)
            ret = self.confirm_dialog(msg, button_type=0)
            return False

        if shot_obj.check_current_filename():
            print 'Saving file ....'
            msg = 'File will be saved as\n\n{}\n\nDo you want to continue ?'.format(shot_obj.new_shot_name)
            ret = self.confirm_dialog(msg, button_type=1)
            if ret == 0:
                shot_obj.save_version_up()
        else:
            msg = 'Shot Name not valid!!\n\n{}\n\nFix the file name first!'.format(shot_obj.cur_filename)
            ret = self.confirm_dialog(msg, button_type=0)
            return False
        return True



def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    # Create ShotSaver UI object
    win = ShotSaverUI()
    win.show()


if __name__ == '__main__':
    main()
