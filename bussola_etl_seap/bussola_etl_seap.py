"""Classes that model SEAP bulletins and methods to get info from them"""
# pylint: disable=redefined-outer-name,singleton-comparison

import log


class SEAPBulletinV1():

    def __init__(self, input_path: str, output_path: str):
        # import file
        self.input_path = input_path
        self.output_path = output_path
        self.bulletin = self.import_bulletin()

    def import_bulletin(self):
        # TO-DO: implement import function
        log.info(f"Importing data from path: {self.input_path}")
        raise NotImplementedError
