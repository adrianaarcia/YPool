import React from 'react';
import ReactDOM from 'react-dom';
import FormSignup from './FormSignup';
import FormSuccess from './FormSuccess';
import Form from './RegistrationForm';


it("FormSignup component renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<FormSignup />, div)
});



it("FormSuccess component renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<FormSuccess />, div)
});



it(" RegistrationForm component renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<Form />, div)
});










