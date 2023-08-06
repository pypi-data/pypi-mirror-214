from enum import Enum

class TruliaSearchType(Enum):
    ForSale = 0
    ForRent = 1
    Sold = 2
    def __str__(self):
        return {
            0: 'for_sale',
            1: 'for_rent',
            2: 'sold'
        }.get(self.value, '')

class TruliaBeds(Enum):
    StudioAndMore = 1
    OneAndMore = 2
    TwoAndMore = 3
    ThreeAndMore = 4
    FourAndMore = 5
    def __str__(self):
        self.name

class TruliaHouseType(Enum):
    House = 0
    Condo = 1
    Townhome = 2
    MultiFamily = 3
    Land = 4
    MobileManufacted = 5
    Other = 6
    def __str__(self):
        self.name

class TruliaSoldDate(Enum):
    SoldInLast9Months = 1
    SoldInLast6Months = 2
    SoldInLast3Months = 3
    def __str__(self):
        self.name

class TruliaRentalType(Enum):
    ApartamentCondoLoft = 1
    SingleFamilyHome = 2
    Townhome = 3
    def __str__(self):
        self.name

class TruliaPriceRangeForRent(Enum):
    Price400 = 400
    Price500 = 500
    Price600 = 600
    Price700 = 700
    Price800 = 800
    Price900 = 900
    Price1000 = 1000
    Price1100 = 1100
    Price1200 = 1200
    Price1300 = 1300
    Price1400 = 1400
    Price1500 = 1500
    Price1600 = 1600
    Price1700 = 1700
    Price1800 = 1800
    Price1900 = 1900
    Price2000 = 2000
    Price2200 = 2200
    Price2400 = 2400
    Price2600 = 2600
    Price2800 = 2800
    Price3000 = 3000
    Price3200 = 3200
    Price3400 = 3400
    Price3600 = 3600
    Price3800 = 3800
    Price4000 = 4000
    Price4200 = 4200
    Price4400 = 4400
    Price4600 = 4600
    Price4800 = 4800
    Price5000 = 5000
    Price7500 = 7500
    Price10_000 = 10_000
    Price15_000 = 15_000
    def __str__(self):
        self.name

class TruliaSort(Enum):
    NewListings = 0
    JustForYou = 1
    MostPhotos = 2
    PriceLoHi = 3
    PriceHiLo = 4
    Mortgage = 5
    Bedrooms = 6
    Bathrooms = 7
    SquareFeet = 8
    def __str__(self):
        self.name

class TruliaPriceRange(Enum):
    Price10k = 10_000
    Price20k = 20_000
    Price30k = 30_000
    Price100k = 100_000
    Price130k = 130_000
    Price150k = 150_000
    Price200k = 200_000
    Price250k = 250_000
    Price300k = 300_000
    Price350k = 350_000
    Price400k = 400_000
    Price450k = 450_000
    Price500k = 500_000
    Price550k = 550_000
    Price600k = 600_000
    Price650k = 650_000
    Price700k = 700_000
    Price750k = 750_000
    Price800k = 800_000
    Price850k = 850_000
    Price900k = 900_000
    Price950k = 950_000
    Price1m = 1_000_000
    Price1m100k = 1_100_000
    Price1m250k = 1_250_000
    Price1m400k = 1_400_000
    Price1m500k = 1_500_000
    Price1m600k = 1_600_000
    Price1m700k = 1_700_000
    Price1m800k = 1_800_000
    Price1m900k = 1_900_000
    Price2m = 2_000_000
    Price2m250k = 2_250_000
    Price2m500k = 2_500_000
    Price2m750k = 2_750_000
    Price3m = 3_000_000
    Price3m500k = 3_500_000
    Price4m = 4_000_000
    Price5m = 5_000_000
    Price10m = 10_000_000
    Price20m = 20_000_000
    def __str__(self):
        self.name
