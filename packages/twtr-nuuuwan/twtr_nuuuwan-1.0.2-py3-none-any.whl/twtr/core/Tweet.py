class Tweet:
    def __init__(self, text: str):
        self.text = text
        self.image_path_list = []

    def add_images(self, image_path_list: list[str]):
        self.image_path_list.extend(image_path_list)
        return self

    def add_image(self, image_path: str):
        self.add_images([image_path])
        return self
