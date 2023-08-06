""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-27 12:26:11
Project:	 vscode-icons
Description: Provide function to use the vscode icons.
"""

import os
import json

class VSCodeIcons():
    def __init__(self) -> None:
        # DEFINING NAMES
        module_name = 'vscode_icons'
        icon_dir = 'icons'
        info_file_name = 'vsicons-icon-theme.json'
        
        # GETTING STATIC ROOT
        try:
            from django.conf import settings
            static_root = os.path.join(settings.STATIC_ROOT, module_name)
        except:
            static_root = os.path.join(os.path.dirname(__file__), 'static', module_name)
        if not os.path.exists(static_root):
            static_root = os.path.join(os.path.dirname(__file__), 'static', module_name)
        
        # GETTING ICON DIR PATH
        self.icon_root = os.path.join(module_name, icon_dir)
        
        # READING INFO
        try:
            with open(os.path.join(static_root, info_file_name), 'rb') as f:
                self.info = json.load(f)
        except:
            self.info = None
        return None
    
    def findDirectoryIcon(self, name):
        """Finding best possible icon for directory."""
        # FINDING ICON
        icon_name = self.info['folderNames'].get(name)
        if icon_name is None: # Default condition
            icon_name = '_folder'
        
        # FINDING ICON PATH
        icon_path = self.info['iconDefinitions'][icon_name]
        icon_name = os.path.basename(icon_path['iconPath'])
        
        # FINDING STATIC PATH
        static_path = os.path.join(self.icon_root, icon_name)
        return static_path
        
    def findFileIcon(self, name):
        """Finding best possible icon for file."""
        # FINDING ICON
        icon_name = self.info['fileNames'].get(name)
        if icon_name is None:
            # GETTING ON THE BASE OF EXT
            ext = os.path.splitext(name)[-1][1:]
            icon_name = self.info['fileExtensions'].get(ext)
            if icon_name is None:
                icon_name = '_file' # Default Condition
        
        # FINDING ICON PATH
        icon_path = self.info['iconDefinitions'][icon_name]
        icon_name = os.path.basename(icon_path['iconPath'])
        
        # FINDING STATIC PATH
        static_path = os.path.join(self.icon_root, icon_name)
        return static_path