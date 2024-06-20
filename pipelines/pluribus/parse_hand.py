def parse_hand(hand_path):
    hand = {}
    with open(hand_path, 'r') as f:
        for line in f:
            line_split = line.split(' = ')
            key = line_split[0]
            value = line_split[1].strip().replace("'", "")
            
            # Boolean
            if value == 'true' or value == 'false':
                value = bool(value)
                
            # Integers
            elif value.isdigit():
                value = int(value)
                
            # List
            elif value.startswith('['):
                value = value[1:-1].split(', ')
                if value[0].isdigit():
                    value = [int(v) for v in value]
            
            hand[key] = value
            
    return hand

        