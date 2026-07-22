# TapHouse Frankfurt — Drinks menu data (extracted from Untappd prints 83218/82683/83221, Jul 2026)

TAP = [
 ("Camba Bavaria Hell","Seeon-Seebruck, Bayern","Lager – Helles","5.2%","21",
  "Refreshing with a delicate malt note; wonderfully balanced and full-bodied. Silver, European Beer Star (German-Style Kellerbier Hell).",
  [("100ml (flight)","2.00"),("300ml","4.40"),("500ml","5.90")]),
 ("Camba Bavaria Pils","Seeon-Seebruck, Bayern","Pilsner – German","5%","35","",
  [("100ml (flight)","2.00"),("300ml","4.40"),("500ml","5.90")]),
 ("Camba Bavaria Jäger Weisse / Simcoe Weisse","Seeon-Seebruck, Bayern","Wheat – Hopfenweisse","5.2%","29",
  "A hopped wheat beer; Chinook gives it a fruity aroma with fine hop notes and bright, zesty citrus.",
  [("100ml (flight)","2.20"),("500ml","5.90")]),
 ("Camba Bavaria Chiemsee Pale","Seeon-Seebruck, Bayern","Pale Ale – Other","5.3%","31",
  "Dry-hopped pale ale — punchy and zesty with grapefruit and citrus over a fruit-basket aroma of mango, passionfruit and pineapple.",
  [("100ml (flight)","2.20"),("300ml","5.90")]),
 ("Camba Bavaria Island","Seeon-Seebruck, Bayern","IPA – New England","6.6%","30","",
  [("100ml (flight)","2.30"),("300ml","6.40")]),
 ("Camba Bavaria Chiemsee Hopla","Seeon-Seebruck, Bayern","Lager – IPL","5.4%","25",
  "A fruity hopped lager — the perfect summer drink.",
  [("100ml (flight)","2.00"),("300ml","5.40")]),
 ("Camba Bavaria Chiemsee Black","Seeon-Seebruck, Bayern","Lager – Dark","5.5%","17",
  "Deep-black lager; full-bodied and harmonious with earthy tones and dark berry.",
  [("100ml (flight)","2.00"),("300ml","5.40")]),
 ("orca brau Algorithmusfrei – Double West Coast Red Ale","Nuremberg, Bayern","Red Ale – Imperial","7.5%","",
  "Big boy. Dry-hopped with Chinook, Centennial, Mosaic. Malty backbone, red and deep. Collab with @probierjunge.",
  [("100ml (flight)","3.10"),("300ml","8.40")]),
 ("Kinn Sjelefred","Florø, Vestland","Brown Ale – English","4.5%","30","",
  [("100ml (flight)","3.30"),("300ml","8.90")]),
 ("Pivovar Matuška Zlatá Raketa 17°","Broumy, Středočeský kraj","IPA – American","7%","67",
  "Hops: Columbus, Citra, Amarillo. Exotic aroma and flavour — a couple of pints and you're in a tropical paradise.",
  [("100ml (flight)","3.50"),("300ml","9.40")]),
 ("Faselbräu – Zum Wohl Peach Cream Cider (Local)","Mörfelden-Walldorf, Hessen","Cider – Other Fruit","5.1%","",
  "Creamy peach cider filled with fruity apple and peach aromas — sweet and crushable.",
  [("100ml (flight)","4.00"),("300ml","10.90")]),
 ("KUEHN KUNZ ROSEN Howlsome (Local)","Mainz, Rheinland-Pfalz","Pale Ale – Other","5.1%","15",
  "Einkorn pale ale hopped with Styrian Wolf.",
  [("100ml (flight)","2.90"),("300ml","7.90")]),
 ("Vogelsang Karmingimpel","Köttmannsdorf, Carinthia","Pale Ale – Fruited","5%","",
  "Citrus meets crisp rhubarb; Motueka and Nectaron bring grapefruit and tropical fruit to a lively, off-dry pale ale.",
  [("100ml (flight)","3.10"),("300ml","8.40")]),
 ("Straßenbräu Too Hop To Handle","Friedrichshain, Berlin","IPA – Imperial","8.6%","",
  "Herbal, citrusy. Big, bold and bitter DIPA, dry-hopped with Simcoe and Cashmere.",
  [("100ml (flight)","3.70"),("300ml","9.90")]),
 ("Two Chefs Exotic Getaway – Mango Guava Passionfruit Sour","Amsterdam, Noord-Holland","Sour – Fruited","7%","",
  "Your tropical escape in a glass — a vibrant burst of mango, guava and passionfruit.",
  [("100ml (flight)","3.60"),("300ml","9.90")]),
 ("ATELIER VRAI I Did, Did I?","Heidelbach, Hessen","Sour – Smoothie","5%","","",
  [("100ml (flight)","3.60"),("300ml","9.90")]),
 ("Camba Bavaria Bavarian Summer – Ltd. Edition April 2026","Seeon-Seebruck, Bayern","IPA – Session","5.3%","46",
  "A session IPA with elegant hop notes of grapefruit and peach — refreshing and fruity.",
  [("100ml (flight)","2.30"),("300ml","6.40")]),
 ("FUERST WIACEK Berlin Fire!","Berlin","IPA – American","6.5%","102",
  "Collaboration with Wren House. West Coast IPA — dry-hopped with Citra, Cascade & Chinook.",
  [("100ml (flight)","3.40"),("300ml","9.40")]),
 ("Blech.Brut TENTAPOD","Bamberg, Bayern","IPA – New England","6.4%","",
  "Dry-hopped with Mosaic, HBC 630 & Simcoe.",
  [("100ml (flight)","3.40"),("300ml","9.40")]),
 ("Sudden Death Smokin' In O'Hio (2026)","Lübeck, Schleswig-Holstein","IPA – Imperial","8%","",
  "Hazy Double IPA with Citra, Strata, Chinook, Columbus. Collab with Stay Trippy, Newark, Ohio.",
  [("100ml (flight)","4.50"),("300ml","12.40")]),
]

