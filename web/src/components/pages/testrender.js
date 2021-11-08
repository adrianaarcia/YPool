import React, { Component } from "react";

class FavouriteTeam extends Component {
  state = {
    teams: [],
    selectedTeam: "",
    validationError: "",
  };

  componentDidMount() {
    fetch("https://yalepool.com/destinations")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let teamsFromApi = data.map((team) => {
          return { value: team, display: team };
        });
        this.setState({
          teams: [
            {
              value: "",
              display: "(Select your favourite team)",
            },
          ].concat(teamsFromApi),
        });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    return (
      <div>
        <select
          value={this.state.selectedTeam}
          onChange={(e) =>
            this.setState({
              selectedTeam: e.target.value,
              validationError:
                e.target.value === ""
                  ? "You must select your favourite team"
                  : "",
            })
          }
        >
          {this.state.teams.map((team) => (
            <option key={team.value} value={team.value}>
              {team.display}
            </option>
          ))}
        </select>
        <div>{this.state.validationError}</div>
      </div>
    );
  }
}

export default FavouriteTeam;
