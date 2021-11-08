import { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

const useForm = (callback, validate, netId, apiKey) => {
  // Values submitted to API
  const history = useHistory();
  const [values, setValues] = useState({
    netId: netId,
    first_name: "",
    last_name: "",
    email: "",
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // For handling form changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  // For handling form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setErrors(validate(values));
    setIsSubmitting(true);

    // API submission section
    const headers = {
      "api-key": apiKey,
    };
    axios
      .post("https://yalepool.com/users", values, {
        headers: headers,
      })
      .then((response) => {
        console.log(response);
        setTimeout(() => {
          history.push("/home");
        }, 2000);
      })
      .catch((error) => {
        console.log(error);
      });
    history.push("/home");
  };

  // For setting errors detected when user fills form
  useEffect(() => {
    if (Object.keys(errors).length === 0 && isSubmitting) {
      callback();
    }
  }, [errors]);

  return { handleChange, handleSubmit, values, errors };
};

export default useForm;
