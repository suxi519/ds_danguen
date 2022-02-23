from src.steps.collect.my_location_allocator import MyLocationAllocator


class VillageParser:
    def __init__(self):
        pass

    def parse_village(self, zip_code: str) -> str:
        words = zip_code.split(sep=' ')
        for word in words:
            if word.endswith('동'):
                return word


allocator = MyLocationAllocator()
addresses = allocator.get_near_addresses()
# zip_code = '경기도 용인시 수지구 상현동 광교리치안'
parser = VillageParser()
for address in addresses:
    keyword = parser.parse_village(address)
    print(keyword)
