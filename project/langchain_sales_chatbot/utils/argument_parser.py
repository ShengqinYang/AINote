import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='这是一个智能AI销售小助手，专为您提供快速、准确和个性化的咨询和支持。当前支持：Apple-AI销售小助手、房地产-AI销售小助手。如有任何问题，请随时向我提问！.')
        self.parser.add_argument('--config_file', type=str, default='role_config.yaml',
                                 help='Configuration file with model and API settings.')
        self.parser.add_argument('--title', type=str, default='Apple-AI销售小助手', help='设置智能AI销售小助手角色')
        self.parser.add_argument('--enable_chat', type=str, default=True, help='是否开启chat智能聊天')

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args
