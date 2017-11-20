
import re
import pymel.core as pm

SHOT_NAME_REGX = r"episode\d{3}_shot\d{3}_v\d+"
"ADadsadsad"
class SHOT():
    def __init__(self, root_path, episode=None, shot=None):
        '''
        Initialize the shot class with base root path for episodes , episode name and shot name
        :param root_path:
        :param episode:
        :param shot:
        '''

        self.shot_path = pm.Path(root_path)
        self.shot_dir = self.shot_path.dirname()
        self.shot_name = None
        self.new_shot_name = None
        self.episode = episode
        self.shot = shot
        self.cur_filename = pm.sceneName().namebase

        self.get_next_version()

    def is_valid_shotname(self, shot_name):
        '''
        Checks a given shot_name if its valid and returns true if the shot_name matches with the given SHOT_NAME_REGX
        :param shot_name:
        :return:
        '''

        regex_obj = re.compile(SHOT_NAME_REGX)
        matches = re.findall(regex_obj, shot_name)
        if matches:
            return True
        else:
            return False

    def get_next_version(self):
        '''
        Scans through the given shot path and returns filename with next version
        :return:
        '''

        all_shot_files = [int(x.namebase.split('_v')[-1]) for x in self.shot_path.listdir() if
                          self.is_valid_shotname(x.namebase)] or [0]
        next_ver = str(max(all_shot_files) + 1).zfill(3)
        self.new_shot_name = '{0}_{1}_v{2}'.format(self.episode, self.shot, next_ver)

        return self.new_shot_name

    def check_current_filename_from_ui(self):
        '''
        checks the current file name against the episode and shot selected from UI
        :return:
        '''

        ui_filename_regx = '{}_{}_v\d+'.format(self.episode,self.shot)
        matches = re.findall(ui_filename_regx, self.cur_filename)
        if matches or  pm.sceneName().namebase == '':
            return True
        else:
            return False

    def check_current_filename(self):
        '''
        Checks the current open filename
        :return:
        '''

        if self.is_valid_shotname(self.cur_filename) or pm.sceneName().namebase == '':
            return True
        return False

    def save_version_up(self):
        '''
        Function to save the file with version up and set the Maya project
        :return:
        '''
        project_path = pm.Path(self.shot_path)
        pm.mel.setProject(project_path)
        pm.system.saveAs('{}/{}'.format(self.shot_path,self.new_shot_name), type='mayaAscii', force=1)
        return True
