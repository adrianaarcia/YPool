import React from "react";
import Dashboard from "./Dashboard/Dashboard";
import RegistrationForm from "./Register/RegistrationForm";

const UserRouting = (props) => {
  return (
    <>
      {console.log("User Routing flag is : " + props.flag)}
      {props.flag ? (
        <Dashboard
          firstName={props.firstName}
          apiKey={props.apiKey}
          netId={props.netId}
        />
      ) : (
        <RegistrationForm apiKey={props.apiKey} netId={props.netId} />
      )}
    </>
  );
};

export default UserRouting;
