export default function validateInfo(values) {
  let errors = {};

  var now = new Date();
  var userDate = new Date(values.date);
  userDate.setHours(values.time.slice(0, 2));
  userDate.setMinutes(values.time.slice(3, 5));

  if (values.origin === values.destination) {
    errors.origin = "Origin cannot be the same as destination";
  }

  if (values.origin === "None" || !values.origin) {
    errors.origin = "Please Specify an Origin";
  }

  if (values.destination === "None" || !values.destination) {
    errors.destination = "Please Specify a Destination";
  }

  if (!values.date || !values.date) {
    errors.date = "Departure date required";
  }

  //   console.log(values.date);

  if (userDate < now) {
    errors.time = "Date and/or time is in the Past";
    errors.date = "Date and/or time is in the Past";
  }

  if (!values.time) {
    errors.time = "Departure time required";
  }

  if (values.preferred_car_type === "None" || !values.preferred_car_type) {
    errors.preferred_car_type = "Car Type cannot be left as None";
  }

  if (values.preferred_group_size === "None" || !values.preferred_group_size) {
    errors.preferred_group_size = "Group Size cannot be left as None";
  }

  let group_size = parseInt(values.preferred_group_size)
  if(values.preferred_car_type === "Regular" && group_size> 3){
    errors.preferred_group_size = "You cannot have a regular car type and a group size greater than 3";
  }

  console.log("Here are the errors before returning")
  console.log(errors)
  return errors;
}
