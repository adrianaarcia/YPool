import React from "react";
import "./Form.css";

const FormSuccess = () => {
  // This function returns an image to show form was submitted successfully.
  return (
    <div className="form-content-right">
      <h1 className="form-success">Thank You For Registering with us!</h1>
      <img className="form-img-2" src="images/success.svg" alt="success" />
    </div>
  );
};

export default FormSuccess;
