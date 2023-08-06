"Functions for generating survey package."
from __future__ import annotations
import os
from importlib.metadata import version
from json import dump
from pathlib import Path
from pynpm import NPMPackage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .structure import Survey


def install_npm_deps(path: str | Path = os.getcwd()) -> None:
    """Install npm dependencies for VelesResearch."""

    npm_dependencies = {
        "name": "Veles Survey",
        "version": version("velesresearch"),
        "private": True,
        "dependencies": {
            "@json2csv/plainjs": "latest",
            "file-saver": "latest",
            "json-loader": "latest",
            "react": "latest",
            "react-dom": "latest",
            "survey-react-ui": "latest",
        },
        "devDependencies": {"react-scripts": "latest"},
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
        },
        "eslintConfig": {"extends": ["react-app", "react-app/jest"]},
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version",
            ],
        },
    }

    if isinstance(path, str):
        path = Path(path)
    path = path / "package.json"
    with open(path, "w", encoding="utf-8") as package_json:
        dump(npm_dependencies, package_json)

    NPMPackage(path).install()


def generate_survey(Survey_object: "Survey", path: str | Path = os.getcwd()) -> None:
    "Saves survey to survey.js file"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{Survey_object.label}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="surveyElement"></div>
  </body>
</html>"""

    index_js = """import React from "react";
import { createRoot } from "react-dom/client";
import SurveyComponent from "./SurveyComponent";

const root = createRoot(document.getElementById("surveyElement"));
root.render(<SurveyComponent />);"""

    index_css = ""

    SurveyComponent = """import React from "react";
import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/defaultV2.min.css";
import "./index.css";
import { json } from "./survey.js";
import { Parser } from '@json2csv/plainjs';
import { saveAs } from "file-saver";

function MakeID(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function SurveyComponent() {
    const survey = new Model(json);
    survey.onComplete.add((sender, options) => {
        const result = Object.assign({ id: MakeID(8) }, sender.data);
        console.log(result)
        const parser = new Parser({ delimiter: ';' });
        const csvData = parser.parse(result);
        const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
        saveAs(blob, "data.csv");
    });
    return (<Survey model={survey} />);
}

export default SurveyComponent;"""

    if isinstance(path, str):
        path = Path(path)

    # package.json
    os.makedirs(path / "src", exist_ok=True)
    os.makedirs(path / "public", exist_ok=True)

    # survey.js
    with open(path / "src" / "survey.js", "w", encoding="utf-8") as survey_js:
        survey_js.write("export const json = ")

    with open(path / "src" / "survey.js", "a", encoding="utf-8") as survey_js:
        from .structure import SurveyEncoder

        dump(Survey_object, survey_js, cls=SurveyEncoder)

    # index.js
    with open(path / "src" / "index.js", "w", encoding="utf-8") as index_js_file:
        index_js_file.write(index_js)

    # index.css
    with open(path / "src" / "index.css", "w", encoding="utf-8") as index_css_file:
        index_css_file.write(index_css)

    # SurveyComponent.jsx
    with open(
        path / "src" / "SurveyComponent.jsx", "w", encoding="utf-8"
    ) as survey_component_file:
        survey_component_file.write(SurveyComponent)

    # index.html
    with open(path / "public" / "index.html", "w", encoding="utf-8") as index_html_file:
        index_html_file.write(index_html)


def build_survey(path: str | Path = os.getcwd()) -> None:
    """Builds survey package."""

    if isinstance(path, str):
        path = Path(path)

    NPMPackage(path).run_script("build")
