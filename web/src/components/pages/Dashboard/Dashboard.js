import React from "react";
import { FooterContainer } from "../../../containers/footer";
import { Button } from "../../Button/Button";
import Navbar from "../../Navbar/Navbar";
import "./Dashboard.css";
import { useHistory } from "react-router-dom";

const ProfilePage = (props) => {
  const history = useHistory();
  const GoToRequest = (e) => {
    e.preventDefault();
    history.push("request");
  };

  const GoToStatus = (e) => {
    e.preventDefault();
    history.push("ridestatus");
  };
  return (
    <>
      <Navbar />

      <div className="flex-wrapper" className="home__profile-section">
        <h1>Welcome {props.firstName}</h1>
        <img
          className="dashboard-img"
          src="images/transportation-png.png"
          alt="dashboard"
        ></img>
        <table className="center_table">
          <tbody>
            <tr>
              <th>
                <Button
                  buttonSize="btn--large"
                  buttonColor="blue"
                  onClick={GoToRequest}
                >
                  Request A Ride
                </Button>
              </th>
              <th>
                <Button
                  buttonSize="btn--large"
                  buttonColor="blue"
                  onClick={GoToStatus}
                >
                  Ride Status
                </Button>{" "}
                {/*We're gonna need an api call here. not where*/}
              </th>
              <th>
                <a
                  rel="noopener noreferrer"
                  target="_self"
                  href="https://yalepool.com/"
                >
                  <Button buttonSize="btn--large" buttonColor="blue">
                    Logout
                  </Button>
                </a>
                {/*There's some logout of cas thing here idk how to do*/}
              </th>
            </tr>
          </tbody>
        </table>
      </div>
      <FooterContainer />
    </>
  );
};

export default ProfilePage;
