import hashlib

import pytest

from careamics_portfolio import PortfolioManager
from careamics_portfolio.portfolio_entry import PortfolioEntry
from careamics_portfolio.utils.pale_blue_dot import PaleBlueDot


class FaultyMD5(PortfolioEntry):
    """Faulty PortfolioEntry.

    A PortfolioEntry with a faulty md5 hash.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL to the dataset.
        file_name (str): Name of the file.
        md5_hash (str): Faulty MD5 hash.
        description (str): Description of the dataset.
        citation (str): Citation of the dataset.
        license (str): License of the dataset.
        files (dict): Dictionary of files.
        size (float): Size of the dataset in MB.
        tags (list): List of tags associated to the dataset.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio="None",
            name="Wikipedia logo",
            url="https://en.wikipedia.org/wiki/Wikipedia_logo#/media/File:Wikipedia-logo-v2.svg",
            file_name="Wikipedia-logo-v2.svg",
            sha256=hashlib.md5(b"I would prefer not to").hexdigest(),
            description="Wikipedia logo",
            citation="Wikipedia",
            license="CC BY-SA 3.0",
            files={
                ".": ["Wikipedia-logo-v2.svg"],
            },
            size=0.4,
            tags=["wikipedia", "logo"],
        )


@pytest.fixture
def faulty_portfolio_entry() -> FaultyMD5:
    """Fixture for a faulty PortfolioEntry.

    Returns
    -------
    FaultyMD5
        A PortfolioEntry with a faulty md5 hash."""
    return FaultyMD5()


@pytest.fixture
def pale_blue_dot() -> PaleBlueDot:
    """Fixture for the PaleBlueDot.

    Returns
    -------
    PaleBlueDot
        The PaleBlueDot picture.
    """
    return PaleBlueDot()


@pytest.fixture
def portfolio() -> PortfolioManager:
    """Fixture for the Portfolio.

    Returns
    -------
    Portfolio
        The Portfolio.
    """
    return PortfolioManager()
