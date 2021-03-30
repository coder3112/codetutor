import json
from typing import List


class VideoJSONParser:

    """
    Class to do custom parsing of videos of format:
    {
        "1": {
            "name": "",
            "videos": [
                {"id" : {
                    "name": name,
                    "link": link
                    "description": description
                    }
                }
             ]
        }
    }

    """

    def __init__(self, video_json) -> None:
        print(video_json)
        self.json = json.loads(video_json)

    def __str__(self) -> str:
        return f"{self.dump()}"

    def __call__(self):
        return self.dump()

    def dump(self):
        # print(self.json)
        # return json.dumps(self.json)
        return self.json

    def add_video(self, section: int, name: str, link: str, description: str) -> str:
        """
        :param section:
            Id of section in which video will be added.
        :param name:
            Name of video to be added.
        :param link:
            Link of video to be added.
        """
        # if not str(section) in self.json:
        #     self.add_section(f"Section {section}")
        if str(section) not in self.json:
            self.add_section(f"Section {section}")
        video_id = len(self.json[str(section)]["videos"])
        print(video_id)
        self.json[str(section)]["videos"].append(
            {f"{video_id}": {"name": name, "link": link, "description": description}}
        )

        return self()

    def add_section(self, section_name: str) -> str:
        """
        :param section_name:
            Name of section to be added
        Section Id is automatically calculated
        """
        new_section_id: int = len(self.json.keys()) + 1
        self.json[f"{new_section_id}"] = {"name": section_name, "videos": []}
        return self()

    def remove_video(self, section: int, video: int) -> str:
        """
        :param section:
            Id of section from which video is to be retreived
        :param video:
            Id of video to be deleted.
        """
        videos: List = self.json[str(section)]["videos"]
        for i, video_id in enumerate(videos):
            if video_id[0] == video:
                del videos[i]
                break
        return self()

    def remove_section(self, section_id: int) -> str:
        """
        :param section_id:
            Id of section to be deleted
        """
        del self.json[f"{section_id}"]
        return self()
