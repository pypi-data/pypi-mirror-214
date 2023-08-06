from careamics_portfolio import PortfolioManager
from careamics_portfolio.utils import get_poochfolio


def test_get_pooch(portfolio: PortfolioManager):
    poochfolio = get_poochfolio()

    # count the number of portfolio entries
    portfolio_dict = portfolio.as_dict()
    count_entries = 0
    for key in portfolio_dict.keys():
        count_entries += len(portfolio_dict[key].list_datasets())

    assert len(poochfolio.registry) == count_entries + 1  # count test dataset
