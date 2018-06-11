import uuid

def create_order_id(nbr_parts=2):
    """ generates a random order id """

    parts = [ str(uuid.uuid4()) for _ in range(nbr_parts) ]
    return "".join(parts).replace('-','')
