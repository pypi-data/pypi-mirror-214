import yaml
from pathlib import Path


class DeployConfig:
    def __init__(self, conf_file):
        if not Path(conf_file).exists():
            raise Exception('Config file path [%s] invalid!' % conf_file)

        with open(conf_file) as fp:
            configs = yaml.load(fp, Loader=yaml.FullLoader)
            deploy_conf = configs["FACE"]
            # N positive for the GPU ID, negative numbers are using CPUs
            self.gpu_id = deploy_conf["GPU_ID"]
            self.face_db = deploy_conf["FACE_DB"]
            self.threshold = deploy_conf["THRESHOLD"]