print("TAP", len(TAP))

# BOTTLE — grouped by category. Each item: (name, origin, style, abv, size, price)
BOTTLE = {
"Alcohol-Free": [
 ("Darmstädter Braustübl Naturradler Alkoholfrei","Darmstadt, Hessen","Shandy – N/A","0%","330ml","5.40"),
 ("orca brau born to be free","Nuremberg, Bayern","Shandy – N/A","—","330ml","5.90"),
 ("Brauhaus Faust Bayrisch Hell Alkoholfrei","Miltenberg, Bayern","Lager – N/A","0.3%","330ml","5.40"),
 ("Maisel's Weisse Alkoholfrei","Bayreuth, Bayern","Wheat – N/A","0.3%","500ml","6.40"),
 ("Kehrwieder MIAMI GROVE","Hamburg","Pale Ale – N/A","0.4%","330ml","6.90"),
 ("Camba Bavaria Free IPA","Seeon-Seebruck, Bayern","IPA – N/A","0.5%","440ml","5.90"),
],
"Gluten-Free": [
 ("Kinn Pilegrim","Florø, Vestland","Pale Ale – GF","4.5%","440ml","8.90"),
 ("Stigbergets Ljus","Gothenburg, Sweden","Lager – GF","5%","330ml","6.90"),
 ("Track Lustre","Manchester, UK","Pale Ale – GF","5.2%","440ml","11.40"),
 ("Mikkeller Space Race","Copenhagen, Denmark","Pale Ale – GF","6.7%","330ml","7.90"),
],
"Lager": [
 ("Brauhaus Faust Natur-Radler","Miltenberg, Bayern","Shandy","2.5%","330ml","5.40"),
 ("Schwarze Rose Neustadt Pils (Local)","Mainz, Rheinland-Pfalz","Pilsner – German","4.8%","440ml","7.40"),
 ("Blech.Brut 8 Bit TWISTBLOOM","Bamberg, Bayern","Pilsner – American","4.9%","440ml","8.40"),
 ("Camba Bavaria Hell","Seeon-Seebruck, Bayern","Lager – Helles","5%","440ml","4.90"),
 ("Camba Bavaria Murphie's Red","Seeon-Seebruck, Bayern","Red Ale – Irish","5%","440ml","5.90"),
 ("Camba Bavaria Chiemsee Hopla","Seeon-Seebruck, Bayern","Lager – IPL","5.1%","440ml","5.40"),
 ("Blech.Brut 8 Bit No Crown. No King.","Bamberg, Bayern","Rauchbier","5.7%","440ml","8.40"),
 ("Camba Bavaria Winterzauber","Seeon-Seebruck, Bayern","Märzen","6%","440ml","5.90"),
 ("Camba Braumeister #90 (Götz Steinl) – Two of Us","Seeon-Seebruck, Bayern","Pilsner – Imperial","6%","440ml","5.90"),
 ("orca brau Burning Hahn: Rauchbock","Nuremberg, Bayern","Rauchbier","6.2%","330ml","6.40"),
 ("Camba Hop Gun – Limited Edition","Seeon-Seebruck, Bayern","Brown Ale – American","6.4%","440ml","5.40"),
 ("Camba Braumeister #97 (M. Wanghofer) – Cherry-Smoke Syndicate","Seeon-Seebruck, Bayern","Smoked Beer","6.5%","440ml","5.90"),
],
"Pale Ale": [
 ("Camba Bavaria Chiemsee Session","Seeon-Seebruck, Bayern","Pale Ale – Session","3.9%","440ml","5.40"),
 ("Camba Bavaria Champ Gang","Seeon-Seebruck, Bayern","Pale Ale – Other","4.8%","440ml","5.90"),
 ("Vogelsang Karmingimpel","Köttmannsdorf, Carinthia","Pale Ale – Fruited","5%","440ml","9.40"),
 ("Camba Bavaria Chiemsee Pale","Seeon-Seebruck, Bayern","Pale Ale – Other","5.3%","440ml","5.90"),
 ("Schwarze Rose Trübe Molle (Local)","Mainz, Rheinland-Pfalz","Pale Ale – NE","5.3%","440ml","8.90"),
 ("Sierra Nevada Pale Ale","Chico, CA","Pale Ale – American","5.6%","355ml","7.40"),
 ("Camba Road-RNR","Seeon-Seebruck, Bayern","Pale Ale – NE","5.9%","440ml","5.90"),
],
"Session IPA": [
 ("Camba Bavarian Summer – Ltd. Edition April 2026","Seeon-Seebruck, Bayern","IPA – Session","5.3%","440ml","5.90"),
],
"IPA": [
 ("Schwarze Rose FREE FALLING | Tattoo Series 2/4","Mainz, Rheinland-Pfalz","IPA – Black","6%","440ml","9.40"),
 ("Northern Monk PP 52.01 // Yorkshire Dales NZ IPA","Leeds, UK","IPA – New Zealand","6%","440ml","10.90"),
 ("Schwarze Rose Magnetic Vibration (Local)","Mainz, Rheinland-Pfalz","IPA – American","6.3%","440ml","9.40"),
 ("Camba \"Polar Kick\" – Brewmaster Edition #98","Seeon-Seebruck, Bayern","IPA – Cold","6.4%","440ml","6.40"),
 ("Salama Neon Brown","Espoo, Finland","IPA – Brown","6.5%","440ml","9.90"),
 ("Camba Bavaria IPA","Seeon-Seebruck, Bayern","IPA – American","6.6%","440ml","5.90"),
 ("Schwarze Rose DEVILS MASK | Tattoo Series 3/4","Mainz, Rheinland-Pfalz","IPA – American","6.8%","440ml","9.40"),
 ("Camba Bavaria Black Shark","Seeon-Seebruck, Bayern","IPA – Imperial","8.5%","440ml","6.90"),
 ("Camba Bavaria Imperial IPA","Seeon-Seebruck, Bayern","IPA – Imperial","8.9%","440ml","6.90"),
],
"NEIPA": [
 ("Blech.Brut TENTAPOD","Bamberg, Bayern","IPA – NE","6.4%","440ml","10.90"),
 ("ATELIER VRAI Stop Making Stupid People Famous 1/5","Heidelbach, Hessen","IPA – NE","6.5%","440ml","10.90"),
 ("Schwarze Rose Dedicated To the Hops (2026) (Local)","Mainz, Rheinland-Pfalz","IPA – NE","6.5%","440ml","9.90"),
 ("Camba Bavaria Island","Seeon-Seebruck, Bayern","IPA – NE","6.6%","440ml","5.90"),
 ("FUERST WIACEK Berlin Daymare (2026)","Berlin","IPA – NE","6.8%","440ml","11.90"),
 ("FUERST WIACEK Berlin Lit!","Berlin","IPA – NE","6.8%","440ml","11.90"),
 ("Schwarze Rose Two Tone #5 Sultana + Eclipse (Local)","Mainz, Rheinland-Pfalz","IPA – NE","6.8%","440ml","9.90"),
 ("Camba Braumeister #82 (F. Gabler) – Black NEIPA","Seeon-Seebruck, Bayern","IPA – Black","6.9%","440ml","5.90"),
 ("ATELIER VRAI Guess What? | Holy Grail | 50% Simcoe","Heidelbach, Hessen","IPA – NE","6.9%","440ml","11.40"),
 ("Yankee & Kraut THICK","Ingolstadt, Bayern","IPA – Imperial","7.4%","440ml","10.90"),
 ("Schwarze Rose Shine Bright Like A Simon (2026) (Local)","Mainz, Rheinland-Pfalz","IPA – Imperial","7.6%","440ml","10.90"),
 ("Schwarze Rose Yellow Pony (Local)","Mainz, Rheinland-Pfalz","IPA – Imperial","7.6%","440ml","10.40"),
 ("ATELIER VRAI Guess What? Ukraine | 75% Citra","Heidelbach, Hessen","IPA – Imperial","7.9%","440ml","12.40"),
 ("Blech.Brut Make Brains Strong Again","Bamberg, Bayern","IPA – Imperial","8%","440ml","11.90"),
 ("Ārpus TDH Hand-Selected Riwaka DIPA","Stapriņi, Latvia","IPA – Imperial","8%","440ml","13.40"),
 ("ATELIER VRAI Please Do Not Put Hand Towels 5/5","Heidelbach, Hessen","IPA – Imperial","8.1%","440ml","11.90"),
 ("FUERST WIACEK Berlin Turtledove","Berlin","IPA – Imperial","8%","440ml","12.90"),
 ("FUERST WIACEK Berlin Stellar!","Berlin","IPA – Imperial","8%","440ml","12.90"),
 ("FUERST WIACEK Berlin Unreal!","Berlin","IPA – Imperial","8%","440ml","12.90"),
 ("Northern Monk A Whole Lot of Faith & Jaipur // Double Hazy","Leeds, UK","IPA – Imperial","8.4%","440ml","11.90"),
 ("Sudden Death Alien Space Meal (2026)","Lübeck, Schleswig-Holstein","IPA – Triple NE","9.5%","440ml","13.90"),
 ("Blech.Brut Urban Ghost","Bamberg, Bayern","IPA – Triple NE","9.5%","440ml","13.40"),
],
"Dark / Stout": [
 ("Samuel Smith Organic Chocolate Stout","Tadcaster, UK","Stout – Other","5%","355ml","8.40"),
 ("Schwarze Rose Lunar Blanket (Local)","Mainz, Rheinland-Pfalz","Stout – Oatmeal","5.2%","440ml","8.90"),
 ("Northern Monk Northern Star™ Porter","Leeds, UK","Porter – Other","5.2%","330ml","7.40"),
 ("Camba Bavaria Chiemsee Black","Seeon-Seebruck, Bayern","Lager – Dark","5.5%","440ml","5.40"),
 ("Põhjala Must Kuld","Tallinn, Estonia","Porter – Other","7.8%","330ml","8.40"),
 ("Delirium Nocturnum (Huyghe)","Melle, Belgium","Belgian Strong Dark Ale","8.5%","330ml","7.90"),
 ("Camba Brewmaster #95 – Spirit of Tallinn (Feb 2026)","Seeon-Seebruck, Bayern","Porter – Baltic","8.8%","440ml","6.90"),
 ("Camba Braumeister #67 (F. Kupferer) – Imperial Power Porter","Seeon-Seebruck, Bayern","Porter – Imperial","9.1%","440ml","7.40"),
 ("Liquid Story I've Seen So Much I'm Blind Again","Braunschweig, Niedersachsen","Stout – Imperial","9.7%","440ml","13.40"),
 ("KUEHN KUNZ ROSEN Velvet Dream","Mainz, Rheinland-Pfalz","Stout – Imperial","10.2%","330ml","12.90"),
 ("LERVIG Konrad's Stout","Stavanger, Norway","Stout – Russian Imperial","10.4%","330ml","10.40"),
 ("LERVIG Midnight Snack","Stavanger, Norway","Stout – Imperial","11%","330ml","11.90"),
 ("Põhjala Pime Öö","Tallinn, Estonia","Stout – Imperial","13.6%","330ml","12.90"),
 ("Põhjala Coffee Culture (Cellar Series)","Tallinn, Estonia","Stout – Imperial","15.5%","330ml","18.90"),
],
"Wheat": [
 ("Camba Bavaria Chiemsee Wit","Seeon-Seebruck, Bayern","Wheat – Witbier","4.8%","440ml","5.40"),
 ("Camba Bavaria Jäger Weisse / Simcoe Weisse","Seeon-Seebruck, Bayern","Wheat – Hopfenweisse","5.2%","440ml","5.40"),
 ("Camba Nelson Reloaded – Ltd. Edition Aug 2025","Seeon-Seebruck, Bayern","Wheat – Hopfenweisse","5.3%","440ml","5.90"),
 ("La Trappe Witte Trappist (2025)","Berkel-Enschot, NL","Wheat – Witbier","5.5%","330ml","5.90"),
 ("Camba Oatlander – Ltd. Edition May 2025","Seeon-Seebruck, Bayern","Wheat – Other","5.6%","440ml","5.90"),
],
"Fruity": [
 ("Brouwerij Lindemans Framboise","Sint-Pieters-Leeuw, Belgium","Lambic – Framboise","2.5%","250ml","6.90"),
 ("Brouwerij Lindemans Kriek","Sint-Pieters-Leeuw, Belgium","Lambic – Kriek","3.5%","250ml","6.40"),
 ("Mongozo Coconut","Melle, Belgium","Fruit Beer","3.6%","330ml","6.90"),
 ("Brouwerij Liefmans Fruitesse","Oudenaarde, Belgium","Fruit Beer","3.8%","250ml","5.40"),
 ("Samuel Smith Organic Apricot","Stamford, UK","Fruit Beer","5.1%","355ml","8.90"),
 ("Brasserie d'Achouffe Chouffe Cherry","Houffalize, Belgium","Fruit Beer","8%","330ml","7.90"),
 ("Delirium Red (Huyghe)","Melle, Belgium","Fruit Beer","8%","330ml","7.90"),
],
"Sour": [
 ("Mikkeller Ich Bin Elderberry","Copenhagen, Denmark","Sour – Berliner Weisse","3.6%","440ml","9.40"),
 ("Garage Beer P9","Barcelona, Spain","Sour – Berliner Weisse","4%","330ml","8.90"),
 ("Vault City Cloudy Lemonade (Citra & Nelson Sauvin)","Edinburgh, UK","Sour – Fruited","4.2%","330ml","8.40"),
 ("Vault City Triple Fruited Mango","Edinburgh, UK","Sour – Fruited","4.8%","330ml","8.40"),
 ("Camba Braumeister #76 (A. Biller) – Lovely Chiemgau","Seeon-Seebruck, Bayern","Farmhouse – Grisette","4.8%","440ml","5.90"),
 ("Blech.Brut Berry Galaxy","Bamberg, Bayern","Sour – Smoothie","5%","440ml","11.40"),
 ("Brasserie Cantillon Classic Gueuze","Anderlecht, Belgium","Lambic – Gueuze","5%","375ml","14.90"),
 ("ATELIER VRAI I Did, Did I?","Heidelbach, Hessen","Sour – Smoothie","5%","440ml","11.40"),
 ("Blech.Brut Mango Mirage","Bamberg, Bayern","Sour – Smoothie","5%","440ml","11.40"),
 ("ATELIER VRAI Never Odd Or Even","Heidelbach, Hessen","Sour – Smoothie","5%","440ml","11.40"),
 ("450 North SLUSHY XL: Vorhees Vitality","Columbus, IN","Sour – Smoothie","5.3%","440ml","16.90"),
 ("Brouwerij Rodenbach Alexander","Roeselare, Belgium","Sour – Flanders Red","5.6%","330ml","7.40"),
 ("Camba Double Trouble","Seeon-Seebruck, Bayern","Farmhouse – Other","5.6%","440ml","5.90"),
 ("Camba Braumeister #86 (F. Kupferer) – Flower Power Sour","Seeon-Seebruck, Bayern","Sour – Other","5.9%","440ml","5.90"),
 ("orca brau Swirl – Raspberry Cheesecake Sour","Nuremberg, Bayern","Sour – Smoothie","6%","330ml","7.90"),
 ("Brouwerij Boon Geuze Mariage Parfait 10","Halle, Belgium","Lambic – Gueuze","10%","375ml","14.90"),
],
"Trappist / Belgian": [
 ("Duvel Moortgat Duvel","Puurs-Sint-Amands, Belgium","Belgian Blonde","6.66%","300ml","6.90"),
 ("La Trappe Dubbel","Berkel-Enschot, NL","Belgian Dubbel","7%","330ml","6.90"),
 ("Trappistes Rochefort 6","Rochefort, Belgium","Belgian Dubbel","7.5%","330ml","6.90"),
 ("La Trappe Tripel (2025)","Berkel-Enschot, NL","Belgian Tripel","8%","330ml","7.40"),
 ("Delirium Tremens (Huyghe)","Melle, Belgium","Belgian Strong Golden Ale","8.5%","330ml","7.90"),
 ("Camba Braumeister #93 (N. Lauer) – Tripel Nik","Seeon-Seebruck, Bayern","Belgian Tripel","8.8%","440ml","6.90"),
 ("Trappistes Rochefort 8","Rochefort, Belgium","Belgian Strong Dark Ale","9.2%","330ml","7.40"),
 ("La Trappe Quadrupel","Berkel-Enschot, NL","Belgian Quadrupel","10%","330ml","8.40"),
 ("Trappistes Rochefort 10","Rochefort, Belgium","Belgian Quadrupel","11.3%","330ml","9.40"),
],
"Bock": [
 ("Camba Braumeister #83 (M. Wanghofer) – White Ram","Seeon-Seebruck, Bayern","Bock – Hell","7.5%","440ml","6.90"),
 ("Glaabsbräu Petrus","Seligenstadt, Hessen","Doppelbock","8.5%","500ml","6.90"),
 ("Camba Bavaria Mastrobator","Seeon-Seebruck, Bayern","Doppelbock","8.5%","440ml","6.40"),
],
"Cider": [
 ("BlakStoc Ginger For My Honey","Lichtenhof, Steiermark","Cider – Herbed","3%","330ml","8.40"),
 ("Faselbräu Pure Apple – Dry Cider","Mörfelden-Walldorf, Hessen","Cider – Dry","4.5%","330ml","8.90"),
 ("Faselbräu Fruit Salad Cider","Mörfelden-Walldorf, Hessen","Cider – Dry","4.5%","330ml","8.90"),
 ("Faselbräu Peach Cream Cider","Mörfelden-Walldorf, Hessen","Cider – Other Fruit","5.1%","330ml","9.40"),
],
}
print("BOTTLE cats", len(BOTTLE), "items", sum(len(v) for v in BOTTLE.values()))

