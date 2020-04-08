from flask import Blueprint, render_template
from gio_db import Plant


plants_page = Blueprint('plants_page',__name__)


@plants_page.route('/plants')
def plants():
    plants_list = Plant.query.all()
    return render_template('plants.html',
                           plants=plants_list,
                           title='Plants List')
