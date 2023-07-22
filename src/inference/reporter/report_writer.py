import json
from pathlib import Path

JSON_REPORT_TEMPLATE_PATH = Path(__file__).parent / 'report_template.json'


class ReportWriter:
    def __init__(self):
        self.report = self.load_report_template()

    def load_report_template(self):
        with open(JSON_REPORT_TEMPLATE_PATH) as f:
            res = json.load(f)
            return res

    def update_configuration_setup(self, **kwargs):
        self._update_report('configurations_setup', **kwargs)

    def update_execution_results(self, **kwargs):
        self._update_report('execution_results', **kwargs)

    def update_framework_info(self, **kwargs):
        self._update_report('framework_info', **kwargs)

    def update_cmd_options(self, **kwargs):
        self._update_report('cmd_options', **kwargs)

    def _update_report(self, section, **kwargs):
        for key, value in kwargs.items():
            if key not in self.report[section]:
                raise AssertionError(f'Key {section}.{key} is missing in json report template')
            self.report[section][key] = value

    def write_report(self, target_file_path: Path):
        if target_file_path.exists():
            target_file_path.unlink()
        with open(target_file_path, 'w', encoding='utf-8') as fp:
            json.dump(self.report, fp, indent=4)