# OTHER THAN BEER. price tuples vary by section.
MIXERS = "All mixers 3.20 € — Water, Cola / Cola Light / Cola Zero, TH Tonic Water, TH Bitter Lemon, TH Spicy Ginger"

SPIRITS = {
"Gin": [
 ("Stobbe 1776 – Premium London Dry Gin","","8.40","5.40"),
],
"Rum": [
 ("Old Monk XXX 7 Y.O. Vatted (Mohan Meakin)","40%","8.40","5.40"),
 ("The Kraken Black Spiced Rum","35%","9.40","5.90"),
 ("Camikara 8 Y.O. Cask Aged Indian Rum","","10.90","6.90"),
 ("Ron Zacapa Centenario Solera 23 Gran Reserva","40%","14.90","8.90"),
],
"Bourbon": [
 ("Maker's Mark Kentucky Straight Bourbon","43%","8.40","5.40"),
],
"Single Malt Whisky": [
 ("Monkey Shoulder Batch 27 Blended Malt","40%","9.90","6.40"),
 ("Indri 'Trini – The Three Wood' Indian Single Malt","46%","10.90","6.90"),
 ("Caol Ila 12 Y.O. Single Malt Scotch","43%","11.90","7.40"),
 ("The Glenlivet 18 Y.O. Single Malt Scotch","40%","16.90","10.90"),
],
"Shots": [
 ("Berliner Luft Pfefferminzlikör","","5.40","3.90"),
 ("Jose Cuervo Especial Gold Reposado Tequila","38%","7.90","4.90"),
 ("Herradura Reposado Tequila","40%","9.90","6.90"),
],
}  # (name, abv, 4cl, 2cl)

