def form_builder(state):
    form = {}
    if state.aadhaar_data:
        form.update({
            "name": state.aadhaar_data.get("name"),
            "dob": state.aadhaar_data.get("dob"),
            "gender": state.aadhaar_data.get("gender"),
            "address": state.aadhaar_data.get("address"),
        })
    if state.pan_data:
        form["pan"] = state.pan_data.get("pan")
    state.form=form
    return state
