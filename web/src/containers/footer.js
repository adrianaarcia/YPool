import React from "react";
import Footer from "../components/footer";
const currentYear = new Date().getFullYear();
console.log = console.warn = console.error = () => {};

export function FooterContainer() {
  return (
    <Footer>
      <Footer.Wrapper>
        <Footer.Row></Footer.Row>
        <p1 style={{ color: "white", textAlign: "center" }}>
          YPool © {currentYear}
        </p1>
      </Footer.Wrapper>
    </Footer>
  );
}

export default FooterContainer;
