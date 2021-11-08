import React from 'react';
import ReactDOM from 'react-dom';
import FooterContainer from './footer';


it("Footer component renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<FooterContainer />, div)
});

