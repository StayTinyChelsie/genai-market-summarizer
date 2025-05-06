# oecd_fetcher.py (fetches and parses OECD data)
import os
import requests
import pandas as pd
from pandasdmx import Request

# Custom SDMX URLs (pre-validated)
oecd_urls = {
    "gdp": "https://sdmx.oecd.org/public/rest/data/OECD.CFE.EDS,DSD_REG_ECO@DF_GDP,2.0/A..AUS+AU1+AU2+AU3+AU4+AU5+AU6+AU7+AU8+AUT+AT11+AT111+AT112+AT113+AT12+AT121+AT122+AT123+AT124+AT125+AT126+AT127+AT13+AT130+AT21+AT211+AT212+AT213+AT22+AT221+AT222+AT223+AT224+AT225+AT226+AT31+AT311+AT312+AT313+AT314+AT315+AT32+AT321+AT322+AT323+AT33+AT331+AT332+AT333+AT334+AT335+AT34+AT341+AT342..GDP..Q.USD_PPP_PS?startPeriod=2019&dimensionAtObservation=AllDimensions",
    "labor_productivity": "https://sdmx.oecd.org/public/rest/data/OECD.CFE.EDS,DSD_REG_ECO_ROPI@DF_LPR_ROPI,2.0/A..AUS+AU1+AU2+AU3+AU4+AU5+AU6+AU7+AU8+AUT+AT11+AT12+AT13+AT21+AT22+AT31+AT32+AT33+AT34..LAB_PROD...USD_PPP_WR?startPeriod=2018&dimensionAtObservation=AllDimensions",
    "expenditure": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,2.0/A.AUS.......XDC.V..?startPeriod=2019&dimensionAtObservation=AllDimensions"
}

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

for key, url in oecd_urls.items():
    print(f"\n📥 Fetching OECD {key.replace('_', ' ').title()} data...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            xml_path = os.path.join(output_dir, f"oecd_{key}.xml")
            with open(xml_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved raw XML to {xml_path}")

            # Attempt to parse using pandasdmx
            req = Request("OECD")
            try:
                dataset = req.data(resource_id=url).write().to_pandas()
                df = pd.DataFrame(dataset)
                csv_path = os.path.join(output_dir, f"oecd_{key}.csv")
                df.to_csv(csv_path)
                print(f"✅ Parsed and saved CSV to {csv_path}")
            except Exception as parse_error:
                print(f"⚠️ Parsing failed for {key}: {parse_error}")
        else:
            print(f"❌ Failed to fetch {key}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching {key}: {e}")

