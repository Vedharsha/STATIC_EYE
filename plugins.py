import importlib
import os

class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]  # Remove .py extension
                module = importlib.import_module(f'{self.plugin_dir}.{module_name}')
                if hasattr(module, 'run_analysis'):
                    self.plugins.append(module)

    def run_plugins(self, apk_file):
        results = {}
        for plugin in self.plugins:
            plugin_name = plugin.__name__.split('.')[-1]
            results[plugin_name] = plugin.run_analysis(apk_file)
        return results

# Example plugin (save this in a separate file in the 'plugins' directory):

