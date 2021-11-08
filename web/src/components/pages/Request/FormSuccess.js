import React from "react";
import "./Form.css";

const FormSuccess = () => {
  // Displays success image upon submission
  return (
    <div className="form-content-right">
      <h1 className="form-success">We have received your match request!</h1>
      <img className="form-img-2" src="images/success.svg" alt="success" />
    </div>
  );
};

export default FormSuccess;
