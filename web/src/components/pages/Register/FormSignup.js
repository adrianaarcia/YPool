import React from "react";
import validate from "./validateInfo";
import useForm from "./useForm";
import "./Form.css";

const FormSignup = (props) => {
  const { handleChange, handleSubmit, values, errors } = useForm(
    props.submitForm,
    validate,
    props.netId,
    props.apiKey
  );

  return (
    <div className="form-content-right">
      <form onSubmit={handleSubmit} className="form" noValidate>
        <h1>Please Register Below To Start Using YPool!</h1>
        <div className="form-inputs">
          <label className="form-label">First Name</label>
          <input
            className="form-input"
            type="text"
            name="first_name"
            placeholder="Enter your First Name"
            value={values.first_name}
            onChange={handleChange}
          />
          {errors.first_name && <p>{errors.first_name}</p>}
        </div>

        <div className="form-inputs">
          <label className="form-label">Last Name</label>
          <input
            className="form-input"
            type="text"
            name="last_name"
            placeholder="Enter your Last Name"
            value={values.last_name}
            onChange={handleChange}
          />
          {errors.last_name && <p>{errors.last_name}</p>}
        </div>
        <div className="form-inputs">
          <label className="form-label">Email</label>
          <input
            className="form-input"
            type="email"
            name="email"
            placeholder="Enter your email"
            value={values.email}
            onChange={handleChange}
          />
          {errors.email && <p>{errors.email}</p>}
        </div>
        <button className="form-input-btn" type="submit">
          Submit
        </button>
      </form>
    </div>
  );
};

export default FormSignup;
