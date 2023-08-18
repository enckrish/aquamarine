import logging

from utils import get_mongo_client

# ID
GROUP_ID = "general-analyzers"
SELF_ID = "general_analyzers-001"

# MONGO CONSTANTS
ROUTING_DB_NAME = "routing-db"
TARGET_MAP_COLL_NAME = "target-map"
GROUP_ANALYZER_COLL_NAME = "group-leader"

logger = logging.getLogger()


def is_target(service: str) -> bool:
    client = get_mongo_client()

    db = client.get_database(ROUTING_DB_NAME)
    map_coll = db.get_collection(TARGET_MAP_COLL_NAME)
    print(map_coll)
    tmap = map_coll.find_one({"service": service})
    if tmap is None:
        return False
    associated_groups = tmap.get('targets')
    if GROUP_ID not in associated_groups:
        logger.info("group id mismatch, accepted", associated_groups)
        return False

    leader_coll = db.get_collection(GROUP_ANALYZER_COLL_NAME)
    leader = leader_coll.find_one({"group_id": GROUP_ID})

    if leader is None:
        return False

    group_leader = leader.get('leader')
    if group_leader != SELF_ID:
        logger.info(f"self is not leader, self id: {SELF_ID} leader: {group_leader}")
        return False

    logger.info("self is leader of a accepted group, analysing")
    return True
