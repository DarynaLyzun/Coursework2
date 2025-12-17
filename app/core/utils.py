"""Utility functions and constants."""

CANDIDATE_LABELS = [
    "Rain", "Cold", "Hot", "Windy", "Freezing", "Warm", 
    "Sunny", "Snow", "Stormy", "Mild", "Cool"
]

# Comprehensive list of incompatible keywords to filter out bad AI predictions.
# Words are matched against the item description (case-insensitive).
INCOMPATIBLE_KEYWORDS = {
    "Freezing": [
        # Tops/Upper body (Light/Summer)
        "short sleeve", "short-sleeve", "sleeveless", "tank top", "crop top", 
        "camisole", "tube top", "halter", "bandeau", "t-shirt", "tee", "polo", 
        "blouse", "tunic", "vest", "shirt", "bodysuit", "corset", "bralette", "top",
        "off-shoulder", "cold shoulder", "spaghetti strap", "strapless", "racerback",
        "muscle shirt", "singlet", "peplum top", "wrap top", "bardot top",
        
        # Bottoms (Short/Light)
        "shorts", "bermuda", "capris", "skort", "mini skirt", "skirt", 
        "culottes", "hot pants", "board shorts", "cycling shorts", "gym shorts",
        "cargo shorts", "denim shorts", "chino shorts", "skater skirt", "pencil skirt",
        
        # Dresses (Summer/Light)
        "dress", "sundress", "maxi dress", "midi dress", "mini dress", 
        "gown", "cocktail", "slip dress", "romper", "jumpsuit", "playsuit",
        "maxi sundress", "summer dress", "beach dress", "wrap dress", "shirt dress",
        "tea dress", "bodycon dress", "skater dress", "pinafore", "shift dress",
        
        # Footwear (Open/Light)
        "sandal", "flip-flop", "slide", "mule", "clog", "slipper", 
        "open toe", "peep toe", "pump", "heel", "flat", "loafer", 
        "espadrille", "canvas", "sneaker", "trainer", "plimsoll",
        "gladiator sandal", "wedge", "slingback", "court shoe", "kitten heel",
        "stiletto", "ballerina", "ballet flat", "moccasin", "boat shoe",
        
        # Swim/Beach
        "swimsuit", "bikini", "monokini", "trunk", "board short", "rash guard", 
        "sarong", "kaftan", "cover-up", "swim shorts", "beachwear", "swimwear",
        "bathing suit", "pareo", "kimono",
        
        # Materials (Lightweight/Thin)
        "linen", "chiffon", "satin", "silk", "lace", "cotton", "sheer", 
        "mesh", "organza", "tulle", "georgette", "viscose", "rayon", "crepe", 
        "seersucker", "poplin", "voile", "eyelet", "broderie", "crochet",
        "jersey", "modal", "lyocell", "bamboo", "hemp", "muslin", "gauze"
    ],
    "Cold": [
        # Tops
        "short sleeve", "short-sleeve", "sleeveless", "tank top", "crop top", 
        "camisole", "tube top", "halter", "bandeau", "t-shirt", "tee", 
        "blouse", "bodysuit", "corset", "top", "strapless", "spaghetti strap",
        "off-shoulder", "muscle tee",
        
        # Bottoms
        "shorts", "bermuda", "hot pants", "mini skirt", "skort", "short shorts",
        "cycling shorts", "running shorts",
        
        # Dresses
        "sundress", "maxi sundress", "slip dress", "summer dress", "beach dress",
        "mini dress", "strapless dress", "boho dress",
        
        # Footwear
        "sandal", "flip-flop", "slide", "mule", "open toe", "peep toe", 
        "espadrille", "slipper", "gladiator", "thong sandal", "pool slide",
        
        # Swim/Beach
        "swimsuit", "bikini", "monokini", "sarong", "cover-up", "swimwear", 
        "bathing suit",
        
        # Materials
        "linen", "chiffon", "sheer", "mesh", "lace", "organza", "seersucker",
        "tulle", "net", "crochet"
    ],
    "Snow": [
        # Footwear (Non-waterproof/Open/Cold)
        "sandal", "flip-flop", "slide", "mule", "open toe", "peep toe", 
        "heel", "pump", "stiletto", "wedge", "flat", "ballerina", 
        "loafer", "moccasin", "boat shoe", "espadrille", "canvas", 
        "sneaker", "trainer", "plimsoll", "running shoe", "converse", "vans",
        "tennis shoe", "skate shoe", "slipper", "loafer", "oxford", "derby",
        "brogue", "monk strap",
        
        # Bottoms
        "shorts", "bermuda", "skort", "mini skirt", "hot pants", "skirt",
        "culottes", "capri", "cropped trouser",
        
        # Tops
        "sleeveless", "tank top", "crop top", "camisole", "tube top", 
        "halter", "bandeau", "short sleeve", "t-shirt", "blouse",
        "mesh top", "sheer top", "lace top",
        
        # Dresses
        "sundress", "slip dress", "dress", "maxi dress", "mini dress",
        "summer dress",
        
        # Swim
        "swimsuit", "bikini", "monokini", "swim trunks"
    ],
    "Rain": [
        # Materials (Water sensitive/Absorbent)
        "suede", "nubuck", "velvet", "silk", "satin", "canvas", 
        "mesh", "white", "cream", "ivory", "light color", "light colour",
        "felt", "wool (untreated)", "cashmere", "knitted", "crochet",
        
        # Footwear (Open/Permeable)
        "sandal", "flip-flop", "slide", "mule", "open toe", "espadrille",
        "slipper", "canvas shoe", "fabric shoe", "suede shoe", "suede boot",
        "ugg", "sheepskin boot"
    ],
    "Hot": [
        # Outerwear
        "coat", "jacket", "parka", "puffer", "down", "trench", "raincoat", 
        "blazer", "cardigan", "poncho", "cape", "cloak", "overcoat", 
        "peacoat", "duffle coat", "bomber jacket", "leather jacket", 
        "denim jacket", "windbreaker", "anorak", "gilet", "vest (padded)",
        
        # Heavy Tops
        "sweater", "jumper", "pullover", "turtleneck", "hoodie", "sweatshirt", 
        "fleece", "knit", "thermal", "flannel", "heavy cotton", "thick shirt",
        "cable knit", "chunky knit",
        
        # Accessories
        "scarf", "beanie", "glove", "mitten", "earmuff", "leg warmer", 
        "thick sock", "tights", "pantyhose",
        
        # Footwear
        "boot", "bootie", "uggs", "wellington", "galoshes", "knee high boot",
        "thigh high boot", "combat boot", "chelsea boot", "hiking boot",
        "snow boot", "winter boot",
        
        # Materials (Heavy/Warm/Synthetic insulation)
        "wool", "cashmere", "fur", "faux fur", "shearling", "leather", 
        "suede", "corduroy", "velvet", "fleece", "down", "synthetic insulation",
        "tweed", "herringbone", "flannel", "boucle", "chenille", "angora",
        "mohair", "alpaca", "neoprene"
    ],
    "Warm": [
        # Heavy Outerwear
        "winter coat", "heavy coat", "parka", "puffer", "down jacket", 
        "fur coat", "shearling", "ski suit", "snow suit", "thick coat",
        "heavy jacket", "wool coat",
        
        # Warm Clothing (Incorrectly tagged as 'Warm Weather')
        "sweater", "jumper", "pullover", "hoodie", "sweatshirt", "fleece",
        "turtleneck", "thermal", "flannel",
        
        # Accessories
        "thick scarf", "heavy gloves", "mittens", "earmuffs", "beanie",
        "fur hat", "ushanka",
        
        # Footwear
        "snow boot", "winter boot", "uggs", "moon boot", "insulated boot",
        
        # Materials
        "heavy wool", "thick knit", "fur", "down", "shearling", "quilted"
    ],
    "Cool": [
        # Very light summer items
        "swimsuit", "bikini", "monokini", "sarong", "cover-up", "swim trunks",
        "board shorts",
        "sundress", "maxi sundress", "summer dress", "slip dress", "beach dress",
        "mini dress", "strapless",
        "flip-flop", "slide", "thong sandal",
        "sheer", "mesh", "see-through", "fishnet",
        "tube top", "bandeau", "micro mini skirt",
        "linen pants"
    ],
    "Mild": [
        "swimsuit", "bikini", "monokini", "snow boot", "ski suit", 
        "heavy parka", "arctic coat"
    ],
    "Stormy": [
        # Light dresses and summer wear are terrible for storms
        "sundress", "maxi dress", "mini dress", "slip dress", "summer dress",
        "beach dress", "wrap dress", "tea dress", "skater dress",
        "short sleeve", "short-sleeve", "sleeveless", "tank top", "crop top",
        "tube top", "halter", "bandeau", "camisole", "strapless",
        "shorts", "mini skirt", "skirt",
        "sandal", "flip-flop", "slide", "mule", "open toe", "peep toe",
        "espadrille", "canvas", "flat", "heel", "pump",
        "swimsuit", "bikini", "monokini", "sarong", "cover-up",
        "linen", "chiffon", "silk", "lace", "sheer", "mesh", "organza"
    ]
}

def get_temperature_label(temp: float) -> str:
    rules = [(0, "Freezing"), (5, "Cold"), (10, "Chilly"), (15, "Cool"), (28, "Warm"), (float('inf'), "Hot")]
    for limit, label in rules:
        if temp < limit: return label
    return "Hot"

def get_humidity_label(humidity: int) -> str:
    rules = [(30, "Dry"), (60, "Comfortable"), (float('inf'), "Humid")]
    for limit, label in rules:
        if humidity < limit: return label
    return "Humid"

def get_wind_label(speed: float) -> str:
    rules = [(1, "Calm"), (4, "Light Breeze"), (8, "Gentle Breeze"), (13, "Moderate Breeze"), (19, "Fresh Breeze"), (25, "Strong Breeze"), (33, "Storm"), (float('inf'), "Hurricane")]
    for limit, label in rules:
        if speed < limit: return label
    return "Hurricane"