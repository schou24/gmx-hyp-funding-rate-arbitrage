from flask import Flask, render_template
from get_net_funding_rate import GetNetFundingRate

app = Flask(__name__)

get_net_funding_rate_btc = GetNetFundingRate("BTC", "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
get_net_funding_rate_eth = GetNetFundingRate("ETH", "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336", "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")
get_net_funding_rate_sol = GetNetFundingRate("SOL", "0x09400D9DB990D5ed3f35D7be61DfAEB900Af03C9", "0x2bcC6D6CdBbDC0a4071e48bb3B969b06B3330c07")
get_net_funding_rate_xrp = GetNetFundingRate("XRP", "0x0CCB4fAa6f1F1B30911619f1184082aB4E25813c", "0xc14e065b0067dE91534e032868f5Ac6ecf2c6868")
get_net_funding_rate_link = GetNetFundingRate("LINK", "0x7f1fa204bb700853D36994DA19F830b6Ad18455C", "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4")

@app.route("/")
def funding_rate_window():
    # BTC
    gmx_long_gmx_short_btc = round(get_net_funding_rate_btc.get_gmx_long_gmx_short(), 5)
    gmx_long_hyp_short_btc = round(get_net_funding_rate_btc.get_gmx_long_hyp_short(), 5)
    hyp_long_gmx_short_btc = round(get_net_funding_rate_btc.get_hyp_long_gmx_short(), 5)
    # ETH
    gmx_long_gmx_short_eth = round(get_net_funding_rate_eth.get_gmx_long_gmx_short(), 5)
    gmx_long_hyp_short_eth = round(get_net_funding_rate_eth.get_gmx_long_hyp_short(), 5)
    hyp_long_gmx_short_eth = round(get_net_funding_rate_eth.get_hyp_long_gmx_short(), 5)
    # SOL
    gmx_long_gmx_short_sol = round(get_net_funding_rate_sol.get_gmx_long_gmx_short(), 5)
    gmx_long_hyp_short_sol = round(get_net_funding_rate_sol.get_gmx_long_hyp_short(), 5)
    hyp_long_gmx_short_sol = round(get_net_funding_rate_sol.get_hyp_long_gmx_short(), 5)
    # XRP
    gmx_long_gmx_short_xrp = round(get_net_funding_rate_xrp.get_gmx_long_gmx_short(), 5)
    gmx_long_hyp_short_xrp = round(get_net_funding_rate_xrp.get_gmx_long_hyp_short(), 5)
    hyp_long_gmx_short_xrp = round(get_net_funding_rate_xrp.get_hyp_long_gmx_short(), 5)
    # LINK
    gmx_long_gmx_short_link = round(get_net_funding_rate_link.get_gmx_long_gmx_short(), 5)
    gmx_long_hyp_short_link = round(get_net_funding_rate_link.get_gmx_long_hyp_short(), 5)
    hyp_long_gmx_short_link = round(get_net_funding_rate_link.get_hyp_long_gmx_short(), 5)

    return render_template(
        "apy_table.html", 
        # BTC
        gmx_long_gmx_short_btc=gmx_long_gmx_short_btc,
        gmx_long_hyp_short_btc=gmx_long_hyp_short_btc,
        hyp_long_gmx_short_btc=hyp_long_gmx_short_btc,
        max_btc = max(gmx_long_gmx_short_btc, gmx_long_hyp_short_btc, hyp_long_gmx_short_btc),
        # ETH
        gmx_long_gmx_short_eth=gmx_long_gmx_short_eth,
        gmx_long_hyp_short_eth=gmx_long_hyp_short_eth,
        hyp_long_gmx_short_eth=hyp_long_gmx_short_eth,
        max_eth = max(gmx_long_gmx_short_eth, gmx_long_hyp_short_eth, hyp_long_gmx_short_eth),
        # SOL
        gmx_long_gmx_short_sol=gmx_long_gmx_short_sol,
        gmx_long_hyp_short_sol=gmx_long_hyp_short_sol,
        hyp_long_gmx_short_sol=hyp_long_gmx_short_sol,
        max_sol = max(gmx_long_gmx_short_sol, gmx_long_hyp_short_sol, hyp_long_gmx_short_sol),
        # XRP
        gmx_long_gmx_short_xrp=gmx_long_gmx_short_xrp,
        gmx_long_hyp_short_xrp=gmx_long_hyp_short_xrp,
        hyp_long_gmx_short_xrp=hyp_long_gmx_short_xrp,
        max_xrp = max(gmx_long_gmx_short_xrp, gmx_long_hyp_short_xrp, hyp_long_gmx_short_xrp),
        # LINK
        gmx_long_gmx_short_link=gmx_long_gmx_short_link,
        gmx_long_hyp_short_link=gmx_long_hyp_short_link,
        hyp_long_gmx_short_link=hyp_long_gmx_short_link,
        max_link = max(gmx_long_gmx_short_link, gmx_long_hyp_short_link, hyp_long_gmx_short_link)
    )
    
if __name__ == "__main__":
    app.run()