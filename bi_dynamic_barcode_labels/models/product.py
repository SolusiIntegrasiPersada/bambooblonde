# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

BARCODE_PREFIX = "21"
EAN13_LENGTH = 13
PRODUCT_REF_LENGTH = 5
BARCODE_AMOUNT_PLACES = 5
BARCODE_TEMPLATE = "%s%s%s%s"


class Product(models.Model):
    _inherit = "product.product"

    def barcode_with_qty(self, product_qty):
        _logger.info(f"original product barcode is {self.barcode}")

        if len(str(self.barcode)) == EAN13_LENGTH and self.barcode.startswith(BARCODE_PREFIX):
            reference = str(self.barcode[2:7])
            qty = str(int(product_qty))
            qty_decimal = str(product_qty).split(".")[1]

            barcode_config = self.env.ref(
                'bi_dynamic_barcode_labels.barcode_labels_config_data')
            decimal_places = barcode_config.barcode_decimal_places
            whole_places = BARCODE_AMOUNT_PLACES - decimal_places

            barcode = BARCODE_TEMPLATE % (BARCODE_PREFIX,
                                          reference.zfill(PRODUCT_REF_LENGTH),
                                          qty.zfill(whole_places),
                                          qty_decimal.ljust(decimal_places, '0'))
            checksum = self.env['barcode.nomenclature'].ean_checksum(
                barcode + "0")
            _logger.info(
                f"EAN check calculated as {checksum} for barcode {barcode} ")
            return barcode + str(checksum)
        else:
            _logger.info(
                f"barcode not starts with the provided prefix {BARCODE_PREFIX}")

    def get_barcode_dynamic(self):
        for doc in self:
            barcode_model = self.get_no_model(doc)

            barcode_categ = self.get_no_categ(doc)

            barcode_color = self.get_no_color(doc)
            barcode_size = self.get_no_size(doc)
            barcode_sequence = self.get_no_sequence(doc)

            barcode = f"{barcode_model}{barcode_categ}{barcode_color}{barcode_size}{barcode_sequence}"
            
            doc.barcode = barcode

    def get_no_sequence(self, doc,params):
        search_product_by_barcode = self.env['product.product'].search([('barcode','ilike',str(params))])
        
        barcode_sequence = str(len(search_product_by_barcode) + 1).zfill(4)
        return barcode_sequence


    def get_no_categ(self, doc):
        categ_name = doc.categ_id.name.upper()

        # Dictionary untuk memetakan nama kategori ke nomor kategori
        categ_mapping = {
            "CAPE": "01",
            "JUMPSUIT": "02",
            "KAFTAN": "03",
            "MAXI DRESS": "04",
            "MIDI DRESS": "05",
            "MINI DRESS": "06",
            "MAXI SKIRT": "07",
            "MIDI SKIRT": "08",
            "MINI SKIRT": "09",
            "PAJAMAS": "10",
            "PANTS": "11",
            "PLAYSUIT": "12",
            "SARONG": "13",
            "SHORTS": "14",
            "TOPS": "15",
            "ACCESSORIES": "16",
            "BAG": "17",
            "BELT": "18",
            "HAIR": "19",
            "HAT": "20",
            "JEWELLERY": "21",
            "SUNGLASESS": "22",
            "BEAUTY": "23",
            "BOOB": "24",
            "GIFTWEAR": "25",
            "HOMEWARES": "26",
            "SHOES": "27",
            "SHOP BAGS": "28"
        }

        # Menggunakan get() untuk mengambil nomor kategori atau nilai default "00" jika tidak ada yang cocok
        barcode_categ = categ_mapping.get(categ_name, "00")

        return barcode_categ

    def get_no_model(self, doc):
        model_categ = doc.product_model_categ_id.name.upper()

    # Dictionary untuk memetakan nama model ke nomor model
        model_mapping = {
            "WOMENS WEAR": "9",
            "MENS WEAR": "8",
            "ACCESSORIES": "7",
            "BODY": "6",
            "GIFTWEAR": "5",
            "HOMEWARES": "4",
            "SHOES": "3"
        }

        # Menggunakan get() untuk mengambil nomor model atau nilai default "0" jika tidak ada yang cocok
        barcode_model = model_mapping.get(model_categ, "0")

        return barcode_model
    def get_no_size(self, doc):
        attribute_size = doc.product_template_variant_value_ids.filtered(
            lambda x: x.attribute_id.name.upper() == "SIZE")
        value_size = attribute_size.name.upper() if attribute_size else ""

        # Dictionary untuk memetakan nama model ke nomor model
        size_mapping = {
            "XS": "01",
            "S": "02",
            "M": "03",
            "L": "04",
            "XL": "05",
            "XXL": "06",
            "ALL SIZE": "09",
            "XS/S": "01",
            "S/M": "02",
            "M/L": "03",
            "6": "01",
            "8": "02",
            "10": "03",
            "12": "04",
            "14": "05",
            "24": "01",
            "26": "02",
            "28": "03",
            "30": "04",
            "32": "05",
            "34": "06",
            "35": "07",
            "36": "08",
            "37": "09",
            "38": "01",
            "39": "02",
            "40": "03",
            "41": "04",
            "42": "05",
            "43": "06",
            "44": "07",
            "45": "08",
            "46": "09"
        }

        # Menggunakan get() untuk mengambil nomor model atau nilai default "0" jika tidak ada yang cocok
        barcode_model = size_mapping.get(value_size, "00")

        return barcode_model


    def get_no_color(self, doc):
        attribute_color = doc.product_template_variant_value_ids.filtered(
            lambda x: x.attribute_id.name.upper() == "COLOR")
        value_color = attribute_color.name.upper() if attribute_color else ""
        # Dictionary untuk memetakan nama model ke nomor model
        color_mapping = {
            "BLACK": "0001",
            "WHITE": "0002",
            "OFFWHT": "0003",
            "NATU": "0004",
            "GOLD": "0005",
            "BLUE": "0006",
            "NAVY": "0007",
            "PINK": "0008",
            "BROWN": "0009",
            "RED": "0010",
            "SAGE": "0011",
            "SILVER": "0012",
            "EGGSHEL": "0013",
            "GLACBLU": "0014",
            "CHOCO": "0015",
            "GREEN": "0016",
            "TAN": "0017",
            "LILAC": "0018",
            "DAREMR": "0019",
            "ASSTED": "0020",
            "CREAM": "0021",
            "STLBLU": "0022",
            "NATURAL": "0023",
            "YELLOW": "0024",
            "LATTE": "0025",
            "MUSHROOM": "0026",
            "HANBLK": "0027",
            "PURPLE": "0028",
            "PALMBLK": "0029",
            "MOCHA": "0030",
            "ROSEY": "0031",
            "DICESPOT": "0032",
            "GREY": "0033",
            "IVORY": "0034",
            "SWFLOBR": "0035",
            "DELILA": "0036",
            "DNDLION": "0037",
            "LPRD": "0038",
            "MERLOT": "0039",
            "ORANGE": "0040",
            "TORTOI": "0041",
            "HIBSTEEL": "0042",
            "PERIWKL": "0043",
            "CHAINDC": "0044",
            "MOTLEO": "0045",
            "ROSE": "0046",
            "FLOWER SKETCH": "0047",
            "MIXPRN": "0048",
            "BEIGE": "0049",
            "BOTANICAL": "0050",
            "CMPGNE": "0051",
            "GINORG": "0052",
            "HANDOTS": "0053",
            "MINT": "0054",
            "OLIVE": "0055",
            "ORCHID": "0056",
            "WILDVNS": "0057",
            "AMBER": "0058",
            "LAVIERD": "0059",
            "LILACFL": "0060",
            "MOSAIC": "0061",
            "NVYFREE": "0062",
            "PYTPRN": "0063",
            "SPFLIBL": "0064",
            "TANSTR": "0065",
            "TIFFYFLO": "0066",
            "CAPSCF": "0067",
            "EDELWEISS GREEN": "0068",
            "EMILY": "0069",
            "MIDNIGHT BLUE": "0070",
            "OMEGA": "0071",
            "REDHIBI": "0072",
            "SMOCKED TIEDYE": "0073",
            "ZEBRAPR": "0074",
            "BLUSTR": "0075",
            "CRUE": "0076",
            "DAISYMS": "0077",
            "LILYPRN": "0078",
            "PARADISE": "0079",
            "SKYBLUE": "0080",
            "TIGERO": "0081",
            "WILDFLO": "0082",
            "BEEHIVE": "0083",
            "LATTICE BLUE": "0084",
            "POLGOLD": "0085",
            "SNOW": "0086",
            "EDELBLU": "0087",
            "PETUNIA FLOWER": "0088",
            "SOLEYLW": "0089",
            "SWEETPEA": "0090",
            "ALLIUM": "0091",
            "ASTERA": "0092",
            "ASTERCHO": "0093",
            "AZALEA": "0094",
            "BASILCA": "0095",
            "BROWN TIE DYE": "0096",
            "CHOCLEO": "0097",
            "DAHLIA": "0098",
            "JWLBLU": "0099",
            "KENYA": "0100",
            "KHAKI": "0101",
            "KHAKIKOL": "0102",
            "KLAHRI": "0103",
            "LILY RED": "0104",
            "MIX": "0105",
            "MUSH": "0106",
            "POPYBLU": "0107",
            "REDSTPM": "0108",
            "SNDYSTR": "0109",
            "SWFLONV": "0110",
            "ZINNIA": "0111",
            "AUBREPNK": "0112",
            "BB STRIPE GREEN": "0113",
            "BOLDBLO": "0114",
            "DMSCBR": "0115",
            "DOTTRFD": "0116",
            "IVY": "0117",
            "LIGBRCK": "0118",
            "NVJOWAL": "0119",
            "PARADIS": "0120",
            "POPPY PINK": "0121",
            "TOSCA": "0122",
            "AUBREY": "0123",
            "BWGHM": "0124",
            "CLEOEMR": "0125",
            "DITSY": "0126",
            "DOT BROWN": "0127",
            "EMRSPOT": "0128",
            "FLOW": "0129",
            "GREEN TEA": "0130",
            "GYPLEO": "0131",
            "INSEASO": "0132",
            "LAILANV": "0133",
            "MOSOLIV": "0134",
            "PEONY": "0135",
            "SGRCLEO": "0136",
            "ABLEOCO": "0137",
            "AZTECTR": "0138",
            "BAJA": "0139",
            "COASTAL BLUE": "0140",
            "COASTAL GREEN": "0141",
            "ITADECO": "0142",
            "JADE": "0143",
            "NUDE": "0144",
            "ROSENVY": "0145",
            "RTROBLK": "0146",
            "SPLIFLO": "0147",
            "SPLIMUS": "0148",
            "VCTORIA": "0149",
            "WAKIKI": "0150",
            "WLDCAT": "0151",
            "CHARCOAL": "0152",
            "CRAMEL": "0153",
            "CRLBAY": "0154",
            "DELAROS": "0155",
            "DITSAGE": "0156",
            "FAIRYRD": "0157",
            "FLIRNAVY": "0158",
            "HAYLEY": "0159",
            "OVGBLK": "0160",
            "ROSTRC": "0161",
            "ROYNAVY": "0162",
            "RTROPAS": "0163",
            "SAHARA": "0164",
            "SAPHIRE BLUE": "0165",
            "SISSYCR": "0166",
            "ALBAFLO": "0167",
            "BLOMBLU": "0168",
            "BLOSSM": "0169",
            "BUNGALO": "0170",
            "CLASSIC STRIPE": "0171",
            "DANDBLK": "0172",
            "DITSHR": "0173",
            "DSYBLU": "0174",
            "EDWEMR": "0175",
            "GUAVA": "0176",
            "JASPRN": "0177",
            "KALAHARI": "0178",
            "MARIFLO": "0179",
            "MIATIE": "0180",
            "MIRANDA": "0181",
            "PIN STRIPE TAN": "0182",
            "TAUPPRN": "0183",
            "ZEBRCHO": "0184",
            "AQUA": "0185",
            "BLKHOLY": "0186",
            "CAMEL": "0187",
            "DMSCUS": "0188",
            "DSYRED": "0189",
            "EMIPNK": "0190",
            "EQBRNST": "0191",
            "FLOMUST": "0192",
            "FRESIA": "0193",
            "GEO": "0194",
            "GOASPOT": "0195",
            "HAWASUN": "0196",
            "JADE GREEN": "0197",
            "MACTIK": "0198",
            "MIA FLOWER": "0199",
            "RED DITSY": "0200",
            "SPRINGSAG": "0201",
            "STONE": "0202",
            "SWIRL": "0203",
            "TRBLTAN": "0204",
            "BBYBLU": "0205",
            "GINGCRM": "0206",
            "GINGSAGE": "0207",
            "GRNFLO": "0208",
            "MEADOW": "0209",
            "MIA FLOWER PINK": "0210",
            "MOSGREN": "0211",
            "PRTUNVY": "0212",
            "RAFIA": "0213",
            "RTRONVY": "0214",
            "VINESBLU": "0215",
            "ALSBLU": "0216",
            "BBYPNK": "0217",
            "BLKGLD": "0218",
            "BLUSTP": "0219",
            "EMBROWHT": "0220",
            "HRINBON": "0221",
            "MAPLE": "0222",
            "PATCHWK": "0223",
            "PEACH": "0224",
            "POME": "0225",
            "ROYALBLU": "0226",
            "TNDPRN": "0227",
            "YELOGHM": "0228",
            "YELOWFLO": "0229",
            "BABYROS": "0230",
            "BLACK SATIN": "0231",
            "BLUE FLOWER": "0232",
            "GEO ANIMAL NAVY": "0233",
            "JASMINE": "0234",
            "POLBLUE": "0235",
            "SQULINE": "0236",
            "TEAL": "0237",
            "WHTLIN": "0238",
            "AMBER BLUE": "0239",
            "ASTSAGE": "0240",
            "BLKEDW": "0241",
            "BLULILY": "0242",
            "BURGNDY": "0243",
            "CANYON": "0244",
            "DENIM": "0245",
            "DSTYROS": "0246",
            "DSYPINK": "0247",
            "FREQSTR": "0248",
            "FULL BLOOM": "0249",
            "FUSPNK": "0250",
            "GIBSLEO": "0251",
            "LAVENDR": "0252",
            "LAVIEDY": "0253",
            "NATURAL MARBLE": "0254",
            "POLSAGE": "0255",
            "ROSEBLU": "0256",
            "SARAHRED": "0257",
            "SWFLORED": "0258",
            "TRIBE GREEN": "0259",
            "TWIGY": "0260",
            "BLUSPNK": "0261",
            "COSMIC": "0262",
            "LNWAYBL": "0263",
            "MILLA": "0264",
            "PEARL GREY": "0265",
            "PETUNIA": "0266",
            "PETUNIA BLACK": "0267",
            "PINBW": "0268",
            "ROYAL TIE DYE": "0269",
            "SARAH BLUE": "0270",
            "STONEIND": "0271",
            "BLACK MARBLE": "0272",
            "BLOSSOM": "0273",
            "CLNPRN": "0274",
            "COBALT BLUE": "0275",
            "EQBLKST": "0276",
            "FLOGAR": "0277",
            "FURPRN": "0278",
            "GRDENIA": "0279",
            "GREEN MARBLE": "0280",
            "LAPALMA": "0281",
            "LTSCRM": "0282",
            "TAUPE": "0283",
            "COBALT": "0284",
            "EASTFLO": "0285",
            "GEOSTN": "0286",
            "GREEN STRIPE": "0287",
            "LIGHT GREY": "0288",
            "NAVYGHM": "0289",
            "WOOD": "0290",
            "BLKNATU": "0291",
            "DASHLN": "0292",
            "LGHTPNK": "0293",
            "LIGHTBRW": "0294",
            "LIGHTOR": "0295",
            "MIXPLN": "0296",
            "NAUEMRD": "0297",
            "PNAPLE": "0298",
            "SPOTBLK": "0299",
            "TURQIS": "0300",
            "BALBABY": "0301",
            "BLKWHT": "0302",
            "CHERYSPT": "0303",
            "DRKBLU": "0304",
            "FEMBLK": "0305",
            "FUCHSIA": "0306",
            "HOTPNK": "0307",
            "KALEIDO": "0308",
            "LEOPARD": "0309",
            "LILACDOT": "0310",
            "MALIBU": "0311",
            "OLVGRN": "0312",
            "PALMTRE": "0313",
            "PEACHRO": "0314",
            "PINKRIB": "0315",
            "PINKSTR": "0316",
            "REDNA": "0317",
            "ROSPNK": "0318",
            "SAND": "0319",
            "SARAHGRN": "0320",
            "SLATE": "0321",
            "SWVGREN": "0322",
            "TRIBAL ARROW": "0323",
            "ASTER": "0324",
            "BLUDNM": "0325",
            "BTGREEN": "0326",
            "BUTTER": "0327",
            "DAHLIAW": "0328",
            "DESERT SAGE": "0329",
            "DSTPLM": "0330",
            "FLOGRN": "0331",
            "FLORENC": "0332",
            "GNGHM": "0333",
            "HANRED": "0334",
            "INDIAN": "0335",
            "IVORY SATIN": "0336",
            "KALABLK": "0337",
            "LEOBRWN": "0338",
            "LILYGRN": "0339",
            "LIMCELL": "0340",
            "MILRED": "0341",
            "MULTGRY": "0342",
            "MUST": "0343",
            "NAUBLOG": "0344",
            "NAUBLUS": "0345",
            "NVYSGR": "0346",
            "ROSEBLK": "0347",
            "RUBYRED": "0348",
            "SAILNVY": "0349",
            "SLATE GREY": "0350",
            "STRIPE": "0351",
            "SUMFLOW": "0352",
            "SWFLOMU": "0353",
            "TANBLK": "0354",
            "TOSCANE": "0355",
            "URSINIA": "0356",
            "WTRMLN": "0357",
            "ACDBLU": "0358",
            "AQUA LURIK": "0359",
            "ARLOFLO": "0360",
            "BALI BABY PASTEL": "0361",
            "BLKSTR": "0362",
            "BLUEGHM": "0363",
            "CLAY": "0364",
            "CORAL": "0365",
            "DARK": "0366",
            "DARKRED": "0367",
            "FLOWER": "0368",
            "GRYSTR": "0369",
            "ICYBLUE": "0370",
            "INDIGO": "0371",
            "LIGBLU": "0372",
            "LIGHT": "0373",
            "LIGHT GREEN": "0374",
            "LIME": "0375",
            "MARBLE": "0376",
            "NAUNVY": "0377",
            "OLIVE STRIPE": "0378",
            "ORIBLUS": "0379",
            "PCHROS": "0380",
            "PLMTRE": "0381",
            "RED FLOWER": "0382",
            "ROYALBL": "0383",
            "RTROBRW": "0384",
            "SOFT PINK": "0385",
            "STRIPE NAVY": "0386",
            "STUPA": "0387",
            "TAN STRIPE": "0388",
            "TORTOISE": "0389",
            "VINTAGE": "0390",
            "WHITE STRIPE": "0391",
            "YELROS": "0392",
            "AQUA MARBLE": "0393",
            "BALI BABY NAVY": "0394",
            "BLKHRT": "0395",
            "BLKWSTR": "0396",
            "BRASS": "0397",
            "BROWN WHITE": "0398",
            "CANDYTIE": "0399",
            "DAISYAG": "0400",
            "GALAXY": "0401",
            "GLDBLK": "0402",
            "HEART": "0403",
            "KYLIEGR": "0404",
            "LAUSTR": "0405",
            "LIGPEAC": "0406",
            "LINEN": "0407",
            "MOCCA": "0408",
            "MRSAFLO": "0409",
            "PASYELO": "0410",
            "PRIMROS": "0411",
            "ROSGLD": "0412",
            "SPOTED": "0413",
            "WHTHRT": "0414",
            "ABSTRAC": "0415",
            "ANMLE": "0416",
            "BALTAMB": "0417",
            "BLACK LENS": "0418",
            "BLANCA": "0419",
            "BLIXMS": "0420",
            "BLKGHM": "0421",
            "BLKNAT": "0422",
            "BLKPALM": "0423",
            "BURGDY": "0424",
            "CHAMPAGNE": "0425",
            "CLEAR": "0426",
            "COCOLIME": "0427",
            "DARKTOR": "0428",
            "DSYLILC": "0429",
            "EMBROBLK": "0430",
            "FRENCH": "0431",
            "JADE CREAM": "0432",
            "KAKADU": "0433",
            "LEMON": "0434",
            "LINMCHA": "0435",
            "LINWHITE": "0436",
            "MOCHA CREAM": "0437",
            "MOSOLIVE": "0438",
            "MRYCHR": "0439",
            "NEWBLU": "0440",
            "PEARL&CINN": "0441",
            "REDTORT": "0442",
            "RFD": "0443",
            "ROSEGD": "0444",
            "ROSGOLD": "0445",
            "SNKSK": "0446",
            "STAR": "0447",
            "TILPRN": "0448",
            "TORBLU": "0449",
            "TOSCA WASH": "0450",
            "TRNGLE": "0451",
            "TROPBERI": "0452",
            "WHITE WASH": "0453",
            "XMSBBY": "0454",
            "ZEBRA": "0455",
            "ZEBRABL": "0456",
            "ANDROID": "0457",
            "ANIMAL": "0458",
            "ARIZONA": "0459",
            "ASSORTED": "0460",
            "ASSTED BASIC": "0461",
            "ASSTED COLORFULL": "0462",
            "AST": "0463",
            "BALIGLD": "0464",
            "BATIK": "0465",
            "BBYWHT": "0466",
            "BIRD": "0467",
            "BLKGOLD": "0468",
            "BLONDE": "0469",
            "BLUSH": "0470",
            "BLUTD": "0471",
            "BROWN LENS": "0472",
            "BRWSGR": "0473",
            "BUSYBODY": "0474",
            "CACTUS": "0475",
            "CAKRA 1": "0476",
            "CAKRA 2": "0477",
            "CARAMEL": "0478",
            "CASPER": "0479",
            "CCNUT": "0480",
            "CCTS": "0481",
            "CHECKERD": "0482",
            "CITRUS": "0483",
            "COASTAL TAUPE": "0484",
            "COATAL BLUE": "0485",
            "COCONUT": "0486",
            "COFFEE": "0487",
            "CREAMGHM": "0488",
            "CRMRED": "0489",
            "CRMTAN": "0490",
            "DARBLU": "0491",
            "DARK MARBLE": "0492",
            "DARK TORTOISE": "0493",
            "DARKCHO": "0494",
            "DONUT": "0495",
            "DRKGRY": "0496",
            "DRKTORT": "0497",
            "DRMPRN": "0498",
            "EDELWEISS SAGE": "0499",
            "ETHNIC": "0500",
            "FLMNGO": "0501",
            "FRANGIPANI": "0502",
            "FRIZZ": "0503",
            "GRDN&WHTMUSK": "0504",
            "GREEN LENS": "0505",
            "GRESTR": "0506",
            "GRNSTR": "0507",
            "HAMSLV": "0508",
            "HAPPY": "0509",
            "HAWSUMR": "0510",
            "HIBBLK": "0511",
            "INGDRM": "0512",
            "IRISBLK": "0513",
            "ISLANDZ": "0514",
            "KISS": "0515",
            "LADYART": "0516",
            "LIFEBEACH": "0517",
            "LILACGHM": "0518",
            "LINBLK": "0519",
            "LIPS": "0520",
            "LMNGRAS": "0521",
            "LUXE": "0522",
            "MAGENTA": "0523",
            "MANDBLU": "0524",
            "MAPS": "0525",
            "MAROON": "0526",
            "MNTBLU": "0527",
            "MNTNATU": "0528",
            "MULTI": "0529",
            "MUSTARD": "0530",
            "NATURAL NAVY": "0531",
            "NEWBLACK": "0532",
            "NVYSTR": "0533",
            "ORSTRIPE": "0534",
            "PCHNATU": "0535",
            "PEARS": "0536",
            "PINECLO": "0537",
            "PIZZA": "0538",
            "PLMPNK": "0539",
            "PLMWHT": "0540",
            "PNKOR": "0541",
            "PNPBLK": "0542",
            "POLKA": "0543",
            "PRIWNKL": "0544",
            "PRPBLU": "0545",
            "PRPORG": "0546",
            "PURPLE MARBLE": "0547",
            "REDTOR": "0548",
            "ROSEGLD": "0549",
            "ROUND": "0550",
            "SANDY": "0551",
            "SKYBLU": "0552",
            "SMALLGH": "0553",
            "SMILE": "0554",
            "STRBERY": "0555",
            "STRBLU": "0556",
            "STRGRY": "0557",
            "STRIPE SKETCH": "0558",
            "STRONG": "0559",
            "SUNYLW": "0560",
            "TERACO": "0561",
            "TIGRJG": "0562",
            "TILEBLK": "0563",
            "TILEBLU": "0564",
            "TMRBL": "0565",
            "TRANS": "0566",
            "TREE": "0567",
            "TROPLEAF": "0568",
            "TRPCAL": "0569",
            "TRPGARDEN": "0570",
            "TURQUIS": "0571",
            "TURTLDY": "0572",
            "UNICORN": "0573",
            "VNL&COCOCREAM": "0574",
            "WAVESLV": "0575",
            "WHITE TORTOISE": "0576",
            "WHTLEO": "0577",
            "WHTWSH": "0578",
            "ZEBRCRM": "0579"

        }

        # Menggunakan get() untuk mengambil nomor model atau nilai default "0" jika tidak ada yang cocok
        barcode_color = color_mapping.get(value_color, "0")

        return barcode_color

    def get_barcode_dynamic(self):
        for doc in self:
            barcode_model = self.get_no_model(doc)

            barcode_categ = self.get_no_categ(doc)

            barcode_color = self.get_no_color(doc)
            barcode_size = self.get_no_size(doc)
            params = f"{barcode_model}{barcode_categ}{barcode_color}{barcode_size}"
            barcode_sequence = self.get_no_sequence(doc,params)

            barcode = f"{barcode_model}{barcode_categ}{barcode_color}{barcode_size}{barcode_sequence}"
            
            doc.barcode = barcode
            
    

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_code = fields.Char(compute='_compute_cost_code', string='Cost Code')
    
    @api.model
    def create(self, values):
        result = super(ProductTemplate,self).create(values)
        
        if result.product_variant_ids :
            result.product_variant_ids.get_barcode_dynamic()
        
        return result
    
    
    def write(self, values):
        res = super(ProductTemplate,self).write(values)
        for x in self :
            if values.get("attribute_line_ids", False):
                x.product_variant_ids.filtered(
            lambda x: not x.barcode or x.barcode == False ).get_barcode_dynamic()
        
        return res

    @api.depends('standard_price')
    def _compute_cost_code(self):
        for product in self:
            master_code = {
                "1": "S",
                "2": "T",
                "3": "O",
                "4": "C",
                "5": "K",
                "6": "B",
                "7": "U",
                "8": "Y",
                "9": "E",
                "0": "R"
            }
            code = ''
            if product.standard_price:
                string_cost = str(product.standard_price)
                for i in string_cost[:-5]:
                    code += master_code[i]
                product.cost_code = code
            else:
                product.cost_code = None
