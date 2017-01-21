import numpy as np

SIZE_TINY = 5
SIZE_SMALL = 10
SIZE_LARGE = 30

locations = [
"attic",
"back_yard",
"basement",
"bathroom",
"bedroom",
"cellar",
"closet",
"crawlspace",
"den",
"dining_room",
"front_yard",
"garage",
"garden",
"hall",
"hallway",
"kitchen",
"laundry",
"living_room",
"lounge",
"master_bedroom",
"office",
"pantry",
"patio",
"playroom",
"porch",
"staircase",
"study",
"sunroom",
"TV_room",
"workshop",
]

clothing = [
"belt",
"boots",
"cap",
"coat",
"dress",
"gloves",
"hat",
"jacket",
"jeans",
"pajamas",
"pants",
"raincoat",
"scarf",
"shirt",
"shoes",
"skirt",
"slacks",
"slippers",
"socks",
"stockings",
"suit",
"sweater",
"sweatshirt",
"t-shirt",
"tie",
"trousers",
"underclothes",
"underpants",
"undershirt",
]


fruit = [
"apple",
"banana",
"cherry",
"grapefruit",
"grapes",
"lemon",
"lime",
"melon",
"orange",
"peach",
"pear",
"persimmon",
"pineapple",
"plum",
"strawberry",
"tangerine",
"watermelon",
]

vegetables = [
"asparagus",
"beans",
"broccoli",
"cabbage",
"carrot",
"celery",
"corn",
"cucumber",
"eggplant",
"green_pepper",
"lettuce",
"onion",
"peas",
"potato",
"pumpkin",
"radish",
"spinach",
"sweet_potato",
"tomato",
"turnip",
]

objects = fruit + vegetables

containers = [
"box",
"pantry",
"bathtub",
"envelope",
"drawer",
"bottle",
"cupboard",
"basket",
"crate",
"suitcase",
"bucket",
"container",
"treasure_chest",
]

colors = ['green', 'blue', 'red']

containers = ['_'.join([color, container]) for container in containers for color in colors]

names = [
"Oliver",
"Ethan",
"Liam",
"Benjamin",
"Lucas",
"Alexander",
"Jacob",
"Mason",
"William",
"Hunter",
"James",
"Logan",
"Owen",
"Noah",
"Carter",
"Nathan",
"Jack",
"Aiden",
"Jackson",
"Jayden",
"Emma",
"Olivia",
"Emily",
"Sophia",
"Ava",
"Chloe",
"Charlotte",
"Abigail",
"Amelia",
"Ella",
"Hannah",
"Isabella",
"Aria",
"Lily",
"Mia",
"Isla",
"Avery",
"Elizabeth",
"Mila",
"Evelyn",
]

assert len(locations) >= SIZE_LARGE
assert len(objects) >= SIZE_LARGE
assert len(containers) >= SIZE_LARGE
assert len(names) >= SIZE_LARGE

def write_world(filepath, locs, objs, conts, nams):

    with open(filepath, 'w') as f:

        f.write('# locations\n')

        for loc in locs:

            f.write('\n')
            f.write('create %s\n' % loc)
            f.write('set %s is_thing\n' % loc)
            f.write('set %s is_location\n' % loc)

        f.write('\n')
        f.write('# objects\n')

        for obj in objs:

            f.write('\n')
            f.write('create %s\n' % obj)
            f.write('set %s is_thing\n' % obj)
            f.write('set %s is_gettable\n' % obj)

        f.write('\n')
        f.write('# containers\n')

        for cont in conts:

            f.write('\n')
            f.write('create %s\n' % cont)
            f.write('set %s is_thing\n' % cont)
            f.write('set %s is_container\n' % cont)

        f.write('\n')
        f.write('# actors\n')

        for nam in nams:

            f.write('\n')
            f.write('create %s\n' % nam)
            f.write('set %s is_actor\n' % nam)
            f.write('set %s is_god\n' % nam)
    
write_world('world_tiny.txt', 
            np.random.choice(locations, SIZE_TINY, replace=False),
            np.random.choice(objects, SIZE_TINY, replace=False),
            np.random.choice(containers, SIZE_TINY, replace=False),
            np.random.choice(names, SIZE_TINY, replace=False))
    
write_world('world_small.txt', 
            np.random.choice(locations, SIZE_SMALL, replace=False),
            np.random.choice(objects, SIZE_SMALL, replace=False),
            np.random.choice(containers, SIZE_SMALL, replace=False),
            np.random.choice(names, SIZE_SMALL, replace=False))
    
write_world('world_large.txt', 
            np.random.choice(locations, SIZE_LARGE, replace=False),
            np.random.choice(objects, SIZE_LARGE, replace=False),
            np.random.choice(containers, SIZE_LARGE, replace=False),
            np.random.choice(names, SIZE_LARGE, replace=False))
