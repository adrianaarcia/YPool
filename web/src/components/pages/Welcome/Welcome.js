import React from 'react';
import { FooterContainer } from '../../../containers/footer';
import HeroSection from '../../HeroSection';
import Navbar from '../../Navbar/Navbar';
import { homeObj } from './Data';


function Welcome() {
    return (
        <>
            <Navbar />
            <HeroSection {...homeObj } />
            <FooterContainer />
            
        </>
    );
}

export default Welcome;