WINE = [
 # (name, abv, 0.1l, 0.2l, bottle)  -- use "" where not offered
 ("Prinz von Hessen – Rosé","11.5%","5.40","8.40","27.90"),
 ("Prinz von Hessen – Landgraf Feinherb Riesling","11.5%","5.40","8.40","27.90"),
 ("Weingut Groh – Sauvignon Blanc","11.5%","5.40","8.40","27.90"),
 ("Weingut Knipser – Sauvignon Blanc Trocken","12%","6.40","9.40","29.90"),
 ("Tenuta Ca' Bolani – Merlot Friuli Aquileia","13%","5.90","8.90","28.90"),
 ("Bodegas Montecillo – Crianza","13.5%","6.90","9.90","30.90"),
 ("Masseria Altemura 'Sasseo' – Primitivo Salento IGT","14.5%","6.90","9.90","30.90"),
]
WINE_SPECIAL = [
 ("Wine Schorle","","","6.90",""),
 ("Aperol Spritz","","","8.90",""),
]
WINE_NA = [  # alcohol-free wine
 ("SOBERCIETY 'Missed You' Sauvignon Blanc","0.5%","6.90","9.90","30.90"),
 ("Kolonne Null – Riesling","0.0%","5.90","8.90","28.90"),
]

SOFT = [
 ("H2O – Vio (medium / still)","0.25l 3.40  ·  0.75l 7.90"),
 ("Apfelschorle","0.3l 3.90"),
 ("Orangensaft (100% Direktsaft, no added sugar)","0.3l 4.90"),
 ("Hausgemachte Limonade Schorle — Maracuja-Minze / Mango-Rosmarin / Himbeere-Hibiskus / Zitrone-Basilikum","0.4l 5.90"),
 ("Coca-Cola / Cola Light / Cola Zero / Fanta","0.2l 3.90"),
 ("Thomas Henry – Bitter Lemon / Spicy Ginger","0.2l 3.90"),
]

