

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
students = []


@app.route("/")
def home():
    return redirect(url_for("add_student"))


# ---------------------------------
# TODO: IMPLEMENT THIS ROUTE
# ---------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        grade = request.form.get("grade")

        # TODO:
        # 1. Validate name
        if not name:
            error="Name is empty"
        # 2. Validate grade is number
        try:
            grade=int(grade)
        except(ValueError,TypeError):
            error="Grade is not int"
        # 3. Validate grade range 0–100
        if not error:
            if (grade >100) or (grade<0):
                error="Grade is out of bounds"
        if not error:
        # 4. Add to students list as dictionary
            students.append({"name": name, "grade":grade})
        # 5. Redirect to /students
            return redirect(url_for("display_students"))


    return render_template("add.html", error=error)


# ---------------------------------
# TODO: IMPLEMENT DISPLAY
# ---------------------------------
@app.route("/students")
def display_students():
    return render_template("students.html", students=students)


# ---------------------------------
# TODO: IMPLEMENT SUMMARY
# ---------------------------------
# ---------------------------------
# IMPLEMENTED SUMMARY
# ---------------------------------
@app.route("/summary")
def summary():
    # Handle empty state so the template doesn't crash
    if not students:
        return render_template(
            "summary.html",
            total_students=0,
            average_grade=0,
            max_grade="-",
            low_grade="-"
        )

    # Calculate total students
    total_students = len(students)

    # Calculate average
    total = 0
    for student in students:
        total += student["grade"]
    average_grade = total / total_students

    # Calculate highest and lowest grades using a generator expression
    max_grade = max(student["grade"] for student in students)
    low_grade = min(student["grade"] for student in students)

    # Pass all calculated variables to the template!
    return render_template(
        "summary.html",
        total_students=total_students,
        average_grade=round(average_grade, 2), # Rounding to 2 decimals looks nicer!
        max_grade=max_grade,
        low_grade=low_grade
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
