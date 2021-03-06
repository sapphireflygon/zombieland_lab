from flask import Blueprint, Flask, redirect, render_template, request
from controllers.zombies_controller import zombies
from models.biting import Biting
from repositories import biting_repository, zombie_repository, human_repository


bitings_blueprint = Blueprint("bitings", __name__)

# INDEX
@bitings_blueprint.route("/bitings")
def bitings():
    bitings = biting_repository.select_all()
    return render_template("bitings/index.html", bitings = bitings)


# NEW
@bitings_blueprint.route("/bitings/new")
def new_biting():
    zombies = zombie_repository.select_all()
    humans = human_repository.select_all()
    return render_template("bitings/new.html", humans=humans, zombies=zombies)


# CREATE
@bitings_blueprint.route("/bitings", methods=["POST"])
def create_biting():
    human_id = request.form["human_id"]
    zombie_id = request.form["zombie_id"]
    zombie = zombie_repository.select(zombie_id)
    human = human_repository.select(human_id)
    new_biting = Biting(human, zombie)
    biting_repository.save(new_biting)
    return redirect("/bitings")


# EDIT
@bitings_blueprint.route("/bitings/<id>/edit")
def edit_biting(id):
    biting = biting_repository.select(id)
    humans = human_repository.select_all()
    zombies = zombie_repository.select_all()
    return render_template("/bitings/edit.html", biting=biting, zombies=zombies, humans=humans)


# UPDATE
@bitings_blueprint.route("/bitings/<id>", methods=["POST"])
def update_biting(id):
    human_id = request.form["human_id"]
    zombie_id = request.form["zombie_id"]
    human = human_repository.select(human_id)
    zombie = zombie_repository.select(zombie_id)
    updated_bite = Biting(human, zombie, id)
    biting_repository.update(updated_bite)
    return redirect("/bitings")


# DELETE
@bitings_blueprint.route("/bitings/<id>/delete", methods=["POST"])
def delete_biting(id):
    biting_repository.delete(id)
    return redirect("/bitings")