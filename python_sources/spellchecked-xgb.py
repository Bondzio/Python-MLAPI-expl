import warnings; warnings.filterwarnings("ignore");
import time
start_time = time.time()

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
#from sklearn import pipeline, model_selection
from sklearn import pipeline, grid_search
#from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import TruncatedSVD
#from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error, make_scorer
#from nltk.metrics import edit_distance
from nltk.stem.porter import *
stemmer = PorterStemmer()
#from nltk.stem.snowball import SnowballStemmer #0.003 improvement but takes twice as long as PorterStemmer
#stemmer = SnowballStemmer('english')
import re
#import enchant
import random
random.seed(2016)

df_train = pd.read_csv('../input/train.csv', encoding="ISO-8859-1")[:1000] #update here
df_test = pd.read_csv('../input/test.csv', encoding="ISO-8859-1")[:1000] #update here
df_pro_desc = pd.read_csv('../input/product_descriptions.csv')[:1000] #update here
df_attr = pd.read_csv('../input/attributes.csv')
df_brand = df_attr[df_attr.name == "MFG Brand Name"][["product_uid", "value"]].rename(columns={"value": "brand"})
num_train = df_train.shape[0]
df_all = pd.concat((df_train, df_test), axis=0, ignore_index=True)
df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')
df_all = pd.merge(df_all, df_brand, how='left', on='product_uid')
print("--- Files Loaded: %s minutes ---" % round(((time.time() - start_time)/60),2))

stop_w = ['for', 'xbi', 'and', 'in', 'th','on','sku','with','what','from','that','less','er','ing'] #'electr','paint','pipe','light','kitchen','wood','outdoor','door','bathroom'
strNum = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}

