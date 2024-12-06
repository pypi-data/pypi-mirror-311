import csv

import pandas as pd
import validators
from django.http import HttpResponse
from djangoldp.models import Model
from djangoldp.views import NoCSRFAuthentication
from rest_framework.views import APIView


# export csv - Old button (export selected lines)
class ExportTerritories(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        response = super(ExportTerritories, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get("origin")
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = (
            "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        )
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response["User"] = request.user.webid()
            except AttributeError:
                pass
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="export.xlsx"'
        for urlid in request.data:
            # Check that the array entries are URLs
            if validators.url(urlid):
                model, instance = Model.resolve(urlid)

        if request.method == "POST" and request.data and isinstance(request.data, list):
            fields = [
                "Nom du territoire",
                "Type de territoire",
                "Etat d'avancement",
                "Description du territoire",
                "Région",
                "Département",
                "année de naissance du projet",
                "origine de la mobilisation",
                "date de reconnaissance en tant que projet émergent",
                "date d'habilitation",
                "type de structure adhérente",
                "nom de la structure adhérente",
                "année d'adhésion",
            ]
            rows = []

            for urlid in request.data:
                # Check that the array entries are URLs
                if validators.url(urlid):
                    model, instance = Model.resolve(urlid)
                    if instance:
                        row = []

                        tzcld_profile = getattr(instance, "tzcld_profile", None)
                        profile = getattr(instance, "profile", None)
                        tzcld_profile_identity = getattr(instance, "tzcld_profile_identity", None)
                        territories_adhesions = getattr(tzcld_profile_identity, "territories_adhesions", None)
                        territories_project_team_members = getattr(tzcld_profile_identity, "territories_project_team_members", None)

                        row.append(getattr(instance, "name", ""))
                        row.append(getattr(getattr(tzcld_profile, "kind", None), "name", ""))
                        row.append(getattr(getattr(tzcld_profile, "step_state", None), "name", ""))
                        row.append(getattr(getattr(profile, "description", None), "name", ""))
                        regions = []
                        departments = []
                        if tzcld_profile:
                            for region in tzcld_profile.regions.all():
                                if region:
                                    regions.append(region.name)
                            for department in tzcld_profile.departments.all():
                                if department:
                                    departments.append(department.name)
                        row.append(", ".join(regions))
                        row.append(", ".join(departments))
                        row.append(getattr(tzcld_profile_identity, "birth_date", ""))
                        row.append(getattr(getattr(tzcld_profile_identity, "origin_mobilization", None), "name", ""))
                        row.append(getattr(tzcld_profile_identity, "emergence_date", ""))
                        row.append(getattr(tzcld_profile_identity, "habilitation_date", ""))
                        if territories_adhesions:
                            types = []
                            names = []
                            years = []
                            for territories_adhesion in territories_adhesions.all():
                                if territories_adhesion:
                                    type = getattr(territories_adhesion, "type", "")
                                    if type:
                                        types.append(type)
                                    name = getattr(territories_adhesion, "name", "")
                                    if name:
                                        names.append(name)
                                    year = getattr(territories_adhesion, "year", "")
                                    if year:
                                        years.append(year.strftime("%d-%m-%Y"))
                            row.append(", ".join(types))
                            row.append(", ".join(names))
                            row.append(", ".join(years))
                        if territories_project_team_members:
                            for member in territories_project_team_members.all():
                                row.append(getattr(member, "first_name", ""))
                                row.append(getattr(member, "last_name", ""))
                                row.append(getattr(member, "mail", ""))
                                row.append(getattr(member, "phone", ""))
                                row.append(getattr(member, "role", ""))
                                row.append(getattr(member, "details", ""))
                                row.append(getattr(getattr(member, "user_state", None), "name", ""))
                                row.append(getattr(member, "attachment_structure", ""))
                                row.append(getattr(member, "etp", ""))
                                row.append(getattr(getattr(member, "training_course", None), "name", ""))
                                row.append(getattr(getattr(member, "training_promotion", None), "name", ""))
                                print(len(fields), len(row))
                                if len(fields) < len(row):
                                    fields = fields + [
                                        "prénom",
                                        "nom",
                                        "mail",
                                        "téléphone",
                                        "rôle",
                                        "précisions",
                                        "statut de la personne",
                                        "structure de rattachement",
                                        "ETP consacré au projet",
                                        "Formation suivie",
                                        "numéro de promotion",
                                    ]

                        rows.append(row)

        df = pd.DataFrame(rows, columns=fields)
        df.to_excel(response, sheet_name="Territoires", index=False)
        if response:
            return response

        return HttpResponse("Not Found")
