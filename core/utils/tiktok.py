from tiktok_uploader.upload import upload_video


class Tiktok:
    @staticmethod
    def upload(video: list[str, str]) -> list:
        """
            Auth by using the cookies.txt file and upload the video on tiktok
            Video item format: [path, description]
            return: list of video ids
        """
        return upload_video(filename=video[0], description=video[1], cookies="cookies.txt")