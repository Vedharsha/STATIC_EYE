import requests
import subprocess
import os

class ToolUpdater:
    def __init__(self):
        self.tools = {
            'jadx': {
                'current_version': self._get_current_version('jadx'),
                'latest_version_url': 'https://api.github.com/repos/skylot/jadx/releases/latest',
                'download_url': 'https://github.com/skylot/jadx/releases/download/v{}/jadx-{}.zip'
            },
            'apktool': {
                'current_version': self._get_current_version('apktool'),
                'latest_version_url': 'https://api.github.com/repos/iBotPeaches/Apktool/releases/latest',
                'download_url': 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_{}.jar'
            }
        }

    def _get_current_version(self, tool):
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return None

    def check_and_update(self):
        for tool, info in self.tools.items():
            latest_version = self._get_latest_version(info['latest_version_url'])
            if latest_version != info['current_version']:
                self._update_tool(tool, latest_version)

    def _get_latest_version(self, url):
        response = requests.get(url)
        return response.json()['tag_name'].lstrip('v')

    def _update_tool(self, tool, version):
        url = self.tools[tool]['download_url'].format(version, version)
        filename = url.split('/')[-1]
        
        subprocess.run(['wget', url])
        
        if tool == 'jadx':
            subprocess.run(['unzip', filename, '-d', '/usr/local/bin'])
        elif tool == 'apktool':
            subprocess.run(['mv', filename, '/usr/local/bin/apktool.jar'])
            with open('/usr/local/bin/apktool', 'w') as f:
                f.write('#!/bin/bash\njava -jar /usr/local/bin/apktool.jar "$@"')
            subprocess.run(['chmod', '+x', '/usr/local/bin/apktool'])

        print(f'{tool} updated to version {version}')