COFFEE = [
 ("Espresso","single 3.90  ·  double 5.40"),
 ("Americano","4.90"),
 ("Cappuccino / Flat White","5.90"),
]
print("SPIRITS", sum(len(v) for v in SPIRITS.values()), "WINE", len(WINE)+len(WINE_NA), "SOFT", len(SOFT), "COFFEE", len(COFFEE))

# Untappd ratings for the 20 taps (aligned to TAP order): (score, checkins)
TAP_RATING = [
 (3.43,16621),(3.37,865),(3.64,9032),(3.64,4107),(3.78,4574),
 (3.46,10753),(3.54,3127),(3.95,342),(3.40,11101),(3.87,8090),
 (4.15,53),(3.76,375),(3.57,224),(3.80,343),(3.30,6294),
 (4.19,114),(3.82,70),(3.84,1356),(4.09,269),(4.10,512),
]
def kfmt(n):
    return f"{n/1000:.1f}k".replace(".0k","k") if n>=1000 else str(n)

# ---- Accurate Untappd styles (fix over-abbreviated styles) + 2 missed beers ----
_STYLE_FIX = {
 "Bock – Hell":"Bock - Hell / Maibock / Lentebock",
 "Brown Ale – American":"Brown Ale - American",
 "Cider – Dry":"Cider - Dry","Cider – Herbed":"Cider - Herbed / Spiced","Cider – Other Fruit":"Cider - Other Fruit",
 "Doppelbock":"Bock - Doppelbock",
 "Farmhouse – Grisette":"Farmhouse Ale - Grisette","Farmhouse – Other":"Farmhouse Ale - Other",
 "Fruit Beer":"Fruit Beer",
 "IPA – American":"IPA - American","IPA – Black":"IPA - Black","IPA – Brown":"IPA - Brown","IPA – Cold":"IPA - Cold",
 "IPA – N/A":"Non-Alcoholic - IPA","IPA – NE":"IPA - New England","IPA – New Zealand":"IPA - New Zealand",
 "IPA – Session":"IPA - Session","IPA – Triple NE":"IPA - Triple New England",
 "Lager – Dark":"Lager - Dark","Lager – Helles":"Lager - Helles","Lager – IPL":"Lager - IPL (India Pale Lager)",
 "Lager – N/A":"Non-Alcoholic - Lager",
 "Lambic – Framboise":"Lambic - Framboise","Lambic – Gueuze":"Lambic - Gueuze","Lambic – Kriek":"Lambic - Kriek",
 "Märzen":"Märzen",
 "Pale Ale – American":"Pale Ale - American","Pale Ale – Fruited":"Pale Ale - Fruited",
 "Pale Ale – N/A":"Non-Alcoholic - Pale Ale","Pale Ale – NE":"Pale Ale - New England",
 "Pale Ale – Other":"Pale Ale - Other","Pale Ale – Session":"Pale Ale - Session",
 "Pilsner – American":"Pilsner - American","Pilsner – German":"Pilsner - German","Pilsner – Imperial":"Pilsner - Imperial / Double",
 "Porter – Baltic":"Porter - Baltic","Porter – Imperial":"Porter - Imperial / Double","Porter – Other":"Porter - Other",
 "Rauchbier":"Rauchbier","Red Ale – Irish":"Red Ale - Irish",
 "Shandy":"Shandy / Radler","Shandy – N/A":"Non-Alcoholic - Shandy / Radler","Smoked Beer":"Smoked Beer",
 "Sour – Berliner Weisse":"Sour - Fruited Berliner Weisse","Sour – Flanders Red":"Sour - Flanders Red Ale",
 "Sour – Fruited":"Sour - Fruited","Sour – Other":"Sour - Other","Sour – Smoothie":"Sour - Smoothie / Pastry",
 "Stout – Imperial":"Stout - Imperial / Double","Stout – Oatmeal":"Stout - Oatmeal","Stout – Other":"Stout - Other",
 "Stout – Russian Imperial":"Stout - Russian Imperial",
 "Wheat – Hopfenweisse":"Wheat Beer - Hopfenweisse","Wheat – N/A":"Non-Alcoholic - Wheat",
 "Wheat – Other":"Wheat Beer - Other","Wheat – Witbier":"Wheat Beer - Witbier / Blanche",
 # Belgian styles already correct
 "Belgian Blonde":"Belgian Blonde","Belgian Dubbel":"Belgian Dubbel","Belgian Quadrupel":"Belgian Quadrupel",
 "Belgian Strong Dark Ale":"Belgian Strong Dark Ale","Belgian Strong Golden Ale":"Belgian Strong Golden Ale","Belgian Tripel":"Belgian Tripel",
}
def _fixstyle(cat,name,old):
    if old=="IPA – Imperial": return "IPA - Imperial / Double New England" if cat=="NEIPA" else "IPA - Imperial / Double"
    if "Space Race" in name or "Stigbergets Ljus" in name: return "Gluten-Free"
    if "Pilegrim" in name: return "Pale Ale - Gluten Free"
    if old=="Pale Ale – GF": return "Pale Ale - Gluten Free"
    if old=="Lager – GF": return "Gluten-Free"
    return _STYLE_FIX.get(old, old.replace(" – "," - "))

