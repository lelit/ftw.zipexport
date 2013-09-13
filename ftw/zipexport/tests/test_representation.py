from ftw.builder import Builder, create
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from ftw.zipexport.interfaces import IZipRepresentation
from unittest2 import TestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter


class TestArchetypeZipRepresentation(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = portal.REQUEST

        self.folder = create(Builder("folder")
                            .titled("Folder 1"))

        self.folderfile = create(Builder("file")
                            .titled("File")
                            .attach_file_containing("Testdata file in folder",
                                                     "test.txt")
                            .within(self.folder))

        subfolder = create(Builder("folder")
                            .titled("SubFolder")
                            .within(self.folder))

        self.subfolderfile = create(Builder("file")
                                    .titled("SubFolderFile")
                                    .attach_file_containing("Testdata file in subfolder",
                                                             "subtest.txt")
                                    .within(subfolder))

    def test_folder_representation_non_recursive_is_empty(self):
        self.assertEquals([], list(getMultiAdapter((self.folder, self.request),
                                             interface=IZipRepresentation)
                                             .get_files(recursive=False)))

    def test_folder_contains_files_in_recursive(self):
        ziprepresentation = getMultiAdapter((self.folder, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files(recursive=True))
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([("/test.txt", "Testdata file in folder"),
                            ("/SubFolder/subtest.txt", "Testdata file in subfolder")],
                            files_converted)

    def test_file_represents_itself(self):
        ziprepresentation = getMultiAdapter((self.folderfile, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([("/test.txt", "Testdata file in folder")],
                            files_converted)