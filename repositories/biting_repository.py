from controllers.zombie_types_controller import zombie_types
from db.run_sql import run_sql
from repositories import zombie_repository, human_repository
from models.biting import Biting
from models.human import Human
from models.zombie import Zombie

def save(bite):
    sql = "INSERT INTO bitings (zombie_id, human_id) VALUES (%s, %s) RETURNING id"
    values = [bite.zombie.id, bite.human.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    bite.id = id

def select_all():
    bitings = []
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)
    for result in results:
        zombie =  zombie_repository.select(result["zombie_id"])
        human = human_repository.select(result["human_id"])
        bite = Biting(human, zombie, result["id"])
        bitings.append(bite)
    return bitings

def select(id):
    sql = "SELECT * FROM bitings WHERE id=%s"
    values = [id]
    result = run_sql(sql, values)[0]
    zombie = zombie_repository.select(result["zombie_id"])
    human = human_repository.select(result["human_id"])
    bite = Biting(human, zombie, result["id"])
    return bite

def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM bitings WHERE id=%s"
    values = [id]
    run_sql(sql, values)

def update(bite):
    sql = "UPDATE bitings SET (human_id, zombie_id) = (%s, %s) WHERE id=%s"
    values = [bite.human.id, bite.zombie.id, bite.id]
    run_sql(sql, values)