for _cat,_items in BOTTLE.items():
    BOTTLE[_cat]=[(n,o,_fixstyle(_cat,n,s),a,sz,p) for (n,o,s,a,sz,p) in _items]

# add the 2 beers missed in first extraction
BOTTLE["Lager"].append(("Camba Bavaria Amber Ale","Seeon-Seebruck, Bayern","Red Ale - American Amber","7.2%","440ml","5.90"))
# insert Boh after Camba... actually after FUERST WIACEK Daymare in NEIPA
_ne=BOTTLE["NEIPA"]; _boh=("FUERST WIACEK Berlin Boh (2026)","Berlin","IPA - New England","6.8%","440ml","11.90")
_idx=next((k+1 for k,it in enumerate(_ne) if "Daymare" in it[0]), len(_ne))
_ne.insert(_idx,_boh)

print("BOTTLE fixed:", sum(len(v) for v in BOTTLE.values()),"items")
print("distinct styles now:", len({it[2] for v in BOTTLE.values() for it in v}))

# Alcohol-Free Cocktails (ISH) — separate Untappd menu missed by the single print. (name, abv, price)
AF_COCKTAILS = [
 ("Daiquiri","0.0%","8.90"),
 ("Espresso Martini","0.0%","8.90"),
 ("Spritz","0.2%","8.90"),
 ("Paloma","0.3%","8.90"),
 ("G&T","0.4%","8.90"),
 ("Mojito","0.5%","8.90"),
]
print("AF_COCKTAILS", len(AF_COCKTAILS))

