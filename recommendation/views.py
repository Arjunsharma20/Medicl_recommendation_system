from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .ml_models import get_prediction, helper
from .models import PatientRecord
from .ml_models import symptoms_dict 


# ---------------- Home ----------------
def home(request):
    return render(request, "home.html")



# ---------------- Patient Dashboard ----------------
def patient_dashboard(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        symptom_text = request.POST.get("symptoms")

        if not (name and age and gender and symptom_text):
            return render(request, "patient_dashboard.html", {
                "message": "⚠️ Please fill in all fields.",
                "symptoms_list": list(symptoms_dict.keys())  # ✅ always send list
            })

        try:
            user_symptoms = [
                s.strip().lower().replace(" ", "_")
                for s in symptom_text.split(",") if s.strip()
            ]

            predicted_disease = get_prediction(user_symptoms)
            desc, prec, meds, diet, wrkout = helper(predicted_disease)

            readable_symptoms = [s.replace("_", " ").title() for s in user_symptoms]

            # Save patient record
            PatientRecord.objects.create(
                name=name,
                age=int(age),
                gender=gender,
                symptoms=", ".join(readable_symptoms),
                predicted_disease=predicted_disease,
                description=desc,
                precautions=", ".join(prec),
                medication=", ".join(meds),
                diet=", ".join(diet),
                workout=", ".join(wrkout),
            )

            # Pass data to results page
            context = {
                "name": name,
                "age": age,
                "gender": gender,
                "symptoms": readable_symptoms,
                "predicted_disease": predicted_disease,
                "description": desc,
                "precautions": prec,
                "medications": meds,
                "diet": diet,
                "workout": wrkout,
            }
            return render(request, "patient_result.html", context)

        except Exception as e:
            return render(request, "patient_dashboard.html", {
                "message": f"❌ Error: {e}",
                "symptoms_list": list(symptoms_dict.keys())
            })

    # GET request
    return render(request, "patient_dashboard.html", {
        "symptoms_list": list(symptoms_dict.keys())  # ✅ send always
    })



# ---------------- Doctor Dashboard ----------------
def doctor_dashboard(request):
    records = PatientRecord.objects.all().order_by("-created_at")
    return render(request, "doctor_dashboard.html", {"records": records})


# ---------------- Contact Page ----------------
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"Message from {name} ({email}):\n\n{message}"

        try:
            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Your email
            )
            return render(request, "contact.html", {"success": True})
        except Exception as e:
            return render(request, "contact.html", {"error": str(e)})

    return render(request, "contact.html")


# ---------------- Static Pages ----------------
def about(request):
    return render(request, "about.html")

def blog(request):
    return render(request, "blog.html")

def developer(request):
    return render(request, "developer.html")
