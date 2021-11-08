import React, { useEffect, useState } from "react";
import axios from "axios";

function DestOptions(props) {
  const [dests, setDests] = useState([]);
  // Section that makes API call for dropdown
  useEffect(() => {
    let mounted = true
    let header = { api_key: props.apiKey };
    axios
      .get("https://yalepool.com/destinations", { headers: header })
      .then((response) => {
        if(mounted){
          setDests(response.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
      return () => mounted = false;
  }, [props.apiKey]);

  return (
    <>
      <option defaultValue value="None">
        ---
      </option>
      {dests.map((dest) => (
        <option key={dest} value={dest}>
          {dest}
        </option>
      ))}
    </>
  );
}

export default DestOptions;
