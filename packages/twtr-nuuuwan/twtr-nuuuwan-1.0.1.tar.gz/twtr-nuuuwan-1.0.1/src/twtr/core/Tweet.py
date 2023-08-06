class Tweet:
    def __init__(self, text: str):
        self.text = text
        self.image_path_list = []

    def add_image(self, image_path: str):
        self.image_path_list.append(image_path)
        return self
