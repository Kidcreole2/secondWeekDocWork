@app.route("/admin_index")
@login_required
def admin_index():
    return render_template("pages/admin/index.html")

