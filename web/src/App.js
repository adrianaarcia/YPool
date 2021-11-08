import "./App.css";
import axios from "axios";
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Welcome from "./components/pages/Welcome/Welcome";
import RequestForm from "./components/pages/Request/RequestForm";
import RideStatus from "./components/pages/RideStatus/RideStatus";
import UserRouting from "./components/pages/UserRouting";
import RingLoader from "react-spinners/RingLoader";
console.log = console.warn = console.error = () => {};

const App = (props) => {
  const netId = { netId: props.flask_token };
  const [isRegistered, setIsRegistered] = useState(false);
  const [userFirstName, setFirstName] = useState("");

  const headers = {
    "api-key": props.api_key,
  };

  // API KEY for testing purposes: "a333b39d-6ff7-4e54-9488-b8ec66d7a39d"
  useEffect(() => {
    axios
      .post("https://yalepool.com/is-registered", netId, {
        headers: headers,
      })
      .then((response) => {
        response = response.data;
        setIsRegistered(response.isRegistered);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios
      .post("https://yalepool.com/is-registered", netId, {
        headers: headers,
      })
      .then((response) => {
        response = response.data;
        setFirstName(response.firstName);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const [loading, setLoading] = useState(false);
  const style = {
    position: "fixed",
    top: "39%",
    left: "45%",
    transform: "translate(-50%, -50%)",
  };

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);
  console.log("isRegistered response: " + isRegistered);
  return (
    <div className="App">
      {loading ? (
        <div style={style}>
          <RingLoader size={150} color={"#4A40FB"} loading={loading} />
        </div>
      ) : (
        <Router>
          <Switch>
            <Route path="/" exact render={() => <Welcome />} />
            <Route
              path="/home"
              exact
              render={() => (
                <UserRouting
                  flag={isRegistered}
                  apiKey={props.api_key}
                  netId={props.flask_token}
                  firstName={userFirstName}
                />
              )}
            />

            <Route
              path="/request"
              exact
              render={() => (
                <RequestForm apiKey={props.api_key} netId={props.flask_token} />
              )}
            />
            <Route
              path="/ridestatus"
              exact
              render={() => (
                <RideStatus apiKey={props.api_key} netId={props.flask_token} />
              )}
            />
          </Switch>
        </Router>
      )}
    </div>
  );
};

export default App;
