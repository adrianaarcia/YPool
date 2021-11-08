import React from 'react';
import ReactDOM from 'react-dom';
import UserRouting from './UserRouting';


it("User Routing component renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<UserRouting />, div)
});

