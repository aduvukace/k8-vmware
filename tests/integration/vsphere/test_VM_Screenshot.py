from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import file_exists, temp_file
from osbot_utils.utils.Misc import random_string

from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.Datastore_File import Datastore_File
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot


class test_Screeshot(TestCase_VM):

    vm_name = f"tests__unit__vsphere__Screeshot_{random_string()}"

    def setUp(self) -> None:
        self.screenshot = VM_Screenshot(self.vm)
        self.vm.task().power_on()
        print()

    def test_download(self):
        path_screenshot_1 = self.screenshot.download()
        assert file_exists(path_screenshot_1)

        # download to specific location
        target_file       = temp_file(extension='.png')
        #target_file       = '/tmp/vm_screenshot_2.png'
        #self.screenshot.vm.wait(2)
        path_screenshot_2 = VM_Screenshot(self.vm, target_file).download()
        assert file_exists(path_screenshot_2)



    def test_save_screnshot_to_datastore(self):
        path_screenshot = self.screenshot.save_screnshot_to_datastore()
        datastore_file  = Datastore_File().set_file_from_path_datastore(path_screenshot)

        assert datastore_file.datastore.name == datastore_file.datastore.name
        assert datastore_file.ds_folder      == self.vm.name()
        assert datastore_file.ds_file        == self.vm.name() + "-1.png"

        assert self.screenshot.ds_screenshot == path_screenshot           # confirm save_screnshot_to_datastore saves the path of the downloaded file to the ds_screenshot variable