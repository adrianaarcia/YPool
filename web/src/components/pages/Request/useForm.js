import { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

const useForm = (callback, validate, netId, apiKey) => {
  const history = useHistory();
  const [values, setValues] = useState({
    netId: netId,
    date: "",
    time: "",
    origin: "",
    destination: "",
    preferred_car_type: "",
    preferred_group_size: "",
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrors(validate(values));

    const headers = {
      "api-key": apiKey,
    };

    if (Object.keys(validate(values)).length === 0) {
      console.log("We gonna submit!");
      axios
        .post("https://yalepool.com/ride-request", values, {
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
    }
  };

  useEffect(() => {
    if (Object.keys(errors).length === 0 && isSubmitting) {
      callback();
    }
  }, [errors]);

  return { handleChange, handleSubmit, values, errors };
};

export default useForm;
