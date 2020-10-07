"""Classes that model SEAP bulletins and methods to get info from them"""
# pylint: disable=redefined-outer-name,singleton-comparison

import log


class SEAPBulletinV1():

    def __init__(self, input_path: str, output_path: str):
        # import file
        self.bulletin = self.import_bulletin(input_path)

    def import_bulletin(self):
        # TO-DO: implement import function
        log.info(f"Importing data from path: {self.input_path}")
        raise NotImplementedError
