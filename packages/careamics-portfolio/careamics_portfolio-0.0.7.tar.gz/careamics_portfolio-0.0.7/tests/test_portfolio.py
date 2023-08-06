import pytest

from careamics_portfolio import PortfolioManager
from careamics_portfolio.portfolio import IterablePortfolio


def list_iterable_portfolios():
    """List all iterable portfolios."""
    portfolio = PortfolioManager()

    list_iter_portfolios = []
    for attribute in vars(portfolio).values():
        if isinstance(attribute, IterablePortfolio):
            list_iter_portfolios.append(attribute)

    return list_iter_portfolios


ITERABLES = list_iterable_portfolios()


@pytest.mark.parametrize("iter_portfolio", ITERABLES)
def test_iterable_portfolios(iter_portfolio: IterablePortfolio):
    """Test that portfolios are iterable.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio to test.
    """
    entries = [entry.name for entry in iter_portfolio]
    assert entries == iter_portfolio.list_datasets()


@pytest.mark.parametrize("iter_portfolio", ITERABLES)
def test_iterable_portfolio_list_datasets(iter_portfolio: IterablePortfolio):
    """Test that the list_datasets method works on portfolios.

    Note: the list_datasets

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio to test.
    """
    datasets = (
        iter_portfolio.list_datasets()
    )  # names of entries, rather than attributes
    assert len(datasets) > 0

    for entry in datasets:
        assert entry in iter_portfolio.as_dict().keys()


@pytest.mark.parametrize("iter_portfolio", ITERABLES)
def test_iterable_portfolio_as_dict(iter_portfolio: IterablePortfolio):
    # denoiseg
    iter_as_dict = iter_portfolio.as_dict()
    assert len(iter_as_dict) > 0

    # check entries
    for entry in iter_as_dict.values():
        assert "URL" in entry
        assert "Citation" in entry
        assert "Description" in entry
        assert "License" in entry
        assert "File size" in entry


def test_portfolio_as_dict(portfolio: PortfolioManager):
    """Test that the as_dict method works on portfolios.

    Parameters:
    -----------
    portfolio : Portfolio
        Portfolio to test.
    """
    portfolio_dict = portfolio.as_dict()
    assert len(portfolio_dict) > 0
    assert len(portfolio_dict) == len(ITERABLES)


def test_export_to_json(tmp_path, portfolio: PortfolioManager):
    """Test that the export Portfolio to json works.

    Parameters
    ----------
    tmp_path : Path
        Temporary path.
    portfolio : Portfolio
        Portfolio to test.
    """
    import json

    # export to json
    path_to_file = tmp_path / "portfolio.json"
    portfolio.to_json(path_to_file)

    # check that the file exists
    assert path_to_file.exists()

    # load json file
    with open(path_to_file) as f:
        data = json.load(f)

        for entry in ITERABLES:
            assert entry.name in data
            assert data[entry.name] == entry.as_dict()


def test_export_to_registry(tmp_path, portfolio: PortfolioManager):
    """Test that the export Portfolio to registry works.

    Parameters
    ----------
    tmp_path : Path
        Temporary path.
    portfolio : Portfolio
        Portfolio to test.
    """
    # export to registry
    path_to_file = tmp_path / "registry.txt"
    portfolio.to_registry(path_to_file)

    # check that the file exists
    assert path_to_file.exists()

    # portfolio as dict
    portfolio_dict = portfolio.as_dict()

    # count the number of entries
    count_entries = 1  # count test dataset
    for key in portfolio_dict.keys():
        count_entries += len(portfolio_dict[key].list_datasets())

    # load registry file
    with open(path_to_file) as f:
        # read lines
        lines = f.readlines()

        # remove comments and empty lines
        lines = [
            line
            for line in lines
            if not line.startswith("#") and not line.startswith("\n")
        ]
        assert len(lines) == count_entries

        # iterate over lines
        for line in lines:
            # split line and name
            name, _, _ = line.strip().split(" ")
            portfolio_name, entry_name = name.split("-")

            if portfolio_name != "test":
                # check that the portfolio exists
                assert portfolio_name in portfolio_dict

                # check that the entry exists
                assert entry_name in portfolio_dict[portfolio_name].list_datasets()
