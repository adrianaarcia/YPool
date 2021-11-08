import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";

ReactDOM.render(
  <App
    flask_token={document.getElementById("root").getAttribute("flask_token")}
    api_key={document.getElementById("root").getAttribute("api_key")}
  />,
  document.getElementById("root")
);
