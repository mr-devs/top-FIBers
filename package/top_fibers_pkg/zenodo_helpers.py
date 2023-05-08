"""
Code for working with the Zenodo API.

Author: Matthew DeVerna
"""
import glob
import os
import requests


class ZenodoAPI:
    def __init__(
        self,
        access_token,
        record_id,
        base_url="https://zenodo.org/api/deposit/depositions",
        matching_str="fib_indices",
    ):
        """
        Initialize the ZenodoAPI object.
        """
        self.access_token = access_token
        self.base_url = base_url
        self.record_id = record_id
        self.matching_str = matching_str
        self.zenodo_info = None
        self.deposition_id = None
        self.bucket_link = None
        self.top_fib_info = None
        self.new_version_url = None
        self.existing_files = []

        print("Initializing Zenodo API class...")
        try:
            print(
                f"\tGetting top FIBers information based on this record: {self.record_id}..."
            )
            r = requests.get(
                f"{self.base_url}/{self.record_id}",
                params={"access_token": self.access_token},
            )
            self.top_fib_info = r.json()
        except Exception as e:
            raise Exception(f"\tProblem getting OSoMe Zenodo information\n{e}")

        try:
            print("\tGetting top FIBers bucket link...")
            self.bucket_link = self.top_fib_info["links"]["bucket"]
            print("Bucket link:", self.bucket_link)
        except Exception as e:
            raise Exception(
                f"\tProblem finding bucket link for top FIBer repository\n", e
            )

        try:
            print("\tGetting existing FIB files...")
            for file_info in self.top_fib_info["files"]:
                fname = file_info["filename"]
                if self.matching_str in fname:
                    self.existing_files.append(fname)
        except Exception as e:
            raise Exception(f"\tProblem finding existing FIB files\n", e)

        print("Zenodo API class initialized successfully!")

    def get_files_to_upload(self, zenodo_dir, file_suffix="*.csv"):
        """
        Get all data files listed in the zenodo_dir and exclude the ones that have already been uploaded.

        Parameters:
        -----------
        - zenodo_dir (str): the directory to search for files
        - file_suffix (str): the suffix of the files in `zenodo_dir`

        Returns:
        ----------
        - files_to_upload (list): a list of FIB files that have not been uploaded to the Zenodo repository
        """
        try:
            print("Building list of files to upload...")
            files_to_upload = []
            data_files = glob.glob(os.path.join(zenodo_dir, file_suffix))
            for file in data_files:
                if os.path.basename(file) not in self.existing_files:
                    files_to_upload.append(file)
            return files_to_upload
        except Exception as e:
            raise Exception(f"Problem creating list of files to upload\n", e)

    def create_new_version(self):
        """
        Create a new version of the deposition.
        """
        # Create a new version of the deposition
        r = requests.post(
            f"{self.base_url}/{self.record_id}/actions/newversion",
            params={"access_token": self.access_token},
            json={},
            headers={"Content-Type": "application/json"},
        )
        if r.status_code != requests.codes.created:
            r.raise_for_status()
        print("Successfully created new version!")
        print(r.json()["links"])
        self.new_version_url = r.json()["links"]["latest_draft"]

    def _upload_file_to_zenodo(self, file_path):
        """
        Upload `file_path` to Zenodo repository `repo_id`.

        Parameters:
        -----------
        - file_path (str): the file to upload

        Returns:
        ----------
        - None
        """
        print("Uploading file:", file_path)
        params = {"access_token": self.access_token}
        filename = os.path.basename(file_path)
        upload_link = f"{self.bucket_link}/{filename}"
        with open(file_path, "rb") as fp:
            r = requests.put(
                upload_link,
                data=fp,
                params=params,
                headers={"Content-Type": "application/octet-stream"},
            )
        if r.status_code != requests.codes.created:
            r.raise_for_status()
        print("Successfully uploaded file!")

    def upload_all_files(self, files_to_upload):
        """
        Upload all files in `files_to_upload`.

        Parameters:
        -----------
        - files_to_upload (list): a list of files to upload

        Returns:
        ----------
        - None
        """
        for file in files_to_upload:
            self._upload_file_to_zenodo(file)
        print("\tSuccessfully uploaded all files!")

    def publish_changes(self):
        """
        Publish changes to Zenodo repository.

        Parameters:
        -----------
        - None

        Returns:
        ----------
        - None
        """
        try:
            print("Trying to publish changes...")
            r = requests.post(
                f"{self.new_version_url}/actions/publish",
                params={"access_token": self.access_token},
            )
        except Exception as e:
            print("Status Code:", r.status_code)
            print("Reason     :", r.reason)
            raise Exception(f"Problem publishing changes\n{e}")
        if r.status_code == 202:
            print("Successfully published changes!")
        else:
            print("Failed to publish changes!")
            print(f"Status code: {r.status_code}")
            print(f"Reason: {r.reason}")
            print(f"Reason: {r.raise_for_status()}")
