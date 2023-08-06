from ..portfolio_entry import PortfolioEntry


class PaleBlueDot(PortfolioEntry):
    """The original Pale Blue Dot image.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL to the dataset.
        file_name (str): Name of the file.
        hash (str): SHA256 hash of the downloaded file.
        description (str): Description of the dataset.
        citation (str): Citation of the dataset.
        license (str): License of the dataset.
        files (dict): Dictionary of files.
        size (float): Size of the dataset in MB.
        tags (list): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio="test",
            name="PaleBlueDot",
            url="https://solarsystem.nasa.gov/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBaUZoIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--4b5b6d8ce74a6930534a08e4d7dd002f24f1efcb/P36254.jpg",
            file_name="P36254.jpg",
            sha256="c83d5de3361a964370fc392ab213c3cf1a23d046406de377a8ac9cb5fbb087f0",
            description="Pale Blue Dot, credit NASA/JPL-Caltech."
            "Original caption: This narrow-angle color image of the"
            " Earth, dubbed 'Pale Blue Dot', is a part of the first"
            " ever 'portrait' of the solar system taken by Voyager "
            "1. The spacecraft acquired a total of 60 frames for a "
            "mosaic of the solar system from a distance of more "
            "than 4 billion miles from Earth and about 32 degrees "
            "above the ecliptic. From Voyager's great distance "
            "Earth is a mere point of light, less than the size of "
            "a picture element even in the narrow-angle camera. "
            "Earth was a crescent only 0.12 pixel in size. "
            "Coincidentally, Earth lies right in the center of one "
            "of the scattered light rays resulting from taking the "
            "image so close to the sun. This blown-up image of the "
            "Earth was taken through three color filters - violet, "
            "blue and green - and recombined to produce the color "
            "image. The background features in the image are "
            "artifacts resulting from the magnification.",
            citation="NASA/JPL-Caltech",
            license="Public domain",
            files={
                ".": ["P36254.jpg"],
            },
            size=0.4,
            tags=["pale blue dot", "voyager", "nasa", "jpl"],
            is_zip=False,
        )
