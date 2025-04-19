from aqt import mw
from aqt.utils import showInfo, askUser, showText


def run_migrations(col):
    migrate_templates_with_prompt(
        "<!-- {{Sound}}-->",
        "<div class=korean-support-sound>{{Sound}}</div>",
        ".korean-support-sound { display: none; }",
    )


def migrate_templates_with_prompt(find_str, replace_str, css_snippet):
    affected = []

    for model in mw.col.models.all():
        for template in model["tmpls"]:
            for key in ["qfmt", "afmt"]:
                if find_str in template[key]:
                    affected.append((model["name"], template["name"]))
                    break

    if not affected:
        return

    summary = "\n".join([f"{m} → {t}" for m, t in affected])
    if not askUser(
        """<div>Due to a change in Anki, older Korean Support Plugin templates need to be migrated. <br> 
                   The following templates contain the old style of templates:"""
        f"<br><br>{summary}<br><br>"
        """If any of these templates aren't used with the Korean Support plugin, please migrate your templates manually. 
                   (See <a href='https://github.com/scottgigante/korean-support/blob/master/README.md#migration'>migration</a>)<br>
                   Do you want to apply the migration?</div>""",
        None,
        False,
        False,
        None,
        "Korean Support",
    ):
        return

    for model in mw.col.models.all():
        changed = False
        for template in model["tmpls"]:
            for key in ["qfmt", "afmt"]:
                if find_str in template[key]:
                    template[key] = template[key].replace(find_str, replace_str)
                    changed = True
        if css_snippet:
            if css_snippet not in model["css"]:
                model["css"] += f"\n{css_snippet}"
                changed = True
        if changed:
            mw.col.models.save(model)

    mw.col.reset()
    showInfo("Migration complete. Templates updated.")