def str_stem(s): 
    if isinstance(s, str):
        s = re.sub(r"(\w)\.([A-Z])", r"\1 \2", s) #Split words with a.A
        s = s.lower()
        s = s.replace("  "," ")
        s = s.replace(",","") #could be number / segment later
        s = s.replace("$"," ")
        s = s.replace("?"," ")
        s = s.replace("-"," ")
        s = s.replace("//","/")
        s = s.replace("..",".")
        s = s.replace(" / "," ")
        s = s.replace(" \\ "," ")
        s = s.replace("."," . ")
        s = re.sub(r"(^\.|/)", r"", s)
        s = re.sub(r"(\.|/)$", r"", s)
        s = re.sub(r"([0-9])([a-z])", r"\1 \2", s)
        s = re.sub(r"([a-z])([0-9])", r"\1 \2", s)
        s = s.replace(" x "," xbi ")
        s = re.sub(r"([a-z])( *)\.( *)([a-z])", r"\1 \4", s)
        s = re.sub(r"([a-z])( *)/( *)([a-z])", r"\1 \4", s)
        s = s.replace("*"," xbi ")
        s = s.replace(" by "," xbi ")
        s = re.sub(r"([0-9])( *)\.( *)([0-9])", r"\1.\4", s)
        s = re.sub(r"([0-9]+)( *)(inches|inch|in|')\.?", r"\1in. ", s)
        s = re.sub(r"([0-9]+)( *)(foot|feet|ft|'')\.?", r"\1ft. ", s)
        s = re.sub(r"([0-9]+)( *)(pounds|pound|lbs|lb)\.?", r"\1lb. ", s)
        s = re.sub(r"([0-9]+)( *)(square|sq) ?\.?(feet|foot|ft)\.?", r"\1sq.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(cubic|cu) ?\.?(feet|foot|ft)\.?", r"\1cu.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1gal. ", s)
        s = re.sub(r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1oz. ", s)
        s = re.sub(r"([0-9]+)( *)(centimeters|cm)\.?", r"\1cm. ", s)
        s = re.sub(r"([0-9]+)( *)(milimeters|mm)\.?", r"\1mm. ", s)
        s = s.replace("�"," degrees ")
        s = re.sub(r"([0-9]+)( *)(degrees|degree)\.?", r"\1deg. ", s)
        s = s.replace(" v "," volts ")
        s = re.sub(r"([0-9]+)( *)(volts|volt)\.?", r"\1volt. ", s)
        s = re.sub(r"([0-9]+)( *)(watts|watt)\.?", r"\1watt. ", s)
        s = re.sub(r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1amp. ", s)
        s = s.replace("  "," ")
        s = s.replace(" . "," ")
        #s = (" ").join([z for z in s.split(" ") if z not in stop_w])
        s = (" ").join([str(strNum[z]) if z in strNum else z for z in s.split(" ")])
        s = (" ").join([stemmer.stem(z) for z in s.split(" ")])
        
        s = s.lower()
        s = s.replace("toliet","toilet")
        s = s.replace("airconditioner","air conditioner")
        s = s.replace("vinal","vinyl")
        s = s.replace("vynal","vinyl")
        s = s.replace("skill","skil")
        s = s.replace("snowbl","snow bl")
        s = s.replace("plexigla","plexi gla")
        s = s.replace("rustoleum","rust-oleum")
        s = s.replace("whirpool","whirlpool")
        s = s.replace("whirlpoolga", "whirlpool ga")
        s = s.replace("whirlpoolstainless","whirlpool stainless")
        
        s = s.replace("steele stake","steel stake")
        s = s.replace("gas mowe","gas mower")
        s = s.replace("metal plate cover gcfi","metal plate cover gfci")
        s = s.replace("lawn sprkinler","lawn sprinkler")
        s = s.replace("ourdoor patio tile","outdoor patio tile")
        s = s.replace("6 teir shelving","6 tier shelving")
        s = s.replace("storage shelve","storage shelf")
        s = s.replace("American Standard Bone round toliet","American Standard Bone round toilet")
        s = s.replace("6 stell","6 steel")
        s = s.replace("fece posts metal","fence posts metal")
        s = s.replace("cushions outdoorlounge","cushions outdoor lounge")
        s = s.replace("pricepfister kitchen faucet g135","price pfister kitchen faucet g135")
        s = s.replace("glaciar bay toiled","glacier bay toilet")
        s = s.replace("glacie bay dual flush","glacier bay dual flush")
        s = s.replace("glacier bay tiolet tank lid","glacier bay toilet tank lid")
        s = s.replace("handycap toilets","handicap toilets")
        s = s.replace("high boy tolet","highboy toilet")
        s = s.replace("gas wayer heaters","gas water heaters")
        s = s.replace("basemetnt window","basement window")
        s = s.replace("rustollum epoxy","rustoleum epoxy")
        s = s.replace("air /heaterconditioner window","air /heat conditioner window")
        s = s.replace("spliter ac unit","splitter ac unit")
        s = s.replace("berh deck over","behr deck over")
        s = s.replace("28 snow thower","28 snow thrower")
        s = s.replace("base board molding boundle","baseboard molding bundle")
        s = s.replace("1 infloor flange","1 in floor flange")
        s = s.replace("10 window sping rod","10 window spring rod")
        s = s.replace("combo powertool kit","combo power tool kit")
        s = s.replace("desalt impact 18","dewalt impact 18")
        s = s.replace("rigid lithium ion batteries fuego drill","ridgid lithium ion batteries fuego drill")
        s = s.replace("fiberglass repir kit","fiberglass repair kit")
        s = s.replace("portable air condtioners","portable air conditioners")
        s = s.replace("wall pannels","wall panels")
        s = s.replace("2X4 SRUDS","2X4 STUDS")
        s = s.replace("frostking window shrink film","frost king window shrink film")
        s = s.replace("Florescent Light Bulbs","Fluorescent Light Bulbs")
        s = s.replace("violet flourescent light","violet fluorescent light")
        s = s.replace("lawn mower- electic","lawn mower- electric")
        s = s.replace("closetmade","closetmaid")
        s = s.replace("greecianmarble floor tile","grecian marble floor tile")
        s = s.replace("join compound wall tile","joint compound wall tile")
        s = s.replace("montagnia contina floor tile","montagna cortina floor tile")
        s = s.replace("porcelin floor tile 6x24","porcelain floor tile 6x24")
        s = s.replace("three wayy","three way")
        s = s.replace("incide wall heater","inside wall heater")
        s = s.replace("westminster pedistal combo","westminster pedestal combo")
        s = s.replace("water softners","water softeners")
        s = s.replace("miricale","miracle")
        s = s.replace("sliding windos locks","sliding window locks")
        s = s.replace("20v dewalt kombo","20v dewalt combo")
        s = s.replace("DEWALT VACCUM","DEWALT VACUUM")
        s = s.replace("lithium 20 dewalt","lithium 20v dewalt")
        s = s.replace("water heather","water heater")
        s = s.replace("riobi blower vac 9056","ryobi blower vac 9056")
        s = s.replace("DRAWEER PULLS","DRAWER PULLS")
        s = s.replace("bagged cinder mulch","bagged cedar mulch")
        s = s.replace("hindges","hinges")
        s = s.replace("chair rail hieght","chair rail height")
        s = s.replace("celling light","ceiling light")
        s = s.replace("tub repair kit procelian","tub repair kit porcelain")
        s = s.replace("dewalr tools","dewalt tools")
        s = s.replace("zinc plated flatbraces","zinc plated flat braces")
        s = s.replace("cieling","ceiling")
        s = s.replace("control celing fan","control ceiling fan")
        s = s.replace("roll roofing lap cemet","roll roofing lap cement")
        s = s.replace("cedart board","cedar board")
        s = s.replace("lg stcking kit","lg stacking kit")
        s = s.replace("ajustable ladder feet","adjustable ladder feet")
        s = s.replace("milwakee M12","milwaukee M12")
        s = s.replace("garden sprayer non pump","garden sprayer no pump")
        s = s.replace("roof rdge flashing","roof edge flashing")
        s = s.replace("cable prime line emergensy open","cable prime line emergency open")
        s = s.replace("roybi l18v","ryobi l18v")
        s = s.replace("milwaukee 18-volt lithium-ion cordlessrotary hammerss","milwaukee 18-volt lithium-ion cordless rotary hammers")
        s = s.replace("bath sinnk","bath sink")
        s = s.replace("bathro sinks","bathroom sinks")
        s = s.replace("bathroom  pedelal sink","bathroom pedestal sink")
        s = s.replace("epoxy concrete pain","epoxy concrete paint")
        s = s.replace("pool suppll","pool supply")
        s = s.replace("3-3 galvinized tubing","3-3 galvanized tubing")
        s = s.replace("portable air conditionar and heater","portable air conditioner and heater")
        s = s.replace("vynal windows","vinyl windows")
        s = s.replace("aluminun tread plate","aluminum tread plate")
        s = s.replace("3/4 vlve","3/4 valve")
        s = s.replace("kitchen ceiling lightening","kitchen ceiling lighting")
        s = s.replace("led fixtues for the kitchen","led fixtures for the kitchen")
        s = s.replace("wall design cermic","wall design ceramic")
        s = s.replace("door chim buttons","door chime buttons")
        s = s.replace("plastice corrugated panels","plastic corrugated panels")
        s = s.replace("doors gaurds","doors guards")
        s = s.replace("24 inche sink and vanity for bath","24 inch sink and vanity for bath")
        s = s.replace("24 swantone vanity top","24 swanstone vanity top")
        s = s.replace("40 wattsolar charged lights","40 watt solar charged lights")
        s = s.replace("buikids toilet seat","buy kids toilet seat")
        s = s.replace("toliet seats","toilet seats")
        s = s.replace("land scaping timbers","landscaping timbers")
        s = s.replace("everblit heavy duty canvas dropcloth","everbilt heavy duty canvas drop cloth")
        s = s.replace("3/4 sharkbits","3/4 sharkbite")
        s = s.replace("bath rom toilets","bathroom toilets")
        s = s.replace("alumanam  sheets","aluminum sheets")
        s = s.replace("huskvarna","husqvarna")
        s = s.replace("treate 2x4","treated 2x4")
        s = s.replace("12000 btuair conditioners window","12000 btu air conditioners window")
        s = s.replace("air conditioner vbration","air conditioner vibration")
        s = s.replace("heith-zenith motion lights","heath-zenith motion lights")
        s = s.replace("small paint rollerss","small paint rollers")
        s = s.replace("fencde posts","fence posts")
        s = s.replace("knoty pine fencing","knotty pine fencing")
        s = s.replace("metal sheet underpenning","metal sheet underpinning")
        s = s.replace("plastic untility shelves","plastic utility shelves")
        s = s.replace("christmass  lights","christmas lights")
        s = s.replace("garlend lights","garland lights")
        s = s.replace("ceilig fan mount","ceiling fan mount")
        s = s.replace("paito table and chairs","patio table and chairs")
        s = s.replace("glacier bay one pice flapper","glacier bay one piece flapper")
        s = s.replace("dcanvas drop cloth","canvas drop cloth")
        s = s.replace("lawn mowre covers","lawn mower covers")
        s = s.replace("vaccum for dw745","vacuum for dw745")
        s = s.replace("Club cadet primer bulb","Cub cadet primer bulb")
        s = s.replace("interior door lcoks","interior door locks")
        s = s.replace("dremel toll kit","dremel tool kit")
        s = s.replace("round up nozzle replacment","roundup nozzle replacement")
        s = s.replace("ceder mulch","cedar mulch")
        s = s.replace("sikalatexr concrete vonding adhesive","sikalatex concrete bonding adhesive")
        s = s.replace("rigid air compressor","ridgid air compressor")
        s = s.replace("garge doors","garage doors")
        s = s.replace("ridding mowers","riding mowers")
        s = s.replace("ridiing lawnmower","riding lawn mower")
        s = s.replace("sliding mirror bathroom medicn cabinets","sliding mirror bathroom medicine cabinets")
        s = s.replace("pastic qtr round","plastic quarter round")
        s = s.replace("robutussin dh 835 replacement wick","robitussin dh 835 replacement wick")
        s = s.replace("brick wall panles","brick wall panels")
        s = s.replace("kitchen floor tikles","kitchen floor tiles")
        s = s.replace("buffer polishewr","buffer polisher")
        s = s.replace("keorsene heater wicks","kerosene heater wicks")
        s = s.replace("1x6 cedar boaed","1x6 cedar board")
        s = s.replace("infered heaters","infrared heaters")
        s = s.replace("1-1/2in. x 1ft. blk pipe","1-1/2in. x 1 ft. black pipe")
        s = s.replace("show me all 60 inch vaniteis","show me all 60 inch vanities")
        s = s.replace("cieling fan","ceiling fan")
        s = s.replace("instant  waater heater gas lp","instant water heater gas lp")
        s = s.replace("woodebn fence panels","wooden fence panels")
        s = s.replace("hardiboard siding","hardie board siding")
        s = s.replace("craft an lawn mower","craftsman lawn mower")
        s = s.replace("kohler wellworth tpoilet","kohler wellworth toilet")
        s = s.replace("moen dhower faucet","moen shower faucet")
        s = s.replace("dewalt hand toolsg saw cordless","dewalt hand tools saw cordless")
        s = s.replace("hindged l bracket","hinged l bracket")
        s = s.replace("ceiling fan canopie for flst ceiling","ceiling fan canopy for flat ceiling")
        s = s.replace("furnance vent delfector","furnace vent deflector")
        s = s.replace("flourescent shop light","fluorescent shop light")
        s = s.replace("bateries","batteries")
        s = s.replace("bath wall tile chanpayne","bath wall tile champagne")
        s = s.replace("floor ceramick","floor ceramic")
        s = s.replace("stone are mb11","stone care mb11")
        s = s.replace("traffic master porcelin ceramic tile portland stone","trafficmaster porcelain ceramic tile portland stone")
        s = s.replace("celing fans hampton bay","ceiling fans hampton bay")
        s = s.replace("outdoor ceilikng fan with light","outdoor ceiling fan with light")
        s = s.replace("36in vinale fence","36in vinyl fence")
        s = s.replace("extention ladder little gaint","extension ladder little giant")
        s = s.replace("closet rod 8 n9ickel","closet rod 8 nickel")
        s = s.replace("closetmaid wire eight itier organizer","closetmaid wire eight tier organizer")
        s = s.replace("shorten pendent lighting","shorten pendant lighting")
        s = s.replace("chainlink gate","chain link gate")
        s = s.replace("4 flourescent","4 fluorescent")
        s = s.replace("lithium batties","lithium batteries")
        s = s.replace("24x73 book shelve case white","24x73 bookshelf case white")
        s = s.replace("linoliuml adhesive","linoleum adhesive")
        s = s.replace("vynal flooring","vinyl flooring")
        s = s.replace("vynal grip strip","vinyl grip strip")
        s = s.replace("hagchet","hatchet")
        s = s.replace("frameless mirro mount","frameless mirror mount")
        s = s.replace("microwarve cart","microwave cart")
        s = s.replace("mosia grout sealer","mosaic grout sealer")
        s = s.replace("backsplach","backsplash")
        s = s.replace("dimable ceiling strip lights","dimmable ceiling strip lights")
        s = s.replace("lithum leaf blower","lithium leaf blower")
        s = s.replace("rayoby batteries","ryobi batteries")
        s = s.replace("pressure washerparts","pressure washer parts")
        s = s.replace("rigid 18v lituim ion nicad","ridgid 18v lithium ion nicad")
        s = s.replace("artric air portable","arctic air portable")
        s = s.replace("8ft wht veranda post sleeve","8 ft white veranda post sleeve")
        s = s.replace("vynal fence","vinyl fence")
        s = s.replace("solar naturlas salt","solar naturals salt")
        s = s.replace("metl flashing","metal flashing")
        s = s.replace("dog fence batt","dog fence battery")
        s = s.replace("onda pressure washer","honda pressure washer")
        s = s.replace("pressue washer","pressure washer")
        s = s.replace("fridgdare air conditioners","frigidaire air conditioners")
        s = s.replace("double pain windows","double pane windows")
        s = s.replace("round flat topmetal post caps","round flat top metal post caps")
        s = s.replace("1/2' plyweood","1/2' plywood")
        s = s.replace("ddummy door knobs interior","dummy door knobs interior")
        s = s.replace("robi battery lawn trimmer","ryobi battery lawn trimmer")
        s = s.replace("weewacker edger","weed wacker edger")
        s = s.replace("prunning shears","pruning shears")
        s = s.replace("steel enrty doors","steel entry doors")
        s = s.replace("forimca","formica")
        s = s.replace("satin nickle door hinge 4 in","satin nickel door hinge 4 in")
        s = s.replace("garden hose repir cuplings","garden hose repair couplings")
        s = s.replace("1/3 hoursepower garbage disposal","1/3 horsepower garbage disposal")
        s = s.replace("chicken wire 16 gauze","chicken wire 16 gauge")
        s = s.replace("wheelbarow","wheelbarrow")
        s = s.replace("didger","dodger")
        s = s.replace("hhigh efficiency round toilet in white","high efficiency round toilet in white")
        s = s.replace("accordian door venetian","accordion door venetian")
        s = s.replace("patio flurniture covers","patio furniture covers")
        s = s.replace("through thewall air conditioner","through the wall air conditioner")
        s = s.replace("Whirpool washer","Whirlpool washer")
        s = s.replace("4x6treaded wood","4x6 treated wood")
        s = s.replace("preature treated lumber 2in. x12in.x12 ft.","pressure treated lumber 2in. x 12 in.x 12 ft.")
        s = s.replace("closetmade wood","closetmaid wood")
        s = s.replace("steam cleanerm mop","steam cleaner mop")
        s = s.replace("steqamers","steamers")
        s = s.replace("pendant shads","pendant shades")
        s = s.replace("battery operated flashingm light","battery operated flashing light")
        s = s.replace("metal flexable water hose","metal flexible water hose")
        s = s.replace("air filter for lawn equitment","air filter for lawn equipment")
        s = s.replace("fiber glass pip insulation","fiberglass pipe insulation")
        s = s.replace("insallation","installation")
        s = s.replace("insullation","insulation")
        s = s.replace("contracor string light","contractor string light")
        s = s.replace("gas furnace and hotwater","gas furnace and hot water")
        s = s.replace("rust oleum cabinet stain kit","rustoleum cabinet stain kit")
        s = s.replace("sjhelf","shelf")
        s = s.replace("small brackets for selves","small brackets for shelves")
        s = s.replace("hecurles","hercules")
        s = s.replace("anderson window grate","andersen window grate")
        s = s.replace("anderson windows","andersen windows")
        s = s.replace("lasron slider windows","larson slider windows")
        s = s.replace("samsung 25.6 french door refridgerator","samsung 25.6 french door refrigerator")
        s = s.replace("closet doors oganizers","closet doors organizers")
        s = s.replace("koehler cimarron bathroom sink","kohler cimarron bathroom sink")
        s = s.replace("kohler pedestal sink cimeron","kohler pedestal sink cimarron")
        s = s.replace("cover for pole structue","cover for pole structure")
        s = s.replace("drils","drills")
        s = s.replace("surface mount channe","surface mount channel")
        s = s.replace("outside corner- dentil","outside corner- dental")
        s = s.replace("14heightx24withx15depth air conditioner","14 heightx24 with 15 depth air conditioner")
        s = s.replace("r30 demin insulation","r30 denim insulation")
        s = s.replace("6 metal tee posts","6 metal t posts")
        s = s.replace("metal fence postsd","metal fence posts")
        s = s.replace("aluminum l cahnnel","aluminum l channel")
        s = s.replace("conner trim moulding","corner trim moulding")
        s = s.replace("cornor board","corner board")
        s = s.replace("pvc planel glue","pvc panel glue")
        s = s.replace("3 in 1 vacum, ryobi","3 in 1 vacuum, ryobi")
        s = s.replace("toliet bowl rebuilding kits","toilet bowl rebuilding kits")
        s = s.replace("swing set accesories","swing set accessories")
        s = s.replace("ventenatural gas heater","vented natural gas heater")
        s = s.replace("square ube wood","square cube wood")
        s = s.replace("swivrl wood anchors","swivel wood anchors")
        s = s.replace("ge gridle","ge griddle")
        s = s.replace("pendant shafe","pendant shade")
        s = s.replace("3/8 pipe galvinized","3/8 pipe galvanized")
        s = s.replace("vaporbarrier, crawl space","vapor barrier, crawl space")
        s = s.replace("self sealant membrane","self sealing membrane")
        s = s.replace("husky work bemch","husky work bench")
        s = s.replace("vanity light fictures","vanity light fixtures")
        s = s.replace("bed frames headboaed","bed frames headboard")
        s = s.replace("replace plasticbathroom  towel holder","replace plastic bathroom towel holder")
        s = s.replace("whirlpool diswasher weather stripping","whirlpool dishwasher weather stripping")
        s = s.replace("36 inch front dooe with casing","36 inch front door with casing")
        s = s.replace("glass back doorr","glass back door")
        s = s.replace("pre hu door","pre hung door")
        s = s.replace("backsplash paneks","backsplash panels")
        s = s.replace("jeffery court mozaic tile","jeffrey court mosaic tile")
        s = s.replace("floo shets","floor sheets")
        s = s.replace("gazhose for dryer machine","gas hose for dryer machine")
        s = s.replace("electric fireplacewater heaters","electric fireplace water heaters")
        s = s.replace("ceiling mounted lighting fixures","ceiling mounted lighting fixtures")
        s = s.replace("tools bloowers","tools blowers")
        s = s.replace("artifical ground cover","artificial ground cover")
        s = s.replace("waxhers and electric dryers","washers and electric dryers")
        s = s.replace("outdoor tilees","outdoor tiles")
        s = s.replace("owens corning ashingles","owens corning shingles")
        s = s.replace("peper towel holder wall mount","paper towel holder wall mount")
        s = s.replace("genecrac generators","generac generators")
        s = s.replace("robyi gas weeder","ryobi gas weeder")
        s = s.replace("acrtlic tape","acrylic tape")
        s = s.replace("foam insulaion panels","foam insulation panels")
        s = s.replace("rumbl;estone","rumblestone")
        s = s.replace("famed sliding door $289.00","framed sliding door $289.00")
        s = s.replace("padio door","patio door")
        s = s.replace("cement boards ciding","cement boards siding")
        s = s.replace("upholstry","upholstery")
        s = s.replace("miror interior doors","mirror interior doors")
        s = s.replace("recessed medicien cabinet","recessed medicine cabinet")
        s = s.replace("bulked washed sand and gravel","bulk washed sand and gravel")
        s = s.replace("sheet stock floorinh","sheet stock flooring")
        s = s.replace("polycarbonite","polycarbonate")
        s = s.replace("dedwalt cordless drill","dewalt cordless drill")
        s = s.replace("ryobi power chalking gun","ryobi power caulking gun")
        s = s.replace("poulan pro lawn motor blades","poulan pro lawn mower blades")
        s = s.replace("diining set outdoor","dining set outdoor")
        s = s.replace("granite countertop glu","granite countertop glue")
        s = s.replace("cyculer saw","circular saw")
        s = s.replace("kitchenaid frenchdoor ref","kitchenaid french door ref")
        s = s.replace("rigid wet dry vac","ridgid wet dry vac")
        s = s.replace("whirlpool caprios 4.3","whirlpool cabrio 4.3")
        s = s.replace("micro wave ovens","microwave ovens")
        s = s.replace("8 valleta edger","8 valletta edger")
        s = s.replace("decking hardsware","decking hardware")
        s = s.replace("utility traiter","utility trailer")
        s = s.replace("ceilin storage","ceiling storage")
        s = s.replace("white wall  bathroon cabinets","white wall bathroom cabinets")
        s = s.replace("tsnkless hot water heater","tankless hot water heater")
        s = s.replace("weed killer consertrated","weed killer concentrate")
        s = s.replace("milwaukee ha,,er drill","milwaukee hammer drill")
        s = s.replace("23 ince","23 inch")
        s = s.replace("stone outside tile","stone outdoor tile")
        s = s.replace("galvanized outdoor celing fan","galvanized outdoor ceiling fan")
        s = s.replace("oil rubbered bronze dor","oil rubbed bronze door")
        s = s.replace("vynik tiles peel  stick","vinyl tiles peel stick")
        s = s.replace("window aircondiioner 12000 but","window air conditioner 12000 btu")
        s = s.replace("60 lb hi strength concrete","60 lb high strength concrete")
        s = s.replace("plexy glass 24 x 24","plexiglass 24 x 24")
        s = s.replace("porch liht fixture","porch light fixture")
        s = s.replace("moving trollie","moving trolley")
        s = s.replace("shoipping cart","shopping cart")
        s = s.replace("accesory bags","accessory bags")
        s = s.replace("garage door 70 lb extention spring","garage door 70 lb extension spring")
        s = s.replace("riobi shop vac filter","ryobi shop vac filter")
        s = s.replace("wet carpet cleaninig","wet carpet cleaning")
        s = s.replace("pvd electrical conduit","pvc electrical conduit")
        s = s.replace("roller up window blinds","roll up window blinds")
        s = s.replace("uplihght","uplight")
        s = s.replace("metal shelfs","metal shelves")
        s = s.replace("dewalt 20v recepicating saw","dewalt 20v reciprocating saw")
        s = s.replace("outdooor carpet","outdoor carpet")
        s = s.replace("step latter","step ladder")
        s = s.replace("kitchen cabinte hardware blue knob","kitchen cabinet hardware blue knob")
        s = s.replace("pivotangle lock hinge","pivot angle lock hinge")
        s = s.replace("plasticl panels","plastic panels")
        s = s.replace("varigated fiber board","variegated fiber board")
        s = s.replace("battery chages","battery charges")
        s = s.replace("1/2 inch blk iron coupling","1/2 inch black iron coupling")
        s = s.replace("defiant led armer max","defiant led armormax")
        s = s.replace("defiant led ight","defiant led light")
        s = s.replace("led flashlightts","led flashlights")
        s = s.replace("pfister pasedena 4 center set faucet","pfister pasadena 4 center set faucet")
        s = s.replace("meguire plastic cleaner","meguiars plastic cleaner")
        s = s.replace("single board pannel","single board panel")
        s = s.replace("foundation fent covers","foundation vent covers")
        s = s.replace("bottom freezer refrdgerators","bottom freezer refrigerators")
        s = s.replace("colbolt drill bits","cobalt drill bits")
        s = s.replace("soundfroofing material","soundproofing material")
        s = s.replace("hanging light masn gar","hanging light mason jar")
        s = s.replace("drywall mudd","drywall mud")
        s = s.replace("delta bathroom falcet","delta bathroom faucet")
        s = s.replace("ridgid 10000 watt","rigid 10000 watt")
        s = s.replace("pvc edgetape white","pvc edge tape white")
        s = s.replace("fireplace mantle","fireplace mantel")
        s = s.replace("drop in sink ovel","drop in sink oval")
        s = s.replace("40ft aluminumm ladder","40 ft aluminum ladder")
        s = s.replace("rigid shop vac filter","ridgid shop vac filter")
        s = s.replace("moen single handle valvue rebuild","moen single handle valve rebuild")
        s = s.replace("hunter ceiling fans accesories strip","hunter ceiling fans accessories strip")
        s = s.replace("wheel barrel","wheelbarrow")
        s = s.replace("16 aluminuim ladder","16 aluminum ladder")
        s = s.replace("1/2' olastic pipe","1/2' plastic pipe")
        s = s.replace("moen 7570 single hanlel faucet","moen 7570 single handle faucet")
        s = s.replace("padtio heater","patio heater")
        s = s.replace("rachet scret drivers","ratchet screwdrivers")
        s = s.replace("water fountain nozle","water fountain nozzle")
        s = s.replace("rigid sander","ridgid sander")
        s = s.replace("anderson 4000 windows","andersen 4000 windows")
        s = s.replace("doublew stainless","double stainless")
        s = s.replace("milwakee m12 cordless heated jacket","milwaukee m12 cordless heated jacket")
        s = s.replace("french door scree doorsscreen door","french door screen doors screen door")
        s = s.replace("samsung refridegrator","samsung refrigerator")
        s = s.replace("flurorescent   light bulbs","fluorescent light bulbs")
        s = s.replace("phillips 40t12cw plus florescent tube","phillips 40t12cw plus fluorescent tube")
        s = s.replace("black and decker timmer parts st4500","black and decker trimmer parts st4500")
        s = s.replace("gas range slide inove","gas range slide in love")
        s = s.replace("baldwin lock stets","baldwin lock sets")
        s = s.replace("6 ft ceder fence","6 ft cedar fence")
        s = s.replace("storeage","storage")
        s = s.replace("beckett fountin pump","beckett fountain pump")
        s = s.replace("polyeurethane exterior","polyurethane exterior")
        s = s.replace("ceiling pannel","ceiling panel")
        s = s.replace("70 celing fan","70 ceiling fan")
        s = s.replace("vynil barackets","vinyl brackets")
        s = s.replace("moen kitchen fauchet","moen kitchen faucet")
        s = s.replace("ridgid model wd1680 filter","rigid model wd1680 filter")
        s = s.replace("point of use electtric","point of use electric")
        s = s.replace("stell finished french patio door","steel finished french patio door")
        s = s.replace("lg elec laundry suite","lg electric laundry suite")
        s = s.replace("outdoor screem","outdoor screen")
        s = s.replace("patio chair cushions/marth stewart","patio chair cushions/martha stewart")
        s = s.replace("24 hollow core closet dor","24 hollow core closet door")
        s = s.replace("rigid miter saw","ridgid miter saw")
        s = s.replace("ruotor table","router table")
        s = s.replace("airconditioner decoritive  cover unit","air conditioner decorative cover unit")
        s = s.replace("miwaukee 18v battery and charger","milwaukee 18v battery and charger")
        s = s.replace("potable air conditioner","portable air conditioner")
        s = s.replace("perhung 30x80 interior door","prehung 30 x 80 interior door")
        s = s.replace("6 dewalt skill saw","6 dewalt skil saw")
        s = s.replace("1x8x8 toung and grove","1x8x8 tongue and groove")
        s = s.replace("river feather door threashold","river feather door threshold")
        s = s.replace("range connnector","range connector")
        s = s.replace("ligt fixture covers","light fixture covers")
        s = s.replace("window flasheing","window flashing")
        s = s.replace("backet metal","bracket metal")
        s = s.replace("horizantel fence panel","horizontal fence panel")
        s = s.replace("rug pad 8 x  10","rug pad 8x10")
        s = s.replace("frigadaire appliances","frigidaire appliances")
        s = s.replace("bath si k cabinets","bath sink cabinets")
        s = s.replace("8x10 outside storage","8x10 outdoor storage")
        s = s.replace("earthgrow mulch","earthgro mulch")
        s = s.replace("10 60 tooth blde","10 60 tooth blade")
        s = s.replace("sink faucet with soap dispencer","sink faucet with soap dispenser")
        s = s.replace("ridgid job max attatchmens","ridgid jobmax attachments")
        s = s.replace("ridgid wrachet head","ridgid ratchet head")
        s = s.replace("celliling light","ceiling light")
        s = s.replace("waterroo concrete paint","waterproof concrete paint")
        s = s.replace("americian standard champion 4 toliets","american standard champion 4 toilets")
        s = s.replace("4 ftawning frame","4 ft awning frame")
        s = s.replace("restour for concrete","restore for concrete")
        s = s.replace("econo florecent bulb","econo fluorescent bulb")
        s = s.replace("florecent bulb holder","fluorescent bulb holder")
        s = s.replace("light fictures","light fixtures")
        s = s.replace("lihonia 4 led work light","lithonia 4 led work light")
        s = s.replace("interrior frnch doors","interior french doors")
        s = s.replace("hamptom bay cusion","hampton bay cushion")
        s = s.replace("wndows","windows")
        s = s.replace("porcalain thinset","porcelain thinset")
        s = s.replace("versabon 50lb","versabond 50 lb")
        s = s.replace("table for outsde","table for outside")
        s = s.replace("hoinda gas edger","honda gas edger")
        s = s.replace("installing sockets for flor","installing sockets for floor")
        s = s.replace("laguna porcelin tile","laguna porcelain tile")
        s = s.replace("showe heads in oil rubbed bronze","shower heads in oil rubbed bronze")
        s = s.replace("chase lounge cushions","chaise lounge cushions")
        s = s.replace("electric detector in simming pool water","electric detector in swimming pool water")
        s = s.replace("elongagated toilet seat","elongated toilet seat")
        s = s.replace("towbehind lawn spreaders","tow behind lawn spreaders")
        s = s.replace("cable poter","cable porter")
        s = s.replace("fraiming nailer electric","framing nailer electric")
        s = s.replace("12 x 12 porcelian floor and wall tile","12 x 12 porcelain floor and wall tile")
        s = s.replace("marrazi","marazzi")
        s = s.replace("range hoodu","range hood")
        s = s.replace("whirpool range","whirlpool range")
        s = s.replace("subway title 3 x 6","subway tile 3 x 6")
        s = s.replace("untique stone","antique stone")
        s = s.replace("post sleeveee","post sleeve")
        s = s.replace("dinning chair seats","dining chair seats")
        s = s.replace("christmas lights icicle colerful","christmas lights icicle colorful")
        s = s.replace("colpay garage door molding","clopay garage door molding")
        s = s.replace("light for public ligthining","light for public lightning")
        s = s.replace("slate timberland shingle","slate timberline shingle")
        s = s.replace("cicular saw blad","circular saw blade")
        s = s.replace("varbide 7 1/4 circular saw blade","carbide 7 1/4 circular saw blade")
        s = s.replace("10 flourescent bulbs","10 fluorescent bulbs")
        s = s.replace("kids outside furnature","kids outside furniture")
        s = s.replace("whirpool gas range","whirlpool gas range")
        s = s.replace("starter fertillzer","starter fertilizer")
        s = s.replace("toro snowerblower light kit","toro snowblower light kit")
        s = s.replace("High Wheel String Trimer","High Wheel String Trimmer")
        s = s.replace("insided house door","inside house door")
        s = s.replace("3 1/2 non-mortison hinges satin finish","3 1/2 non-mortise hinges satin finish")
        s = s.replace("miracle grow garden soil","miracle gro garden soil")
        s = s.replace("miracle grow spray dispensers","miracle gro spray dispensers")
        s = s.replace("alure flooring black oak","allure flooring black oak")
        s = s.replace("sweeping atatchment for weed wacker","sweeping attachment for weed wacker")
        s = s.replace("retangle bathroom sinks","rectangular bathroom sinks")
        s = s.replace("underthe cabinet microwaves","under the cabinet microwaves")
        s = s.replace("24 inch lover doors","24 inch louvered doors")
        s = s.replace("window drip egedg","window drip edge")
        s = s.replace("rechargable portable air compressor","rechargeable portable air compressor")
        s = s.replace("birkmann 5 burner","brinkmann 5 burner")
        s = s.replace("whirlpool gasnstove self cleaning oven","whirlpool gas stove self cleaning oven")
        s = s.replace("havc brush","hvac brush")
        s = s.replace("discharge  hose 1.5 inces","discharge hose 1.5 inches")
        s = s.replace("6 ft laminite countertop","6 ft laminate countertop")
        s = s.replace("pool vaccum","pool vacuum")
        s = s.replace("1/2 in.x 1/2 in. thread albow male to male","1/2 in.x 1/2 in. threaded elbow male to male")
        s = s.replace("sofet","soffit")
        s = s.replace("sliding patio doort","sliding patio door")
        s = s.replace("30inch flourescent tubes","30 inch fluorescent tubes")
        s = s.replace("phillips light bulbs","philips light bulbs")
        s = s.replace("stainless steel sinl","stainless steel sink")
        s = s.replace("burgular bars for front porch","burglar bars for front porch")
        s = s.replace("oach lights","coach lights")
        s = s.replace("2 in lnsulated bushings","2 in insulated bushings")
        s = s.replace("motion lught","motion light")
        s = s.replace("residental  light sensor security lights","residential light sensor security lights")
        s = s.replace("vertical blind accsesories","vertical blind accessories")
        s = s.replace("1/2 in ree bar","1/2 in rebar")
        s = s.replace("cloths rod and shelf brackets","clothes rod and shelf brackets")
        s = s.replace("fire rated buildng materials","fire rated building materials")
        s = s.replace("hot point water filer","hotpoint water filter")
        s = s.replace("bathroom cabinet without fermaldehyde","bathroom cabinet without formaldehyde")
        s = s.replace("9.6 bvolt","9.6 volt")
        s = s.replace("rustoleum  bright coach metallic","rustoleum bright coat metallic")
        s = s.replace("stone effect sante cecilia top","stone effects santa cecilia top")
        s = s.replace("suspanded ceiling","suspended ceiling")
        s = s.replace("4x8 plywood pressure treeted","4x8 plywood pressure treated")
        s = s.replace("acess panel","access panel")
        s = s.replace("genie excellartor garage door opener","genie excelerator garage door opener")
        s = s.replace("ge dish washer with 46 dba rating","ge dishwasher with 46 dba rating")
        s = s.replace("wood and concret stain","wood and concrete stain")
        s = s.replace("8 foot flour sent","8 foot fluorescent")
        s = s.replace("infared grills","infrared grills")
        s = s.replace("wirless interconnected smoke dedector","wireless interconnected smoke detector")
        s = s.replace("luever","leuver")
        s = s.replace("3 in roung head bolt","3 in round head bolt")
        s = s.replace("rachet","ratchet")
        s = s.replace("rigid 12 volt","ridgid 12 volt")
        s = s.replace("sharkbit","sharkbite")
        s = s.replace("hamiltton collectin","hamilton collection")
        s = s.replace("kitchen aide wine and beverage  refrigerator","kitchenaid wine and beverage refrigerator")
        s = s.replace("paint markers burgondy color","paint markers burgundy color")
        s = s.replace("glass washer with sucktion cups","glass washer with suction cups")
        s = s.replace("andersor doors","anderson doors")
        s = s.replace("hickory cabinett","hickory cabinet")
        s = s.replace("repacement can type light bulbs","replacement can type light bulbs")
        s = s.replace("ceeling patio shades","ceiling patio shades")
        s = s.replace("white vainty 8 faucet","white vanity 8 faucet")
        s = s.replace("daylight florisant bulb 36inch","daylight fluorescent bulb 36 inch")
        s = s.replace("contact paoer","contact paper")
        s = s.replace("air  bathtubes","air bathtubs")
        s = s.replace("cushions for wecker furniture","cushions for wicker furniture")
        s = s.replace("galvinized poles 20long","galvanized poles 20 long")
        s = s.replace("siegel light pendent","siegel light pendant")
        s = s.replace("spaonges","sponges")
        s = s.replace("extorior shatters","exterior shutters")
        s = s.replace("led blubs","led bulbs")
        s = s.replace("4 inch back flow prenter","4 inch backflow preventer")
        s = s.replace("silding closet doors track","sliding closet doors track")
        s = s.replace("10000 btu windowair condiioner","10000 btu window air conditioner")
        s = s.replace("sewer pipe hoider","sewer pipe holder")
        s = s.replace("vinal blind paint","vinyl blind paint")
        s = s.replace("fuacet","faucet")
        s = s.replace("picinic tables","picnic tables")
        s = s.replace("all in one topmount kraus sinks","all in one top mount kraus sinks")
        s = s.replace("solar post lmapy","solar post lamp")
        s = s.replace("transormations","transformations")
        s = s.replace("daltiles sandy beach","daltile sandy beach")
        s = s.replace("wallmount indoor lights with plug","wall mounted indoor lights with plug")
        s = s.replace("kennal kit","kennel kit")
        s = s.replace("46 high output grow florescent bulb","46 high output grow fluorescent bulb")
        s = s.replace("frost fee freezers","frost free freezers")
        s = s.replace("stainles steel door handle","stainless steel door handle")
        s = s.replace("combo drill makita 20v","combi drill makita 20v")
        s = s.replace("shop vacumm","shop vacuum")
        s = s.replace("primer for led paint","primer for lead paint")
        s = s.replace("outdoor gas fiepits","outdoor gas firepits")
        s = s.replace("hallway pendendant lighting","hallway pendant lighting")
        s = s.replace("chesapeke oak flooring","chesapeake oak flooring")
        s = s.replace("ryobi multi tool acccessories","ryobi multi tool accessories")
        s = s.replace("ryobi raidos","ryobi radios")
        s = s.replace("milwaukee skill saw","milwaukee skil saw")
        s = s.replace("ligh chrismas hanging tree","light christmas hanging tree")
        s = s.replace("galvinized screws","galvanized screws")
        s = s.replace("led  circuline bulbs","led circline bulbs")
        s = s.replace("kholer elongated toilet seat","kohler elongated toilet seat")
        s = s.replace("tolet seats","toilet seats")
        s = s.replace("ock blade knife piece 3","lock blade knife piece 3")
        s = s.replace("portable airconditioner","portable air conditioner")
        s = s.replace("window aircondition","window air conditioner")
        s = s.replace("36 vx 72 commercial outdoor mats","36 x 72 commercial outdoor mats")
        s = s.replace("runner commerical","runner commercial")
        s = s.replace("montagna dappy gray","montagna dapple gray")
        s = s.replace("soil temperture test kit","soil temperature test kit")
        s = s.replace("basement  tolet","basement toilet")
        s = s.replace("32  door threshhold","32 door threshold")
        s = s.replace("hampton bay oak bast cabinets","hampton bay oak base cabinets")
        s = s.replace("charbroil parts","char broil parts")
        s = s.replace("qucikie mop","quickie mop")
        s = s.replace("concret anchor bolts","concrete anchor bolts")
        s = s.replace("24 whtie storage cabinet","24 white storage cabinet")
        s = s.replace("door handle deabolt kit","door handle deadbolt kit")
        s = s.replace("ge profile 30 inch charcoal folters","ge profile 30 inch charcoal filters")
        s = s.replace("49 inch napolian vanity top","49 inch napoleon vanity top")
        s = s.replace("4in pvc  franco cuppling","4in pvc fernco coupling")
        s = s.replace("graveless gravaless sewer pipe","graveless graveless sewer pipe")
        s = s.replace("shower fllor","shower floor")
        s = s.replace("riverera screen doors","riviera screen doors")
        s = s.replace("animal deterent","animal deterrent")
        s = s.replace("woodpeckers repellant","woodpeckers repellent")
        s = s.replace("wood buring insert 200-250","wood burning insert 200-250")
        s = s.replace("spectrazide ant","spectracide ant")
        s = s.replace("gas grill accesories","gas grill accessories")
        s = s.replace("elecronic insect repeller","electronic insect repeller")
        s = s.replace("slyvanna motion nite light","sylvania motion nite light")
        s = s.replace("4 in pvs end cap","4 in pvc end cap")
        s = s.replace("delta portor shower and tub trim","delta porter shower and tub trim")
        s = s.replace("replacment mini bulbs","replacement mini bulbs")
        s = s.replace("braxilian cherry laminate","brazilian cherry laminate")
        s = s.replace("15 amp tampe resistant outlets","15 amp tamper resistant outlets")
        s = s.replace("hydraulic jack renat","hydraulic jack rental")
        s = s.replace("32 x 32 shower baser","32 x 32 shower base")
        s = s.replace("electronic bed bug repellant","electronic bed bug repellent")
        s = s.replace("ridgid auger","rigid auger")
        s = s.replace("2000 psi force nozzzle","2000 psi force nozzle")
        s = s.replace("25 height beveragecooler","25 height beverage cooler")
        s = s.replace("anderson windows 400 seriesimpact resistant","andersen windows 400 series impact resistant")
        s = s.replace("drill 20 lithium battery","drill 20v lithium battery")
        s = s.replace("extertal air vent  cover","external air vent cover")
        s = s.replace("resin shesd","resin sheds")
        s = s.replace("8x8x4 conctete block","8x8x4 concrete block")
        s = s.replace("tun faucet spout","tub faucet spout")
        s = s.replace("continuos curtain rods","continuous curtain rods")
        s = s.replace("upholstry cleaner","upholstery cleaner")
        s = s.replace("ureka vaccuum","eureka vacuum")
        s = s.replace("30 towel rods brushed nicol","30 towel rods brushed nickel")
        s = s.replace("1/2 gal thermos","1/2 gallon thermos")
        s = s.replace("unbralla fabric top only","umbrella fabric top only")
        s = s.replace("outdoor cieling fans","outdoor ceiling fans")
        s = s.replace("20 amps cros hinghs breaker","20 amps cross highs breaker")
        s = s.replace("mixing tubn","mixing tub")
        s = s.replace("gfi circuit breaker","gfci circuit breaker")
        s = s.replace("wrought iuron fence panels","wrought iron fence panels")
        s = s.replace("ac air vent sleave","ac air vent sleeve")
        s = s.replace("air ventalation deflector","air ventilation deflector")
        s = s.replace("buddahs hand tree","buddha's hand tree")
        s = s.replace("lawm mowers","lawn mowers")
        s = s.replace("asathbula 7 piece","ashtabula 7 piece")
        s = s.replace("recessed lightjs","recessed lights")
        s = s.replace("hing pin door dtop","hinge pin door stop")
        s = s.replace("elerical outlets plates","electrical outlets plates")
        s = s.replace("bed tool boc","bed tool box")
        s = s.replace("16 inch fabn","16 inch fan")
        s = s.replace("battery poerated motion sensor","battery operated motion sensor")
        s = s.replace("grqss","grass")
        s = s.replace("troy build trimmer extension","troy bilt trimmer extension")
        s = s.replace("mansonry impact bit","masonry impact bit")
        s = s.replace("high output basebord","high output baseboard")
        s = s.replace("shower door sealparts","shower door seal parts")
        s = s.replace("12 inch hight wall cabinet","12 inch height wall cabinet")
        s = s.replace("light s for sno throwers","lights for snow throwers")
        s = s.replace("ceiling medallians","ceiling medallions")
        s = s.replace("medalion","medallion")
        s = s.replace("everbilt sloted","everbilt slotted")
        s = s.replace("transparant redwood stain","transparent redwood stain")
        s = s.replace("black and decker scub buster extreme","black and decker scrub buster extreme")
        s = s.replace("mobilehome siding","mobile home siding")
        s = s.replace("shutter screwws","shutter screws")
        s = s.replace("hampton pation set with firepit","hampton patio set with firepit")
        s = s.replace("industreial wire","industrial wire")
        s = s.replace("vegtable seeds","vegetable seeds")
        s = s.replace("masterpeice 72","masterpiece 72")
        s = s.replace("5/4 lumbe","5/4 lumber")
        s = s.replace("dawn to dusk lig","dawn to dusk light")
        s = s.replace("dusk to dawn motion sensoroutdoor lighting fixtures","dusk to dawn motion sensor outdoor lighting fixtures")
        s = s.replace("cordless sweeperr","cordless sweeper")
        s = s.replace("mill valley colle","mill valley college")
        s = s.replace("outdoorstorage bin","outdoor storage bin")
        s = s.replace("haging wire","hanging wire")
        s = s.replace("4 in white recessed haol baffle in soft white","4 in white recessed led baffle in soft white")
        s = s.replace("11 1/2x25 1/2 white aluminun","11 1/2 x 25 1/2 white aluminum")
        s = s.replace("saratoga hickorya","saratoga hickory")
        s = s.replace("surface gringer","surface grinder")
        s = s.replace("kidie co2","kidde co2")
        s = s.replace("batterys and charger kits","batteries and charger kits")
        s = s.replace("nutru ninja","nutri ninja")
        s = s.replace("23.5 shower door nickle","23.5 shower door nickel")
        s = s.replace("glass panel retiner","glass panel retainer")
        s = s.replace("12v replacement blubs","12v replacement bulbs")
        s = s.replace("martha steward","martha stewart")
        s = s.replace("1 1/2inchbrasswalltube18 inch","1 1/2 inch brass wall tube 18 inch")
        s = s.replace("brown color scheem","brown color scheme")
        s = s.replace("spiral latters","spiral letters")
        s = s.replace("24 incyh range","24 inch range")
        s = s.replace("8x8 ezup canopie cover","8x8 ez up canopy cover")
        s = s.replace("kitcheen door blind","kitchen door blind")
        s = s.replace("flourescent balast 120-2/32is","fluorescent ballast 120-2/32is")
        s = s.replace("vinyl lattiace","vinyl lattice")
        s = s.replace("1/4 28 threadded connector","1/4 28 threaded connector")
        s = s.replace("kitchaid 3 burner","kitchenaid 3 burner")
        s = s.replace("10 condiut pvc","10 conduit pvc")
        s = s.replace("WEBER GRILL GENIS 310","WEBER GRILL GENESIS 310")
        s = s.replace("wall mount tub fauet moen","wall mount tub faucet moen")
        s = s.replace("sower cleaner","shower cleaner")
        s = s.replace("batteryfor alarm system","battery for alarm system")
        s = s.replace("bed gugs","bed bugs")
        s = s.replace("show the pric of washer and dryer","show the price of washer and dryer")
        s = s.replace("washer  electic dryer","washer electric dryer")
        s = s.replace("ho hub couplings","no hub couplings")
        s = s.replace("battey string trimmers","battery string trimmers")
        s = s.replace("3/4 in. wide quarteround","3/4 in. wide quarter round")
        s = s.replace("ac dip pans","ac drip pans")
        s = s.replace("rutland wood stove termometer","rutland wood stove thermometer")
        s = s.replace("outdoor daucets","outdoor faucets")
        s = s.replace("badless vacuum cleaners","bagless vacuum cleaners")
        s = s.replace("dewalt 20 volt xr hamer","dewalt 20 volt xr hammer")
        s = s.replace("dewalt drillimpact tool 20 volt xr","dewalt drill impact tool 20 volt xr")
        s = s.replace("martha steward bath mirror","martha stewart bath mirror")
        s = s.replace("infared thermometer","infrared thermometer")
        s = s.replace("millwaukee 1/2 ele.c drill","milwaukee 1/2 elec drill")
        s = s.replace("25 watt 4 foot flourescent","25 watt 4 foot fluorescent")
        s = s.replace("boscj bit","bosch bit")
        s = s.replace("barbque grills","barbecue grills")
        s = s.replace("brinkman grill burner","brinkmann grill burner")
        s = s.replace("malbu replacement  led light bubles","malibu replacement led light bulbs")
        s = s.replace("natural stone tiele","natural stone tile")
        s = s.replace("stone vaneer","stone veneer")
        s = s.replace("stone venner sequia","stone veneer sequoia")
        s = s.replace("ceiling fan replacement clades","ceiling fan replacement blades")
        s = s.replace("transformet for flurescent tube lights","transformer for fluorescent tube lights")
        s = s.replace("refrigerator frenchdoor","refrigerator french door")
        s = s.replace("flourescent paint","fluorescent paint")
        s = s.replace("marking baint","marking paint")
        s = s.replace("mirrir hanger","mirror hanger")
        s = s.replace("chrisymas tree bags","christmas tree bags")
        s = s.replace("comercial food processor","commercial food processor")
        s = s.replace("picture haning kitpicture hanging kit","picture hanging kit picture hanging kit")
        s = s.replace("bathroom vanity cabinetwithouttops","bathroom vanity cabinets without tops")
        s = s.replace("amcrest survelliance systems","amcrest surveillance systems")
        s = s.replace("30 inch refigrator","30 inch refrigerator")
        s = s.replace("chain saw eletric","chainsaw electric")
        s = s.replace("power dprayer","power sprayer")
        s = s.replace("douglas fur fake christmas trees","douglas fir fake christmas trees")
        s = s.replace("brinkman grill","brinkmann grill")
        s = s.replace("dual switch dimer","dual switch dimmer")
        s = s.replace("Ortho Wed B Gone max","Ortho Weed B Gon max")
        s = s.replace("ortho weed be gone","ortho weed b gon")
        s = s.replace("4ft flourescent bulb t8","4ft fluorescent bulb t8")
        s = s.replace("18 volt 1/2 roter hammer","18 volt 1/2 roto hammer")
        s = s.replace("cabinents with drawers","cabinets with drawers")
        s = s.replace("7 mil trash bgs","7 mil trash bags")
        s = s.replace("1/2 ntp to 1/2","1/2 npt to 1/2")
        s = s.replace("3/8 rachert set","3/8 ratchet set")
        s = s.replace("hunter shower eshaust fan with light","hunter shower exhaust fan with light")
        s = s.replace("vanity in mahogany  mirros","vanity in mahogany mirrors")
        s = s.replace("hasmmock bed","hammock bed")
        s = s.replace("composit fencing","composite fencing")
        s = s.replace("post insurts","post inserts")
        s = s.replace("3500 psi pressue washer","3500 psi pressure washer")
        s = s.replace("idylus air purifier","idylis air purifier")
        s = s.replace("garden solenoide valves","garden solenoid valves")
        s = s.replace("window plastic instulation","window plastic insulation")
        s = s.replace("engineered wood floorcleaners","engineered wood floor cleaners")
        s = s.replace("parquee flooring","parquet flooring")
        s = s.replace("dermal saw max ultra","dremel saw max ultra")
        s = s.replace("external structual connector screw","external structural connector screw")
        s = s.replace("tv shelv","tv shelf")
        s = s.replace("kithen cabinets 18 white","kitchen cabinets 18 white")
        s = s.replace("1 1/2 couplingg","1 1/2 coupling")
        s = s.replace("porceline faucet handle","porcelain faucet handle")
        s = s.replace("duplex outlet and ubs charger","duplex outlet and usb charger")
        s = s.replace("1/4 quarter round cherries jublilee","1/4 quarter round cherries jubilee")
        s = s.replace("lg hausys viaterra","lg hausys viatera")
        s = s.replace("bear semi transparent cedar stain","behr semi transparent cedar stain")
        s = s.replace("27 mivrowave","27 microwave")
        s = s.replace("gardinias","gardenias")
        s = s.replace("ull spectrum plant light","full spectrum plant light")
        s = s.replace("942196brinkmann 2 burner","942196 brinkmann 2 burner")
        s = s.replace("gargage storage ideas","garage storage ideas")
        s = s.replace("outside horizontal storage sheds","outdoor horizontal storage sheds")
        s = s.replace("bouganvilla","bougainvillea")
        s = s.replace("led recressed lighting","led recessed lighting")
        s = s.replace("3 x3 marle tile","3x3 marble tile")
        s = s.replace("concrete saw dewall","concrete saw dewalt")
        s = s.replace("replacement glass for pellet stive","replacement glass for pellet stove")
        s = s.replace("porcelin tile black pencil tile","porcelain tile black pencil tile")
        s = s.replace("smoke dectectors","smoke detectors")
        s = s.replace("humidifier fulters","humidifier filters")
        s = s.replace("3/4 in. pvc assesories","3/4 in. pvc accessories")
        s = s.replace("12 inch sower head","12 inch shower head")
        s = s.replace("22 mm impact ocket","22mm impact socket")
        s = s.replace("garvanized wood screws","galvanized wood screws")
        s = s.replace("interlocking rubbber floor mats","interlocking rubber floor mats")
        s = s.replace("Hose end nozzel","Hose end nozzle")
        s = s.replace("led energy efficient kitchen lites","led energy efficient kitchen lights")
        s = s.replace("barn syslet door","barn style door")
        s = s.replace("rat or mice poision","rat or mice poison")
        s = s.replace("led ressed deameable lights","led recessed dimmable lights")
        s = s.replace("prelit tree mutli","pre lit tree multi")
        s = s.replace("sodering iron","soldering iron")
        s = s.replace("tub suround","tub surround")
        s = s.replace("fireplace screen assessories","fireplace screen accessories")
        s = s.replace("acrilic white paint","acrylic white paint")
        s = s.replace("gibraltor locking","gibraltar locking")
        s = s.replace("air conditioner sideays","air conditioner sideways")
        s = s.replace("white inyrtior paint","white interior paint")
        s = s.replace("100 watt candlebra","100 watt candelabra")
        s = s.replace("llhampton bay patio rocker","hampton bay patio rocker")
        s = s.replace("lock brushed nicke;","lock brushed nickel;")
        s = s.replace("structered media","structured media")
        s = s.replace("summit 24 inch ss gaqs range","summit 24 inch ss gas range")
        s = s.replace("ryobl battery","ryobi battery")
        s = s.replace("replacement carbrator for robyi","replacement carburetor for ryobi")
        s = s.replace("balist","ballast")
        s = s.replace("pressuer washer","pressure washer")
        s = s.replace("22 storage shelve","22 storage shelf")
        s = s.replace("32' strorm door","32' storm door")
        s = s.replace("hazardous locationlight fixture globe","hazardous location light fixture globe")
        s = s.replace("john deer bagger","john deere bagger")
        s = s.replace("ridinng lawn mowers mulching","riding lawn mowers mulching")
        s = s.replace("1/2 fpt x 1/2 inch pex","1/2 npt x 1/2 inch pex")
        s = s.replace("2 kindorff straps","2 kindorf straps")
        s = s.replace("telemechanic square d","telemecanique square d")
        s = s.replace("thresh hold","threshold")
        s = s.replace("24x24 framless recessed mount mirrored medicine","24x24 frameless recessed mount mirrored medicine")
        s = s.replace("600 connector cylander","600 connector cylinder")
        s = s.replace("well pump submerciable","well pump submersible")
        s = s.replace("security gate pannel","security gate panel")
        s = s.replace("1/4-20 jamb nuts","1/4-20 jam nuts")
        s = s.replace("american standard flush valvu","american standard flush valve")
        s = s.replace("stove adopter","stove adapter")
        s = s.replace("kitchenaide dishwasher","kitchenaid dishwasher")
        s = s.replace("roofing leadders","roofing ladders")
        s = s.replace("heath zenity 180 security light","heath zenith 180 security light")
        s = s.replace("solar  powerd lights","solar powered lights")
        s = s.replace("24 white walloven","24 white wall oven")
        s = s.replace("kitchen aide mixer","kitchenaid mixer")
        s = s.replace("10 in w 30 in l inetrior vent","10 in w 30 in l interior vent")
        s = s.replace("co smoke detector kiddie","co smoke detector kidde")
        s = s.replace("vacum aa bag 58236c","vacuum aa bag 58236c")
        s = s.replace("sealant for sideing","sealant for siding")
        s = s.replace("come along and chaincome along and chain","come along and chain come along and chain")
        s = s.replace("wall paper bprder","wallpaper border")
        s = s.replace("cararra tile","carrara tile")
        s = s.replace("14 gauge strranded wire","14 gauge stranded wire")
        s = s.replace("30 gal electirc water heater","30 gal electric water heater")
        s = s.replace("guarter round tile","quarter round tile")
        s = s.replace("summit gril","summit grill")
        s = s.replace("gavanized pipe 20 feet","galvanized pipe 20 feet")
        s = s.replace("melamine sheliving","melamine shelving")
        s = s.replace("composite fiscia board","composite fascia board")
        s = s.replace("spunge mop refill","sponge mop refill")
        s = s.replace("wall mount outside motion dector","wall mount outdoor motion detector")
        s = s.replace("bisquit tub refinish kit","biscuit tub refinish kit")
        s = s.replace("patternn paint rollers","pattern paint rollers")
        s = s.replace("built in wall nitch","built in wall niche")
        s = s.replace("ironboard built in","iron board built in")
        s = s.replace("behr melrot","behr merlot")
        s = s.replace("led shoplightmakita light","led shop light makita light")
        s = s.replace("armazone","amazon")
        s = s.replace("soild 6 panel interior door","solid 6 panel interior door")
        s = s.replace("dishs for 8","dishes for 8")
        s = s.replace("1 1/4 steel ppes","1 1/4 steel pipes")
        s = s.replace("pull out drw","pull out draw")
        s = s.replace("swffer mop","swiffer mop")
        s = s.replace("milwaukee m18 tootls","milwaukee m18 tools")
        s = s.replace("bronzw phone wall jack cover","bronze phone wall jack cover")
        s = s.replace("flourscent lights size 18x24","fluorescent lights size 18x24")
        s = s.replace("berber carpeting destiny doeskin","berber carpet destiny doeskin")
        s = s.replace("spring heavy dut","spring heavy duty")
        s = s.replace("2 in pvc pipe incresers","2 in pvc pipe increasers")
        s = s.replace("lifetime rouind table","lifetime round table")
        s = s.replace("16x26 recesssed medicine cabinets","16x26 recessed medicine cabinets")
        s = s.replace("rolling barn dorr hardware","rolling barn door hardware")
        s = s.replace("huricane panel caps","hurricane panel caps")
        s = s.replace("73 inch anderson patio screen doors","73 inch andersen patio screen doors")
        s = s.replace("barbque grill temperature guage","barbecue grill temperature gauge")
        s = s.replace("bath tub shower repair lit","bathtub shower repair kit")
        s = s.replace("entery door sidelights","entry door sidelights")
        s = s.replace("5 burnerner brikman gas grill","5 burner brinkmann gas grill")
        s = s.replace("battub floor mat","bathtub floor mat")
        s = s.replace("outlet wallplate with cover","outlet wall plate with cover")
        s = s.replace("fungacide","fungicide")
        s = s.replace("tuband tile latex caulk","tub and tile latex caulk")
        s = s.replace("natural gas barbeque","natural gas barbecue")
        s = s.replace("hallogen bulb  flood","halogen bulb flood")
        s = s.replace("roudulf","rudolf")
        s = s.replace("cellular shade 23.75x37","cellular shade 23.75x 37")
        s = s.replace("wyndham vanities with no tops","wyndham vanities without tops")
        s = s.replace("frigidare gas range","frigidaire gas range")
        s = s.replace("frigidare refrigerator","frigidaire refrigerator")
        s = s.replace("dishwasher moiunting kit","dishwasher mounting kit")
        s = s.replace("black refrigeratore","black refrigerator")
        s = s.replace("barcello estates light fi","bercello estates light fi")
        s = s.replace("kohler ch730 maintance kits","kohler ch730 maintenance kits")
        s = s.replace("phillips led slimline a19","philips led slimline a19")
        s = s.replace("asburn mahogany medicine cabinate","ashburn mahogany medicine cabinet")
        s = s.replace("stove top replacement patr","stove top replacement part")
        s = s.replace("hampton bay pendent light parts","hampton bay pendant light parts")
        s = s.replace("wall mountreading light","wall mount reading light")
        s = s.replace("heat on malamine tape","heat on melamine tape")
        s = s.replace("vinal plank selection","vinyl plank selection")
        s = s.replace("marble qwhite","marble white")
        s = s.replace("reheem performance 75 gal water heater","rheem performance 75 gal water heater")
        s = s.replace("cover for a double barrow grill","cover for a double barrel grill")
        s = s.replace("water taste kits","water test kits")
        s = s.replace("roybi gas trimmer repair kit","ryobi gas trimmer repair kit")
        s = s.replace("masonary dril bits","masonry drill bits")
        s = s.replace("bath and shower facet set","bath and shower faucet set")
        s = s.replace("sanding sponce","sanding sponge")
        s = s.replace("silestone sammples","silestone samples")
        s = s.replace("ge mwr filter","ge mwf filter")
        s = s.replace("rectangele garbage can","rectangle garbage can")
        s = s.replace("light podt sensor","light post sensor")
        s = s.replace("honewell wireless doorbell","honeywell wireless doorbell")
        s = s.replace("vertical door slide mechanis","vertical door slide mechanism")
        s = s.replace("2 inch bye 6 inch thick board","2 inch by 6 inch thick board")
        s = s.replace("28x80 contl splt rh","28x80 control split rh")
        s = s.replace("doors exterior with top windo","doors exterior with top window")
        s = s.replace("water filter for vanitys","water filter for vanities")
        s = s.replace("hampton bay geogian wall plates aged bronze","hampton bay georgian wall plates aged bronze")
        s = s.replace("18 wat let lamps","18 watt led lamps")
        s = s.replace("qstatic cling window film","static cling window film")
        s = s.replace("eletric pole hedge clippers","electric pole hedge clippers")
        s = s.replace("moen voss lightin","moen voss lighting")
        s = s.replace("dreamline showeruni door","dreamline shower door")
        s = s.replace("dewaqlt air nailers","dewalt air nailers")
        s = s.replace("hex drill chcuck","hex drill chuck")
        s = s.replace("vinal siding per box","vinyl siding per box")
        s = s.replace("verticle blind","vertical blind")
        s = s.replace("chome  framed mirror","chrome framed mirror")
        s = s.replace("b onnet","bonnet")
        s = s.replace("dowel sprial","dowel spiral")
        s = s.replace("deck tdiles","deck tiles")
        s = s.replace("driveing bits","driving bits")
        s = s.replace("water putifiers","water purifiers")
        s = s.replace("clyvus","clivus")
        s = s.replace("old style nailshand forgednails","old style nails hand forged nails")
        s = s.replace("grohe essencekitchen faucet","grohe essence kitchen faucet")
        s = s.replace("femle end hose repair","female end hose repair")
        s = s.replace("garden hose reair kits","garden hose repair kits")
        s = s.replace("bathroom facets","bathroom faucets")
        s = s.replace("kitchenaid refrigerator bottom frrezer","kitchenaid refrigerator bottom freezer")
        s = s.replace("chrome/polished brass 2-handle 4-in centerset bathroom fauc","chrome/polished brass 2-handle 4-in centerset bathroom faucet")
        s = s.replace("spackilng knife","spackling knife")
        s = s.replace("cadelabra light bulbs led","candelabra light bulbs led")
        s = s.replace("roller bracker for frameless shower doors","roller bracket for frameless shower doors")
        s = s.replace("morola tile metro penny","merola tile metro penny")
        s = s.replace("48 inchled tube","48 inch led tube")
        s = s.replace("corner sorage","corner storage")
        s = s.replace("glaciar bay crystal shower","glacier bay crystal shower")
        s = s.replace("tosco ivory tile","tosca ivory tile")
        s = s.replace("elecric screw driver batteries","electric screwdriver batteries")
        s = s.replace("mobilehome wall paint","mobile home wall paint")
        s = s.replace("chainsaw rplacement chains","chainsaw replacement chains")
        s = s.replace("electric guage cable","electric gauge cable")
        s = s.replace("f15 t5 florescent","f15 t5 fluorescent")
        s = s.replace("sprinkler conroller","sprinkler controller")
        s = s.replace("wireless light sitch","wireless light switch")
        s = s.replace("16x16x60boxes for moving","16x16x60 boxes for moving")
        s = s.replace("engeenered wood","engineered wood")
        s = s.replace("frigidare microwave","frigidaire microwave")
        s = s.replace("nals for subfloor","nails for subfloor")
        s = s.replace("verathane","varathane")
        s = s.replace("remote controlle light dimmer","remote controlled light dimmer")
        s = s.replace("koehler shower door","kohler shower door")
        s = s.replace("burgluar bar tool","burglar bar tool")
        s = s.replace("greem roofing shingles","green roofing shingles")
        s = s.replace("milwoki circular saw","milwaukee circular saw")
        s = s.replace("tub faucets bronza","tub faucets bronze")
        s = s.replace("bathtubdoor towel racks","bathtub door towel racks")
        s = s.replace("ac exhaust extention","ac exhaust extension")
        s = s.replace("outside deck boards composit","outside deck boards composite")
        s = s.replace("4inch ligh junction box","4 inch light junction box")
        s = s.replace("gardenn containers","garden containers")
        s = s.replace("plant continers","plant containers")
        s = s.replace("3 paint bbrush","3 paint brush")
        s = s.replace("26 in woodsaddle stool","26 in wood saddle stool")
        s = s.replace("adhensive with nozzle","adhesive with nozzle")
        s = s.replace("swanstone kitchen sink accesories","swanstone kitchen sink accessories")
        s = s.replace("pvc to corragated connector","pvc to corrugated connector")
        s = s.replace("unsanded grout bisquit","unsanded grout biscuit")
        s = s.replace("spray paint rust-oleum gray","spray paint rustoleum gray")
        s = s.replace("brushes drils","brushed drills")
        s = s.replace("indoor mounting tpe","indoor mounting tape")
        s = s.replace("indoor grow light blubs","indoor grow light bulbs")
        s = s.replace("thinset morter","thin set mortar")
        s = s.replace("flourescent g25 60watt","fluorescent g25 60 watt")
        s = s.replace("diatemaceous earth","diatomaceous earth")
        s = s.replace("23' biview surface mount med cab chestnut","23' bi view surface mount med cab chestnut")
        s = s.replace("72 hour carpt","72 hour carpet")
        s = s.replace("2 ' galvanise street 90","2 ' galvanized street 90")
        s = s.replace("maytab bravos","maytag bravos")
        s = s.replace("600w incandecent toggle dimmer","600w incandescent toggle dimmer")
        s = s.replace("galvanized wire 10 guage","galvanized wire 10 gauge")
        s = s.replace("assemble hight 17 inches","assembled height 17 inches")
        s = s.replace("pvc t coulpler","pvc t coupler")
        s = s.replace("water heatere drain pan","water heater drain pan")
        s = s.replace("faucet steam washers","faucet stem washers")
        s = s.replace("heat window filtm","heat window film")
        s = s.replace("dewalt circlular saw blades","dewalt circular saw blades")
        s = s.replace("5plinth block","plinth block")
        s = s.replace("french pation doors with sidepanels","french patio doors with side panels")
        s = s.replace("30 unfinish filler","30 unfinished filler")
        s = s.replace("home depot in cambrige","home depot in cambridge")
        s = s.replace("faucet siphon hose connecter","faucet siphon hose connector")
        s = s.replace("black out doors spray paint","black outdoor spray paint")
        s = s.replace("anderson storm door full view easy install","andersen storm door full view easy install")
        s = s.replace("ice marker water kits","ice maker water kits")
        s = s.replace("adhesive magnetized roll","adhesive magnetic roll")
        s = s.replace("metal kkitchen cabines","metal kitchen cabinets")
        s = s.replace("2' x 1 1/2 reducing busing thread","2' x 1 1/2 reducing bushing threaded")
        s = s.replace("abs rambit pipe saver","abs rambut pipe saver")
        s = s.replace("33 in w x 18 icnh depth vanity","33 in w x 18 inch depth vanity")
        s = s.replace("built in landry shelving","built in laundry shelving")
        s = s.replace("grey rubbermaid trash barrells","grey rubbermaid trash barrels")
        s = s.replace("sawall blades","sawzall blades")
        s = s.replace("9v battery ackup","9v battery backup")
        s = s.replace("1/2 in. fip x 7/16 in. or 1/2 in. slip joint angle stop valv","1/2 in. fip x 7/16 in. or 1/2 in. slip joint angle stop valve")
        s = s.replace("peir block","pier block")
        s = s.replace("under ceiling garag storage","under ceiling garage storage")
        s = s.replace("stone effects backsplash cool fushion","stone effects backsplash cool fusion")
        s = s.replace("desoldering vacum pump","desoldering vacuum pump")
        s = s.replace("elrctric welders","electric welders")
        s = s.replace("unfinushed kitchen cabinets","unfinished kitchen cabinets")
        s = s.replace("3 pole range reciptical","3 pole range receptacle")
        s = s.replace("sink cutting oard","sink cutting board")
        s = s.replace("steel tubing falanges","steel tubing flanges")
        s = s.replace("outdoor unskid tiles","outdoor non skid tiles")
        s = s.replace("6 round headlag bolt","6 round head lag bolt")
        s = s.replace("cyprees fence","cypress fence")
        s = s.replace("75 qrt cooler  with wheels","75 quart cooler with wheels")
        s = s.replace("buit in themostat","built in thermostat")
        s = s.replace("speacalty bit set","specialty bit set")
        s = s.replace("curtain rod classic sqaure finial","curtain rod classic square finial")
        s = s.replace("silk poinsetia","silk poinsettia")
        s = s.replace("1 1/4 pvcsch 80","1 1/4 pvc sch 80")
        s = s.replace("grill ousite door","grill outside door")
        s = s.replace("lumionaire","luminaire")
        s = s.replace("adienne bathroom vanity light","adrienne bathroom vanity light")
        s = s.replace("chashing led lights","chasing led lights")
        s = s.replace("24 inch vessal tops","24 inch vessel tops")
        s = s.replace("co2 detector kiddie","co2 detector kidde")
        s = s.replace("white glazed 4 tilw","white glazed 4 tile")
        s = s.replace("wood lattace","wood lattice")
        s = s.replace("premaid stair railing","premade stair railing")
        s = s.replace("3 function double walll switch","3 function double wall switch")
        s = s.replace("koehler shower faucet with spray","kohler shower faucet with spray")
        s = s.replace("askley electric  fireplace","ashley electric fireplace")
        s = s.replace("blind for paladian","blind for paladin")
        s = s.replace("regancy railin","regency railing")
        s = s.replace("weatherside purit","weatherside purity")
        s = s.replace("vent a hood dampr","vent a hood damper")
        s = s.replace("light tropper 2x4","light troffer 2x4")
        s = s.replace("30 amp generater receptical","30 amp generator receptacle")
        s = s.replace("prefab wood gate panals","prefab wood gate panels")
        s = s.replace("floating corner shelfing","floating corner shelving")
        s = s.replace("fridgidaire dehumidifier","frigidaire dehumidifier")
        s = s.replace("pegs for cabinent shelves","pegs for cabinet shelves")
        s = s.replace("100 amp to 200a lit","100 amp to 200 a lot")
        s = s.replace("decorative metal sceen","decorative metal screen")
        s = s.replace("lacross weather pro center","lacrosse weather pro center")
        s = s.replace("behr flat white marque","behr flat white marquee")
        s = s.replace("high output floresant","high output fluorescent")
        s = s.replace("behr hawian paint","behr hawaiian paint")
        s = s.replace("pressure vaccuum breaker o-ring","pressure vacuum breaker o-ring")
        s = s.replace("psint gun","paint gun")
        s = s.replace("wine coller","wine cooler")
        s = s.replace("rug ruunners","rug runners")
        s = s.replace("clock control for fridgidare gas stove","clock control for frigidaire gas stove")
        s = s.replace("outlet expsnsion surge protector","outlet expansion surge protector")
        s = s.replace("rigid pipe threader","ridgid pipe threader")
        s = s.replace("electical box","electrical box")
        s = s.replace("insect granuels","insect granules")
        s = s.replace("compsit outside corner","composite outside corner")
        s = s.replace("cabinet kitchen ligth","cabinet kitchen light")
        s = s.replace("dewalt ratchet srewdriver","dewalt ratchet screwdriver")
        s = s.replace("18.5 outside chair cushiobs","18.5 outside chair cushions")
        s = s.replace("fenching and gate latches","fencing and gate latches")
        s = s.replace("heater for refrigertor","heater for refrigerator")
        s = s.replace("motion detect indoor","motion detector indoor")
        s = s.replace("refrigerater french doors ge brand","refrigerator french doors ge brand")
        s = s.replace("tiki tourches","tiki torches")
        s = s.replace("gren house kits","greenhouse kits")
        s = s.replace("5000 btu aircondition","5000 btu air conditioner")
        s = s.replace("airator dishwasher","aerator dishwasher")
        s = s.replace("2x6 metal brakets","2x6 metal brackets")
        s = s.replace("weldn 3","weldon 3")
        s = s.replace("ceiling paint pray","ceiling paint spray")
        s = s.replace("flourescent fixture metal parts","fluorescent fixture metal parts")
        s = s.replace("natural hickery kitchen cabinets","natural hickory kitchen cabinets")
        s = s.replace("kitchen aide dishwasher","kitchenaid dishwasher")
        s = s.replace("led track lightning systems","led track lighting systems")
        s = s.replace("duplex receptacle nickle","duplex receptacle nickel")
        s = s.replace("12 foot ceadar","12 foot cedar")
        s = s.replace("faux wood shade 100 jnches","faux wood shade 100 inches")
        s = s.replace("contracto0r hose","contractor hose")
        s = s.replace("lspacers for toilet bowl","spacers for toilet bowl")
        s = s.replace("aftificial prelit christmas trees","artificial prelit christmas trees")
        s = s.replace("paint colores by rooms","paint colors by rooms")
        s = s.replace("warm whit led bulb","warm white led bulb")
        s = s.replace("clamps for unistruct","clamps for unistrut")
        s = s.replace("kitchen trviso price phister","kitchen treviso price pfister")
        s = s.replace("10guage copper wire 3 stand","10 gauge copper wire 3 stand")
        s = s.replace("deep frezer with glass cover","deep freezer with glass cover")
        s = s.replace("powder clorine shock treatment","powder chlorine shock treatment")
        s = s.replace("galvanaized can","galvanized can")
        s = s.replace("prebent aluminum facia","prebent aluminum fascia")
        s = s.replace("vinyl scrapper for jack hammer","vinyl scraper for jack hammer")
        s = s.replace("dwaft  outside plants","dwarf outside plants")
        s = s.replace("tilebath walls small","tile bath walls small")
        s = s.replace("2 ton aircondition","2 ton air conditioner")
        s = s.replace("martha stewart metalic paint gallon","martha stewart metallic paint gallon")
        s = s.replace("schilage electronic deadbolts locks","schlage electronic deadbolts locks")
        s = s.replace("60x65shower doors","60x65 shower doors")
        s = s.replace("tile slide cuter","tile slide cutter")
        s = s.replace("eagle peak hoickory","eagle peak hickory")
        s = s.replace("gas black range worldpool","gas black range whirlpool")
        s = s.replace("trigger makita skillsaw","trigger makita skil saw")
        s = s.replace("hardi lap hanger","hardie lap hanger")
        s = s.replace("master flow insolated duct wrap","master flow insulated duct wrap")
        s = s.replace("replacment stove knobs","replacement stove knobs")
        s = s.replace("outdoor alrm","outdoor alarm")
        s = s.replace("wireless outdoor thermom","wireless outdoor thermometer")
        s = s.replace("faun paint","fawn paint")
        s = s.replace("wireless security caamera","wireless security camera")
        s = s.replace("fiet electric led gu10","feit electric led gu10")
        s = s.replace("stair unners","stair runners")
        s = s.replace("stainstess steel spray paint","stainless steel spray paint")
        s = s.replace("mount blanv","mont blanc")
        s = s.replace("riobi power tool combo","ryobi power tool combo")
        s = s.replace("24 sydey collection","24 sydney collection")
        s = s.replace("air compresser","air compressor")
        s = s.replace("no tresspassing signs","no trespassing signs")
        s = s.replace("flexable 6 inch","flexible 6 inch")
        s = s.replace("wall beveled framelessmirror","wall beveled frameless mirror")
        s = s.replace("slidein range bisque","slide in range bisque")
        s = s.replace("router templit kits letters","router template kits letters")
        s = s.replace("american sandard 1660.225,","american standard 1660.225,")
        s = s.replace("onyx sand porcelian","onyx sand porcelain")
        s = s.replace("watherproof electrical boxes","weatherproof electrical boxes")
        s = s.replace("carpet remmnant","carpet remnant")
        s = s.replace("8' sigle wall gal pipe","8' single wall galv pipe")
        s = s.replace("byfold hinges","bi fold hinges")
        s = s.replace("terra cota quarry stones","terracotta quarry stones")
        s = s.replace("rustolem appliance touch up paint","rustoleum appliance touch up paint")
        s = s.replace("rain nickle","rain nickel")
        s = s.replace("whirlpool light bulb part 8206232","whirlpool light bulb part 8206232a")
        s = s.replace("Vigaro fall fertilizer","Vigoro fall fertilizer")
        s = s.replace("pneumatic cynlinder","pneumatic cylinder")
        s = s.replace("20 ft electical romex","20 ft electrical romex")
        s = s.replace("medicine cabinets recessable black","medicine cabinets recessed black")
        s = s.replace("krass 30 inch kitchen sink","kraus 30 inch kitchen sink")
        s = s.replace("stainless steel grat","stainless steel grate")
        s = s.replace("suncort 8' duct fans","suncourt 8' duct fans")
        s = s.replace("nutmag mirrors","nutmeg mirrors")
        s = s.replace("clawfoot tub faucit kit","clawfoot tub faucet kit")
        s = s.replace("protective pper","protective paper")
        s = s.replace("touchless dishwashing kintchen dispenser","touchless dishwashing kitchen dispenser")
        s = s.replace("air temperture contorl valve","air temperature control valve")
        s = s.replace("melinger hand truck wheals","melinger hand truck wheels")
        s = s.replace("watt premiere water filters","watt premier water filters")
        s = s.replace("weed killer spray contaner","weed killer spray container")
        s = s.replace("18in hardware coth","18in hardware cloth")
        s = s.replace("ac window supprt","ac window support")
        s = s.replace("vegetable plannter","vegetable planter")
        s = s.replace("soap punp","soap pump")
        s = s.replace("wall paper  murial glue","wallpaper mural glue")
        s = s.replace("vertical binds hardware","vertical blinds hardware")
        s = s.replace("rubbermaid verital sheds","rubbermaid vertical sheds")
        s = s.replace("1/2 in. extension joint","1/2 in. expansion joint")
        s = s.replace("curtin rods","curtain rods")
        s = s.replace("edge glued rounda","edge glued rounds")
        s = s.replace("plywood edge taope","plywood edge tape")
        s = s.replace("36' copoktop","36' cooktop")
        s = s.replace("curtains non black out","curtains not blackout")
        s = s.replace("honolule center drain","honolulu center drain")
        s = s.replace("toliet snake","toilet snake")
        s = s.replace("black and deckerbattery pack","black and decker battery pack")
        s = s.replace("beer and wine combination frigerator","beer and wine combination refrigerator")
        s = s.replace("mess wire fencing","mesh wire fencing")
        s = s.replace("ecosmart 90 led daylight br30","ecosmart 90w led daylight br30")
        s = s.replace("miniture bulbs 2 pin","miniature bulbs 2 pin")
        s = s.replace("dishwasher water connection vlave","dishwasher water connection valve")
        s = s.replace("ant bait raps","ant bait traps")
        s = s.replace("coragated aluimin special order","corrugated aluminum special order")
        s = s.replace("carpot canopy 10x20","carport canopy 10x20")
        s = s.replace("10 foot white ethjernet cable","10 foot white ethernet cable")
        s = s.replace("polished chrome cbinet pulls","polished chrome cabinet pulls")
        s = s.replace("cooper tubing","copper tubing")
        s = s.replace("dwarf pereniel plants","dwarf perennial plants")
        s = s.replace("lampost motion detector","lamp post motion detector")
        s = s.replace("3 gutter oulets","3 gutter outlets")
        s = s.replace("kohler shower ddoors for tubs in nickel","kohler shower doors for tubs in nickel")
        s = s.replace("zep liquid air fresher","zep liquid air freshener")
        s = s.replace("rewiring built in oven","wiring built in oven")
        s = s.replace("10/4 SJ CABLE","10/4 SJO CABLE")
        s = s.replace("tempered glass wndow","tempered glass window")
        s = s.replace("mataeials needed for paver patio","materials needed for paver patio")
        s = s.replace("tankles water heater gas outdoor","tankless water heater gas outdoor")
        s = s.replace("ypermethrin","cypermethrin")
        s = s.replace("kwikset halifax door leaver","kwikset halifax door lever")
        s = s.replace("ryobi coordless 18v starter kit","ryobi cordless 18v starter kit")
        s = s.replace("habor gazeebo","harbor gazebo")
        s = s.replace("electric barbeque grills","electric barbecue grills")
        s = s.replace("rasin raised garden bed","resin raised garden bed")
        s = s.replace("barbeque grills big and easy","barbecue grills big and easy")
        s = s.replace("floor warming matt","floor warming mat")
        s = s.replace("machette","machete")
        s = s.replace("cool  tube lgts","cool tube lights")
        s = s.replace("universal faucet connect","universal faucet connector")
        s = s.replace("daltile hexgon","daltile hexagon")
        s = s.replace("hurracaine brackets","hurricane brackets")
        s = s.replace("martha stewart curtiins","martha stewart curtains")
        s = s.replace("byfold doors","bifold doors")
        s = s.replace("2 tier adjustable cabinet orgainzer","2 tier adjustable cabinet organizer")
        s = s.replace("7w compact flourescent bulb","7w compact fluorescent bulb")
        s = s.replace("singel wall stove pipe","single wall stove pipe")
        s = s.replace("wheeld  trimmer","wheeled trimmer")
        s = s.replace("boader rocks","border rocks")
        s = s.replace("crown moldinf jig","crown molding jig")
        s = s.replace("small refridgerators","small refrigerators")
        s = s.replace("blind courner","blind corner")
        s = s.replace("asphault gap repair","asphalt gap repair")
        s = s.replace("no. 30 ridgid cutting wheel","no. 30 rigid cutting wheel")
        s = s.replace("battery cable conector","battery cable connector")
        s = s.replace("coranado baseboard pine","coronado baseboard pine")
        s = s.replace("cerrowire 18 gauge","cerro wire 18 gauge")
        s = s.replace("universal exstention cord","universal extension cord")
        s = s.replace("wirlpool counterdepth side by side refrigrator","whirlpool counter depth side by side refrigerator")
        s = s.replace("cedar bahr 502 stain","cedar behr 502 stain")
        s = s.replace("small tracerse rods","small traverse rods")
        s = s.replace("yelloe safet tape","yellow safety tape")
        s = s.replace("elctric heating lamps","electric heating lamps")
        s = s.replace("t8 flourescent bulbs","t8 fluorescent bulbs")
        s = s.replace("u bents fluorescent","u bend fluorescent")
        s = s.replace("pergo lamate flooring","pergo laminate flooring")
        s = s.replace("sweenys mole and gopher repelant","sweeney's mole and gopher repellent")
        s = s.replace("rg6 connecto","rg6 connector")
        s = s.replace("ge electriv burners","ge electric burners")
        s = s.replace("replacement part for koehler toilet kb3","replacement part for kohler toilet kb3")
        s = s.replace("furiture paint, stain and varnish","furniture paint, stain and varnish")
        s = s.replace("mission prarie camber top slab","mission prairie camber top slab")
        s = s.replace("mirr edge","mirror edge")
        s = s.replace("orbital sanding disck","orbital sanding disc")
        s = s.replace("quickrete 50 lb mix","quikrete 50 lb mix")
        s = s.replace("high efficiency dust baf rigid vac","high efficiency dust bag ridgid vac")
        s = s.replace("liminate flooring cleaning","laminate flooring cleaning")
        s = s.replace("gtxworks trimmer spools","gt worx trimmer spools")
        s = s.replace("securty bar mounts","security bar mounts")
        s = s.replace("fall supression kit","fall suppression kit")
        s = s.replace("weatherproof boom box","waterproof boombox")
        s = s.replace("geld wen 2500 96 x 36","jeld wen 2500 96 x 36")
        s = s.replace("enfineered floors drifting sand","engineered floors drifting sand")
        s = s.replace("well pump back presure valve","well pump back pressure valve")
        s = s.replace("heavy duty shevlving","heavy duty shelving")
        s = s.replace("mmodel","model")
        s = s.replace("frigidare stainless refrig","frigidaire stainless refrig")
        s = s.replace("rusteoulm spray paint","rustoleum spray paint")
        s = s.replace("t5 high output ligh","t5 high output light")
        s = s.replace("sandpap","sandpaper")
        s = s.replace("cerowire 12 gauge","cerro wire 12 gauge")
        s = s.replace("what rings for toitets","what rings for toilets")
        s = s.replace("infrared theomomter","infrared thermometer")
        s = s.replace("1x6 toungh  groove","1x6 tongue groove")
        s = s.replace("v ceader board","v cedar board")
        s = s.replace("sodpstone","soapstone")
        s = s.replace("10 yeaer smoke detectors/carbon monoxide combo","10 year smoke detectors/carbon monoxide combo")
        s = s.replace("kkohler toilet seat","kohler toilet seat")
        s = s.replace("pink toliet seat elongated","pink toilet seat elongated")
        s = s.replace("flexiblr bit","flexible bit")
        s = s.replace("coleman instasmart grill","coleman instastart grill")
        s = s.replace("exide battery 75,car battrey","exide battery 75,car battery")
        s = s.replace("black cherry stainer","black cherry stain")
        s = s.replace("1x4 pre primed mfd trim","1 x 4 pre primed mdf trim")
        s = s.replace("mnt movr combo shovel","mnt move combo shovel")
        s = s.replace("100 watt candlabra bulb","100 watt candelabra bulb")
        s = s.replace("samsung black stainles","samsung black stainless")
        s = s.replace("dewalt jig saw blad","dewalt jig saw blade")
        s = s.replace("alluminum downspout connector","aluminum downspout connector")
        s = s.replace("alltyp of fences","all type of fences")
        s = s.replace("clow hammer 16 0z","claw hammer 16 0z")
        s = s.replace("tomatoe plants","tomato plants")
        s = s.replace("white lacquer wall selves","white lacquer wall shelves")
        s = s.replace("pressure guage","pressure gauge")
        s = s.replace("slid pad","slide pad")
        s = s.replace("female hose connectore","female hose connector")
        s = s.replace("solor lamp outside","solar lamp outside")
        s = s.replace("daltile urban camoflogue","daltile urban camouflage")
        s = s.replace("deocorative screws for hanging pictures","decorative screws for hanging pictures")
        s = s.replace("kitchen composie double sinks","kitchen composite double sinks")
        s = s.replace("whitesilicone","white silicone")
        s = s.replace("self contained recepticles","self contained receptacles")
        s = s.replace("brass handel door","brass handle door")
        s = s.replace("charley brown christmas trees","charlie brown christmas trees")
        s = s.replace("carbon fiber vinel","carbon fiber vinyl")
        s = s.replace("phillips fluorescent 40","philips fluorescent 40")
        s = s.replace("36 inxh return air grill","36 inch return air grill")
        s = s.replace("garden pond pump impellor","garden pond pump impeller")
        s = s.replace("vinal flooring 25 year warranty","vinyl flooring 25 year warranty")
        s = s.replace("mulcing blades for troy built","mulching blades for troy bilt")
        s = s.replace("5 1/4 deckboard","5 1/4 deck board")
        s = s.replace("plaste dip","plasti dip")
        s = s.replace("cemnt pads for makita bo5030","cement pads for makita bo5030")
        s = s.replace("ge beverage refriderator","ge beverage refrigerator")
        s = s.replace("bathroom  plummbing","bathroom plumbing")
        s = s.replace("gas pire column","gas fire column")
        s = s.replace("confrence","conference")
        s = s.replace("clock cuitain rod wood","clock curtain rod wood")
        s = s.replace("decrotive outdoor lighting","decorative outdoor lighting")
        s = s.replace("ballast for single t12 fluorscent bulb","ballast for single t12 fluorescent bulb")
        s = s.replace("workstar cordless and recharable work light","workstar cordless and rechargeable work light")
        s = s.replace("light bulb 250 cfl","light bulb 250w cfl")
        s = s.replace("rubber gromet","rubber grommet")
        s = s.replace("spray metallicpaint","spray metallic paint")
        s = s.replace("paint quart zise","paint quart size")
        s = s.replace("blinds for portch","blinds for porch")
        s = s.replace("sable browj 95","sable brown 95")
        s = s.replace("1/2  conduet","1/2 conduit")
        s = s.replace("wooden curton rod brackets","wooden curtain rod brackets")
        s = s.replace("corbels and shelfs","corbels and shelves")
        s = s.replace("seimens typ qt breaker","siemens type qt breaker")
        s = s.replace("steel builco","steel bilco")
        s = s.replace("metal joinst","metal joist")
        s = s.replace("externol patio doors","external patio doors")
        s = s.replace("FENSE LIGHTING","FENCE LIGHTING")
        s = s.replace("oil bronzed wine glass rack","oiled bronze wine glass rack")
        s = s.replace("klien lether pouch","klein leather pouch")
        s = s.replace("shark rocket filtes","shark rocket filters")
        s = s.replace("4x7 ruggs","4 x 7 rugs")
        s = s.replace("24 elicreic stove","24 electric stove")
        s = s.replace("grill hasmilton","grill hamilton")
        s = s.replace("air vents for plumping","air vents for plumbing")
        s = s.replace("gazebo with shelfs","gazebo with shelves")
        s = s.replace("expanding plastic sleeves for scews","expanding plastic sleeves for screws")
        s = s.replace("oli rubbed bronze drain","oil rubbed bronze drain")
        s = s.replace("clothsline rope","clothesline rope")
        s = s.replace("stove gas replacement knops","stove gas replacement knobs")
        s = s.replace("rechargale batteries for solar lights","rechargeable batteries for solar lights")
        s = s.replace("standard artificial grasa synthetic lawn turf","standard artificial grass synthetic lawn turf")
        s = s.replace("new deck for rtz 50","new deck for rzt 50")
        s = s.replace("wire shelv liner","wire shelf liner")
        s = s.replace("wood paint with primerin blue","wood paint with primer in blue")
        s = s.replace("fabreeze","febreze")
        s = s.replace("ceilng fan","ceiling fan")
        s = s.replace("manuel for 425 - 1649","manual for 425 - 1649")
        s = s.replace("14 in dimond circular saw blade","14 in diamond circular saw blade")
        s = s.replace("berhr  solid 213 deep","behr solid 213 deep")
        s = s.replace("driveway m arkers","driveway markers")
        s = s.replace("commercil threshold","commercial threshold")
        s = s.replace("multinozzle spray painting","multi nozzle spray painting")
        s = s.replace("shower nitch","shower niche")
        s = s.replace("1/2x1/2 quater round","1/2 x 1/2 quarter round")
        s = s.replace("Insulted work gloves","Insulated work gloves")
        s = s.replace("5000 lumnes","5000 lumens")
        s = s.replace("magnets for gromets","magnets for grommets")
        s = s.replace("toro springkler","toro sprinkler")
        s = s.replace("motion sensoring black decorative lamp","motion sensing black decorative lamp")
        s = s.replace("proclean concentrated drain cleaner","pro clean concentrated drain cleaner")
        s = s.replace("feather river doorsth sidelights","feather river doors sidelights")
        s = s.replace("ridgid       powerwasher  parts","ridgid power washer parts")
        s = s.replace("skill pressure sander","skil pressure sander")
        s = s.replace("outdoor vertical sheda","outdoor vertical sheds")
        s = s.replace("brick web thin brick flats","brickweb thin brick flats")
        s = s.replace("airguard undelayment","airguard underlayment")
        s = s.replace("toyotaa","toyota")
        s = s.replace("round rug for kitch","round rug for kitchen")
        s = s.replace("round one piece tiolet","round one piece toilet")
        s = s.replace("sppeed square","speed square")
        s = s.replace("adirondak chair","adirondack chair")
        s = s.replace("hickory hadwre touch of spring","hickory hardware touch of spring")
        s = s.replace("garge door handle","garage door handle")
        s = s.replace("whiteled tree","white led tree")
        s = s.replace("airosol epoxy paint","aerosol epoxy paint")
        s = s.replace("ice ring machine","ice rink machine")
        s = s.replace("deep expresso walnut/new ellenton","deep espresso walnut/new ellenton")
        s = s.replace("interior walls bieges brown","interior walls beige brown")
        s = s.replace("pet disinfectent","pet disinfectant")
        s = s.replace("altra furniture parsons credenza desk with drawer and bookc","altra furniture parsons credenza desk with drawer and books")
        s = s.replace("gorilla gold cpvc gluetm","gorilla gold cpvc glue")
        s = s.replace("aligator clips","alligator clips")
        s = s.replace("irrigation pipe connectoer","irrigation pipe connector")
        s = s.replace("citronella fire pot fue","citronella fire pot fuel")
        s = s.replace("garden spreklers heads","garden sprinklers heads")
        s = s.replace("light swith insulation","light switch insulation")
        s = s.replace("dual lock 3m veclro","dual lock 3m velcro")
        s = s.replace("water proof mc connecter","waterproof dc connector")
        s = s.replace("snow blowerr scraper blade","snowblower scraper blade")
        s = s.replace("vesel tub","vessel tub")
        s = s.replace("carrrs","careers")
        s = s.replace("odl 6' x 6'retractable screens","odl 6' x 6 retractable screens")
        s = s.replace("outdoord storage locker","outdoor storage locker")
        s = s.replace("standing seam roof panals","standing seam roof panels")
        s = s.replace("phillips 65w 2 pack","philips 65w 2 pack")
        s = s.replace("2 squares double 5 vinly siding","2 squares double 5 vinyl siding")
        s = s.replace("fabric steam cleamer","fabric steam cleaner")
        s = s.replace("scikkens  stain","sikkens stain")
        s = s.replace("polyethylne cap","polyethylene cap")
        s = s.replace("decorative interor glass doors","decorative interior glass doors")
        s = s.replace("vanity top for two vessell","vanity top for two vessel")
        s = s.replace("giant bird of paridise","giant bird of paradise")
        s = s.replace("almeda hickory","alameda hickory")
        s = s.replace("cabinet ba rpulls in bronze","cabinet bar pulls in bronze")
        s = s.replace("l screwa","l screws")
        s = s.replace("johan deer 0 turns","john deere 0 turns")
        s = s.replace("milwankee 7 pc set","milwaukee 7 pc set")
        s = s.replace("faucet pl801l 18 guage","faucet pl801l 18 gauge")
        s = s.replace("12 light bronze chandilier","12 light bronze chandelier")
        s = s.replace("flourecent  light plastic covers","fluorescent light plastic covers")
        s = s.replace("roof pannel foam","roof panel foam")
        s = s.replace("under cabinet lighting ro-hs","under cabinet lighting rohs")
        s = s.replace("round lshower kit","round shower kit")
        s = s.replace("concreet enchors","concrete anchors")
        s = s.replace("woodwen pallet","wooden pallet")
        s = s.replace("shigles","shingles")
        s = s.replace("comercial plank doors","commercial plank doors")
        s = s.replace("stainless steel kithen faucet with soap dispenser","stainless steel kitchen faucet with soap dispenser")
        s = s.replace("m4 50 srcew","m4 50 screw")
        s = s.replace("splitbolt connector","split bolt connector")
        s = s.replace("charming 18 roll","charmin 18 roll")
        s = s.replace("table glass oatu","table glass oahu")
        s = s.replace("kohlor flush for toilet tank 4421","kohler flush for toilet tank 4421")
        s = s.replace("outdoor pendant lioghting","outdoor pendant lighting")
        s = s.replace("24 inflex gas line","24 in flex gas line")
        s = s.replace("lawn mower rechargeable batterys","lawn mower rechargeable batteries")
        s = s.replace("merola metalic tile","merola metallic tile")
        s = s.replace("above ground pool vaccume","above ground pool vacuum")
        s = s.replace("bosss water softner","boss water softener")
        s = s.replace("moen one handel kitchen faucet repair parts","moen one handle kitchen faucet repair parts")
        s = s.replace("sanding machinehardwood floors","sanding machine hardwood floors")
        s = s.replace("super patch driverway sealler","super patch driveway sealer")
        s = s.replace("sschlueter shower system","schluter shower system")
        s = s.replace("offset flang","offset flange")
        s = s.replace("aluminium tube rectangle","aluminium tube rectangular")
        s = s.replace("legrad keystone cat5e jack","legrand keystone cat5e jack")
        s = s.replace("yellow jacket extenison cord","yellow jacket extension cord")
        s = s.replace("Habachi","Hibachi")
        s = s.replace("mini pendant braket","mini pendant bracket")
        s = s.replace("hose to presure washer","hose to pressure washer")
        s = s.replace("gliddon speed wall","glidden speed wall")
        s = s.replace("new age produucts","new age products")
        s = s.replace("archor tub and shower faucet trim","archer tub and shower faucet trim")
        s = s.replace("space saving stoage","space saving storage")
        s = s.replace("vinyl flooring that clicks togther","vinyl flooring that clicks together")
        s = s.replace("gladden smooth stone","glidden smooth stone")
        s = s.replace("knape vogt baseket","knape vogt basket")
        s = s.replace("ul liquidthight 25","ul liquidtight 25")
        s = s.replace("white glossy furniture pain","white gloss furniture paint")
        s = s.replace("square bannister","square banister")
        s = s.replace("greenh wall paint","green wall paint")
        s = s.replace("tile medalions for the floor or wall","tile medallions for the floor or wall")
        s = s.replace("milwalke brewers garden flag","milwaukee brewers garden flag")
        s = s.replace("versatiube","versatube")
        s = s.replace("kenocen can nozzle","kenken can nozzle")
        s = s.replace("mosaic esterior","mosaic exterior")
        s = s.replace("winow wheels","window wheels")
        s = s.replace("stud popers","stud poppers")
        s = s.replace("trane 2.5 toon 13 seer heat pump","trane 2.5 ton 13 seer heat pump")
        s = s.replace("ultra vue quick screeen","ultra vue quick screen")
        s = s.replace("watterproof cleated boots","waterproof cleated boots")
        s = s.replace("hdx pneumaitic paint","hdx pneumatic paint")
        s = s.replace("biscue dishwashers","bisque dishwashers")
        s = s.replace("sunbrella sipcovers","sunbrella slipcovers")
        s = s.replace("miracle grow water absorbing crystals","miracle gro water absorbing crystals")
        s = s.replace("disposal rim and stopperkohler","disposal rim and stopper kohler")
        s = s.replace("long brakets","long brackets")
        s = s.replace("freplace gloves","fireplace gloves")
        s = s.replace("ridgid power drve pipe threadrs","ridgid power drive pipe threader")
        s = s.replace("12x24 shefl","12x24 shelf")
        s = s.replace("1x6 prime molding","1x6 primed molding")
        s = s.replace("countertop soap dispensor","countertop soap dispenser")
        s = s.replace("bushbutton for door bell","push button for doorbell")
        s = s.replace("cauk saver","caulk saver")
        s = s.replace("rubber stipper","rubber stopper")
        s = s.replace("16 inch flourescent","16 inch fluorescent")
        s = s.replace("pendents amber","pendants amber")
        s = s.replace("newtone broan round 751","nutone broan round 751")
        s = s.replace("danze shower vlve","danze shower valve")
        s = s.replace("wooden track drawer replacment","wooden track drawer replacement")
        s = s.replace("single granit bathroom vanity","single granite bathroom vanity")
        s = s.replace("oval steele tubs","oval steel tubs")
        s = s.replace("liquid weed and feeed","liquid weed and feed")
        s = s.replace("outodoor oatoman","outdoor ottoman")
        s = s.replace("nutone vaccum wall plate","nutone vacuum wall plate")
        s = s.replace("collor clamp","collar clamp")
        s = s.replace("pure air ultra filtration syste,m","pure air ultra filtration system")
        s = s.replace("llantana","lantana")
        s = s.replace("white melimine cabinet","white melamine cabinet")
        s = s.replace("2-handlet diverter repair kit","2-handle diverter repair kit")
        s = s.replace("mosiac lamps","mosaic lamps")
        s = s.replace("exterior pipeinsulation","exterior pipe insulation")
        s = s.replace("warm espresso bamboo quarteround","warm espresso bamboo quarter round")
        s = s.replace("hardwood medialons","hardwood medallions")
        s = s.replace("tub/hand shoer diverter with trim","tub/hand shower diverter with trim")
        s = s.replace("locite 2 plus 1","loctite 2 plus 1")
        s = s.replace("kwiksest door handle delta","kwikset door handle delta")
        s = s.replace("frame nail hitschi","frame nailer hitachi")
        s = s.replace("30 mirrow medicine cabinet","30 mirrored medicine cabinet")
        s = s.replace("pecane trees","pecan trees")
        s = s.replace("lifeproof carpet sample lower trasure","lifeproof carpet sample lower treasure")
        s = s.replace("umbrell hole ring","umbrella hole ring")
        s = s.replace("melmane wood","melamine wood")
        s = s.replace("melomine accessories","melamine accessories")
        s = s.replace("windows single hang","windows single hung")
        s = s.replace("portabe bar","portable bar")
        s = s.replace("crystable table set lamps","crystal table set lamps")
        s = s.replace("schlage handleset bermingham","schlage handleset birmingham")
        s = s.replace("lp gas converion kit","lp gas conversion kit")
        s = s.replace("quart exterior semi glass enamel","quart exterior semi gloss enamel")
        s = s.replace("woodrx ultra natural","wood rx ultra natural")
        s = s.replace("brushed barringnton","brushed barrington")
        s = s.replace("leather lgue","leather glue")
        s = s.replace("moen bronze low arch faucet","moen bronze low arc faucet")
        s = s.replace("18 inch linen closit","18 inch linen closet")
        s = s.replace("bear paint green myth","behr paint green myth")
        s = s.replace("solar light rechargable batteries","solar light rechargeable batteries")
        s = s.replace("solar powered emergancy unit","solar powered emergency unit")
        s = s.replace("kohler 3 handle shower reapair kit","kohler 3 handle shower repair kit")
        s = s.replace("thermadore black cast kitchen sink","thermador black cast kitchen sink")
        s = s.replace("dental shelf door","dentil shelf door")
        s = s.replace("seed starting mixx","seed starting mix")
        s = s.replace("rubberaid dust mop","rubbermaid dust mop")
        s = s.replace("phillips bugle-head finethread sharp","phillips bugle-head fine thread sharp")
        s = s.replace("black laminate shelfing","black laminate shelving")
        s = s.replace("ice maker cylinoid ge","ice maker solenoid ge")
        s = s.replace("home decorators mantle green","home decorators mantel green")
        s = s.replace("perrenial white daisy like","perennial white daisy like")
        s = s.replace("chamber-top halifax glass dooor","chamber-top halifax glass door")
        s = s.replace("depp well socket set","deep well socket set")
        s = s.replace("hanger racc vertical","hanger rack vertical")
        s = s.replace("tool package with pilers,needlenose","tool package with pliers,needlenose")
        s = s.replace("fome core board","foam core board")
        s = s.replace("colaroo outdoor shades corded","coolaroo outdoor shades corded")
        s = s.replace("decoator chain","decorator chain")
        s = s.replace("rust oleum dark hunter green spray enamel paint","rustoleum dark hunter green spray enamel paint")
        s = s.replace("lights and siloutte","lights and silhouette")
        s = s.replace("real live orchred plants","real live orchid plants")
        s = s.replace("2ftx3ft industrail rbber mat","2ftx3ft industrial rubber mat")
        s = s.replace("fernace vent shut off","furnace vent shut off")
        s = s.replace("cedar wood balisters","cedar wood balusters")
        s = s.replace("gliden premium semi gloss quart","glidden premium semi gloss quart")
        s = s.replace("mosaic tile costal mist","mosaic tile coastal mist")
        s = s.replace("toilet lever kphler brass","toilet lever kohler brass")
        s = s.replace("front doors - poinye zinc","front doors - pointe zinc")
        s = s.replace("matte bailey mohogany","matte bailey mahogany")
        s = s.replace("wesleyand","wesleyan")
        s = s.replace("plasic diffuser","plastic diffuser")
        s = s.replace("cover kage for pet","cover page for pet")
        s = s.replace("network agapter","network adapter")
        s = s.replace("whitehaus bathroom sinl","whitehaus bathroom sink")
        s = s.replace("icey tech","icey tek")
        s = s.replace("kaorik wine","kalorik wine")
        s = s.replace("susbenders","suspenders")
        s = s.replace("policarbonate case","polycarbonate case")
        s = s.replace("shaw livng rugs model rac66","shaw living rugs model rac66")
        s = s.replace("carpet in bassment","carpet in basement")
        s = s.replace("bifold doorsfold plantation","bi fold doors fold plantation")
        s = s.replace("handheld seed speader","handheld seed spreader")
        s = s.replace("hot dipped galvinized coil nails","hot dipped galvanized coil nails")
        s = s.replace("hand saw sharpner","hand saw sharpener")
        s = s.replace("mattress foam protecter","mattress foam protector")
        s = s.replace("n utdriver bit","nut driver bit")
        s = s.replace("lattice wwod tone","lattice wood tone")
        s = s.replace("our door receptacles","outdoor receptacles")
        s = s.replace("great outdors","great outdoors")
        s = s.replace("exterior string ligts","exterior string lights")
        s = s.replace("dog ,cat,repellant","dog ,cat,repellent")
        s = s.replace("20a wht nylon duple","20a wht nylon duplex")
        s = s.replace("fatmax leveler premier","fatmax level premier")
        s = s.replace("ralph laren brown paints","ralph lauren brown paints")
        s = s.replace("liquid bi fuels","liquid biofuels")
        s = s.replace("scrubbin sponge","scrubbing sponge")
        s = s.replace("ceramic tile  tooth brush and  soap holder","ceramic tile toothbrush and soap holder")
        s = s.replace("cultured marbl;e shower walls","cultured marble shower walls")
        s = s.replace("did recorder player","dvd recorder player")
        s = s.replace("golith","goliath")
        s = s.replace("black maytag french door refrigirator","black maytag french door refrigerator")
        s = s.replace("stair nose santos maogani","stair nose santos mahogany")
        s = s.replace("l tub fauctes","l tub faucets")
        s = s.replace("eyebolt brass","eye bolt brass")
        s = s.replace("terracotta exteriorpaint","terracotta exterior paint")
        s = s.replace("manuel venting sky light","manual venting skylight")
        s = s.replace("bathroom fan motion sencer","bathroom fan motion sensor")
        s = s.replace("hard start capacitator","hard start capacitor")
        s = s.replace("windows gazing bead","windows glazing bead")
        s = s.replace("vanitiy top back splach","vanity top backsplash")
        s = s.replace("large yellow screw inground anchors","large yellow screw in ground anchors")
        s = s.replace("heavy duty polyurathane","heavy duty polyurethane")
        s = s.replace("folfable stool","foldable stool")
        s = s.replace("charlston south carolina","charleston south carolina")
        s = s.replace("pine flooring, tang end grove","pine flooring, tongue and groove")
        s = s.replace("starter fuil","starter fuel")
        s = s.replace("granite colr group prices","granite color group prices")
        s = s.replace("calanvreas","calaveras")
        s = s.replace("golden krome spray","gold chrome spray")
        s = s.replace("g e micewave","g e microwave")
        s = s.replace("sheet meatal hole cutter","sheet metal hole cutter")
        s = s.replace("zurn hot short stemcartridge","zurn hot short stem cartridge")
        s = s.replace("outdoor picture ftames","outdoor picture frames")
        s = s.replace("shower pad porceleain","shower pan porcelain")
        s = s.replace("battery under counter lightening","battery under counter lighting")
        s = s.replace("elictric door bail","electric door bell")
        s = s.replace("barbeque insert","barbecue insert")
        s = s.replace("barclay glass bathroom shelfs","barclay glass bathroom shelves")
        s = s.replace("preserva wood caryon","preserva wood crayon")
        s = s.replace("white grey floor tile mosiac","white grey floor tile mosaic")
        s = s.replace("minwax wood puty","minwax wood putty")
        s = s.replace("the  govenore","the governor")
        s = s.replace("diverter 5 in. tub spout with slip fit connection in chrom","diverter 5 in. tub spout with slip fit connection in chrome")
        s = s.replace("vinyl plank blue slatr","vinyl plank blue slate")
        s = s.replace("frameless shwoer panel","frameless shower panel")
        s = s.replace("virtue usa huntshire","virtu usa huntshire")
        s = s.replace("3.5 Hindge","3.5 Hinge")
        s = s.replace("round plastic  tablrs","round plastic tables")
        s = s.replace("paint storage contaiers","paint storage containers")
        s = s.replace("centerset 2-handle weall","centerset 2-handle wall")
        s = s.replace("wax ring with self taping bolts","wax ring with self tapping bolts")
        s = s.replace("gama sonic winsor pier base","gama sonic windsor pier base")
        s = s.replace("pilla windows","pella windows")
        s = s.replace("dresser acessories","dresser accessories")
        s = s.replace("duel compression 1/2 x 3/8 valve","dual compression 1/2 x 3/8 valve")
        s = s.replace("american atanderd plebe 4086","american standard plebe 4086")
        s = s.replace("dyson ball allergy vaccume","dyson ball allergy vacuum")
        s = s.replace("low woltage relay","low voltage relay")
        s = s.replace("hand steam cleanere","hand steam cleaner")
        s = s.replace("eiectric concrte mixer","electric concrete mixer")
        s = s.replace("pemco sill extender","pemko sill extender")
        s = s.replace("silver branzing rods","silver brazing rods")
        s = s.replace("sanding beltsr","sanding belts")
        s = s.replace("dorr faceplates","door faceplates")
        s = s.replace("stainless steel ball beating for hinges","stainless steel ball bearing for hinges")
        s = s.replace("stabilty","stability")
        s = s.replace("hose bibb replacement valve","hose bib replacement valve")
        s = s.replace("long shower curtins","long shower curtains")
        s = s.replace("crub rubber","crumb rubber")
        s = s.replace("swivel saftey cover","swivel safety cover")
        s = s.replace("makita oscilating saw","makita oscillating saw")
        s = s.replace("whithaus faucet speckled brass","whitehaus faucet speckled brass")
        s = s.replace("energy efficent skylight","energy efficient skylight")
        s = s.replace("garden seed packs","garden seed packets")
        s = s.replace("boshe double bevel sliding miter saw","bosch double bevel sliding miter saw")
        s = s.replace("taylor test lit","taylor test kit")
        s = s.replace("chargril grill","charbroil grill")
        s = s.replace("over ran","overran")
        s = s.replace("recipricating saw 15 amp","reciprocating saw 15 amp")
        s = s.replace("mikita 18v 2.6 ah","makita 18v 2.6 ah")
        s = s.replace("no burn spry","no burn spray")
        s = s.replace("cuctis soil","cactus soil")
        s = s.replace("brushed stainless cabin ate hardware","brushed stainless cabinet hardware")
        s = s.replace("fork lift strps","forklift straps")
        s = s.replace("electrian","electrician")
        s = s.replace("doorbell chimes and transformr","doorbell chimes and transformer")
        s = s.replace("faux diamondplate","faux diamond plate")
        s = s.replace("milstead vintage maple engineered flooring","millstead vintage maple engineered flooring")
        s = s.replace("ce tech coaxial cablenail in clips","ce tech coaxial cable nail in clips")
        s = s.replace("bq heat distributipn plates","bbq heat distribution plates")
        s = s.replace("metal lath stuko","metal lath stucco")
        s = s.replace("cord less drill portcable","cordless drill porter cable")
        s = s.replace("round bulb sting lights","round bulb string lights")
        s = s.replace("lp coversion kit maytag dryer","lp conversion kit maytag dryer")
        s = s.replace("chase lounger covers","chaise lounge covers")
        s = s.replace("insl-x pure step","insl-x sure step")
        s = s.replace("gerber knife tactiical","gerber knife tactical")
        s = s.replace("deecals number","decals number")
        s = s.replace("hampton bat 26'. w tilt out hamper white","hampton bay 26'. w tilt out hamper white")
        s = s.replace("outdoor chritstmas light remote","outdoor christmas light remote")
        s = s.replace("wood fuelpellets","wood fuel pellets")
        s = s.replace("cpipe lamp","pipe lamp")
        s = s.replace("wiemans stainless cleaner","weimans stainless cleaner")
        s = s.replace("10  roll up outside blinds","10 roll up outdoor blinds")
        s = s.replace("wainscote","wainscot")
        s = s.replace("heat resistant spicket","heat resistant spigot")
        s = s.replace("garage shelve","garage shelf")
        s = s.replace("shevles","shelves")
        s = s.replace("storage shelfs","storage shelves")
        s = s.replace("proipane","propane")
        s = s.replace("ventless gas heters","ventless gas heaters")
        s = s.replace("vinal fencing","vinyl fencing")
        s = s.replace("toliet bowl","toilet bowl")
        s = s.replace("toliet bowl wrench","toilet bowl wrench")
        s = s.replace("fanc wire","fancy wire")
        s = s.replace("t post fence assesories","t post fence accessories")
        s = s.replace("telescooping ladder","telescoping ladder")
        s = s.replace("spring haven brown all weather wicked","spring haven brown all weather wicker")
        s = s.replace("36 exterior steele door","36 exterior steel door")
        s = s.replace("faucetskitchen","faucets kitchen")
        s = s.replace("batt insulatiom","batt insulation")
        s = s.replace("congolium","congoleum")
        s = s.replace("vinal flooring","vinyl flooring")
        s = s.replace("vynil floorring","vinyl flooring")
        s = s.replace("clacier bay toliet","glacier bay toilet")
        s = s.replace("GLAZER BAY TOILET","GLACIER BAY TOILET")
        s = s.replace("norton hot water heater ingniter","norton hot water heater igniter")
        s = s.replace("undercounter lighs","under counter lights")
        s = s.replace("stainless refridgerator","stainless refrigerator")
        s = s.replace("stainless steel refridgerator","stainless steel refrigerator")
        s = s.replace("window ac manuel operation","window ac manual operation")
        s = s.replace("rustolem","rustoleum")
        s = s.replace("18v drill brushles","18v drill brushless")
        s = s.replace("dining sets outdo?","dining sets outdoor?")
        s = s.replace("eat resistant epoxy","heat resistant epoxy")
        s = s.replace("cordless drils","cordless drills")
        s = s.replace("3 piece bfush set","3 piece brush set")
        s = s.replace("kitchen faucet installtion tools","kitchen faucet installation tools")
        s = s.replace("Moen Kitchen sink fauset","Moen Kitchen sink faucet")
        s = s.replace("plaqstic bucket","plastic bucket")
        s = s.replace("3m winow film","3m window film")
        s = s.replace("water softner","water softener")
        s = s.replace("flourescent light bulp","fluorescent light bulb")
        s = s.replace("closermaid cabinet","closetmaid cabinet")
        s = s.replace("raised panel extirior doors","raised panel exterior doors")
        s = s.replace("blcktop repair kit","blacktop repair kit")
        s = s.replace("peal and stick flashning","peel and stick flashing")
        s = s.replace("marshaltown 6 inch","marshalltown 6 inch")
        s = s.replace("vynel wall tiles","vinyl wall tiles")
        s = s.replace("presusre treated  post","pressure treated post")
        s = s.replace("LAWN LEAF VACUM","LAWN LEAF VACUUM")
        s = s.replace("space heatres","space heaters")
        s = s.replace("alumium fence 6 ft 6ft","aluminum fence 6 ft 6 ft")
        s = s.replace("bathroom sinks kholer","bathroom sinks kohler")
        s = s.replace("pedistal","pedestal")
        s = s.replace("clear eppoxy","clear epoxy")
        s = s.replace("wood fir plank flooring","wood for plank flooring")
        s = s.replace("quickcrete waterproof cement","quikrete waterproof cement")
        s = s.replace("rood rake","roof rake")
        s = s.replace("propane gas tank meater","propane gas tank meter")
        s = s.replace("ac cooling fin straightenrs","ac cooling fin straightener")
        s = s.replace("slidng panel lock","sliding panel lock")
        s = s.replace("closet maiid cabinets","closet maid cabinets")
        s = s.replace("ridge power tools combo packs","ridgid power tools combo packs")
        s = s.replace("backsplash tiiles","backsplash tiles")
        s = s.replace("cabinet knobsd","cabinet knobs")
        s = s.replace("cabnet knobs","cabinet knobs")
        s = s.replace("dealt air compressor parts","dewalt air compressor parts")
        s = s.replace("spgot","spigot")
        s = s.replace("paver bricks scolloped","paver bricks scalloped")
        s = s.replace("CHASE LOUNGE","CHAISE LOUNGE")
        s = s.replace("layndry tu","laundry tu")
        s = s.replace("submeribale pedistal sump pump","submersible pedestal sump pump")
        s = s.replace("celling fans","ceiling fans")
        s = s.replace("wall sconse","wall sconce")
        s = s.replace("93 inch widecellular shades","93 inch wide cellular shades")
        s = s.replace("post white ligth","post white light")
        s = s.replace("palmero brushed nickel ceiling fan","palermo brushed nickel ceiling fan")
        s = s.replace("aromaticeatern red cedar planking","aromatic eastern red cedar planking")
        s = s.replace("black and decker hobby crafter","black and decker hobbycrafter")
        s = s.replace("front load fridaire","front load frigidaire")
        s = s.replace("pedestial washer","pedestal washer")
        s = s.replace("whilrpool front loader washer","whirlpool front loader washer")
        s = s.replace("extrior louvored wood door 30x80","exterior louvered wood door 30x80")
        s = s.replace("interior doorser","interior doors")
        s = s.replace("dill battery 12v model g0805","drill battery 12v model g0805")
        s = s.replace("10 stair lader","10 stair ladder")
        s = s.replace("milwakee 1/2 impact cordless","milwaukee 1/2 impact cordless")
        s = s.replace("kolher","kohler")
        s = s.replace("floor slealer","floor sealer")
        s = s.replace("high traffic floor polurethane paint","high traffic floor polyurethane paint")
        s = s.replace("sawzall blades miluakee","sawzall blades milwaukee")
        s = s.replace("vaccum hose","vacuum hose")
        s = s.replace("vynal repalcement windows","vinyl replacement windows")
        s = s.replace("vinil for flors","vinyl for floors")
        s = s.replace("led withe","led white")
        s = s.replace("squar flushmount lights","square flush mount lights")
        s = s.replace("huskey 18","husky 18")
        s = s.replace("remove oder from kerosine","remove odor from kerosene")
        s = s.replace("25ft huskt tape","25 ft husky tape")
        s = s.replace("plastic corrougeted roofing","plastic corrugated roofing")
        s = s.replace("kholerhighland white toilet","kohler highline white toilet")
        s = s.replace("toilet seat for briggs toliet","toilet seat for briggs toilet")
        s = s.replace("steel shelve","steel shelf")
        s = s.replace("dig irritation drip","dig irrigation drip")
        s = s.replace("kohler pedastal sink","kohler pedestal sink")
        s = s.replace("high loss natural jabota","high loss natural jatoba")
        s = s.replace("Huskavarna","Husqvarna")
        s = s.replace("power cordclass 2 power model xy_2900600_u","power cord class 2 power model xy_2900600_u")
        s = s.replace("treaated plywood","treated plywood")
        s = s.replace("air condtioning wall unit","air conditioning wall unit")
        s = s.replace("wall air conditioneer","wall air conditioner")
        s = s.replace("window ac insaller","window ac installer")
        s = s.replace("sensor porch ligts","sensor porch lights")
        s = s.replace("miricile applet or and tray","miracle applet or and tray")
        s = s.replace("paint refil tray","paint refill tray")
        s = s.replace("door knobs exteria","door knobs exterior")
        s = s.replace("exhaustless portable airconditioner","exhaustless portable air conditioner")
        s = s.replace("portable aircondition","portable air conditioner")
        s = s.replace("oscilliating too","oscillating tool")
        s = s.replace("PYWOOD","PLYWOOD")
        s = s.replace("rigid nailer","ridgid nailer")
        s = s.replace("bankoft toilet biscuit","bancroft toilet biscuit")
        s = s.replace("mown pull down faucet","moen pull down faucet")
        s = s.replace("lo gas water heater","low gas water heater")
        s = s.replace("richman water heater","richmond water heater")
        s = s.replace("tall toliet","tall toilet")
        s = s.replace("ridding mower covers","riding mower covers")
        s = s.replace("hole angel  jig","hole angle jig")
        s = s.replace("10 deep kitchen sink porcelin","10 deep kitchen sink porcelain")
        s = s.replace("plastic tiles pcv","plastic tiles pvc")
        s = s.replace("vinyl sheeti","vinyl sheet")
        s = s.replace("samsungelectric ranges","samsung electric ranges")
        s = s.replace("frameless shoer doors","frameless shower doors")
        s = s.replace("webber charcoal grill","weber charcoal grill")
        s = s.replace("kerosine heaters","kerosene heaters")
        s = s.replace("kersone heaters","kerosene heaters")
        s = s.replace("propain heater","propane heater")
        s = s.replace("heating elements for dyer whirlpool","heating elements for dryer whirlpool")
        s = s.replace("safty glasses","safety glasses")
        s = s.replace("eletric stove","electric stove")
        s = s.replace("Schecule 40 Pipe","Schedule 40 Pipe")
        s = s.replace("bayonett saw blades","bayonet saw blades")
        s = s.replace("sconses","sconces")
        s = s.replace("52' pinacle ceiling fan","52' pinnacle ceiling fan")
        s = s.replace("atic  fans with lubers","attic fans with louvers")
        s = s.replace("cealing fans","ceiling fans")
        s = s.replace("hampton bay out door celing fan","hampton bay outdoor ceiling fan")
        s = s.replace("out  door celing fan","outdoor ceiling fan")
        s = s.replace("kitchen exaust fan","kitchen exhaust fan")
        s = s.replace("Cimmaron","Cimarron")
        s = s.replace("fridgedaire","frigidaire")
        s = s.replace("frigidaire washer door striker/catch","frigidaire washer door striker/latch")
        s = s.replace("lawn mover wrench","lawn mower wrench")
        s = s.replace("bmboo lattecie","bamboo lattice")
        s = s.replace("1 handle tub and shower faucet shower and tub vlaves","1 handle tub and shower faucet shower and tub valves")
        s = s.replace("hansgroph faucets bathroom","hansgrohe faucets bathroom")
        s = s.replace("led  light bulbsbulbs","led light bulbs bulbs")
        s = s.replace("landscape srone","landscape stone")
        s = s.replace("braid nailer combo kit","brad nailer combo kit")
        s = s.replace("doors for mobilhomes","doors for mobile homes")
        s = s.replace("smaller closet lights","small closet lights")
        s = s.replace("traficmaster","trafficmaster")
        s = s.replace("hardi  board smooth","hardie board smooth")
        s = s.replace("wainscoating","wainscoting")
        s = s.replace("galvanisedround fire pit ring","galvanized round fire pit ring")
        s = s.replace("electrichot water heaters residential","electric hot water heaters residential")
        s = s.replace("garage shelf unjit","garage shelf unit")
        s = s.replace("stone baxksplash","stone backsplash")
        s = s.replace("pendent cealing fixture","pendant ceiling fixture")
        s = s.replace("undercabinet ligghts","under cabinet lights")
        s = s.replace("martha stewartcabinet pull","martha stewart cabinet pull")
        s = s.replace("4 fluorescant fixture covers","4 fluorescent fixture covers")
        s = s.replace("exterior vanyl french door","exterior vinyl french door")
        s = s.replace("adheasive","adhesive")
        s = s.replace("lineulium floor","linoleum floor")
        s = s.replace("plexiglass selves","plexiglass shelves")
        s = s.replace("Allure mellowood flooring","Allure mellow wood flooring")
        s = s.replace("allure tile sedon?","allure tile sedona?")
        s = s.replace("allure vinyl tilecordoba","allure vinyl tile cordoba")
        s = s.replace("wood veener facing for kitchen cabinets","wood veneer facing for kitchen cabinets")
        s = s.replace("painters plastice","painters plastic")
        s = s.replace("granitne sealer","granite sealer")
        s = s.replace("55 inch cultured marble vanity tope","55 inch cultured marble vanity top")
        s = s.replace("mirros","mirrors")
        s = s.replace("garge floor paint","garage floor paint")
        s = s.replace("weather indoor and outpoor temp","weather indoor and outdoor temp")
        s = s.replace("ryobi blower with batery","ryobi blower with battery")
        s = s.replace("powerwasher hose","power washer hose")
        s = s.replace("mikita 9.5 volt drill","makita 9.5 volt drill")
        s = s.replace("vinal fence straps","vinyl fence straps")
        s = s.replace("black chandelier wjth black shades","black chandelier with black shades")
        s = s.replace("medecine cabinet","medicine cabinet")
        s = s.replace("medicient cabinet","medicine cabinet")
        s = s.replace("serface mount medicine cabinets","surface mount medicine cabinets")
        s = s.replace("husqvarna presure washer","husqvarna pressure washer")
        s = s.replace("back yard weather forecasteer","backyard weather forecaster")
        s = s.replace("chain link fenceing","chain link fencing")
        s = s.replace("jogsaw tool","jigsaw tool")
        s = s.replace("lg ruff wall instalation","lg ruff wall installation")
        s = s.replace("pcv pipe sement","pvc pipe cement")
        s = s.replace("hardi trim","hardietrim")
        s = s.replace("vynal siding insol","vinyl siding insol")
        s = s.replace("cheapete gas 40 gallon hot water heater","cheapest gas 40 gallon hot water heater")
        s = s.replace("powervent water heater","power vent water heater")
        s = s.replace("exterieur door 32 inch","exterior door 32 inch")
        s = s.replace("vynal floor matting","vinyl floor matting")
        s = s.replace("door knobsw","door knobs")
        s = s.replace("black decke weed eaters","black decker weed eaters")
        s = s.replace("lectric string trimmer cst1200r","electric string trimmer cst1200r")
        s = s.replace("1.4 mircowave over the stove","1.4 microwave over the stove")
        s = s.replace("stove excaust fan","stove exhaust fan")
        s = s.replace("mobile home extior doors","mobile home exterior doors")
        s = s.replace("wood lathesw","wood lathes")
        s = s.replace("anderson replacement double hung window 34.5x36.5","andersen replacement double hung window 34.5x 36.5")
        s = s.replace("contrcator baseboard","contractor baseboard")
        s = s.replace("moehn kitchen facet 87211srssd","moen kitchen faucet 87211srs")
        s = s.replace("repare kit for 2-handle side sprayer kitchen faucet","repair kit for 2-handle side sprayer kitchen faucet")
        s = s.replace("ecco friendly garden hose","eco friendly garden hose")
        s = s.replace("flex gardn hose","flex garden hose")
        s = s.replace("garden host 50","garden hose 50")
        s = s.replace("bathroon lighting","bathroom lighting")
        s = s.replace("lanscape timber","landscape timber")
        s = s.replace("bathroom valnity lights","bathroom vanity lights")
        s = s.replace("gas pressure regular","gas pressure regulator")
        s = s.replace("ashely 48 in electric chi","ashley 48 in electric chi")
        s = s.replace("2x6 treted  8ft long","2x6 treated 8ft long")
        s = s.replace("wheel borrow","wheelbarrow")
        s = s.replace("whellbarrow","wheelbarrow")
        s = s.replace("scement bags","cement bags")
        s = s.replace("accordian door","accordion door")
        s = s.replace("Electic Lawn Mowers","Electric Lawn Mowers")
        s = s.replace("hampton bay cabinetscornor cabinetupper","hampton bay cabinets corner cabinet upper")
        s = s.replace("electric pump for sprying","electric pump for spraying")
        s = s.replace("front foor 2 siding","front door 2 siding")
        s = s.replace("whirlpool lgas dryer","whirlpool gas dryer")
        s = s.replace("pressure treated lumber spaint","pressure treated lumber paint")
        s = s.replace("rhee. 40 gallon water heaters","rheem. 40 gallon water heaters")
        s = s.replace("8x96 white decrotive shelf","8x96 white decorative shelf")
        s = s.replace("bathroom pendastal","bathroom pedestal")
        s = s.replace("r25/r30 faced insullation","r25/r30 faced insulation")
        s = s.replace("heavy dutty letter support","heavy duty letter support")
        s = s.replace("ceder decking","cedar decking")
        s = s.replace("negitave air machine","negative air machine")
        s = s.replace("outdoor maouse traps","outdoor mouse traps")
        s = s.replace("storeage shed","storage shed")
        s = s.replace("car canoply","car canopy")
        s = s.replace("commerical tile","commercial tile")
        s = s.replace("1 1/2 colated rock screws","1 1/2 collated rock screws")
        s = s.replace("sheeet rock mud","sheetrock mud")
        s = s.replace("counterdepth fridge","counter depth fridge")
        s = s.replace("maytag refregirator","maytag refrigerator")
        s = s.replace("whirlpool  french door frig 30 wide","whirlpool french door fridge 30 wide")
        s = s.replace("wirlpool 30 wide french door","whirlpool 30 wide french door")
        s = s.replace("dleta shower faucet handles","delta shower faucet handles")
        s = s.replace("38 grainte composit sink","38 granite composite sink")
        s = s.replace("blown in insulaation","blown in insulation")
        s = s.replace("foam insulatino","foam insulation")
        s = s.replace("doors interiorwith door jams","doors interior with door jams")
        s = s.replace("residentialsteel door and frame","residential steel door and frame")
        s = s.replace("wood swimg set kits","wood swing set kits")
        s = s.replace("quickcrete resurfacer","quikrete resurfacer")
        s = s.replace("2 inch srew cap","2 inch screw cap")
        s = s.replace("30 gar builtin ranges","30 gas built in ranges")
        s = s.replace("samsong stive","samsung stove")
        s = s.replace("chissel","chisel")
        s = s.replace("rigid compound miter saw","ridgid compound miter saw")
        s = s.replace("rigid compound miter saw dust pouch","ridgid compound miter saw dust pouch")
        s = s.replace("shampoo and lotion automatice dispenser","shampoo and lotion automatic dispenser")
        s = s.replace("wall scone","wall sconce")
        s = s.replace("rubber for refridgerators","rubber for refrigerators")
        s = s.replace("water proofing shower membrame","waterproofing shower membrane")
        s = s.replace("fridigdaire back gas range","frigidaire black gas range")
        s = s.replace("cabrio dryder","cabrio dryer")
        s = s.replace("whilrpool cabrio dryer","whirlpool cabrio dryer")
        s = s.replace("light switcht sensor","light switch sensor")
        s = s.replace("calutta marble laminate countertop","calcutta marble laminate countertop")
        s = s.replace("vinylcorner boards 4 inch","vinyl corner boards 4 inch")
        s = s.replace("plastix box","plastic box")
        s = s.replace("scurity screen doors","security screen doors")
        s = s.replace("nonadhesive vinyl flooring","non adhesive vinyl flooring")
        s = s.replace("trafficmaster interloclk","trafficmaster interlock")
        s = s.replace("anntenias","antennas")
        s = s.replace("clothes dryer srand","clothes dryer stand")
        s = s.replace("eletric water heater","electric water heater")
        s = s.replace("sharkbike push to connect 3/4","sharkbite push to connect 3/4")
        s = s.replace("fuel nozzle furnance","fuel nozzle furnace")
        s = s.replace("ryobi one batery","ryobi one battery")
        s = s.replace("5/8   floring plywood weatherproof","5/8 flooring plywood weatherproof")
        s = s.replace("mitter saw manual","miter saw manual")
        s = s.replace("selenoid for dryer","solenoid for dryer")
        s = s.replace("presure coated wood","pressure coated wood")
        s = s.replace("composote lumber","composite lumber")
        s = s.replace("14 awgsoilid wire","14 awg solid wire")
        s = s.replace("welded wire fenching 12 gauge","welded wire fencing 12 gauge")
        s = s.replace("patio chair cusions","patio chair cushions")
        s = s.replace("viynl patches","vinyl patches")
        s = s.replace("7 in. stove pie","7 in. stove pipe")
        s = s.replace("whirlpoolgas stove","whirlpool gas stove")
        s = s.replace("whirpool microwave 1.4 cu ft","whirlpool microwave 1.4 cu ft")
        s = s.replace("whirpool refrigerator","whirlpool refrigerator")
        s = s.replace("3' nailes","3' nails")
        s = s.replace("nailer  tooal","nailer tool")
        s = s.replace("weed  barier","weed barrier")
        s = s.replace("oped garage door indicator","open garage door indicator")
        s = s.replace("styrafoam","styrofoam")
        s = s.replace("10 foot step laddert","10 foot step ladder")
        s = s.replace("3 1/2 hardwar","3 1/2 hardware")
        s = s.replace("double control shower vavle","double control shower valve")
        s = s.replace("replacement shower encosure rod","replacement shower enclosure rod")
        s = s.replace("baby gurad gate","baby guard gate")
        s = s.replace("joint compund light weight","joint compound lightweight")
        s = s.replace("sheetrock high preformance joint compound","sheetrock high performance joint compound")
        s = s.replace("1x2 appearnce boards","1x2 appearance boards")
        s = s.replace("lumber 2x8 composit","lumber 2x8 composite")
        s = s.replace("floot ball","float ball")
        s = s.replace("dewalt empact driver","dewalt impact driver")
        s = s.replace("bosh cordless combo set","bosch cordless combo set")
        s = s.replace("ryobi 18v battwery","ryobi 18v battery")
        s = s.replace("kihchen cabinet slidr shelves","kitchen cabinet slide shelves")
        s = s.replace("chesnut border edging","chestnut border edging")
        s = s.replace("outdoor seat cushions 24.5 whte","outdoor seat cushions 24.5 white")
        s = s.replace("12x12 tile msaic","12x12 tile mosaic")
        s = s.replace("skill screwdriver battery","skil screwdriver battery")
        s = s.replace("manual for airens lawnmower","manual for ariens lawn mower")
        s = s.replace("gas stabilisor","gas stabilizer")
        s = s.replace("4 x 4 white pocelain tile","4 x 4 white porcelain tile")
        s = s.replace("rigid pipe cutter","ridgid pipe cutter")
        s = s.replace("24 regrigerators","24 refrigerators")
        s = s.replace("refrigerato 33 inch wide","refrigerator 33 inch wide")
        s = s.replace("smudge proof stainless steele","smudge proof stainless steel")
        s = s.replace("whirpool amana","whirlpool amana")
        s = s.replace("moen banbury 24 in. doubletowel bar","moen banbury 24 in. double towel bar")
        s = s.replace("4' r;ubber top set base","4' rubber top set base")
        s = s.replace("extension  springes","extension springs")
        s = s.replace("grass string trimmer electric homelight","grass string trimmer electric homelite")
        s = s.replace("craftman style lights","craftsman style lights")
        s = s.replace("glacier bay delmare expresso wall mirror","glacier bay del mar espresso wall mirror")
        s = s.replace("dollie 600 lbs","dolly 600 lbs")
        s = s.replace("patio tille","patio tile")
        s = s.replace("eucalptus white board","eucalyptus white board")
        s = s.replace("vynal tile","vinyl tile")
        s = s.replace("heat reducing window flim","heat reducing window film")
        s = s.replace("Porach Light","Porch Light")
        s = s.replace("brissell zing vacuum bags","bissell zing vacuum bags")
        s = s.replace("toillet","toilet")
        s = s.replace("kitchen aid refrigirator light bulb:","kitchenaid refrigerator light bulb:")
        s = s.replace("chadelier","chandelier")
        s = s.replace("cararra marble","carrara marble")
        s = s.replace("coedless makita chainsaw with batteries","cordless makita chainsaw with batteries")
        s = s.replace("mikita cordless drill","makita cordless drill")
        s = s.replace("antique brass hindges for doors","antique brass hinges for doors")
        s = s.replace("riobi battery","ryobi battery")
        s = s.replace("feerzer","freezer")
        s = s.replace("schlade wirell door lock","schlage wireless door lock")
        s = s.replace("water proff board","waterproof board")
        s = s.replace("celing light holder","ceiling light holder")
        s = s.replace("wood toold","wood tools")
        s = s.replace("4 inch insolation","4 inch insulation")
        s = s.replace("Urehtane Foam Sheet","Urethane Foam Sheet")
        s = s.replace("4 center lavatory facuet","4 center lavatory faucet")
        s = s.replace("Shower facuet","Shower faucet")
        s = s.replace("electric dyrer heater elemnet","electric dryer heater element")
        s = s.replace("milluakee drill bits","milwaukee drill bits")
        s = s.replace("scrren wire","screen wire")
        s = s.replace("safegaurd 30 synthetic felt","safeguard 30 synthetic felt")
        s = s.replace("hampden bay chandelier","hampton bay chandelier")
        s = s.replace("1/2 inch pnumatic stapler","1/2 inch pneumatic stapler")
        s = s.replace("12' firetreat 2x4","12' fire treated 2x4")
        s = s.replace("american-standarfairfield elongated one-piece 1.6 gpf toilet","american-standard fairfield elongated one-piece 1.6 gpf toilet")
        s = s.replace("toilet aquaia","toilet aquia")
        s = s.replace("Comercial electric","Commercial electric")
        s = s.replace("light puff defuser","light puff diffuser")
        s = s.replace("ryobi drill prass","ryobi drill press")
        s = s.replace("110v ectric dryers","110v electric dryers")
        s = s.replace("FIRE RESTISTANT BOARD","FIRE RESISTANT BOARD")
        s = s.replace("vinyle plankj","vinyl plank")
        s = s.replace("cordless backpack vaccume","cordless backpack vacuum")
        s = s.replace("hampton baysolar bird lights","hampton bay solar bird lights")
        s = s.replace("kohler chair height elongated toliet","kohler chair height elongated toilet")
        s = s.replace("electic fireplace","electric fireplace")
        s = s.replace("hampton bay jmestown","hampton bay jamestown")
        s = s.replace("surfacemount kitchen sink","surface mount kitchen sink")
        s = s.replace("rigid wet nozzelsqueegee","ridgid wet nozzle squeegee")
        s = s.replace("vacumns","vacuums")
        s = s.replace("gble vent","gable vent")
        s = s.replace("ventalation","ventilation")
        s = s.replace("biinds and shades","blinds and shades")
        s = s.replace("copact drills cordless","compact drills cordless")
        s = s.replace("ridge 18v hammer","ridgid 18v hammer")
        s = s.replace("heavy dutty garden hose","heavy duty garden hose")
        s = s.replace("1/2'  extirior plywood","1/2' exterior plywood")
        s = s.replace("gutter water reflector","gutter water deflector")
        s = s.replace("under cabinet led light accesory pack","under cabinet led light accessory pack")
        s = s.replace("armstroung floor adhesive","armstrong floor adhesive")
        s = s.replace("whirlpoolstainless steel refrig","whirlpool stainless steel refrig")
        s = s.replace("black and decker elctric","black and decker electric")
        s = s.replace("cordless edgere","cordless edger")
        s = s.replace("white electrtical outlets","white electrical outlets")
        s = s.replace("tan unmbrella","tan umbrella")
        s = s.replace("gothic fence picketts","gothic fence pickets")
        s = s.replace("vinyl 1 bilnd","vinyl 1 blinds")
        s = s.replace("console tab;le","console table")
        s = s.replace("T-5 florescent light fixtures","T-5 fluorescent light fixtures")
        s = s.replace("royobi pedestal grinder wheel","ryobi pedestal grinder wheel")
        s = s.replace("wall panaling","wall paneling")
        s = s.replace("PORCH STAIR RAILLING","PORCH STAIR RAILING")
        s = s.replace("micro fibe","microfiber")
        s = s.replace("champion toliet part","champion toilet parts")
        s = s.replace("rr vaccum filter","rr vacuum filter")
        s = s.replace("exhust fan","exhaust fan")
        s = s.replace("corragated metal","corrugated metal")
        s = s.replace("gasolene generaters and inverters","gasoline generators and inverters")
        s = s.replace("stailess steel top stoves","stainless steel top stoves")
        s = s.replace("top freezer refrigeratot","top freezer refrigerator")
        s = s.replace("3/4 inche rock","3/4 inch rock")
        s = s.replace("12 roofing pannel","12 roofing panel")
        s = s.replace("blakck in decker edger","black and decker edger")
        s = s.replace("tile scrapper","tile scraper")
        s = s.replace("brick morter","brick mortar")
        s = s.replace("cement blodks","cement blocks")
        s = s.replace("unmortified mortor","unmodified mortar")
        s = s.replace("bifold door hardw","bifold door hardware")
        s = s.replace("metal scerews","metal screws")
        s = s.replace("sliding doos for backyard","sliding doors for backyard")
        s = s.replace("screen fame corner","screen frame corner")
        s = s.replace("electric lawn mowerectrical","electric lawn mower electrical")
        s = s.replace("clacer bay all n one sink","glacier bay all in one sink")
        s = s.replace("sola water fountain","solar water fountain")
        s = s.replace("closet clothes rackclosetmaid","closet clothes rack closetmaid")
        s = s.replace("passload","paslode")
        s = s.replace("kitchen tile backspl","kitchen tile backsplash")
        s = s.replace("viyle fencing","vinyl fencing")
        s = s.replace("flexible tourche extension","flexible torch extension")
        s = s.replace("6 pnl molded","6 panel molded")
        s = s.replace("soild core flush pre hung door","solid core flush prehung door")
        s = s.replace("convction heater","convection heater")
        s = s.replace("closet orginizer shoe rack wire","closet organizer shoe rack wire")
        s = s.replace("freesstanding","free standing")
        s = s.replace("mmirror closet doors","mirror closet doors")
        s = s.replace("maratha stewart monogram wreath","martha stewart monogram wreath")
        s = s.replace("edsel heavy duty 5","edsal heavy duty 5")
        s = s.replace("11 ft extension cord groud","11 ft extension cord ground")
        s = s.replace("indoor/otdoor extensions cords e176194","indoor/outdoor extension cords e176194")
        s = s.replace("outdoor extention cords e","outdoor extension cords e")
        s = s.replace("unface insulation 23 inches wide","unfaced insulation 23 inches wide")
        s = s.replace("porble toilets","portable toilets")
        s = s.replace("toilet saftey seat","toilet safety seat")
        s = s.replace("silca sand","silica sand")
        s = s.replace("tall 18 in storage cabnet","tall 18 in storage cabinet")
        s = s.replace("20x8 storge shed","20 x 8 storage shed")
        s = s.replace("rubbermade shed","rubbermaid shed")
        s = s.replace("rubbermaid resin storage cabnetsn","rubbermaid resin storage cabinets")
        s = s.replace("cedar wod chips","cedar wood chips")
        s = s.replace("hidraulic tools","hydraulic tools")
        s = s.replace("celing fans with lighting and remote","ceiling fans with lighting and remote")
        s = s.replace("fridigidaire drop in oven","frigidaire drop in oven")
        s = s.replace("tub surround pices","tub surround prices")
        s = s.replace("allure flooring oak expresso","allure flooring oak espresso")
        s = s.replace("pass and seymore light cover switch","pass and seymour light cover switch")
        s = s.replace("28x54 replacment window","28x54 replacement windows")
        s = s.replace("anderson windows new constraction","anderson windows new construction")
        s = s.replace("swamp  oolers","swamp coolers")
        s = s.replace("wahing machines","washing machines")
        s = s.replace("interior primed mdf crown mouldin","interior primed mdf crown moulding")
        s = s.replace("built in convectionoven","built in convection oven")
        s = s.replace("flpwers for your garden","flowers for your garden")
        s = s.replace("closetr rod","closet rod")
        s = s.replace("unfinished wide bplanked hickory flooring","unfinished wide plank hickory flooring")
        s = s.replace("48v to 110 invertor","48v to 110v inverter")
        s = s.replace("landscape  wateting","landscape watering")
        s = s.replace("sockets for  fluorescence fixtres","sockets for fluorescent fixtures")
        s = s.replace("woodceramic floor tile","wood ceramic floor tile")
        s = s.replace("brigsg and stations 500 seris","briggs and stations 500 series")
        s = s.replace("green carpert","green carpet")
        s = s.replace("pressure treated step tread 6ft","pressure treated stair tread 6ft")
        s = s.replace("hand pump gfor water","hand pump for water")
        s = s.replace("rutic lighting","rustic lighting")
        s = s.replace("cender blocks","cinder blocks")
        s = s.replace("talsrar","talstar")
        s = s.replace("rybi power tools","ryobi power tools")
        s = s.replace("portercable 6 gal","porter cable 6 gal")
        s = s.replace("table covers waterproff","table covers waterproof")
        s = s.replace("solid alium square tubing","solid aluminum square tubing")
        s = s.replace("deck post jhardware","deck post hardware")
        s = s.replace("hunter new bronzel fans","hunter new bronze fans")
        s = s.replace("16d framin","16d framing")
        s = s.replace("moen brushed nickel batharoom","moen brushed nickel bathroom")
        s = s.replace("barriar plastic","barrier plastic")
        s = s.replace("window ac/hehat  units","window ac/heat units")
        s = s.replace("icycle lights","icicle lights")
        s = s.replace("4 gallon expanion","4 gallon expansion")
        s = s.replace("floor mount lawndry seek","floor mount laundry sink")
        s = s.replace("high addhesion primer","high adhesion primer")
        s = s.replace("24 gauge wire connectorsa","24 gauge wire connectors")
        s = s.replace("sterio wire for indoor speakers","stereo wire for indoor speakers")
        s = s.replace("garage bicyclestorage","garage bicycle storage")
        s = s.replace("how mustall tankless water heater","how install tankless water heater")
        s = s.replace("chelsea white acrylic oval in rectangl","chelsea white acrylic oval in rectangle")
        s = s.replace("cleaning jeta for whirlpool","cleaning jets for whirlpool")
        s = s.replace("bathroom faucet replacment valve","bathroom faucet replacement valve")
        s = s.replace("3x5 cemet board","3x5 cement board")
        s = s.replace("vaccumm","vacuum")
        s = s.replace("ghroe shower headstrong shower heads","grohe shower headstrong shower heads")
        s = s.replace("mial boxes","mail boxes")
        s = s.replace("claw tups","claw tips")
        s = s.replace("facia corner brace","fascia corner brace")
        s = s.replace("pegisas sink top","pegasus sink top")
        s = s.replace("mirroes for doors","mirrors for doors")
        s = s.replace("counter depth refridgidere","counter depth refrigerator")
        s = s.replace("corrigaed fiberglass roofing","corrugated fiberglass roofing")
        s = s.replace("window airconditionerwith heaters","window air conditioners with heaters")
        s = s.replace("extention rail for opener","extension rail for opener")
        s = s.replace("whitecomposite fascia board","white composite fascia board")
        s = s.replace("vanity topp 31 white","vanity top 31 white")
        s = s.replace("underhood range fan","under hood range fan")
        s = s.replace("price pfister  trevisa","price pfister treviso")
        s = s.replace("milwaukee cordlees tools","milwaukee cordless tools")
        s = s.replace("pendent light","pendant light")
        s = s.replace("pre-emergent weed contro","pre-emergent weed control")
        s = s.replace("is this item in stoes?","is this item in store?")
        s = s.replace("door home secutity","door home security")
        s = s.replace("3oo watt haalogen bulbs","3oo watt halogen bulbs")
        s = s.replace("96 in flourescent bulbs","96 in fluorescent bulbs")
        s = s.replace("shop ceiling fane","shop ceiling fan")
        s = s.replace("aaa batteries everready gold","aaa batteries eveready gold")
        s = s.replace("buth tub faucet","bathtub faucet")
        s = s.replace("delta montecello tub faucet","delta monticello tub faucet")
        s = s.replace("ge spring water heater","geospring water heater")
        s = s.replace("ge water heater egnighter","ge water heater igniter")
        s = s.replace("31x19 one piecs bathroom sink","31x19 one piece bathroom sink")
        s = s.replace("replacment clips for wire rack","replacement clips for wire rack")
        s = s.replace("ac air diverer","ac air diverter")
        s = s.replace("3 sewer pipce","3 sewer pipe")
        s = s.replace("3' electical pipe","3' electrical pipe")
        s = s.replace("large outside horizontal storage shed","large outdoor horizontal storage shed")
        s = s.replace("swing hangar hardware","swing hanger hardware")
        s = s.replace("dim able balafon flood light","dimmable balafon flood light")
        s = s.replace("phillips exterior led","philips exterior led")
        s = s.replace("banity 11 watt light bulb","vanity 11 watt light bulb")
        s = s.replace("kithchen install","kitchen install")
        s = s.replace("magnet stainless steel for diswasher","magnet stainless steel for dishwasher")
        s = s.replace("phone  spliter","phone splitter")
        s = s.replace("receptical","receptacle")
        s = s.replace("water resistent electrical outlets","water resistant electrical outlets")
        s = s.replace("kitchenaid superb oven","kitchenaid superba oven")
        s = s.replace("403esprit 2x4 ceing tile","403 esprit 2x4 ceiling tile")
        s = s.replace("wall excess panel","wall access panel")
        s = s.replace("drop celing tiles","drop ceiling tiles")
        s = s.replace("pvc drop in celing tiles","pvc drop in ceiling tiles")
        s = s.replace("pl gas hose","lp gas hose")
        s = s.replace("12 v landscaping ligtening fixture","12v landscape lighting fixture")
        s = s.replace("behr white external semigloss paint","behr white exterior semi gloss paint")
        s = s.replace("GRAGE DOOR OPENER","GARAGE DOOR OPENER")
        s = s.replace("grage doors","garage doors")
        s = s.replace("24 inch med oak base","24 inch medium oak base")
        s = s.replace("okeefes working hands","o'keeffe's working hands")
        s = s.replace("phenofin","penofin")
        s = s.replace("8 foot galvinezed","8 foot galvanized")
        s = s.replace("12 mobil home air duct","12 mobile home air duct")
        s = s.replace("door hinges for americana refrigator","door hinges for americana refrigerator")
        s = s.replace("tub drain kit bronz","tub drain kit bronze")
        s = s.replace("halligon light bulb","halogen light bulb")
        s = s.replace("husky rachet","husky ratchet")
        s = s.replace("andersen vnyl windows","andersen vinyl windows")
        s = s.replace("balwind double cilynder lock","baldwin double cylinder lock")
        s = s.replace("drop down ceiling ppanel","drop down ceiling panel")
        s = s.replace("arearugs and mats","area rugs and mats")
        s = s.replace("dark expresso paint for wood","dark espresso paint for wood")
        s = s.replace("melamine shelvees","melamine shelves")
        s = s.replace("mosaic whitel and black tile","mosaic white and black tile")
        s = s.replace("8 wre wheel","8 wire wheel")
        s = s.replace("9'  plna replament blade","9' plane replacement blade")
        s = s.replace("saw zall blades","sawzall blades")
        s = s.replace("pain pot","paint pot")
        s = s.replace("drain cleaneraner machines","drain cleaner machines")
        s = s.replace("anderson storm doors pet","andersen storm doors pet")
        s = s.replace("basement window replacement insructions","basement window replacement instructions")
        s = s.replace("grill cover brinkman double grill","grill cover brinkmann double grill")
        s = s.replace("gerber daisies","gerbera daisies")
        s = s.replace("gerber daisy","gerbera daisy")
        s = s.replace("exterior wood stainolid color","exterior wood stain color")
        s = s.replace("2700 br30 led","2700k br30 led")
        s = s.replace("3m wheather stripping","3m weather stripping")
        s = s.replace("barn doorhinges","barn door hinges")
        s = s.replace("plywood progect","plywood project")
        s = s.replace("28 guage screen","28 gauge screen")
        s = s.replace("lampsade pendent light","lamp shade pendant light")
        s = s.replace("kitchen cabiner corner","kitchen cabinet corner")
        s = s.replace("paatio swings","patio swings")
        s = s.replace("12 bar chian for echo","12 bar chain for echo")
        s = s.replace("bix max 7x7","big max 7x7")
        s = s.replace("bathtub faucethandle replacement parts","bathtub faucet handle replacement parts")
        s = s.replace("prelit spiral trees","pre lit spiral trees")
        s = s.replace("12 sthel chainsaws","12 stihl chainsaws")
        s = s.replace("10 ft drain house","10 ft drain hose")
        s = s.replace("american standard tiolet flappers","american standard toilet flappers")
        s = s.replace("solar out doors post lights","solar outdoor post lights")
        s = s.replace("kitchen cabinet with counertop","kitchen cabinet with countertop")
        s = s.replace("Painting Cabniets","Painting Cabinets")
        s = s.replace("18x18 teracota porcelain floor tiles","18x18 terracotta porcelain floor tiles")
        s = s.replace("drywal","drywall")
        s = s.replace("pencle trim tile","pencil trim tile")
        s = s.replace("vinyl latice","vinyl lattice")
        s = s.replace("angle findeer","angle finder")
        s = s.replace("laminate tile comercial","laminate tile commercial")
        s = s.replace("couner deep refrigerators","counter deep refrigerators")
        s = s.replace("chritmas tree","christmas tree")
        s = s.replace("plug in carbon monoxcide","plug in carbon monoxide")
        s = s.replace("cabinet handels","cabinet handles")
        s = s.replace("frigidair drop in","frigidaire drop in")
        s = s.replace("7' hex hed bolt","7' hex head bolt")
        s = s.replace("vent fllters","vent filters")
        s = s.replace("horizontall","horizontal")
        s = s.replace("3 x 6 blace tile","3 x 6 black tile")
        s = s.replace("rostoluem  spray paint","rustoleum spray paint")
        s = s.replace("power drill battery an charger","power drill battery and charger")
        s = s.replace("rayobi blue charger","ryobi blue charger")
        s = s.replace("robyi","ryobi")
        s = s.replace("5/4 pressure treaded decking","5/4 pressure treated decking")
        s = s.replace("white carrara herring bome","white carrara herringbone")
        s = s.replace("sailr blue","sailor blue")
        s = s.replace("charbroil classic","char broil classic")
        s = s.replace("14 electric concrete saw with vc-u dch300","14 electric concrete saw with vac-u dch 300")
        s = s.replace("potable air conditioners","portable air conditioners")
        s = s.replace("fin heating  tubeing","fin heating tubing")
        s = s.replace("fine/line baseboarrd","fine/line baseboard")
        s = s.replace("hot water heating eliment","hot water heating element")
        s = s.replace("toiet","toilet")
        s = s.replace("hole house fan","whole house fan")
        s = s.replace("montaga bay tile","montego bay tile")
        s = s.replace("40 gal liquid propan","40 gal liquid propane")
        s = s.replace("4 x 4 pos cap","4x4 post cap")
        s = s.replace("white quartz cointertop","white quartz countertop")
        s = s.replace("elongated bone toilest","elongated bone toilet")
        s = s.replace("white acryl paint","white acrylic paint")
        s = s.replace("foundstion vents","foundation vents")
        s = s.replace("sqeaky carpet stair kit","squeaky carpet stair kit")
        s = s.replace("defusiers for floors","diffusers for floors")
        s = s.replace("8' galvanized roll top edginh","8' galvanized roll top edging")
        s = s.replace("marithon water heater element","marathon water heater element")
        s = s.replace("wirerless light switch","wireless light switch")
        s = s.replace("moen posi-temp tim kit","moen posi-temp trim kit")
        s = s.replace("shower dooroil rubbed bronze","shower door oil rubbed bronze")
        s = s.replace("wireing","wiring")
        s = s.replace("kitchen aid architecs series 11","kitchenaid architect series 11")
        s = s.replace("wall oven combon","wall oven combo")
        s = s.replace("survival babkpack","survival backpack")
        s = s.replace("wire dstaples","wire staples")
        s = s.replace("4in drain gratewhite","4in drain grate white")
        s = s.replace("shitch cover","switch cover")
        s = s.replace("vitarera quartz","viatera quartz")
        s = s.replace("5/8-in masonary drill bit","5/8-in masonry drill bit")
        s = s.replace("brinkman grill grates","brinkmann grill grates")
        s = s.replace("pest repellant","pest repellent")
        s = s.replace("bathun drain plunger","bathtub drain plunger")
        s = s.replace("incounter gas cook range","encounter gas cook range")
        s = s.replace("peat moss bails","peat moss bales")
        s = s.replace("3-piece bath accessory kit in chrom","3-piece bath accessory kit in chrome")
        s = s.replace("alameda hickey laminate","alameda hickory laminate")
        s = s.replace("flooring moisture barier","flooring moisture barrier")
        s = s.replace("vinylcove base","vinyl cove base")
        s = s.replace("ge diswasher","ge dishwasher")
        s = s.replace("b10  led bub","b10 led bulb")
        s = s.replace("cub cadetcordless hedge trimmer","cub cadet cordless hedge trimmer")
        s = s.replace("hampton bay jewelery armoire wht","hampton bay jewelry armoire white")
        s = s.replace("perenials","perennials")
        s = s.replace("heat ventss","heat vents")
        s = s.replace("mobil home glass door","mobile home glass door")
        s = s.replace("lamanet floor cutter","laminate floor cutter")
        s = s.replace("on off valvefor tub faucet","on off valve for tub faucet")
        s = s.replace("assie grill fire and ash","aussie grill fire and ash")
        s = s.replace("hanging worklight fixtures ceiling","hanging work light fixtures ceiling")
        s = s.replace("20 amp tamper resitance duplex receptacle","20 amp tamper resistant duplex receptacle")
        s = s.replace("liqwuid nail","liquid nail")
        s = s.replace("1/2 tee pvcp","1/2 tee pvc")
        s = s.replace("toilet repair kit cadet 3 flowise 2-piece 1.28 gpf round fro","toilet repair kit cadet 3 flowise 2-piece 1.28 gpf round front")
        s = s.replace("50 amp turn look plug","50 amp turn lock plug")
        s = s.replace("6x6 colunm caps","6x6 column caps")
        s = s.replace("12 valleta","12 valletta")
        s = s.replace("pellitized lime","pelletized lime")
        s = s.replace("concrete sonic tub","concrete sonic tube")
        s = s.replace("110 air conditior an heat","110 air conditioner and heat")
        s = s.replace("what is best for settingfence  posts in soil?","what is best for setting fence posts in soil?")
        s = s.replace("washer dryer folding worksurface","washer dryer folding work surface")
        s = s.replace("outdoor spigot spliter","outdoor spigot splitter")
        s = s.replace("alumiunm gate","aluminum gate")
        s = s.replace("lawm mower","lawn mower")
        s = s.replace("door floor plate  slideing doors","door floor plate sliding doors")
        s = s.replace("akkegro","allegro")
        s = s.replace("wead burner","weed burner")
        s = s.replace("galvinized nails 3","galvanized nails 3")
        s = s.replace("artifical turf border","artificial turf border")
        s = s.replace("oppeuss light trim ring","oppeus light trim ring")
        s = s.replace("12 ft john boat","12ft jon boat")
        s = s.replace("outdoor coucg","outdoor couch")
        s = s.replace("drywall panel hoisst","drywall panel hoist")
        s = s.replace("ego   hainsaw","ego chainsaw")
        s = s.replace("hibascus plant","hibiscus plant")
        s = s.replace("pullbehind fertilizer spreader","pull behind fertilizer spreader")
        s = s.replace("door latch uard","door latch guard")
        s = s.replace("water suppy box","water supply box")
        s = s.replace("octagon eve vents","octagon eave vents")
        s = s.replace("el ctrical s ez","electrical sez")
        s = s.replace("varnishe","varnish")
        s = s.replace("klien rg6","klein rg6")
        s = s.replace("floor matt","floor mat")
        s = s.replace("60 shower ddor","60 shower door")
        s = s.replace("blue tapeexhaust fan/light","blue tape exhaust fan/light")
        s = s.replace("rocks hydrophonics","rocks hydroponics")
        s = s.replace("mesquito spray","mosquito spray")
        s = s.replace("alumiun grove in","aluminum grove in")
        s = s.replace("lithonia outdoor wall paks","lithonia outdoor wall packs")
        s = s.replace("60 in. shower door brushed nicker","60 in. shower door brushed nickel")
        s = s.replace("makit 12v","makita 12v")
        s = s.replace("black and yellow non skip tape","black and yellow non skid tape")
        s = s.replace("skylifghts","skylights")
        s = s.replace("led hale gin g9","led halogen g9")
        s = s.replace("electrical pipe flexable","electrical pipe flexible")
        s = s.replace("emt stroas","emt straps")
        s = s.replace("ridged 1 emt conduit","rigid 1 emt conduit")
        s = s.replace("baliey window roller shades","bailey window roller shades")
        s = s.replace("hampton bay reswood valley 5 pc patio seating set with fire","hampton bay redwood valley 5 pc patio seating set with fire")
        s = s.replace("lawn grass catchbag","lawn grass catcher bag")
        s = s.replace("1/4 lauwan under layment","1/4 lauan underlayment")
        s = s.replace("window tintinig","window tinting")
        s = s.replace("4 inch round bellbox cover","4 inch round bell box cover")
        s = s.replace("vinal latice fence","vinyl lattice fence")
        s = s.replace("solar pest repelers","solar pest repellers")
        s = s.replace("barn doorspring latches","barn door spring latches")
        s = s.replace("3 gauge copper phhn","3 gauge copper thhn")
        s = s.replace("three wire hottube","three wire hot tub")
        s = s.replace("shope cloths","shop clothes")
        s = s.replace("bbostitch tool set","bostitch tool set")
        s = s.replace("outdoor hightop dining","outdoor high top dining")
        s = s.replace("delata raincan","delta raincan")
        s = s.replace("soap wash maching tilde","soap wash machine tilde")
        s = s.replace("16 ftdecking boards","16 ft decking boards")
        s = s.replace("1 amp receptical","1 amp receptacle")
        s = s.replace("outdoor gfi","outdoor gfci")
        s = s.replace("bbq burner replacment","bbq burner replacement")
        s = s.replace("levin 25 wat usb","levin 25 watt usb")
        s = s.replace("delta diverte rhandle in rb","delta diverter handle in rb")
        s = s.replace("3 pane craftsman door","3 panel craftsman door")
        s = s.replace("charolettetown","charlottetown")
        s = s.replace("raised toelit sseat","raised toilet seat")
        s = s.replace("webber spirit gas grill","weber spirit gas grill")
        s = s.replace("adapter for extention cord","adapter for extension cord")
        s = s.replace("bathrub and shower wall kits","bathtub and shower wall kits")
        s = s.replace("sofit vents 4x16","soffit vents 4 x 16")
        s = s.replace("1/2 inch isp water supply line","1/2 inch ips water supply line")
        s = s.replace("eurothem thermostatic valve","eurotherm thermostatic valve")
        s = s.replace("plactic totes  36 inches wide","plastic totes 36 inches wide")
        s = s.replace("pest control diat","pest control diet")
        s = s.replace("black cobwoys star","black cowboys star")
        s = s.replace("whirpool oven 5.1","whirlpool oven 5.1")
        s = s.replace("min fridges for campers","mini fridges for campers")
        s = s.replace("howards restore a finish","howards restor a finish")
        s = s.replace("ge just cut fraiser fur","ge just cut fraser fir")
        s = s.replace("25 watt warmlight bulb","25 watt warm light bulb")
        s = s.replace("kichen island","kitchen island")
        s = s.replace("duel mount stainless steel sinks","dual mount stainless steel sinks")
        s = s.replace("home sevalance cameras","home surveillance cameras")
        s = s.replace("marbel vinyl tile","marble vinyl tile")
        s = s.replace("30 entry door 9 litr","30 entry door 9 lite")
        s = s.replace("roxul sale n sound","roxul safe n sound")
        s = s.replace("4 guage use","4 gauge use")
        s = s.replace("jigsaw  tblades","jigsaw t blades")
        s = s.replace("jigsaww blades","jigsaw blades")
        s = s.replace("clawfoot tub cutain","clawfoot tub curtain")
        s = s.replace("raised garden  ed","raised garden bed")
        s = s.replace("58.75x80 sliding glass door","58.75x 80 sliding glass door")
        s = s.replace("1/4 nich tee","1/4 inch tee")
        s = s.replace("alluminun wire splice","aluminum wire splice")
        s = s.replace("2 sheet metal screrw","2 sheet metal screw")
        s = s.replace("non electically conductive epoxy","non electrically conductive epoxy")
        s = s.replace("led fluoreecent light replacement","led fluorescent light replacement")
        s = s.replace("t8 8 ft 4-light flourescent fixture","t8 8 ft 4-light fluorescent fixture")
        s = s.replace("othor ant killer","ortho ant killer")
        s = s.replace("spectacide for lawnscarpenter ants","spectracide for lawns carpenter ants")
        s = s.replace("ccurved shower door","curved shower door")
        s = s.replace("4in pvc electrcial boxes","4in pvc electrical boxes")
        s = s.replace("hampton bay fan replacemtn","hampton bay fan replacement")
        s = s.replace("6' remodel can valted celing  cans","6' remodel can vaulted ceiling cans")
        s = s.replace("roman tub faucers","roman tub faucets")
        s = s.replace("flourescent paint by rustoleum","fluorescent paint by rustoleum")
        s = s.replace("hidden fastners","hidden fasteners")
        s = s.replace("otdoor sola","outdoor solar")
        s = s.replace("solar post l8ghts","solar post lights")
        s = s.replace("plus 3 tintet","plus 3 tinted")
        s = s.replace("barbeque tools","barbecue tools")
        s = s.replace("circular flourecent lights","circular fluorescent lights")
        s = s.replace("rain barrells","rain barrels")
        s = s.replace("gagarage storage cabinets","garage storage cabinets")
        s = s.replace("brown blasplash tile","brown backsplash tile")
        s = s.replace("evap cooler theromsat","evap cooler thermostat")
        s = s.replace("undergroud telephone wire","underground telephone wire")
        s = s.replace("cop mail adapter","cop male adapter")
        s = s.replace("set crews for glass","set screws for glass")
        s = s.replace("roybi lazer circular saw","ryobi laser circular saw")
        s = s.replace("walnuit stain","walnut stain")
        s = s.replace("ruber door extension","rubber door extension")
        s = s.replace("home decorators cinamon","home decorators cinnamon")
        s = s.replace("apoxy patch","epoxy patch")
        s = s.replace("batroom fan heater light","bathroom fan heater light")
        s = s.replace("commercial radient ceiling heaters","commercial radiant ceiling heaters")
        s = s.replace("surveilance camera","surveillance camera")
        s = s.replace("tub facet set","tub faucet set")
        s = s.replace("solistone pebbble","solistone pebble")
        s = s.replace("1 1/4 galvenized steel pipe fittings","1 1/4 galvanized steel pipe fittings")
        s = s.replace("22.4 cubit feet refrigerator","22.4 cubic feet refrigerator")
        s = s.replace("behr premium plus ultrta","behr premium plus ultra")
        s = s.replace("autoficial grass","artificial grass")
        s = s.replace("huskey scocket set","husky socket set")
        s = s.replace("husky black toll boxes","husky black tool boxes")
        s = s.replace("isunderlayment requiered for metal roof","is underlayment required for metal roof")
        s = s.replace("safety glass with perscription","safety glass with prescription")
        s = s.replace("polished brass 8 spread lavitory faucet","polished brass 8 spread lavatory faucet")
        s = s.replace("heat only therostats","heat only thermostats")
        s = s.replace("65 watt dim able","65 watt dimmable")
        s = s.replace("1-1/4 pocket hole screwsw","1-1/4 pocket hole screws")
        s = s.replace("wwod floor runner","wood floor runner")
        s = s.replace("bostic wood floor glue","bostik wood floor glue")
        s = s.replace("hand shovles","hand shovels")
        s = s.replace("garage orgnize","garage organizer")
        s = s.replace("diamond plate storge unit","diamond plate storage unit")
        s = s.replace("silcone","silicone")
        s = s.replace("packing suplies","packing supplies")
        s = s.replace("ridgid planner","ridgid planer")
        s = s.replace("shower fiberglas","shower fiberglass")
        s = s.replace("curtain rod wrp","curtain rod wrap")
        s = s.replace("fire place accessories gas loggs","fireplace accessories gas logs")
        s = s.replace("recesseingd light housing","recessed light housing")
        s = s.replace("100 amps circuit braker","100 amps circuit breaker")
        s = s.replace("delta satin nickle shower systems","delta satin nickel shower systems")
        s = s.replace("auqatic shower & bath","aquatic shower")
        s = s.replace("termini mosquito garlic spray","terminix mosquito garlic spray")
        s = s.replace("arbourist safety climbing belt","arborist safety climbing belt")
        s = s.replace("vynal wood fence","vinyl wood fence")
        s = s.replace("acrylic primere","acrylic primer")
        s = s.replace("20' facia board","20' fascia board")
        s = s.replace("17 1/2 high tolite","17 1/2 high toilet")
        s = s.replace("howard restore a finish","howard restor a finish")
        s = s.replace("tub enclouseure with tub","tub enclosure with tub")
        s = s.replace("leaf guards for stomr windows","leaf guards for storm windows")
        s = s.replace("sliding tub soors","sliding tub doors")
        s = s.replace("amdry wallpanel","amdry wall panel")
        s = s.replace("22.1 refrierator","22.1 refrigerator")
        s = s.replace("fram boxes","frame boxes")
        s = s.replace("patio  tbricks","patio bricks")
        s = s.replace("6 foot treshold","6 foot threshold")
        s = s.replace("florencet light cover","fluorescent light cover")
        s = s.replace("taracota drain pan","terracotta drain pan")
        s = s.replace("smaller single deadbolt lock","small single deadbolt lock")
        s = s.replace("lmainate boards","laminate boards")
        s = s.replace("acuria lattace panels","acurio lattice panels")
        s = s.replace("adirondeck cusion","adirondack cushion")
        s = s.replace("oscilating fan","oscillating fan")
        s = s.replace("washing machine plug adapator","washing machine plug adapter")
        s = s.replace("concrette pier","concrete pier")
        s = s.replace("southren gray tile","southern gray tile")
        s = s.replace("dealt portable table saw table","dewalt portable table saw table")
        s = s.replace("matte heat resistant pain","matte heat resistant paint")
        s = s.replace("White Temper Resistant Duplex Outlet","White Tamper Resistant Duplex Outlet")
        s = s.replace("screws for deckin","screws for decking")
        s = s.replace("20 gl. hose end sprayer","20 gal. hose end sprayer")
        s = s.replace("sliding door storage cabi nets","sliding door storage cabinets")
        s = s.replace("tinted masonary sealer","tinted masonry sealer")
        s = s.replace("kids toilet seateat","kids toilet seat eat")
        s = s.replace("anderson storm door screen roller","andersen storm door screen roller")
        s = s.replace("vaccuum cleaners for hardwood and carpet","vacuum cleaners for hardwood and carpet")
        s = s.replace("copper baluseter","copper baluster")
        s = s.replace("aluninion circular blade","aluminium circular blade")
        s = s.replace("ceiling light nickle 2-light","ceiling light nickel 2-light")
        s = s.replace("adirondac, patio chair","adirondack, patio chair")
        s = s.replace("flourescent tube","fluorescent tube")
        s = s.replace("polyurethane adhesiv","polyurethane adhesive")
        s = s.replace("extirior clear spray paint","exterior clear spray paint")
        s = s.replace("outdoor faucwts","outdoor faucets")
        s = s.replace("asphaul based coating","asphalt based coating")
        s = s.replace("3/8 couipling","3/8 coupling")
        s = s.replace("2x4x10 pressure treater","2x4x10 pressure treated")
        s = s.replace("koehler faucet","kohler faucet")
        s = s.replace("led rop light clips","led rope light clips")
        s = s.replace("square d double brakers","square d double breakers")
        s = s.replace("30 inchesbathroom vanity","30 inches bathroom vanity")
        s = s.replace("1/2 ' copper fiting","1/2 ' copper fitting")
        s = s.replace("capital cap for colum","capital cap for column")
        s = s.replace("grass turf pavewrs","grass turf pavers")
        s = s.replace("lowvoltage indoor accent lights","low voltage indoor accent lights")
        s = s.replace("dremel minimate cordless moto tool","dremel minimite cordless moto tool")
        s = s.replace("96 right hand miter tyhoon ice","96 right hand miter typhoon ice")
        s = s.replace("magnet base tool loight","magnetic base tool light")
        s = s.replace("robi 18v saw","ryobi 18v saw")
        s = s.replace("5 light hanging chandielier","5 light hanging chandelier")
        s = s.replace("Moem faucet repair","Moen faucet repair")
        s = s.replace("3x6 daltile white 101 kohler","3x6 daltile white k101 kohler")
        s = s.replace("lock cmbo","lock combo")
        s = s.replace("trimmer/edger's, gas powered","trimmer/edgers, gas powered")
        s = s.replace("generaor for fridge","generator for fridge")
        s = s.replace("led light bulbs dimable spot","led light bulbs dimmable spot")
        s = s.replace("outdoor seatting cushions","outdoor seating cushions")
        s = s.replace("full size frigde","full size fridge")
        s = s.replace("ASHPHALT SEALER","ASPHALT SEALER")
        s = s.replace("behr ultra pint","behr ultra paint")
        s = s.replace("emparador mosaic bamboo brick","emperador mosaic bamboo brick")
        s = s.replace("bath mirror cabintes","bath mirror cabinets")
        s = s.replace("floor squeege","floor squeegee")
        s = s.replace("squeege","squeegee")
        s = s.replace("allure golden oaksku579331","allure golden oak sku 579331")
        s = s.replace("artificial turf for petrs","artificial turf for pets")
        s = s.replace("8 foot florescent light bulb","8 foot fluorescent light bulb")
        s = s.replace("3x3 diamond thread plate","3x3 diamond tread plate")
        s = s.replace("handical rail","handicap rail")
        s = s.replace("moen grab bar securemount","moen grab bar secure mount")
        s = s.replace("ceiling mount electical box","ceiling mount electrical box")
        s = s.replace("stainless steal hose clamps","stainless steel hose clamps")
        s = s.replace("sod grass san agustino","sod grass san agustin")
        s = s.replace("bateries  9v","batteries 9v")
        s = s.replace("kohler brushed nickle framless shower doors","kohler brushed nickel frameless shower doors")
        s = s.replace("mirro shower doors","mirror shower doors")
        s = s.replace("daylillies","daylilies")
        s = s.replace("fridgedaire fridge","frigidaire fridge")
        s = s.replace("storage buiding 12' x 20'","storage building 12' x 20'")
        s = s.replace("pvc valvez","pvc valves")
        s = s.replace("socket magnectic extension","socket magnetic extension")
        s = s.replace("shop vac aacessories","shop vac accessories")
        s = s.replace("roll jp door","roll up door")
        s = s.replace("rollup door","roll up door")
        s = s.replace("steibler eltron","stiebel eltron")
        s = s.replace("liquid itght non metalic","liquid tight non metallic")
        s = s.replace("metalic lquid tight","metallic liquid tight")
        s = s.replace("22 bin plastic drawer parts storage organiz","22 bin plastic drawer parts storage organizer")
        s = s.replace("marroon roof screws","maroon roof screws")
        s = s.replace("battery opererated lighting","battery operated lighting")
        s = s.replace("roybi pop up","ryobi pop up")
        s = s.replace("connectorv 30","connector 30")
        s = s.replace("ge gfi braker 30amp","ge gfci breaker 30 amp")
        s = s.replace("pipe swer","pipe sewer")
        s = s.replace("treaded pvc pipe fitting","threaded pvc pipe fitting")
        s = s.replace("cornewr bathtub","corner bathtub")
        s = s.replace("whirlpool apron bathtup","whirlpool apron bathtub")
        s = s.replace("veranda facia","veranda fascia")
        s = s.replace("rrecessed light trim ring","recessed light trim ring")
        s = s.replace("1 light steele sconce","1 light steel sconce")
        s = s.replace("7' 90 elboq","7' 90 elbow")
        s = s.replace("drawer guides and slides","drawer glides and slides")
        s = s.replace("christmsa dog","christmas dog")
        s = s.replace("light weight coccrete","lightweight concrete")
        s = s.replace("hardwoo flooring 2 1/4 in","hardwood flooring 2 1/4 in")
        s = s.replace("garden hose filter attactchent","garden hose filter attachment")
        s = s.replace("milwaukie saw blades","milwaukee saw blades")
        s = s.replace("dewalt extention cord","dewalt extension cord")
        s = s.replace("hampton bay high gloss jabot laminate","hampton bay high gloss jatoba laminate")
        s = s.replace("20v blacker and decker charger","20v black and decker charger")
        s = s.replace("15 water depth bathub","15 water depth bathtub")
        s = s.replace("magnetized wall covering","magnetic wall covering")
        s = s.replace("fire brick and morter","fire brick and mortar")
        s = s.replace("anderson french wood patio door 400 series","andersen frenchwood patio door 400 series")
        s = s.replace("outdoor baners","outdoor banners")
        s = s.replace("osciallating blade to cut tile","oscillating blade to cut tile")
        s = s.replace("one way valae","one way valve")
        s = s.replace("black decker matris","black decker matrix")
        s = s.replace("makita skill saw","makita skil saw")
        s = s.replace("tuscon patio pavers","tucson patio pavers")
        s = s.replace("plastic florring","plastic flooring")
        s = s.replace("fungicidal seed innoculant","fungicidal seed inoculant")
        s = s.replace("pcv coated hardware cloth","pvc coated hardware cloth")
        s = s.replace("2x2 ceiling tilepantq22s","2x2 ceiling tile paint 22s")
        s = s.replace("rectangulat wihite ceramic sink bathroom","rectangular white ceramic sink bathroom")
        s = s.replace("battery operataed wall light","battery operated wall light")
        s = s.replace("72 inchtrack light","72 inch track light")
        s = s.replace("suny citrus fertilizer","sunny citrus fertilizer")
        s = s.replace("48 inch aluminum shower curtin rod","48 inch aluminum shower curtain rod")
        s = s.replace("dehumidifyer","dehumidifier")
        s = s.replace("earthquaike","earthquake")
        s = s.replace("phillips led sparkle  light bulbs","philips led sparkle light bulbs")
        s = s.replace("metalic silver spray","metallic silver spray")
        s = s.replace("all retaing wall","all retaining wall")
        s = s.replace("high temperate sealant","high temperature sealant")
        s = s.replace("greecian white porcelein marble","greecian white porcelain marble")
        s = s.replace("shelves stailess stel","shelves stainless steel")
        s = s.replace("wallmounted garage  shelves","wall mounted garage shelves")
        s = s.replace("remote meat thermom","remote meat thermometer")
        s = s.replace("pvc threaded elbo","pvc threaded elbow")
        s = s.replace("summit 20 in elctric range","summit 20 in electric range")
        s = s.replace("groung fault electric outlet","ground fault electrical outlet")
        s = s.replace("prenneols flower seeds","perennials flower seeds")
        s = s.replace("hyrdaulic oil for kohler","hydraulic oil for kohler")
        s = s.replace("hot/cold porcelin handles","hot/cold porcelain handles")
        s = s.replace("white vanites with tops","white vanities with tops")
        s = s.replace("exterier door keypad","exterior door keypad")
        s = s.replace("purpor power","purple power")
        s = s.replace("automatic drower closer","automatic drawer closer")
        s = s.replace("potable firepace","portable fireplace")
        s = s.replace("azelas","azaleas")
        s = s.replace("mta distributions log splitter","mta distributors log splitter")
        s = s.replace("standing town rack","standing towel rack")
        s = s.replace("zinser stain cover","zinsser stain cover")
        s = s.replace("weed trimer push type","weed trimmer push type")
        s = s.replace("centipe grass seed","centipede grass seed")
        s = s.replace("36  curved showered curtain rod","36 curved shower curtain rod")
        s = s.replace("4 quck grip 101","4 quick grip 101")
        s = s.replace("metal gringing weel  5/8","metal grinding wheel 5/8")
        s = s.replace("weelbarrow","wheelbarrow")
        s = s.replace("baraar emy","bazaar emy")
        s = s.replace("wetbar sink and faucet","wet bar sink and faucet")
        s = s.replace("perenial flowers","perennial flowers")
        s = s.replace("infred turkey fryer","infrared turkey fryer")
        s = s.replace("oil rubbed bronse bathroom lighting","oil rubbed bronze bathroom lighting")
        s = s.replace("solor power lighting  for exterior","solar power lighting for exterior")
        s = s.replace("infloor heating antifreeze","in floor heating antifreeze")
        s = s.replace("galvinized conduit pipe","galvanized conduit pipe")
        s = s.replace("double curtain rod connecter","double curtain rod connector")
        s = s.replace("drop cieling tiles 2ft by 4 ft","drop ceiling tiles 2ft by 4ft")
        s = s.replace("plug in led night lite photocell","plug in led night light photocell")
        s = s.replace("rough limber","rough lumber")
        s = s.replace("48x48 windoww","48x48 window")
        s = s.replace("high intensity t5 flourescent lights","high intensity t5 fluorescent lights")
        s = s.replace("brinly hardy 40 inc tow behind","brinly hardy 40 inch tow behind")
        s = s.replace("ornge 5x7 rugs","orange 5x7 rugs")
        s = s.replace("kitchenmaid built-in double drawer","kitchenaid built-in double drawer")
        s = s.replace("safety latter","safety ladder")
        s = s.replace("blind replacemetn","blind replacement")
        s = s.replace("stainless steeel collated nails","stainless steel collated nails")
        s = s.replace("hang rials barnyard doors","hang rails barnyard doors")
        s = s.replace("tall black toliet","tall black toilet")
        s = s.replace("fint tube","find tube")
        s = s.replace("24 inches rerefrigerator","24 inches refrigerator")
        s = s.replace("ge microwave wall oven comb","ge microwave wall oven combo")
        s = s.replace("presure treated","pressure treated")
        s = s.replace("husky 46 9 drawer mobil","husky 46 9 drawer mobile")
        s = s.replace("apartment size ge  refrigertor stainless steel","apartment size ge refrigerator stainless steel")
        s = s.replace("penedtrating stain","penetrating stain")
        s = s.replace("briggsstraton 11 horse air filter","briggs stratton 11 horse air filter")
        s = s.replace("hoovwe cordless vacuum cleaners","hoover cordless vacuum cleaners")
        s = s.replace("tumbler dryer hose and claps","tumble dryer hose and clamps")
        s = s.replace("antique truch","antique truck")
        s = s.replace("hohler black and tan","kohler black and tan")
        s = s.replace("spray and forget house nad deck","spray and forget house and deck")
        s = s.replace("apriaire humidifier water panel","aprilaire humidifier water panel")
        s = s.replace("unsanded groutr","unsanded grout")
        s = s.replace("60 wat soft watt 2700k a19 dimibal led","60 watt soft watt 2700k a19 dimmable led")
        s = s.replace("7.5 mconnection for 9000 btu","7.5 connection for 9000 btu")
        s = s.replace("dimer switch and fan control","dimmer switch and fan control")
        s = s.replace("granitecounter top cararra","granite countertop carrara")
        s = s.replace("20 amp decor outlet ivory","20 amp decora outlet ivory")
        s = s.replace("rock wall papper","rock wallpaper")
        s = s.replace("thin set fray","thin set gray")
        s = s.replace("glass mirrior doors 72x80","glass mirror doors 72x80")
        s = s.replace("heirloom whie","heirloom white")
        s = s.replace("wood shelfing","wood shelving")
        s = s.replace("kohler top mont bathroom  sink","kohler top mount bathroom sink")
        s = s.replace("outdoor dust to dawn light","outdoor dusk to dawn light")
        s = s.replace("windowbalance","window balance")
        s = s.replace("gunstock oak liamate","gunstock oak laminate")
        s = s.replace("gardden benches","garden benches")
        s = s.replace("strended electrical wire","stranded electrical wire")
        s = s.replace("counter refinsher","counter refinishing")
        s = s.replace("unfinished wood p-lant stand","unfinished wood plant stand")
        s = s.replace("celing fan 60","ceiling fan 60")
        s = s.replace("porta nailor","porta nailer")
        s = s.replace("t fittin","t fitting")
        s = s.replace("bousch lazer level gll2-80p","bosch laser level gll2-80p")
        s = s.replace("2 1/2 inch nail boxe","2 1/2 inch nail box")
        s = s.replace("bonda body filler","bondo body filler")
        s = s.replace("window manganetic lock","window magnetic lock")
        s = s.replace("cat 5 cable uv restance","cat 5 cable uv resistance")
        s = s.replace("3 4  toilet phlange","3 4 toilet flange")
        s = s.replace("aa batteried","aa batteries")
        s = s.replace("6 pvc flixible coupling pipe","6 pvc flexible coupling pipe")
        s = s.replace("7 footaluminum awning","7 foot aluminum awning")
        s = s.replace("carburator","carburetor")
        s = s.replace("water mainfold","water manifold")
        s = s.replace("kholer bathroom wall lights","kohler bathroom wall lights")
        s = s.replace("toro belt pully","toro belt pulley")
        s = s.replace("paper lawn  tefuse bags","paper lawn refuse bags")
        s = s.replace("wadrobe moving boxes","wardrobe moving boxes")
        s = s.replace("ultra clarifer, pool","ultra clarifier, pool")
        s = s.replace("trash caninet slide","trash cabinet slide")
        s = s.replace("craftig pvc cabinets","crafting pvc cabinets")
        s = s.replace("plastic organozers","plastic organizers")
        s = s.replace("rj45 crinp tool","rj45 crimp tool")
        s = s.replace("darby 18 inch dishwasher","danby 18 inch dishwasher")
        s = s.replace("10 x 10 gaxebo garden house","10x10 gazebo garden house")
        s = s.replace("colonial caseing","colonial casing")
        s = s.replace("tarp for outsid furniture","tarp for outside furniture")
        s = s.replace("phlne batteries","phone batteries")
        s = s.replace("eatrhwise mower blades","earthwise mower blades")
        s = s.replace("outdoor artifical lawn","outdoor artificial lawn")
        s = s.replace("dual mount porcelin kitchen sinks","dual mount porcelain kitchen sinks")
        s = s.replace("sflexible shower","flexible shower")
        s = s.replace("savfavieh rug pad","safavieh rug pad")
        s = s.replace("tigerwood perigo laminate flooring","tigerwood pergo laminate flooring")
        s = s.replace("2' flourescent lighting","2' fluorescent lighting")
        s = s.replace("concerte stair railings","concrete stair railings")
        s = s.replace("indoor infered heaters","indoor infrared heaters")
        s = s.replace("tensil ties","tinsel ties")
        s = s.replace("20 ampweather proof recepticles","20 amp weatherproof receptacles")
        s = s.replace("hdmi cabl","hdmi cable")
        s = s.replace("matage double oven ranges","maytag double oven ranges")
        s = s.replace("navarra sierra passage doorknob set","navarra sierra passage door knob set")
        s = s.replace("outdoor furniture cover martha steward","outdoor furniture cover martha stewart")
        s = s.replace("divonshire","devonshire")
        s = s.replace("marine grade painr","marine grade paint")
        s = s.replace("counter and appliance gaperaser","counter and appliance gap eraser")
        s = s.replace("whirpool range hood 36","whirlpool range hood 36")
        s = s.replace("flourecent","fluorescent")
        s = s.replace("drain spoutts","drain spouts")
        s = s.replace("1/4 shut off velves","1/4 shut off valves")
        s = s.replace("porta cool","portacool")
        s = s.replace("yard walll","yard wall")
        s = s.replace("kohler elongaterd toilet seat","kohler elongated toilet seat")
        s = s.replace("kohler lighted tolet seats","kohler lighted toilet seats")
        s = s.replace("cree led bub 6-pack","cree led bulb 6-pack")
        s = s.replace("concrere chisel","concrete chisel")
        s = s.replace("pedistal sink, 27'","pedestal sink, 27'")
        s = s.replace("florsent  replacement diffuser","fluorescent replacement diffuser")
        s = s.replace("chlorox","clorox")
        s = s.replace("core aeretor","core aerator")
        s = s.replace("water proofing connector","waterproof connector")
        s = s.replace("washer/dryr","washer/dryer")
        s = s.replace("cambria java refridgerator","cambria java refrigerator")
        s = s.replace("decrotive metal deck rail incecerts","decorative metal deck rail inserts")
        s = s.replace("whirl pool water heater pilot","whirlpool water heater pilot")
        s = s.replace("siemens double pole gfi","siemens double pole gfci")
        s = s.replace("hampton bay alenxander oak","hampton bay alexander oak")
        s = s.replace("32 inchvinyl screen doors","32 inch vinyl screen doors")
        s = s.replace("hamptonbay shaker cabinets wall","hampton bay shaker cabinets wall")
        s = s.replace("3/8 entension","3/8 extension")
        s = s.replace("10x12 outdoor gazabos","10x12 outdoor gazebos")
        s = s.replace("seet metal tools","sheet metal tools")
        s = s.replace("boch gll","bosch gll")
        s = s.replace("dealt 8v screwdriver","dewalt 8v screwdriver")
        s = s.replace("hand heald showers and ada grab bars","hand held showers and ada grab bars")
        s = s.replace("200 amp outdoor circut breaker panel","200 amp outdoor circuit breaker panel")
        s = s.replace("fingerprint lockset","fingerprint locks")
        s = s.replace("weekender powerwasher extension arms","weekender power washer extension arms")
        s = s.replace("makita drill batterie charger","makita drill battery charger")
        s = s.replace("ridgid fan","rigid fan")
        s = s.replace("swifer wet cloth","swiffer wet cloth")
        s = s.replace("hot water recirculator","hot water recirculation")
        s = s.replace("riding mower blabes","riding mower blades")
        s = s.replace("chain sherpeners","chain sharpeners")
        s = s.replace("relief valve for  rudd hot water heater","relief valve for ruud hot water heater")
        s = s.replace("ceiling     light brackt","ceiling light bracket")
        s = s.replace("perferated pipe","perforated pipe")
        s = s.replace("bath room sink accecories","bathroom sink accessories")
        s = s.replace("ding room set","dining room set")
        s = s.replace("2 ton expoxy","2 ton epoxy")
        s = s.replace("cutkler hammer breaker","cutler hammer breaker")
        s = s.replace("red color cauking","red color caulking")
        s = s.replace("strap and t hindge","strap and t hinge")
        s = s.replace("screw driver 10 iches","screwdriver 10 inches")
        s = s.replace("shower glass slelves","shower glass shelves")
        s = s.replace("playststion 4 destiny bundle","playstation 4 destiny bundle")
        s = s.replace("air conditiooning filter 14'","air conditioning filter 14'")
        s = s.replace("sliding reversable patio door","sliding reversible patio door")
        s = s.replace("rust oleam pinters touch black","rust oleum painters touch black")
        s = s.replace("apron sink firecaly two bowl","apron sink fireclay two bowl")
        s = s.replace("condesate pump","condensate pump")
        s = s.replace("bronze outdoor ceiling dan","bronze outdoor ceiling fan")
        s = s.replace("8 guage wire","8 gauge wire")
        s = s.replace("capacitor for quaterhorse motor 110 volts","capacitor for quarter horse motor 110 volts")
        s = s.replace("anderson storm doors antique bronze","andersen storm doors antique bronze")
        s = s.replace("gas enthonal free","gas ethanol free")
        s = s.replace("is item at homedop","is item at home depot")
        s = s.replace("drain stopper exstension","drain stopper extension")
        s = s.replace("no tresspassing","no trespassing")
        s = s.replace("100 gallon storage ben","100 gallon storage bin")
        s = s.replace("paint hardner","paint hardener")
        s = s.replace("mystick permanent adhesive value pack","mystik permanent adhesive value pack")
        s = s.replace("clear vlyvynal an rolls","clear polyvinyl and rolls")
        s = s.replace("kliz primers","kilz primers")
        s = s.replace("one way scrue removal tool","one way screw removal tool")
        s = s.replace("stainless dishwaser smugde proof","stainless dishwasher smudge proof")
        s = s.replace("hex shank drill bitt sets","hex shank drill bit sets")
        s = s.replace("3.9 high effeciency front load washer","3.9 high efficiency front load washer")
        s = s.replace("concret patio floor","concrete patio floor")
        s = s.replace("in the ground rodiron plant hanger","in the ground rod iron plant hanger")
        s = s.replace("anderson storm door series 2500 sandtone polished brass","andersen storm door series 2500 sandstone polished brass")
        s = s.replace("stainless steele  screws","stainless steel screws")
        s = s.replace("spray sealent for showers","spray sealant for showers")
        s = s.replace("split line air conditioing","split line air conditioning")
        s = s.replace("water softner pellet","water softener pellet")
        s = s.replace("shelac","shellac")
        s = s.replace("helti tools","hilti tools")
        s = s.replace("PHILLIPS POST LIGHT BULB","PHILIPS POST LIGHT BULB")
        s = s.replace("post light bulbl","post light bulb")
        s = s.replace("tiolet","toilet")
        s = s.replace("indoor home decor raindeer","indoor home decor reindeer")
        s = s.replace("dinning tables","dining tables")
        s = s.replace("patio dinning tables","patio dining tables")
        s = s.replace("dremel router acessary","dremel router accessory")
        s = s.replace("accordion door harware","accordion door hardware")
        s = s.replace("edget tape","edge tape")
        s = s.replace("verneer edging tool","veneer edging tool")
        s = s.replace("drywall fastner","drywall fastener")
        s = s.replace("heat pump acessories","heat pump accessories")
        s = s.replace("scroll saw spirsl blade","scroll saw spiral blade")
        s = s.replace("kitchen mat boack","kitchen mat black")
        s = s.replace("chamberlain chain  and pulliepaarts","chamberlain chain and pulley parts")
        s = s.replace("swivle fitting for gas","swivel fitting for gas")
        s = s.replace("SOLDERING IRORN","SOLDERING IRON")
        s = s.replace("oaint marker","paint marker")
        s = s.replace("upsidedowncan marker paint","upside down can marker paint")
        s = s.replace("rope chritsmas lights","rope christmas lights")
        s = s.replace("shower curtin rod","shower curtain rod")
        s = s.replace("scoaring pads","scouring pads")
        s = s.replace("spring set for price fister","spring set for price pfister")
        s = s.replace("laquer thinner","lacquer thinner")
        s = s.replace("mout faucet water filter","mount faucet water filter")
        s = s.replace("NEUMATIC DOOR ARM","PNEUMATIC DOOR ARM")
        s = s.replace("ceiling tile square fotage","ceiling tile square footage")
        s = s.replace("ne angle base","neo angle base")
        s = s.replace("1/4 in.-20 x 1 in. stainless steel flat-head socket cap scre","1/4 in.-20 x 1 in. stainless steel flat-head socket cap screw")
        s = s.replace("flexable pipe for propane","flexible pipe for propane")
        s = s.replace("daltile accent peices","daltile accent pieces")
        s = s.replace("specticide weed and grass rtu refill","spectracide weed and grass rtu refill")
        s = s.replace("wood ddeck kits","wood deck kits")
        s = s.replace("closetmaid hang9ing shelf","closetmaid hanging shelf")
        s = s.replace("asb shower  with curtian","asb shower with curtain")
        s = s.replace("ptouch labeling tape","p touch labeling tape")
        s = s.replace("misquito","mosquito")
        s = s.replace("yard fooger","yard fogger")
        s = s.replace("plastic splash guarf","plastic splash guard")
        s = s.replace("3 light celling mount","3 light ceiling mount")
        s = s.replace("textered wallpaper","textured wallpaper")
        s = s.replace("thermostat w remote senser","thermostat w remote sensor")
        s = s.replace("spray oil prier","spray oil primer")
        s = s.replace("maxx shower door","maax shower door")
        s = s.replace("corion shower base","corian shower base")
        s = s.replace("stapler hammers","staple hammers")
        s = s.replace("2in non metalic standing coupling","2in non metallic standing coupling")
        s = s.replace("backyard xs capes","backyard xscapes")
        s = s.replace("kraylon non skid","krylon non skid")
        s = s.replace("pendent lights wit conversion kits","pendant lights with conversion kits")
        s = s.replace("american wood charllotesville natural hickory","american wood charlottesville natural hickory")
        s = s.replace("1/0 aqg","1/0 awg")
        s = s.replace("artci shag rug","arctic shag rug")
        s = s.replace("omen single hole bathroom faucet","moen single hole bathroom faucet")
        s = s.replace("john deere d100 sereissnow blade","john deere d100 series snow blade")
        s = s.replace("brownbrick wallpaper","brown brick wallpaper")
        s = s.replace("clear corrougated sheets","clear corrugated sheets")
        s = s.replace("pressuer control valve","pressure control valve")
        s = s.replace("white acryllic sheet","white acrylic sheet")
        s = s.replace("wg307work  jaw saw","wg307 worx jawsaw")
        s = s.replace("plaskolight ceiling panel","plaskolite ceiling panel")
        s = s.replace("charger y maintainer","charger and maintainer")
        s = s.replace("waterless urinal conversion kist","waterless urinal conversion kit")
        s = s.replace("hot water heating recirculitating pumps","hot water heater recirculating pumps")
        s = s.replace("two gang carlton switch red dpt","two gang carlton switch red dot")
        s = s.replace("kohler shower cartidges","kohler shower cartridges")
        s = s.replace("rigid portable tool boxes","ridgid portable tool boxes")
        s = s.replace("magniflier lamp","magnifier lamp")
        s = s.replace("irragation controler","irrigation controller")
        s = s.replace("minala rope","manila rope")
        s = s.replace("wood sculture tool","wood sculpture tool")
        s = s.replace("combination fan and lightwall switches","combination fan and light wall switches")
        s = s.replace("acid stian","acid stain")
        s = s.replace("bathtub deck mouted faucet with sprayer","bathtub deck mounted faucet with sprayer")
        s = s.replace("attachments for zero turn  touro","attachments for zero turn toro")
        s = s.replace("wood pellats for grills","wood pellets for grills")
        s = s.replace("whirpool 7000 washer","whirlpool 7000 washer")
        s = s.replace("kitchenover sink lighting","kitchen over sink lighting")
        s = s.replace("pegasus antique black side spalsh","pegasus antique black side splash")
        s = s.replace("lock tight pl","loctite pl")
        s = s.replace("landscasping ms international polish black stone","landscaping ms international polish black stone")
        s = s.replace("1.4 cubit ft micro wave","1.4 cubic ft microwave")
        s = s.replace("square soffet vents","square soffit vents")
        s = s.replace("exterior for pastic shutters","exterior for plastic shutters")
        s = s.replace("exterior hous shutters","exterior house shutters")
        s = s.replace("nutone ventiliation fan parts","nutone ventilation fan parts")
        s = s.replace("belt anf tie rack","belt and tie rack")
        s = s.replace("no elecetrity lights","no electricity lights")
        s = s.replace("merola porcelain mosiac","merola porcelain mosaic")
        s = s.replace("knotches","notches")
        s = s.replace("savavieh soho","safavieh soho")
        s = s.replace("double doors with security licks","double doors with security locks")
        s = s.replace("glass tile backsp gpxtpnrf","glass tile backsp gpx pnrf")
        s = s.replace("cabibet shelf pins","cabinet shelf pins")
        s = s.replace("kolher repair","kohler repair")
        s = s.replace("mantle brakets","mantle brackets")
        s = s.replace("masonry painnt","masonry paint")
        s = s.replace("muliti locks","multi locks")
        s = s.replace("serger sewimg machine","serger sewing machine")
        s = s.replace("mirror installation hardwawrd","mirror installation hardware")
        s = s.replace("walnut porcelian","walnut porcelain")
        s = s.replace("40 airens mulching kit","40 ariens mulching kit")
        s = s.replace("porcelaine cleaner","porcelain cleaner")
        s = s.replace("monococcon 8x8 ceramic azuvi tile","monococcion 8x8 ceramic azuvi tile")
        s = s.replace("black patioo set","black patio set")
        s = s.replace("3/8 viyl j channel","3/8 vinyl j channel")
        s = s.replace("5/8 j chann","5/8 j channel")
        s = s.replace("home alerty","home alert")
        s = s.replace("linen storage cabnit","linen storage cabinet")
        s = s.replace("natur gas heat","natural gas heat")
        s = s.replace("repacement toilet handle","replacement toilet handle")
        s = s.replace("poyurethane clear satin","polyurethane clear satin")
        s = s.replace("garbage desposal","garbage disposal")
        s = s.replace("fire restaint paint","fire resistant paint")
        s = s.replace("bathroom floting ball","bathroom floating ball")
        s = s.replace("kitchen aid processer","kitchenaid processor")
        s = s.replace("fire extinguishhers","fire extinguishers")
        s = s.replace("trex fenc","trex fence")
        s = s.replace("circular sawshop vac","circular saw shop vac")
        s = s.replace("arylic wood paint","acrylic wood paint")
        s = s.replace("appache mills plush tiles","apache mills plush tiles")
        s = s.replace("phillips tuvpl-l 36","philips tuv pl-l 36")
        s = s.replace("framed inerior door","framed interior door")
        s = s.replace("end squicky floor","end squeaky floor")
        s = s.replace("hoover prower scub deluxe","hoover power scrub deluxe")
        s = s.replace("pernennial grass seed","perennial grass seed")
        s = s.replace("phone linesplice connectors","phone line splice connectors")
        s = s.replace("grow boz and pots","grow box and pots")
        s = s.replace("organic leafgrow soil","organic leaf grow soil")
        s = s.replace("6 foot pation table","6 foot patio table")
        s = s.replace("replacement patio unbrella pole","replacement patio umbrella pole")
        s = s.replace("exteriro door 30 * 80","exterior door 30 * 80")
        s = s.replace("oilrubbed bronze 3/8in riser","oil rubbed bronze 3/8in riser")
        s = s.replace("latge storage containers","large storage containers")
        s = s.replace("fridgidaire water filter","frigidaire water filter")
        s = s.replace("sheeking  for log cabin","seeking for log cabin")
        s = s.replace("modern shower facuet","modern shower faucet")
        s = s.replace("mirror, brushed nichel","mirror, brushed nickel")
        s = s.replace("antic brass chandelier","antique brass chandelier")
        s = s.replace("bufflo box wrench","buffalo box wrench")
        s = s.replace("armstrong hardwood flooring422250z5p","armstrong hardwood flooring 422250z5p")
        s = s.replace("mixet math faucet","mixet bath faucet")
        s = s.replace("24 port patch pane","24 port patch panel")
        s = s.replace("black postlantern","black post lantern")
        s = s.replace("needel valve","needle valve")
        s = s.replace("wood ballusters","wood balusters")
        s = s.replace("sharkbite sprinler","sharkbite sprinkler")
        s = s.replace("1/2 hp genie screw drive garage door openner","1/2 hp genie screw drive garage door opener")
        s = s.replace("black dimmable gimble lights","black dimmable gimbal lights")
        s = s.replace("power gable mount attic fac","power gable mount attic fan")
        s = s.replace("door threshholds","door thresholds")
        s = s.replace("rubber office chair sweel","rubber office chair wheel")
        s = s.replace("16x7 garage door sandtone","16x7 garage door sandstone")
        s = s.replace("dal tile 12x24 porcelaine  black tile","daltile 12x24 porcelain black tile")
        s = s.replace("non ferroue saw blade","non ferrous saw blade")
        s = s.replace("aluminum three way swich","aluminum three way switch")
        s = s.replace("racheting wrench","ratcheting wrench")
        s = s.replace("shower wal hook","shower wall hook")
        s = s.replace("inflatable pool pumper","inflatable pool pump")
        s = s.replace("cub cadet 46 balde","cub cadet 46 blade")
        s = s.replace("spade terminalsnylon insulated","spade terminals nylon insulated")
        s = s.replace("jimmyproof lock","jimmy proof lock")
        s = s.replace("braSS pie fittings","braSS pipe fittings")
        s = s.replace("brushed nichol hanging lights","brushed nickel hanging lights")
        s = s.replace("lockbox keydoor lock","lockbox key door lock")
        s = s.replace("white cabnet 30 inch base","white cabinet 30 inch base")
        s = s.replace("ryobi replacemet batteries","ryobi replacement batteries")
        s = s.replace("bath bord","bath board")
        s = s.replace("aerp garden","aerogarden")
        s = s.replace("white sign lettters","white sign letters")
        s = s.replace("sqaure vessel sink","square vessel sink")
        s = s.replace("i beam brackest","i beam brackets")
        s = s.replace("paint for aluminun siding","paint for aluminum siding")
        s = s.replace("digital temp monotor","digital temp monitor")
        s = s.replace("floatinf shelving","floating shelving")
        s = s.replace("light buld for stinger zapper","light bulb for stinger zapper")
        s = s.replace("custom counterto","custom countertop")
        s = s.replace("replacement delta faucet cartrigdge","replacement delta faucet cartridge")
        s = s.replace("laundry bnasket","laundry basket")
        s = s.replace("air conditon cooper soft","air conditioner copper soft")
        s = s.replace("wood qwik bolts","wood kwik bolts")
        s = s.replace("bolt conrete anchors","bolt concrete anchors")
        s = s.replace("outdoor dining se?","outdoor dining set?")
        s = s.replace("glass sheet mosiacs","glass sheet mosaics")
        s = s.replace("whites parkle","white sparkle")
        s = s.replace("fiskers titanium 1 1/2 loppers","fiskars titanium 1 1/2 loppers")
        s = s.replace("cement mason bit","cement masonry bit")
        s = s.replace("bananna leaves plant","banana leaves plant")
        s = s.replace("fi nish screws","finish screws")
        s = s.replace("tolet handle left hand","toilet handle left hand")
        s = s.replace("sika repair shp","sika repair shop")
        s = s.replace("murry circuit breakers 20 amps","murray circuit breakers 20 amps")
        s = s.replace("hand pipe theader","hand pipe threader")
        s = s.replace("powermate  walkbehind trimmer","powermate walk behind trimmer")
        s = s.replace("metal      clothes handing carts","metal clothes hanging carts")
        s = s.replace("electric radiatior heat","electric radiator heat")
        s = s.replace("shopvac filter hepa","shop vac filter hepa")
        s = s.replace("hampton bay fenving","hampton bay fencing")
        s = s.replace("knife sharppener","knife sharpener")
        s = s.replace("atttic heat barrier","attic heat barrier")
        s = s.replace("wondow curtains","window curtains")
        s = s.replace("american standard town square widespread facet","american standard town square widespread faucet")
        s = s.replace("5.0 chest freezerz","5.0 chest freezers")
        s = s.replace("20 amp surger protector","20 amp surge protector")
        s = s.replace("f 30  flourescent light fixture","f30 fluorescent light fixture")
        s = s.replace("1/2 inch rubber lep tips","1/2 inch rubber leg tips")
        s = s.replace("threader rod end coupler","threaded rod end coupler")
        s = s.replace("lamated counter tops","laminate countertops")
        s = s.replace("railing kit system round ballusters","railing kit system round balusters")
        s = s.replace("sintetic grass","synthetic grass")
        s = s.replace("landry sink","laundry sink")
        s = s.replace("solar led light dust to dawn","solar led light dusk to dawn")
        s = s.replace("pegro xp coffee step","pergo xp coffee step")
        s = s.replace("maytag two door refridgerator","maytag two door refrigerator")
        s = s.replace("reprobramable combination lock","programmable combination lock")
        s = s.replace("pnematic flooring nails 16 gauge","pneumatic flooring nailer 16 gauge")
        s = s.replace("outide dog kennel","outside dog kennel")
        s = s.replace("6 incn door knocker","6 inch door knocker")
        s = s.replace("non programmable vertical  thermost","non programmable vertical thermostat")
        s = s.replace("windser light coco","windsor light coco")
        s = s.replace("cooling towes","cooling towers")
        s = s.replace("glacier bay  shower catridge","glacier bay shower cartridge")
        s = s.replace("ge discontinnued top freezers","ge discontinued top freezers")
        s = s.replace("security camaras","security cameras")
        s = s.replace("toiles partes","toilet parts")
        s = s.replace("pegasus ntique brass","pegasus antique brass")
        s = s.replace("water pic shower head chrome","waterpik shower head chrome")
        s = s.replace("85 gall tall 4500","85 gal tall 4500")
        s = s.replace("contempery ceiling fans","contemporary ceiling fans")
        s = s.replace("toile seat lid","toilet seat lid")
        s = s.replace("milwaukee noncontact tester","milwaukee non contact tester")
        s = s.replace("emser ocuntry","emser country")
        s = s.replace("front screen for a gazeebo","front screen for a gazebo")
        s = s.replace("fatpack 18v","fat pack 18v")
        s = s.replace("bathroom kraft made","bathroom kraftmaid")
        s = s.replace("1/4 qk connect x 1/8 mip","1/4 quick connect x 1/8 mip")
        s = s.replace("plate for faucet stoper","plate for faucet stopper")
        s = s.replace("femaie gas fitting quick disonnect","female gas fitting quick disconnect")
        s = s.replace("recesse light bulbs","recessed light bulbs")
        s = s.replace("3m 60926 vapor catridges","3m 60926 vapor cartridges")
        s = s.replace("weather strip for commerial door","weather strip for commercial door")
        s = s.replace("arcadia mettal  locks","arcadia metal locks")
        s = s.replace("gekko gauges","gecko gauges")
        s = s.replace("frigidaire water firlters","frigidaire water filters")
        s = s.replace("30 par haolgen bulbs","30 par halogen bulbs")
        s = s.replace("red devil scraperreplacement bldes","red devil scraper replacement blades")
        s = s.replace("gcfi outlet","gfci outlet")
        s = s.replace("mohawk oak wood fllors","mohawk oak wood floors")
        s = s.replace("all porpose stools","all purpose stools")
        s = s.replace("primered floor molding","primed floor molding")
        s = s.replace("glass cleaner concintrete","glass cleaner concentrate")
        s = s.replace("30 amp surface mount recepticle","30 amp surface mount receptacle")
        s = s.replace("60 x 100 aluminun mesh","60 x 100 aluminum mesh")
        s = s.replace("tile border black and whit","tile border black and white")
        s = s.replace("peir mount black","pier mount black")
        s = s.replace("xtra wide baby gates","extra wide baby gates")
        s = s.replace("roffing caulk","roofing caulk")
        s = s.replace("1/2 inc pvc treaded connector","1/2 inch pvc threaded connector")
        s = s.replace("electric  hock for lift","electric shock for lift")
        s = s.replace("greak","greek")
        s = s.replace("airfilter 20x24","air filter 20x24")
        s = s.replace("extenion cord storage","extension cord storage")
        s = s.replace("shluter","schluter")
        s = s.replace("circular saw rrip fence","circular saw rip fence")
        s = s.replace("HEATED TOLIET SEAT","HEATED TOILET SEAT")
        s = s.replace("rount magnet","round magnet")
        s = s.replace("handi cap sink faucett","handicap sink faucet")
        s = s.replace("arc fault circute breaker 1pole 15 amp","arc fault circuit breaker 1 pole 15 amp")
        s = s.replace("oreck full reease carpet cleaner","oreck full release carpet cleaner")
        s = s.replace("min split mounting brackets","mini split mounting brackets")
        s = s.replace("kholer sink 20x17","kohler sink 20x17")
        s = s.replace("heavy duty extensoion cordyellow only","heavy duty extension cord yellow only")
        s = s.replace("3 newll post","3 newel post")
        s = s.replace("veraluz 4 light bathroom vanity","varaluz 4 light bathroom vanity")
        s = s.replace("anual combo","annual combo")
        s = s.replace("ciling pan","ceiling pan")
        s = s.replace("syllicone lube","silicone lube")
        s = s.replace("hdx 20' hight velocity floor fan","hdx 20' high velocity floor fan")
        s = s.replace("30 inch kitchenaide cooktops","30 inch kitchenaid cooktops")
        s = s.replace("kusshuln concrete mixer","kushlan concrete mixer")
        s = s.replace("roles of concreate mesh","roles of concrete mesh")
        s = s.replace("hardward for pull out waste bin","hardware for pull out waste bin")
        s = s.replace("glass towel bar braket","glass towel bar bracket")
        s = s.replace("living room cabnets","living room cabinets")
        s = s.replace("1-1/4 extention pvc","1-1/4 extension pvc")
        s = s.replace("metal double gain boxes","metal double gang boxes")
        s = s.replace("fabric umbella","fabric umbrella")
        s = s.replace("club cadet 46  belt","cub cadet 46 belt")
        s = s.replace("window air conditionerriding lawn mowers","window air conditioner riding lawn mowers")
        s = s.replace("digital cammera","digital camera")
        s = s.replace("prppane pan","propane pan")
        s = s.replace("oride plant","pride plant")
        s = s.replace("home decorator outoddor patio cordless shades","home decorator outdoor patio cordless shades")
        s = s.replace("1x1 square tubeing","1x1 square tubing")
        s = s.replace("water filter for frigidaire refrigirator","water filter for frigidaire refrigerator")
        s = s.replace("linier track pendant","linear track pendant")
        s = s.replace("medal stud finder","metal stud finder")
        s = s.replace("mke m12 heated hoddie kit","mke m12 heated hoodie kit")
        s = s.replace("bilt in pool","built in pool")
        s = s.replace("buit in shower base","built in shower base")
        s = s.replace("grohsafe roughin valve 35015","grohsafe rough in valve 35015")
        s = s.replace("tank insualation","tank insulation")
        s = s.replace("khols double toilet bowl","kohl's double toilet bowl")
        s = s.replace("atlantiic can racks","atlantic can racks")
        s = s.replace("skylites","skylights")
        s = s.replace("kwikset passive door knob","kwikset passage door knob")
        s = s.replace("loadspeaker","loudspeaker")
        s = s.replace("koehler enamel cast iron sink","kohler enameled cast iron sink")
        s = s.replace("tood handle lock","todd handle lock")
        s = s.replace("sable brow grout","sable brown grout")
        s = s.replace("rewd bird feeder","red bird feeder")
        s = s.replace("lilac aera rug","lilac area rug")
        s = s.replace("lightsavannah 3-light burnished ing fixtures","light savannah 3-light burnished ing fixtures")
        s = s.replace("clear vynil for patio","clear vinyl for patio")
        s = s.replace("intersate battery","interstate battery")
        s = s.replace("jeldewen prairie mission door","jeld wen prairie mission door")
        s = s.replace("honey oak tmolding","honey oak t molding")
        s = s.replace("COMPLET SHOWER KIT","COMPLETE SHOWER KIT")
        s = s.replace("36' florescent light bulb","36' fluorescent light bulb")
        s = s.replace("melon sunbrellap","melon sunbrella")
        s = s.replace("28 kg washign machine","28 kg washing machine")
        s = s.replace("metal trash cas","metal trash cans")
        s = s.replace("front door with side transome","front door with side transom")
        s = s.replace("tribecia","tribeca")
        s = s.replace("exterior shutters byrgundy","exterior shutters burgundy")
        s = s.replace("light switchvers for little girls","light switches for little girls")
        s = s.replace("miraposa whirlpool tub","mariposa whirlpool tub")
        s = s.replace("schoolhouse pendqnt light","schoolhouse pendant light")
        s = s.replace("cablrail","cable rail")
        s = s.replace("vinly seat cleaner","vinyl seat cleaner")
        s = s.replace("metal 3 tiertrolley","metal 3 tier trolley")
        s = s.replace("white pendant uplight","white pendant light")
        s = s.replace("lbathroom vanity lights chrome 3","bathroom vanity lights chrome 3")
        s = s.replace("brushed nickel knobw","brushed nickel knobs")
        s = s.replace("Renassaince","Renaissance")
        s = s.replace("simpon strong tie wedge","simpson strong tie wedge")
        s = s.replace("silocone repairs","silicone repairs")
        s = s.replace("chocolate brown blackspash","chocolate brown backsplash")
        s = s.replace("portabel tabel, plastic","portable table, plastic")
        s = s.replace("safavieh courtyard dark biege area rug","safavieh courtyard dark beige area rug")
        s = s.replace("theromometer smart","thermometer smart")
        s = s.replace("hummngbird feeders","hummingbird feeders")
        s = s.replace("diverter handels","diverter handles")
        s = s.replace("dynamic desighn planters","dynamic design planters")
        s = s.replace("pri meld flush bi fold doors","primed flush bifold doors")
        s = s.replace("fisher and penkel","fisher and paykel")
        s = s.replace("price of 1 gal beher marquee paint","price of 1 gal behr marquee paint")
        s = s.replace("makersbot","makerbot")
        s = s.replace("shelter logic sun sahde","shelterlogic sun shade")
        s = s.replace("moen 4 port pex vavle","moen 4 port pex valve")
        s = s.replace("ceiling fan extension wre","ceiling fan extension wire")
        s = s.replace("single knobreplacement for shower kohler","single knob replacement for shower kohler")
        s = s.replace("high gloss waterborne acrylic enamal","high gloss waterborne acrylic enamel")
        s = s.replace("cattale","cattle")
        s = s.replace("double deountable","double demountable")
        s = s.replace("fantsastic","fantastic")
        s = s.replace("milwaulkee battery charger","milwaukee battery charger")
        s = s.replace("tandom 30 20","tandem 30 20")
        s = s.replace("schluter kurdie","schluter kerdi")
        s = s.replace("square buckes","square buckets")
        s = s.replace("pro series vinal post","pro series vinyl post")
        s = s.replace("krud cutter rust","krud kutter rust")
        s = s.replace("warm espresso distresed","warm espresso distressed")
        s = s.replace("levinton phone tv combo","leviton phone tv combo")
        s = s.replace("makita planner knives","makita planer knives")
        s = s.replace("barictric walk in tubs","bariatric walk in tubs")
        s = s.replace("woper blades","wiper blades")
        s = s.replace("kidcraft 18 doll furniture","kidkraft 18 doll furniture")
        s = s.replace("stickon shower wall tower","stick on shower wall tower")
        s = s.replace("riding lawn mower accesores","riding lawn mower accessories")
        s = s.replace("towel bar nickel gracier 18'","towel bar nickel glacier 18'")
        s = s.replace("compreshion repair kit","compression repair kit")
        s = s.replace("huskie air compressors accessories","husky air compressors accessories")
        s = s.replace("36 inch neo angle glass doooors","36 inch neo angle glass doors")
        s = s.replace("gerber cohort fine edg knife","gerber cohort fine edge knife")
        s = s.replace("work force prpane heatr","workforce propane heater")
        s = s.replace("progress lighting nottingdon","progress lighting nottington")
        s = s.replace("dog leash atachments","dog leash attachments")
        s = s.replace("elaphent ear","elephant ear")
        s = s.replace("veeneer wood tape","veneer wood tape")
        s = s.replace("siccsers","scissors")
        s = s.replace("klien folding 6ft ruler","klein folding 6ft ruler")
        s = s.replace("wall socket covedrs","wall socket covers")
        s = s.replace("klein 8 inch plies","klein 8 inch pliers")
        s = s.replace("screen doors: screen tight doors 32 in. unfinished wood t-ba","screen doors: screen tight doors 32 in. unfinished wood t-bar")
        s = s.replace("g e dishwaaher","g e dishwasher")
        s = s.replace("white semigloass","white semi gloss")
        s = s.replace("shop swiming pools","shop swimming pools")
        s = s.replace("rectangular baulaster","rectangular baluster")
        s = s.replace("cedar 0roofing shingles","cedar roofing shingles")
        s = s.replace("prehung door fanlite","prehung door fan lite")
        s = s.replace("martha suart carpet tobacco leaf","martha stewart carpet tobacco leaf")
        s = s.replace("furnance gas upflow","furnace gas upflow")
        s = s.replace("spalted m aple","spalted maple")
        s = s.replace("crimpling pleirs","crimping pliers")
        s = s.replace("cold stem for glacer bay faucets","cold stem for glacier bay faucets")
        s = s.replace("holegen flood light 35w","halogen flood light 35w")
        s = s.replace("ridgid ipact wrench","rigid impact wrench")
        s = s.replace("twin wsher dryer gas","twin washer dryer gas")
        s = s.replace("Diamond HArd Acrylic Enamal","Diamond HArd Acrylic Enamel")
        s = s.replace("stainless steel wall pannels","stainless steel wall panels")
        s = s.replace("perenial bulb","perennial bulb")
        s = s.replace("caroilne avenue 36 in single vanity in white marble top in l","caroline avenue 36 in single vanity in white marble top in l")
        s = s.replace("broadway collectionchrome vanity fixture","broadway collection chrome vanity fixture")
        s = s.replace("vogoro flower","vigoro flower")
        s = s.replace("guarge parnel","gauge panel")
        s = s.replace("sweeep pan","sweep pan")
        s = s.replace("dewalt magnetic drive quide","dewalt magnetic drive guide")
        s = s.replace("milwuakee magnetic drive guide","milwaukee magnetic drive guide")
        s = s.replace("stainlss steel wire wheels","stainless steel wire wheels")
        s = s.replace("deltile 3x6 ceramic blue","daltile 3x6 ceramic blue")
        s = s.replace("discontinuedbrown and tan area rug","discontinued brown and tan area rug")
        s = s.replace("frost protectionm","frost protection")
        s = s.replace("5 tier chandalier","5 tier chandelier")
        s = s.replace("perry hickory laminte","perry hickory laminate")
        s = s.replace("carpet chessnut","carpet chestnut")
        s = s.replace("midnight blue irridecent","midnight blue iridescent")
        s = s.replace("under cabinet black flourescent","under cabinet black fluorescent")
        s = s.replace("concord charcole runner","concord charcoal runner")
        s = s.replace("gibrallar post series cedar post","gibraltar post series cedar post")
        s = s.replace("jefrrey court 3x12","jeffrey court 3x12")
        s = s.replace("baking panb","baking pan")
        s = s.replace("dustless ginder","dustless grinder")
        s = s.replace("paw print doorbe;;","paw print doorbell;;")
        s = s.replace("rustolium paint american accesnts","rustoleum paint american accents")
        s = s.replace("costum key","custom key")
        s = s.replace("halh circle glass shelf","half circle glass shelf")
        s = s.replace("pedestial snk","pedestal sink")
        s = s.replace("cordless celullar","cordless cellular")
        s = s.replace("scounces wall light outside","sconces wall light outside")
        s = s.replace("gas powere wood chipper","gas powered wood chipper")
        s = s.replace("hampton bay brillant maple laminate","hampton bay brilliant maple laminate")
        s = s.replace("t8 flourescent bulbs 4 ft 2 pack","t8 fluorescent bulbs 4 ft 2 pack")
        s = s.replace("leminate floor alexandrea","laminate floor alexandria")
        s = s.replace("reflector 50w flurecent","reflector 50w fluorescent")
        s = s.replace("he xl 44 range","ge xl44 range")
        s = s.replace("branch protctor paint","branch protector paint")
        s = s.replace("rehargeable aa batteries for landscape lighting","rechargeable aa batteries for landscape lighting")
        s = s.replace("msa safet work hat","msa safety work hat")
        s = s.replace("conemporary hanging outdoor light fixture","contemporary hanging outdoor light fixture")
        s = s.replace("piano door hing","piano door hinge")
        s = s.replace("kohler whole houser generator","kohler whole house generator")
        s = s.replace("dynasty collecion","dynasty collection")
        s = s.replace("chesapeke nightstand in cherry","chesapeake nightstand in cherry")
        s = s.replace("kohler glas shower door 4ft","kohler glass shower door 4ft")
        s = s.replace("apartment size refreidgerator","apartment size refrigerator")
        s = s.replace("centerpise","centerprise")
        s = s.replace("motar for large tilw","mortar for large tile")
        s = s.replace("bathroom lightning 48 inch","bathroom lighting 48 inch")
        s = s.replace("panle clamp","panel clamp")
        s = s.replace("roll up door fo shed","roll up door for shed")
        s = s.replace("oil rubbed bronze airgap for dishwasher","oil rubbed bronze air gap for dishwasher")
        s = s.replace("multi plub adapter","multi plug adapter")
        s = s.replace("decorative  clarance","decorative clarence")
        s = s.replace("tamper resistant combo outet black","tamper resistant combo outlet black")
        s = s.replace("polyurethane collors","polyurethane colors")
        s = s.replace("scrool lever","scroll lever")
        s = s.replace("gentec smoke detector","gentex smoke detector")
        s = s.replace("kohler claxton biscuit sink","kohler caxton biscuit sink")
        s = s.replace("strapping for cielings","strapping for ceilings")
        s = s.replace("wall mounteddrop leaf table","wall mounted drop leaf table")
        s = s.replace("chamberlain intercomm","chamberlain intercom")
        s = s.replace("sumpter oask","sumpter oak")
        s = s.replace("torino chandler 5 light bn","torino chandelier 5 light bn")
        s = s.replace("allure red mahoghany","allure red mahogany")
        s = s.replace("ge personal eletrical home security","ge personal electric home security")
        s = s.replace("for rent sighn","for rent sign")
        s = s.replace("coper clad aluminum","copper clad aluminum")
        s = s.replace("homeywell cool moisture humidifier filters","honeywell cool moisture humidifier filters")
        s = s.replace("hdc fairlawm jasper cane","hdc fairlawn jasper cane")
        s = s.replace("wire fen c e","wire fence")
        s = s.replace("cap screww everbilt 1/4in x2in","cap screw everbilt 1/4in x2in")
        s = s.replace("metal  urathane","metal urethane")
        s = s.replace("blitz colth","blitz cloth")
        s = s.replace("commercial accunts","commercial accounts")
        s = s.replace("electic chainsaw worx","electric chainsaw worx")
        s = s.replace("power toll accesories","power tool accessories")
        s = s.replace("leviton - decora 3 gang midway nylon wall plate - light almo","leviton - decora 3 gang midway nylon wall plate - light almond")
        s = s.replace("pond filter mediumpond filter pads","pond filter media pond filter pads")
        s = s.replace("tall wine cabnet","tall wine cabinet")
        s = s.replace("bulk calking","bulk caulking")
        s = s.replace("insolated cooler with a strap","insulated cooler with a strap")
        s = s.replace("concete placer","concrete placer")
        s = s.replace("transmissin leak stopper","transmission leak stopper")
        s = s.replace("toilet in buisk","toilet in buick")
        s = s.replace("black wire hidder","black wire hider")
        s = s.replace("braid trim ceramic title molding","braid trim ceramic tile molding")
        s = s.replace("laundry tub fosets valves","laundry tub faucets valves")
        s = s.replace("schlage plymoth orbit oil rubbed bronze","schlage plymouth orbit oil rubbed bronze")
        s = s.replace("romanic poetry flat interior paint","romantic poetry flat interior paint")
        s = s.replace("worklight 500 watt bullbs","worklight 500 watt bulbs")
        s = s.replace("elvies ornament","elvis ornament")
        s = s.replace("dpcam camera","dropcam camera")
        s = s.replace("clorine tabs for septic","chlorine tabs for septic")
        s = s.replace("interor door framed","interior door frame")
        s = s.replace("hot dipped galvanized screwes","hot dipped galvanized screws")
        s = s.replace("14 ft. w x29 ft. l x 14 ft.h","14 ft. w x 29 ft. x 14 ft.h")
        s = s.replace("water resistent top","water resistant top")
        s = s.replace("galvinize 2 in box of screws","galvanized 2 in box of screws")
        s = s.replace("taupe teasure carpet","taupe treasure carpet")
        s = s.replace("nickle vanity lighting mosaics","nickel vanity lighting mosaics")
        s = s.replace("heat circualtor","heat circulator")
        s = s.replace("flexible pvc joing","flexible pvc joint")
        s = s.replace("14 metal abresive blade","14 metal abrasive blade")
        s = s.replace("foldin g patio doors","folding patio doors")
        s = s.replace("primeline mirror sliding doors","prime line mirror sliding doors")
        s = s.replace("sanora maple flooring","sonora maple flooring")
        s = s.replace("plastic paint containwes with lid","plastic paint containers with lid")
        s = s.replace("deck  fasting systems","deck fastening systems")
        s = s.replace("long handled squeege window cleaning","long handled squeegee window cleaning")
        s = s.replace("lsnd scape trim edger","landscape trim edger")
        s = s.replace("rust oleum aged iron","rustoleum aged iron")
        s = s.replace("redi ledge cooner","redi ledge corner")
        s = s.replace("milwakee work radio","milwaukee work radio")
        s = s.replace("progress piedmot","progress piedmont")
        s = s.replace("home security camera cablee","home security camera cable")
        s = s.replace("white rock daltale","white rock daltile")
        s = s.replace("japenes lilacs","japanese lilacs")
        s = s.replace("thickrubber mat","thick rubber mat")
        s = s.replace("topdown bottom up shades","top down bottom up shades")
        s = s.replace("locktite 9oz 2in1 premium sealant","loctite 9oz 2in1 premium sealant")
        s = s.replace("evaporative thermstate","evaporative thermostat")
        s = s.replace("red devil paint cleanaer","red devil paint cleaner")
        s = s.replace("beer wine refrigeratr","beer wine refrigerator")
        s = s.replace("forced air vents covrs","forced air vents covers")
        s = s.replace("ew drops marquee paint","dew drops marquee paint")
        s = s.replace("kitchen sink and fawcet black dual mount","kitchen sink and faucet black dual mount")
        s = s.replace("dimmable fluoreecent","dimmable fluorescent")
        s = s.replace("textured 6 pannel hollow core primed composite prehung inter","textured 6 panel hollow core primed composite prehung inter")
        s = s.replace("dakato 4 light","dakota 4 light")
        s = s.replace("playset handels","playset handles")
        s = s.replace("vauhhan hammers","vaughan hammers")
        s = s.replace("sterling frosted glass shower ath doors","sterling frosted glass shower bath doors")
        s = s.replace("autom tic drawer lite","automatic drawer light")
        s = s.replace("all trellisses","all trellises")
        s = s.replace("american standard 5324.019 enlongate toilet seat","american standard 5324.019 elongated toilet seat")
        s = s.replace("15 in built in maytag trash compactorr","15 in built in maytag trash compactor")
        s = s.replace("3 butto pico pj-3b","3 button pico pj-3b")
        s = s.replace("ligth","light")
        s = s.replace("sissors","scissors")
        
        return s
    else:
        return "null"

def seg_words(str1, str2):
    str2 = str2.lower()
    str2 = re.sub("[^a-z0-9./]"," ", str2)
    str2 = [z for z in set(str2.split()) if len(z)>2]
    words = str1.lower().split(" ")
    s = []
    for word in words:
        if len(word)>3:
            s1 = []
            s1 += segmentit(word,str2,True)
            if len(s)>1:
                s += [z for z in s1 if z not in ['er','ing','s','less'] and len(z)>1]
            else:
                s.append(word)
        else:
            s.append(word)
    return (" ".join(s))

def segmentit(s, txt_arr, t):
    st = s
    r = []
    for j in range(len(s)):
        for word in txt_arr:
            if word == s[:-j]:
                r.append(s[:-j])
                #print(s[:-j],s[len(s)-j:])
                s=s[len(s)-j:]
                r += segmentit(s, txt_arr, False)
    if t:
        i = len(("").join(r))
        if not i==len(st):
            r.append(st[i:])
    return r

def str_common_word(str1, str2):
    words, cnt = str1.split(), 0
    for word in words:
        if str2.find(word)>=0:
            cnt+=1
    return cnt

def str_whole_word(str1, str2, i_):
    cnt = 0
    while i_ < len(str2):
        i_ = str2.find(str1, i_)
        if i_ == -1:
            return cnt
        else:
            cnt += 1
            i_ += len(str1)
    return cnt

def fmean_squared_error(ground_truth, predictions):
    fmean_squared_error_ = mean_squared_error(ground_truth, predictions)**0.5
    return fmean_squared_error_

RMSE  = make_scorer(fmean_squared_error, greater_is_better=False)

class cust_regression_vals(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    def transform(self, hd_searches):
        d_col_drops=['id','relevance','search_term','product_title','product_description','product_info','attr','brand']
        hd_searches = hd_searches.drop(d_col_drops,axis=1).values
        return hd_searches

class cust_txt_col(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, x, y=None):
        return self
    def transform(self, data_dict):
        return data_dict[self.key].apply(str)

#comment out the lines below use df_all.csv for further grid search testing
#if adding features consider any drops on the 'cust_regression_vals' class
#*** would be nice to have a file reuse option or script chaining option on Kaggle Scripts ***
df_all['search_term'] = df_all['search_term'].map(lambda x:str_stem(x))
df_all['product_title'] = df_all['product_title'].map(lambda x:str_stem(x))
df_all['product_description'] = df_all['product_description'].map(lambda x:str_stem(x))
df_all['brand'] = df_all['brand'].map(lambda x:str_stem(x))
print("--- Stemming: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['product_info'] = df_all['search_term']+"\t"+df_all['product_title'] +"\t"+df_all['product_description']
print("--- Prod Info: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['len_of_query'] = df_all['search_term'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_title'] = df_all['product_title'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_description'] = df_all['product_description'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_brand'] = df_all['brand'].map(lambda x:len(x.split())).astype(np.int64)
print("--- Len of: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['search_term'] = df_all['product_info'].map(lambda x:seg_words(x.split('\t')[0],x.split('\t')[1]))
#print("--- Search Term Segment: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['query_in_title'] = df_all['product_info'].map(lambda x:str_whole_word(x.split('\t')[0],x.split('\t')[1],0))
df_all['query_in_description'] = df_all['product_info'].map(lambda x:str_whole_word(x.split('\t')[0],x.split('\t')[2],0))
print("--- Query In: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['query_last_word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0].split(" ")[-1],x.split('\t')[1]))
df_all['query_last_word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0].split(" ")[-1],x.split('\t')[2]))
print("--- Query Last Word In: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
df_all['word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[2]))
df_all['ratio_title'] = df_all['word_in_title']/df_all['len_of_query']
df_all['ratio_description'] = df_all['word_in_description']/df_all['len_of_query']
df_all['attr'] = df_all['search_term']+"\t"+df_all['brand']
df_all['word_in_brand'] = df_all['attr'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
df_all['ratio_brand'] = df_all['word_in_brand']/df_all['len_of_brand']
df_brand = pd.unique(df_all.brand.ravel())
d={}
i = 1000
for s in df_brand:
    d[s]=i
    i+=3
df_all['brand_feature'] = df_all['brand'].map(lambda x:d[x])
df_all['search_term_feature'] = df_all['search_term'].map(lambda x:len(x))
df_all.to_csv('df_all.csv')
#df_all = pd.read_csv('df_all.csv', encoding="ISO-8859-1", index_col=0)
df_train = df_all.iloc[:num_train]
df_test = df_all.iloc[num_train:]
id_test = df_test['id']
y_train = df_train['relevance'].values
X_train =df_train[:]
X_test = df_test[:]
print("--- Features Set: %s minutes ---" % round(((time.time() - start_time)/60),2))

rfr = RandomForestRegressor(n_estimators = 500, n_jobs = -1, random_state = 2016, verbose = 2)
tfidf = TfidfVectorizer(ngram_range=(1, 1), stop_words='english')
tsvd = TruncatedSVD(n_components=10, random_state = 2016)
clf = pipeline.Pipeline([
        ('union', FeatureUnion(
                    transformer_list = [
                        ('cst',  cust_regression_vals()),  
                        ('txt1', pipeline.Pipeline([('s1', cust_txt_col(key='search_term')), ('tfidf1', tfidf), ('tsvd1', tsvd)])),
                        ('txt2', pipeline.Pipeline([('s2', cust_txt_col(key='product_title')), ('tfidf2', tfidf), ('tsvd2', tsvd)])),
                        ('txt3', pipeline.Pipeline([('s3', cust_txt_col(key='product_description')), ('tfidf3', tfidf), ('tsvd3', tsvd)])),
                        ('txt4', pipeline.Pipeline([('s4', cust_txt_col(key='brand')), ('tfidf4', tfidf), ('tsvd4', tsvd)]))
                        ],
                    transformer_weights = {
                        'cst': 1.0,
                        'txt1': 0.5,
                        'txt2': 0.25,
                        'txt3': 0.0,
                        'txt4': 0.5
                        },
                #n_jobs = -1
                )), 
        ('rfr', rfr)])
param_grid = {'rfr__max_features': [10], 'rfr__max_depth': [20]}
model = grid_search.GridSearchCV(estimator = clf, param_grid = param_grid, n_jobs = -1, cv = 2, verbose = 20, scoring=RMSE)
model.fit(X_train, y_train)

print("Best parameters found by grid search:")
print(model.best_params_)
print("Best CV score:")
print(model.best_score_)
print(model.best_score_ + 0.47003199274)

y_pred = model.predict(X_test)
pd.DataFrame({"id": id_test, "relevance": y_pred}).to_csv('submission.csv',index=False)
print("--- Training & Testing: %s minutes ---" % round(((time.time() - start_time)/60),2))

from sklearn.feature_extraction import text
import nltk

df_outliers = pd.read_csv('df_all.csv', encoding="ISO-8859-1", index_col=0)
#stop_ = list(text.ENGLISH_STOP_WORDS)
stop_ = []
d={}
for i in range(len(df_outliers)):
    s = str(df_outliers['search_term'][i]).lower()
    #s = s.replace("\n"," ")
    #s = re.sub("[^a-z]"," ", s)
    #s = s.replace("  "," ")
    a = set(s.split(" "))
    for b_ in a:
        if b_ not in stop_ and len(b_)>0:
            if b_ not in d:
                d[b_] = [1,str_common_word(b_, df_outliers['product_title'][i]),str_common_word(b_, df_outliers['brand'][i]),str_common_word(b_, df_outliers['product_description'][i])]
            else:
                d[b_][0] += 1
                d[b_][1] += str_common_word(b_, df_outliers['product_title'][i])
                d[b_][2] += str_common_word(b_, df_outliers['brand'][i])
                d[b_][3] += str_common_word(b_, df_outliers['product_description'][i])
ds2 = pd.DataFrame.from_dict(d,orient='index')
ds2.columns = ['count','in title','in brand','in prod']
ds2 = ds2.sort_values(by=['count'], ascending=[False])

f = open("word_review.csv", "w")
f.write("word|count|in title|in brand|in description\n")
for i in range(len(ds2)):
    f.write(ds2.index[i] + "|" + str(ds2["count"][i]) + "|" + str(ds2["in title"][i]) + "|" + str(ds2["in brand"][i]) + "|" + str(ds2["in prod"][i]) + "\n")
f.close()
print("--- Word List Created: %s minutes ---" % round(((time.time() - start_time)/60),2))