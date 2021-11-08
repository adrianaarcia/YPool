import React from "react";
import ReactDOM from "react-dom";
import RideStatus from "./RideStatus";

it("RideStatus component renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<RideStatus />, div);
});
