import React from "react";
import ReactDOM from "react-dom";
import Dashboard from "./Dashboard";

it("Dashboard component renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<Dashboard />, div);
});
