from models import *

@app.route("/admin")
@login_required
def admin_index():
    users = Users.query.all()
    institutes = Institute.query.all()
    return render_template("pages/admin/index.html", users=users, institutes=institutes)

@app.route("/admin/<who>/<action>")
@app.route("/admin/<who>/update/<who_id>")
