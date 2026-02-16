from enum import Enum


class ProductCategory(str, Enum):
    """Основные категории товаров для маркетплейса"""

    # Электроника и техника
    SMARTPHONES = "smartphones"
    LAPTOPS_AND_TABLETS = "laptops_and_tablets"
    COMPUTERS_AND_COMPONENTS = "computers_and_components"
    TV_AND_VIDEO = "tv_and_video"
    AUDIO = "audio"
    PHOTO_AND_VIDEO_CAMERAS = "photo_and_video_cameras"
    GAMING = "gaming"
    SMART_HOME = "smart_home"
    ACCESSORIES_ELECTRONICS = "accessories_electronics"

    # Бытовая техника
    LARGE_APPLIANCES = "large_appliances"
    SMALL_APPLIANCES = "small_appliances"
    CLIMATE_CONTROL = "climate_control"
    KITCHEN_APPLIANCES = "kitchen_appliances"

    # Одежда, обувь, аксессуары
    WOMENS_CLOTHING = "womens_clothing"
    MENS_CLOTHING = "mens_clothing"
    KIDS_CLOTHING = "kids_clothing"
    SHOES = "shoes"
    BAGS_AND_WALLETS = "bags_and_wallets"
    ACCESSORIES = "accessories"
    UNDERWEAR_AND_SLEEPWEAR = "underwear_and_sleepwear"
    SPORT_CLOTHING = "sport_clothing"

    # Красота и здоровье
    COSMETICS = "cosmetics"
    PERFUMERY = "perfumery"
    HAIR_CARE = "hair_care"
    FACE_AND_BODY_CARE = "face_and_body_care"
    MAKEUP = "makeup"
    HEALTH_AND_PHARMACY = "health_and_pharmacy"

    # Дом и сад
    FURNITURE = "furniture"
    HOME_TEXTILE = "home_textile"
    KITCHEN_AND_TABLEWARE = "kitchen_and_tableware"
    LIGHTING = "lighting"
    DECOR_AND_INTERIOR = "decor_and_interior"
    GARDEN_AND_PLANTS = "garden_and_plants"
    REPAIR_AND_TOOLS = "repair_and_tools"

    # Детские товары
    TOYS = "toys"
    BABY_CARE = "baby_care"
    CHILDREN_FURNITURE = "children_furniture"
    SCHOOL_AND_CREATIVITY = "school_and_creativity"

    # Спорт и активный отдых
    SPORT_EQUIPMENT = "sport_equipment"
    FITNESS_AND_GYM = "fitness_and_gym"
    TOURISM_AND_CAMPING = "tourism_and_camping"
    BICYCLES_AND_SCOOTERS = "bicycles_and_scooters"

    # Автотовары
    AUTO_PARTS = "auto_parts"
    CAR_ACCESSORIES = "car_accessories"
    MOTORCYCLES_AND_SCOOTERS = "motorcycles_and_scooters"
    TIRES_AND_WHEELS = "tires_and_wheels"

    # Продукты и зоотовары
    FOOD_AND_DRINKS = "food_and_drinks"
    PET_SUPPLIES = "pet_supplies"
    PET_FOOD = "pet_food"

    # Книги, хобби, канцелярия
    BOOKS = "books"
    STATIONERY = "stationery"
    BOARD_GAMES_AND_PUZZLES = "board_games_and_puzzles"
    HANDMADE_AND_HOBBY = "handmade_and_hobby"
    COLLECTIBLES = "collectibles"

    # Ювелирные изделия и часы
    JEWELRY = "jewelry"
    WATCHES = "watches"

    # Другое
    OTHER = "other"