# --- LIVE FEED OVERRIDE --------------------------------------------------------
# If build.mjs produced public/_drinks.json (parsed from the live Untappd feed),
# use it for TAP / TAP_RATING / BOTTLE. Curated tap descriptions are merged by name;
# spirits/wine/soft/coffee stay curated above. Falls back to the snapshot if missing.
import os as _os, json as _json
_J = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'public', '_drinks.json')
if _os.path.exists(_J):
    try:
        _live = _json.load(open(_J, encoding='utf-8'))
        _desc = { t[0]: t[5] for t in TAP }
        if _live.get('tap'):
            TAP = [ (t['name'], t.get('loc',''), t.get('style',''), t.get('abv',''), t.get('ibu',''),
                     (t.get('desc') or _desc.get(t['name'],'')), [tuple(p) for p in t.get('prices',[])]) for t in _live['tap'] ]
            TAP_RATING = [ tuple(t.get('rating',(0,0))) for t in _live['tap'] ]
            TAP_NUM = [ int(t['num']) if t.get('num') is not None else i+1 for i,t in enumerate(_live['tap']) ]
        if _live.get('bottle'):
            BOTTLE = { cat: [ (b['name'], b.get('loc',''), b.get('style',''), b.get('abv',''), b.get('size',''), b.get('price',''), tuple(b.get('rating',(0,0)))) for b in items ]
                       for cat, items in _live['bottle'].items() }
        print('drinks.json override applied:', len(TAP), 'taps,', sum(len(v) for v in BOTTLE.values()), 'bottles')
    except Exception as _e:
        print('drinks.json override skipped:', _e)
